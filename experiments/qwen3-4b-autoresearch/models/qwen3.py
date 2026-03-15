"""
Qwen3-4B Model Implementation
Based on Qwen3 Technical Report (arXiv:2505.09388)

Key Features:
- Grouped Query Attention (GQA)
- SwiGLU activation
- RMSNorm with pre-normalization
- Rotary Positional Embeddings (RoPE)
- QK-Normalization (new in Qwen3)
- No QKV bias (efficiency improvement)
"""

import math
from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass
class Qwen3Config:
    """Qwen3-4B Configuration"""
    # Model dimensions
    n_layers: int = 36
    n_heads: int = 32
    n_kv_heads: int = 8          # GQA: 4 query heads per KV head
    d_model: int = 3072
    d_ff: int = 8192             # ~2.7x d_model for SwiGLU
    head_dim: int = 96           # d_model // n_heads

    # Vocabulary
    vocab_size: int = 50304
    max_seq_len: int = 2048

    # Architecture features
    qk_norm: bool = True         # QK-Normalization
    tie_weights: bool = True     # Tie input/output embeddings
    rope_base: float = 1000000.0 # Extended RoPE base

    # Training
    dropout: float = 0.0
    bias: bool = False           # No bias in linear layers (Qwen3 design)
    norm_eps: float = 1e-6


class RMSNorm(nn.Module):
    """Root Mean Square Layer Normalization"""

    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # RMS normalization
        rms = torch.sqrt(torch.mean(x ** 2, dim=-1, keepdim=True) + self.eps)
        return self.weight * x / rms


