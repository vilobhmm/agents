"""
Qwen3-4B Training Script for AutoResearch
==========================================

This script will be autonomously modified by AI agents to discover
optimal hyperparameters and training strategies.

Training runs for exactly 5 minutes per experiment.
Expects ~100 experiments overnight (~8 hours).

Based on:
- Karpathy's AutoResearch framework
- Qwen3 Technical Report (arXiv:2505.09388)
- TinyStories dataset (karpathy/tinystories-gpt4-clean)
"""

import os
import time
import math
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from datasets import load_dataset

# Import model
import sys
sys.path.append(str(Path(__file__).parent))
from models.qwen3 import Qwen3Model, Qwen3Config


# =============================================================================
# HYPERPARAMETERS - Modified by AutoResearch Agent
# =============================================================================

@dataclass
class TrainConfig:
    """Training configuration - AI agent modifies these values"""

    # Model architecture
    n_layers: int = 36
    n_heads: int = 32
    n_kv_heads: int = 8
    d_model: int = 3072
    d_ff: int = 8192

    # Training
    batch_size: int = 8
    gradient_accumulation_steps: int = 8  # Effective batch: 8 * 8 = 64
    max_iters: int = 10000                # Maximum iterations (5 min limit)
    learning_rate: float = 6e-4
    min_lr: float = 6e-5                  # 10% of max LR
    warmup_iters: int = 2000
    weight_decay: float = 0.1
    grad_clip: float = 1.0

    # Architecture features
    qk_norm: bool = True
    tie_weights: bool = True
    gradient_checkpointing: bool = True

    # Optimizer
    beta1: float = 0.9
    beta2: float = 0.95

    # Data
    seq_length: int = 2048
    vocab_size: int = 50304

    # System
    device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    dtype: str = 'bfloat16'  # Use bfloat16 if available
    compile: bool = True     # torch.compile for speed

    # Evaluation
    eval_interval: int = 500
    eval_iters: int = 100

    # Experiment
    experiment_time_limit: int = 300  # 5 minutes in seconds


# =============================================================================
# Dataset: TinyStories
# =============================================================================

class TinyStoriesDataset(Dataset):
    """TinyStories dataset from HuggingFace"""

    def __init__(self, split: str = 'train', seq_length: int = 2048):
        print(f"Loading TinyStories dataset ({split})...")
        self.seq_length = seq_length

        # Load from HuggingFace
        dataset = load_dataset("karpathy/tinystories-gpt4-clean", split=split)

        # Tokenize using GPT-2 tokenizer
        from transformers import GPT2Tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

        # Tokenize all stories and concatenate
        print("Tokenizing...")
        all_tokens = []
        for story in dataset['story']:
            tokens = self.tokenizer.encode(story)
            all_tokens.extend(tokens)
            all_tokens.append(self.tokenizer.eos_token_id)

        self.tokens = torch.tensor(all_tokens, dtype=torch.long)
        print(f"Loaded {len(self.tokens):,} tokens")

    def __len__(self):
        return (len(self.tokens) - self.seq_length) // self.seq_length

    def __getitem__(self, idx):
        start = idx * self.seq_length
        end = start + self.seq_length + 1  # +1 for target

        chunk = self.tokens[start:end]
        x = chunk[:-1]
        y = chunk[1:]

        return x, y


# =============================================================================
# Learning Rate Schedule
# =============================================================================

def get_lr(it: int, config: TrainConfig) -> float:
    """Cosine learning rate schedule with warmup"""

    # Warmup
    if it < config.warmup_iters:
        return config.learning_rate * (it + 1) / config.warmup_iters

    # Cosine decay
    decay_ratio = (it - config.warmup_iters) / (config.max_iters - config.warmup_iters)
    decay_ratio = max(0, min(1, decay_ratio))  # Clamp to [0, 1]

    coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))
    return config.min_lr + coeff * (config.learning_rate - config.min_lr)


# =============================================================================
# Training Loop
# =============================================================================