class RotaryEmbedding(nn.Module):
    """Rotary Positional Embeddings (RoPE)"""

    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 10000.0):
        super().__init__()
        self.dim = dim
        self.max_seq_len = max_seq_len
        self.base = base

        # Precompute frequencies
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2).float() / dim))
        self.register_buffer("inv_freq", inv_freq)

        # Precompute cos/sin for efficiency
        t = torch.arange(max_seq_len, dtype=torch.float32)
        freqs = torch.outer(t, inv_freq)
        emb = torch.cat([freqs, freqs], dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :])
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :])

    def forward(self, x: torch.Tensor, seq_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return (
            self.cos_cached[:, :, :seq_len, :],
            self.sin_cached[:, :, :seq_len, :]
        )


def apply_rotary_emb(
    q: torch.Tensor,
    k: torch.Tensor,
    cos: torch.Tensor,
    sin: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Apply rotary embeddings to queries and keys"""
    # Reshape for rotation
    q_r, q_i = q[..., ::2], q[..., 1::2]
    k_r, k_i = k[..., ::2], k[..., 1::2]

    # Rotate
    q_out_r = q_r * cos[..., ::2] - q_i * sin[..., ::2]
    q_out_i = q_r * sin[..., 1::2] + q_i * cos[..., 1::2]
    k_out_r = k_r * cos[..., ::2] - k_i * sin[..., ::2]
    k_out_i = k_r * sin[..., 1::2] + k_i * cos[..., 1::2]

    # Combine
    q_out = torch.stack([q_out_r, q_out_i], dim=-1).flatten(-2)
    k_out = torch.stack([k_out_r, k_out_i], dim=-1).flatten(-2)

    return q_out, k_out


class GroupedQueryAttention(nn.Module):
    """
    Grouped Query Attention (GQA)

    Key-value pairs are shared across groups of query heads.
    Qwen3-4B: 32 query heads, 8 KV heads (4:1 ratio)
    """

    def __init__(self, config: Qwen3Config):
        super().__init__()
        self.n_heads = config.n_heads
        self.n_kv_heads = config.n_kv_heads
        self.head_dim = config.head_dim
        self.d_model = config.d_model

        # Number of query heads per KV head
        assert config.n_heads % config.n_kv_heads == 0
        self.n_rep = config.n_heads // config.n_kv_heads

        # Projections (no bias in Qwen3)
        self.q_proj = nn.Linear(config.d_model, config.n_heads * config.head_dim, bias=False)
        self.k_proj = nn.Linear(config.d_model, config.n_kv_heads * config.head_dim, bias=False)
        self.v_proj = nn.Linear(config.d_model, config.n_kv_heads * config.head_dim, bias=False)
        self.o_proj = nn.Linear(config.n_heads * config.head_dim, config.d_model, bias=False)

        # QK-Normalization (new in Qwen3)
        self.qk_norm = config.qk_norm
        if self.qk_norm:
            self.q_norm = RMSNorm(config.head_dim, eps=config.norm_eps)
            self.k_norm = RMSNorm(config.head_dim, eps=config.norm_eps)

        # RoPE
        self.rotary = RotaryEmbedding(
            config.head_dim,
            max_seq_len=config.max_seq_len,
            base=config.rope_base
        )

        self.dropout = config.dropout

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
        use_cache: bool = False,
        past_kv: Optional[Tuple[torch.Tensor, torch.Tensor]] = None
    ) -> Tuple[torch.Tensor, Optional[Tuple[torch.Tensor, torch.Tensor]]]:
        B, T, C = x.shape

        # Project to Q, K, V
        q = self.q_proj(x).view(B, T, self.n_heads, self.head_dim)
        k = self.k_proj(x).view(B, T, self.n_kv_heads, self.head_dim)
        v = self.v_proj(x).view(B, T, self.n_kv_heads, self.head_dim)

        # QK-Normalization (Qwen3 innovation)
        if self.qk_norm:
            q = self.q_norm(q)
            k = self.k_norm(k)

        # Apply RoPE
        cos, sin = self.rotary(x, T)
        q, k = apply_rotary_emb(q, k, cos, sin)

        # Transpose for attention: (B, n_heads, T, head_dim)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        # Handle KV cache for inference
        if past_kv is not None:
            k_cache, v_cache = past_kv
            k = torch.cat([k_cache, k], dim=2)
            v = torch.cat([v_cache, v], dim=2)

        # Repeat KV heads for GQA
        if self.n_rep > 1:
            k = k.repeat_interleave(self.n_rep, dim=1)
            v = v.repeat_interleave(self.n_rep, dim=1)

        # Attention scores
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)

        # Apply causal mask
        if mask is not None:
            scores = scores + mask

        # Softmax and dropout
        attn = F.softmax(scores, dim=-1)
        if self.dropout > 0:
            attn = F.dropout(attn, p=self.dropout, training=self.training)

        # Apply attention to values
        out = torch.matmul(attn, v)  # (B, n_heads, T, head_dim)

        # Reshape and project
        out = out.transpose(1, 2).contiguous().view(B, T, -1)
        out = self.o_proj(out)

        # Return with cache if requested
        kv_cache = (k, v) if use_cache else None
        return out, kv_cache


class SwiGLU(nn.Module):
    """
    SwiGLU Activation Function

    SwiGLU(x) = Swish(W1 * x) ⊗ (W2 * x)
    where Swish(x) = x * sigmoid(x)

    Uses 3 linear projections for efficient implementation.
    """

    def __init__(self, d_model: int, d_ff: int, bias: bool = False):
        super().__init__()
        self.w1 = nn.Linear(d_model, d_ff, bias=bias)  # Gate
        self.w2 = nn.Linear(d_model, d_ff, bias=bias)  # Up projection
        self.w3 = nn.Linear(d_ff, d_model, bias=bias)  # Down projection

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # SwiGLU: swish(gate) * up_proj
        gate = F.silu(self.w1(x))  # SiLU = Swish
        up = self.w2(x)
        return self.w3(gate * up)


class Qwen3Block(nn.Module):
    """Qwen3 Transformer Block with Pre-LayerNorm"""

    def __init__(self, config: Qwen3Config):
        super().__init__()
        self.attention = GroupedQueryAttention(config)
        self.feed_forward = SwiGLU(config.d_model, config.d_ff, bias=config.bias)

        # Pre-normalization (normalize before attention/FFN)
        self.ln1 = RMSNorm(config.d_model, eps=config.norm_eps)
        self.ln2 = RMSNorm(config.d_model, eps=config.norm_eps)

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
        use_cache: bool = False,
        past_kv: Optional[Tuple] = None
    ) -> Tuple[torch.Tensor, Optional[Tuple]]:
        # Pre-norm + Attention + Residual
        attn_out, kv_cache = self.attention(self.ln1(x), mask, use_cache, past_kv)
        x = x + attn_out

        # Pre-norm + FFN + Residual
        x = x + self.feed_forward(self.ln2(x))

        return x, kv_cache


class Qwen3Model(nn.Module):
    """Qwen3-4B Language Model"""

    def __init__(self, config: Qwen3Config):
        super().__init__()
        self.config = config

        # Token embeddings
        self.embed = nn.Embedding(config.vocab_size, config.d_model)

        # Transformer blocks
        self.blocks = nn.ModuleList([
            Qwen3Block(config) for _ in range(config.n_layers)
        ])

        # Final layer norm
        self.ln_f = RMSNorm(config.d_model, eps=config.norm_eps)

        # Output projection (LM head)
        if config.tie_weights:
            self.lm_head = None  # Use tied embeddings
        else:
            self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        """Initialize weights following Qwen3 strategy"""
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(
        self,
        idx: torch.Tensor,
        targets: Optional[torch.Tensor] = None,
        use_cache: bool = False,
        past_kvs: Optional[list] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor], Optional[list]]:
        B, T = idx.shape

        # Token embeddings
        x = self.embed(idx)

        # Create causal mask
        mask = torch.triu(torch.full((T, T), float('-inf'), device=idx.device), diagonal=1)

        # Transformer blocks
        new_kvs = [] if use_cache else None
        for i, block in enumerate(self.blocks):
            past_kv = past_kvs[i] if past_kvs else None
            x, kv_cache = block(x, mask, use_cache, past_kv)
            if use_cache:
                new_kvs.append(kv_cache)

        # Final layer norm
        x = self.ln_f(x)

        # Language modeling head
        if self.lm_head is not None:
            logits = self.lm_head(x)
        else:
            # Tied weights: reuse embedding matrix
            logits = F.linear(x, self.embed.weight)

        # Compute loss if targets provided
        loss = None
        if targets is not None:
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                targets.view(-1),
                ignore_index=-1
            )

        return logits, loss, new_kvs

    def generate(
        self,
        idx: torch.Tensor,
        max_new_tokens: int,
        temperature: float = 1.0,
        top_k: Optional[int] = None
    ) -> torch.Tensor:
        """Generate tokens autoregressively"""
        for _ in range(max_new_tokens):
            # Crop context if needed
            idx_cond = idx if idx.size(1) <= self.config.max_seq_len else idx[:, -self.config.max_seq_len:]

            # Forward pass
            logits, _, _ = self(idx_cond)

            # Get logits for last position
            logits = logits[:, -1, :] / temperature

            # Optional top-k sampling
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = float('-inf')

            # Sample from distribution
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)

            # Append to sequence
            idx = torch.cat([idx, idx_next], dim=1)

        return idx

    def count_parameters(self) -> dict:
        """Count model parameters"""
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        embedding = self.embed.weight.numel()
        non_embedding = total - embedding

        return {
            'total': total,
            'trainable': trainable,
            'embedding': embedding,
            'non_embedding': non_embedding
        }


def create_qwen3_4b(vocab_size: int = 50304) -> Qwen3Model:
    """Create Qwen3-4B model with default configuration"""
    config = Qwen3Config(vocab_size=vocab_size)
    model = Qwen3Model(config)

    print("Qwen3-4B Model Created")
    print(f"Parameters: {model.count_parameters()}")

    return model


if __name__ == "__main__":
    # Test model creation
    model = create_qwen3_4b()

    # Test forward pass
    batch_size, seq_len = 4, 128
    idx = torch.randint(0, 50304, (batch_size, seq_len))

    logits, loss, _ = model(idx, targets=idx)
    print(f"\nTest forward pass:")
    print(f"Input shape: {idx.shape}")
    print(f"Output shape: {logits.shape}")
    print(f"Expected: ({batch_size}, {seq_len}, 50304)")