def train():
    """Main training loop - runs for exactly 5 minutes"""

    config = TrainConfig()
    print("=" * 80)
    print("Qwen3-4B AutoResearch Training")
    print("=" * 80)
    print(json.dumps(asdict(config), indent=2))
    print("=" * 80)

    # Set random seed
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(42)

    # Setup device
    device = config.device
    dtype = torch.bfloat16 if config.dtype == 'bfloat16' and torch.cuda.is_bf16_supported() else torch.float32
    print(f"Device: {device}")
    print(f"Dtype: {dtype}")

    # Create datasets
    train_dataset = TinyStoriesDataset('train', config.seq_length)
    val_dataset = TinyStoriesDataset('validation', config.seq_length)

    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )

    # Create model
    model_config = Qwen3Config(
        n_layers=config.n_layers,
        n_heads=config.n_heads,
        n_kv_heads=config.n_kv_heads,
        d_model=config.d_model,
        d_ff=config.d_ff,
        vocab_size=config.vocab_size,
        max_seq_len=config.seq_length,
        qk_norm=config.qk_norm,
        tie_weights=config.tie_weights
    )

    model = Qwen3Model(model_config).to(device)

    # Print model info
    params = model.count_parameters()
    print(f"\nModel Parameters:")
    print(f"  Total: {params['total']:,}")
    print(f"  Non-embedding: {params['non_embedding']:,}")
    print(f"  Embedding: {params['embedding']:,}")

    # Compile model (PyTorch 2.0+)
    if config.compile and hasattr(torch, 'compile'):
        print("Compiling model with torch.compile...")
        model = torch.compile(model)

    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        betas=(config.beta1, config.beta2),
        weight_decay=config.weight_decay
    )

    # Training state
    iter_num = 0
    best_val_loss = float('inf')
    start_time = time.time()

    # Gradient scaler for mixed precision
    scaler = torch.cuda.amp.GradScaler(enabled=(dtype == torch.bfloat16))

    print("\nStarting training (5 minute limit)...")
    print("=" * 80)

    # Infinite data iterator
    train_iter = iter(train_loader)

    # Training loop with time limit
    while True:
        # Check time limit (5 minutes = 300 seconds)
        elapsed = time.time() - start_time
        if elapsed >= config.experiment_time_limit:
            print(f"\n⏱️  Time limit reached ({config.experiment_time_limit}s)")
            break

        # Update learning rate
        lr = get_lr(iter_num, config)
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

        # Gradient accumulation
        model.train()
        optimizer.zero_grad()
        total_loss = 0.0

        for micro_step in range(config.gradient_accumulation_steps):
            try:
                x, y = next(train_iter)
            except StopIteration:
                train_iter = iter(train_loader)
                x, y = next(train_iter)

            x, y = x.to(device), y.to(device)

            # Forward pass with mixed precision
            with torch.cuda.amp.autocast(dtype=dtype):
                _, loss, _ = model(x, targets=y)
                loss = loss / config.gradient_accumulation_steps

            total_loss += loss.item()

            # Backward pass
            scaler.scale(loss).backward()

        # Gradient clipping
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), config.grad_clip)

        # Optimizer step
        scaler.step(optimizer)
        scaler.update()

        # Logging
        if iter_num % 10 == 0:
            print(f"iter {iter_num:5d} | loss {total_loss:.4f} | lr {lr:.2e} | {elapsed:.1f}s")

        # Evaluation
        if iter_num % config.eval_interval == 0 and iter_num > 0:
            model.eval()
            val_loss = 0.0

            with torch.no_grad():
                for eval_iter, (x, y) in enumerate(val_loader):
                    if eval_iter >= config.eval_iters:
                        break

                    x, y = x.to(device), y.to(device)

                    with torch.cuda.amp.autocast(dtype=dtype):
                        _, loss, _ = model(x, targets=y)

                    val_loss += loss.item()

            val_loss /= min(config.eval_iters, len(val_loader))

            print("-" * 80)
            print(f"📊 Validation | iter {iter_num} | loss {val_loss:.4f}")
            print("-" * 80)

            # Track best
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                print(f"✨ New best validation loss: {best_val_loss:.4f}")

        iter_num += 1

        # Safety: max iterations
        if iter_num >= config.max_iters:
            break

    # Final evaluation
    print("\n" + "=" * 80)
    print("Final Evaluation")
    print("=" * 80)

    model.eval()
    final_val_loss = 0.0

    with torch.no_grad():
        for eval_iter, (x, y) in enumerate(val_loader):
            if eval_iter >= config.eval_iters:
                break

            x, y = x.to(device), y.to(device)

            with torch.cuda.amp.autocast(dtype=dtype):
                _, loss, _ = model(x, targets=y)

            final_val_loss += loss.item()

    final_val_loss /= min(config.eval_iters, len(val_loader))

    # Results
    results = {
        'final_val_loss': final_val_loss,
        'best_val_loss': best_val_loss,
        'iterations': iter_num,
        'time_seconds': time.time() - start_time,
        'config': asdict(config)
    }

    print(f"\n📈 Results:")
    print(f"   Final validation loss: {final_val_loss:.4f}")
    print(f"   Best validation loss: {best_val_loss:.4f}")
    print(f"   Iterations: {iter_num}")
    print(f"   Time: {results['time_seconds']:.1f}s")

    # Save results for autoresearch
    results_file = Path(__file__).parent / 'logs' / 'latest_result.json'
    results_file.parent.mkdir(exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved to: {results_file}")
    print("=" * 80)

    return final_val_loss


if __name__ == "__main__":
    train()
