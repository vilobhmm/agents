# LLM Architecture Gallery - Pool of Ideas

> Comprehensive collection of Large Language Model architectures from Sebastian Raschka's research (2024-2026)
>
> **Sources:**
> - [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/)
> - [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
> - [A Dream of Spring for Open-Weight LLMs (Jan-Feb 2026)](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)

---

## Table of Contents

1. [Architecture Evolution Overview](#architecture-evolution-overview)
2. [Core Architectural Components](#core-architectural-components)
3. [Major LLM Architectures (2024-2026)](#major-llm-architectures-2024-2026)
4. [Architecture Innovations & Patterns](#architecture-innovations--patterns)
5. [Comparative Analysis](#comparative-analysis)
6. [Implementation Ideas](#implementation-ideas)

---

## Architecture Evolution Overview

### Key Insight
**Models from GPT-2 (2019) to DeepSeek V3 and Llama 4 (2024-2025) are structurally similar**, but key details have evolved:

| Component | 2019 (GPT-2) | 2024-2026 (Modern) |
|-----------|--------------|---------------------|
| **Positional Embeddings** | Absolute | Rotary (RoPE) |
| **Attention Mechanism** | Multi-Head Attention (MHA) | Grouped-Query Attention (GQA) / MLA |
| **Activation Functions** | GELU | SwiGLU |
| **Architecture Type** | Dense | Dense + MoE (Mixture of Experts) |
| **Context Length** | 1K-2K tokens | 128K-1M+ tokens |

### Core Philosophy (2026 Consensus)
> "Various model architectures (all derived from the original GPT model) work well. Modeling performance is likely attributed to **dataset quality and training recipes** rather than architecture design itself."
>
> — Sebastian Raschka, February 2026

---

## Core Architectural Components

### 1. Attention Mechanisms

#### Multi-Head Attention (MHA) - Classic
```
Traditional approach: Each head has its own Q, K, V projections
- High memory usage
- Standard in GPT-2, BERT, early transformers
```

#### Grouped-Query Attention (GQA) - Industry Default (2024-2026)
```
Shares key-value pairs across groups of query heads
- Memory efficient
- Used in: Llama 4, Qwen3, Mistral Small 3.1, SmolLM3, Gemma 3
- Industry standard for most 2025-2026 models
```

**Architecture Pattern:**
- Multiple query heads per group
- Shared K, V across group
- Reduces KV cache size
- Minimal computational overhead

#### Multi-Head Latent Attention (MLA) - Advanced
```
Compresses key-value pairs into low-dimensional latent space before caching
- Maximum memory savings (better than GQA)
- Higher computational overhead
- Used in: DeepSeek V3/R1, Kimi K2.5, GLM-5, Ling 2.5
```

**Trade-off:**
- **GQA**: Better speed, good memory savings
- **MLA**: Maximum memory savings, slower inference

#### Gated DeltaNet
```
Novel attention variant
- Used in: Qwen3.5
- Experimental approach combining gating with attention
```

### 2. Positional Encodings

#### Rotary Positional Embeddings (RoPE)
```
Standard in modern LLMs (2024-2026)
- Relative position encoding
- Better long-context handling
- Enables context extension
- Used in: Nearly all modern models
```

**Benefits:**
- Naturally extends to longer sequences
- Maintains positional relationships
- No absolute position limit

### 3. Activation Functions

#### SwiGLU (Swish-Gated Linear Unit)
```
Current industry standard
- Replaces GELU/ReLU
- Better training dynamics
- Slightly higher compute cost
- Used in: Most 2024-2026 models
```

**Formula:**
```
SwiGLU(x) = Swish(W₁x) ⊗ (W₂x)
where Swish(x) = x · σ(βx)
```

### 4. Normalization

#### Layer Normalization Variants
- **Pre-LayerNorm**: Before attention/FFN (standard)
- **Post-LayerNorm**: After attention/FFN (legacy)
- **RMSNorm**: Root Mean Square Normalization (more efficient)

Most 2025-2026 models use **Pre-LayerNorm** with **RMSNorm**.

---

## Major LLM Architectures (2024-2026)

### 1. DeepSeek Series

#### DeepSeek V3 (December 2024)
**Specs:**
- **Total Parameters**: 671B
- **Active Parameters**: 37B
- **Architecture**: MoE (Mixture of Experts)
- **Experts**: 256 total, 9 active per token
- **Expert Hidden Size**: 2,048
- **Context Length**: 128K tokens

**Key Innovations:**
- Multi-Head Latent Attention (MLA)
- MoE in each transformer block (except first 3)
- No shared expert
- Efficient auxiliary loss for load balancing

**Architecture Pattern:**
```
[Input] → [3 Dense Layers] → [253 MoE Layers] → [Output]
Each MoE Layer:
  - MLA attention
  - Top-9 expert routing
  - 2,048 hidden size per expert
```

#### DeepSeek R1 (January 2025)
**Focus:** Reinforcement Learning reasoning model
- Based on V3 architecture
- Enhanced reasoning capabilities
- Chain-of-thought training

#### DeepSeek V3.1 (August 2025)
**Specs:**
- **Parameters**: 671B (37B active)
- **Context**: 128K tokens
- **Hybrid**: Combines V3 + R1 strengths

#### DeepSeek V3.2 (Late 2025)
**Latest refinement** with improved performance

**Use Cases:**
- Code generation (excellent)
- Long-context tasks
- Reasoning-heavy applications

---

### 2. Llama Series (Meta)

#### Llama 4 (2024-2025)
**Base Model:**
- Grouped-Query Attention (GQA)
- RoPE positional embeddings
- SwiGLU activation

#### Llama 4 Maverick (MoE Variant)
**Specs:**
- **Architecture**: MoE
- **Active Experts**: 2 per token
- **Expert Hidden Size**: 8,192
- **Pattern**: Alternates MoE and dense modules

**Architectural Difference from DeepSeek V3:**
```
Llama 4 Maverick:    [Dense] → [MoE] → [Dense] → [MoE] → ...
DeepSeek V3:         [Dense × 3] → [MoE] → [MoE] → [MoE] → ...

Expert Configuration:
Llama 4 Maverick:    2 experts @ 8,192 hidden size
DeepSeek V3:         9 experts @ 2,048 hidden size
```

**Philosophy:**
- Fewer, larger experts (Llama)
- More, smaller experts (DeepSeek)

---

### 3. Qwen Series (Alibaba)

#### Qwen3 (Late 2024)
**Specs:**
- **Model**: 235B total (22B active)
- **Attention**: Grouped-Query Attention (GQA)
- **Architecture**: MoE

**Key Change:**
- Removed shared expert (used in Qwen2.5-MoE)
- Similar architecture to DeepSeek V3

#### Qwen3.5 (2025)
**Innovation:**
- **Gated DeltaNet** attention mechanism
- Experimental attention variant
- Novel approach to attention computation

#### Qwen3-Coder-Next (February 2026)
**Specs:**
- **Total Parameters**: 80B
- **Active Parameters**: 3B
- **Specialization**: Code generation

**Achievement:**
- **Outperformed much larger models** on coding tasks
- Beat DeepSeek V3.2 and Kimi K2.5
- Demonstrates: Small, specialized > Large, general (for specific tasks)

**Architecture Insight:**
```
80B total, only 3B active = 3.75% activation rate
Extremely efficient for code tasks
```

---

### 4. Kimi Series

#### Kimi K2 (2025)
**Key Feature:**
- Multi-Head Latent Attention (MLA)
- Adapted from DeepSeek's approach

#### Kimi K2.5 (Late 2025)
**Refinement:**
- Enhanced MLA implementation
- Improved memory efficiency
- Long-context specialization

**Use Cases:**
- Long-document analysis
- Multi-turn conversations
- Memory-constrained environments

---

### 5. GLM Series

#### GLM-4.5 (2024)
**Architecture:**
- General Language Model
- Encoder-decoder style
- Unique position in the landscape

#### GLM-5 (2025)
**Innovation:**
- Multi-Head Latent Attention (MLA)
- Adopted advanced attention mechanism
- Enhanced performance

---

### 6. OLMo Series (AI2)

#### OLMo 2 (2024-2025)
**Philosophy:**
- **Fully open**: Data, code, training process
- Research-focused architecture
- Reproducible training

**Contribution:**
- Open science approach
- Detailed documentation
- Training transparency

---

### 7. Gemma Series (Google)

#### Gemma 3 (2024-2025)
**Architecture:**
- Grouped-Query Attention (GQA)
- Standard modern architecture
- Efficient inference

**Sizes:**
- Multiple size variants
- Optimized for different use cases

---

### 8. Mistral Series

#### Mistral Small 3.1 (2024-2025)
**Focus:**
- Efficient small model
- Grouped-Query Attention (GQA)
- High quality despite size

**Design Philosophy:**
- Quality over quantity
- Efficient architecture
- Practical deployment

---

### 9. SmolLM3 (Hugging Face)

**Specs:**
- **Extremely small** model
- Grouped-Query Attention (GQA)
- Efficient for edge devices

**Use Cases:**
- Mobile deployment
- Edge computing
- Resource-constrained environments

**Innovation:**
- Proves small models can be capable
- Efficient training recipes
- Distillation techniques

---

### 10. Grok Series (xAI)

#### Grok 2.5 (2024-2025)
**Architecture:**
- MoE (Mixture of Experts)
- Large-scale training
- Real-time data integration

**Unique Feature:**
- Integration with X (Twitter) data
- Real-time information

---

### 11. GPT-OSS (2024-2025)

**Concept:**
- Open-source GPT architecture
- Community-driven development
- Standard transformer architecture

---

### 12. Ling Series

#### Ling 2.5 (2026)
**Innovation:**
- Multi-Head Latent Attention (MLA)
- Part of MLA adoption wave
- Regional focus (China)

---

### 13. Sarvam (India)

#### Sarvam 30B & 100B (2026)
**Specialization:**
- **Indian languages** (Hindi, Tamil, Telugu, etc.)
- Regional focus
- Multilingual architecture

**Performance:**
- **90% preference** on Indian language texts
- Demonstrates importance of language-specific training
- Cultural and linguistic adaptation

**Architecture:**
- Standard modern components
- Likely GQA or MLA
- Optimized for multilingual tasks

**Significance:**
- Shows regional models can excel
- Language-specific optimization matters
- Dataset quality for target languages

---

### 14. MiniMax Series

#### MiniMax M2.5 (2026)
**Design:**
- **Grouped Query Attention only**
- No additional efficiency tweaks
- Simple, effective architecture

**Philosophy:**
- Simplicity over complexity
- Proves GQA is sufficient
- Clean architecture

---

### 15. Nanbeige 4.1 (2026)

**Design:**
- Similar to MiniMax M2.5
- **GQA without extra optimizations**
- Validates simple approach

**Insight:**
- Complex architectures not always needed
- Good training > fancy architecture
- Data quality matters most

---

## Architecture Innovations & Patterns

### Attention Mechanism Trends (2024-2026)

#### The Three Schools
1. **GQA School** (Majority)
   - Llama 4, Qwen3, Mistral, Gemma 3, SmolLM3
   - Industry default
   - Best balance of speed and memory

2. **MLA School** (Innovation Leaders)
   - DeepSeek V3/R1, Kimi K2.5, GLM-5, Ling 2.5
   - Maximum memory efficiency
   - Research-driven

3. **Experimental School**
   - Qwen3.5 (Gated DeltaNet)
   - Novel mechanisms
   - Future exploration

### MoE (Mixture of Experts) Design Patterns

#### Pattern 1: High Expert Count, Small Size
**Example: DeepSeek V3**
```
- 256 total experts
- 9 active experts
- 2,048 hidden size per expert
- MoE in every layer (except first 3)
```

**Benefits:**
- Fine-grained specialization
- Better load balancing
- More routing options

#### Pattern 2: Low Expert Count, Large Size
**Example: Llama 4 Maverick**
```
- Fewer total experts
- 2 active experts
- 8,192 hidden size per expert
- Alternates MoE and dense layers
```

**Benefits:**
- Simpler routing
- Larger expert capacity
- Easier to train

#### Pattern 3: No Shared Expert
**Trend in 2025-2026:**
- Qwen3 removed shared expert
- DeepSeek V3 has no shared expert
- **Insight**: Shared experts may not be necessary

### Context Length Evolution

| Model | Context Length | Year |
|-------|---------------|------|
| GPT-2 | 1K | 2019 |
| GPT-3 | 2K | 2020 |
| GPT-4 | 8K-32K | 2023 |
| Claude 2 | 100K | 2023 |
| Gemini 1.5 | 1M | 2024 |
| DeepSeek V3 | 128K | 2024 |
| GPT-4 Turbo | 128K | 2024 |

**Enabling Technologies:**
- RoPE (Rotary Positional Embeddings)
- Efficient attention mechanisms (GQA, MLA)
- Memory optimizations
- Training improvements

---

## Comparative Analysis

### Architecture Similarity Matrix

```
High Similarity:
├── DeepSeek V3 ↔ Qwen3 235B (MoE structure)
├── Llama 4 ↔ Mistral ↔ Gemma 3 (GQA standard)
├── Kimi K2.5 ↔ GLM-5 ↔ Ling 2.5 (MLA adoption)
└── MiniMax M2.5 ↔ Nanbeige 4.1 (Pure GQA)

Unique Architectures:
├── Qwen3.5 (Gated DeltaNet)
├── Sarvam (Multilingual specialization)
└── SmolLM3 (Extreme efficiency)
```

### Performance vs. Architecture Insights

#### Key Finding: Size ≠ Performance
**Qwen3-Coder-Next (80B/3B active) > DeepSeek V3.2 (671B/37B active)**
- For code generation tasks
- Specialization matters
- Dataset quality > parameter count

#### Key Finding: Simple Works
**MiniMax M2.5 & Nanbeige 4.1**
- Use only GQA (no fancy techniques)
- Achieve competitive performance
- Training > architecture complexity

#### Key Finding: Regional Specialization
**Sarvam (Indian languages)**
- 90% preference on target languages
- Specialized training data crucial
- One size doesn't fit all

### Efficiency Comparison

| Model | Total Params | Active Params | Activation Rate | Efficiency Strategy |
|-------|--------------|---------------|-----------------|---------------------|
| DeepSeek V3 | 671B | 37B | 5.5% | MoE + MLA |
| Llama 4 Maverick | ~400B* | ~20B* | ~5%* | MoE + GQA |
| Qwen3 | 235B | 22B | 9.4% | MoE + GQA |
| Qwen3-Coder | 80B | 3B | 3.75% | Extreme MoE |
| Sarvam | 30-100B | N/A | N/A | Dense + Multilingual |

*Estimated values

---

## Implementation Ideas

### 1. Build Your Own Architecture

#### Starter Architecture (Modern Standard)
```python
class ModernLLM:
    components = {
        'attention': 'Grouped-Query Attention (GQA)',
        'positional': 'RoPE (Rotary Positional Embeddings)',
        'activation': 'SwiGLU',
        'normalization': 'RMSNorm (Pre-LayerNorm)',
        'architecture': 'Decoder-only transformer'
    }

    # This will work well for most use cases (2024-2026 consensus)
```

#### Advanced Architecture (Memory-Optimized)
```python
class AdvancedLLM:
    components = {
        'attention': 'Multi-Head Latent Attention (MLA)',
        'positional': 'RoPE',
        'activation': 'SwiGLU',
        'normalization': 'RMSNorm',
        'architecture': 'Decoder-only transformer'
    }

    # Better for long-context or memory-constrained scenarios
```

#### MoE Architecture (Efficiency)
```python
class MoELLM:
    components = {
        'attention': 'GQA or MLA',
        'positional': 'RoPE',
        'activation': 'SwiGLU',
        'normalization': 'RMSNorm',
        'architecture': 'MoE transformer',
        'expert_config': {
            'total_experts': 128,  # Adjust based on compute
            'active_experts': 4-8,
            'routing': 'Top-K',
            'load_balancing': 'Auxiliary loss'
        }
    }
```

### 2. Specialization Strategies

#### Code-Specialized Model (Inspired by Qwen3-Coder)
- **Small active parameters** (3-5B)
- **Large total capacity** (80-100B with MoE)
- **Specialized dataset**: GitHub, StackOverflow, documentation
- **Expert specialization**: Different languages per expert

#### Multilingual Model (Inspired by Sarvam)
- **Language-specific experts**
- **Balanced multilingual training**
- **Regional dataset focus**
- **Cultural context integration**

#### Long-Context Model (Inspired by Kimi K2)
- **MLA attention** for memory efficiency
- **Extended RoPE**
- **128K+ context length**
- **Document-level training**

### 3. Efficiency Techniques to Implement

#### Memory Optimization
1. **Gradient Checkpointing**: Save memory during training
2. **Mixed Precision**: FP16/BF16 for faster training
3. **FlashAttention**: Efficient attention computation
4. **KV Cache Optimization**: GQA or MLA

#### Training Optimization
1. **Dataset Quality**: Most important factor (2026 consensus)
2. **Data Mix**: Careful curation of training data
3. **Learning Rate Schedule**: Cosine with warmup
4. **Batch Size**: Large batches with gradient accumulation

#### Inference Optimization
1. **MoE Routing**: Efficient expert selection
2. **Quantization**: INT8/INT4 for deployment
3. **Speculative Decoding**: Faster generation
4. **Continuous Batching**: Higher throughput

### 4. Research Directions (Inspired by 2026 Trends)

#### Attention Mechanism Exploration
- **Gated DeltaNet** (Qwen3.5) - explore gating mechanisms
- **Hybrid attention** - combine different attention types
- **Linear attention** - O(n) complexity research

#### MoE Architecture Innovation
- **Dynamic expert count** - adjust based on task
- **Hierarchical experts** - multi-level specialization
- **Expert merging** - reduce expert count post-training

#### Specialized Model Development
- **Domain-specific models** (code, math, science)
- **Language-specific models** (regional languages)
- **Task-specific models** (reasoning, summarization)

### 5. Training Recipe Template

```python
training_config = {
    'architecture': {
        'attention': 'GQA',  # or MLA for long context
        'experts': None,     # or MoE config
        'hidden_size': 4096,
        'num_layers': 32,
        'num_heads': 32,
        'head_dim': 128
    },
    'data': {
        'quality': 'HIGH_PRIORITY',  # Most important!
        'mix': {
            'web': 0.45,
            'books': 0.20,
            'code': 0.15,
            'academic': 0.10,
            'conversation': 0.10
        },
        'deduplication': True,
        'filtering': 'aggressive'
    },
    'training': {
        'optimizer': 'AdamW',
        'learning_rate': 1e-4,
        'schedule': 'cosine_with_warmup',
        'warmup_steps': 2000,
        'batch_size': 4096,  # tokens per batch
        'gradient_accumulation': 8,
        'mixed_precision': 'bf16',
        'gradient_checkpointing': True
    },
    'evaluation': {
        'benchmarks': ['MMLU', 'HumanEval', 'GSM8K', 'BBH'],
        'frequency': 'every_1000_steps'
    }
}
```

---

## Key Takeaways (2024-2026)

### 1. **Architecture Matters Less Than Expected**
> "Various model architectures work well. Performance is attributed to **dataset quality and training recipes** rather than architecture design."

### 2. **GQA is the Safe Default**
- Industry standard for 2024-2026
- Good balance of efficiency and performance
- Used by majority of new models

### 3. **MLA for Specialized Use Cases**
- Best for long-context applications
- Memory-constrained environments
- Worth the computational overhead when memory is critical

### 4. **MoE Enables Scaling**
- Activate only what you need (3-10% of parameters)
- Two valid approaches: many-small or few-large experts
- No shared expert is the trend

### 5. **Specialization > General Scaling**
- Qwen3-Coder (3B active) > DeepSeek V3 (37B active) for code
- Sarvam dominates Indian languages
- **Domain-specific data + focused architecture > massive general model**

### 6. **Simple Can Be Sufficient**
- MiniMax M2.5 and Nanbeige 4.1: Just GQA, nothing fancy
- Competitive performance
- **Good training > architectural complexity**

### 7. **Long Context is Standard**
- 128K+ context is expected in 2024-2026
- Enabled by RoPE + efficient attention
- Required for modern applications

### 8. **Open Weights Explosion**
- 10+ major architectures released in Jan-Feb 2026 alone
- Rapid innovation cycle
- Community-driven improvements

---

## Future Directions (Post-2026)

### Predicted Trends

1. **Further Specialization**
   - More domain-specific models
   - Task-specific architectures
   - Regional and language-specific models

2. **Efficiency Focus**
   - Smaller active parameters
   - Better MoE routing
   - Novel attention mechanisms

3. **Longer Contexts**
   - 1M+ token context (already demonstrated by Gemini)
   - Efficient long-context attention
   - Multi-document reasoning

4. **Hybrid Approaches**
   - Combining different attention mechanisms
   - Dense + MoE mixing
   - Multi-modal integration

5. **Training Innovation**
   - Better data curation
   - Synthetic data generation
   - Curriculum learning

---

## Resources & References

### Sebastian Raschka's Work
- 🌐 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/)
- 📝 [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
- 📝 [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
- 📝 [Technical Tour of DeepSeek Models](https://magazine.sebastianraschka.com/p/technical-deepseek)
- 📝 [The State of LLMs 2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025)
- 📝 [Beyond Standard LLMs](https://magazine.sebastianraschka.com/p/beyond-standard-llms)
- 📺 [Narrated Video Lecture](https://x.com/rasbt/status/1965798055141429523)

### Additional Resources
- 📚 [LLMs from Scratch (GitHub)](https://github.com/rasbt/LLMs-from-scratch)
- 🎤 [PyConDE 2026 Keynote](https://2026.pycon.de/keynote-sebastian-raschka/)
- 🎙️ [Interview on State of Open LLMs](https://www.interconnects.ai/p/interviewing-sebastian-raschka)

### Model Documentation
- DeepSeek: [Complete Guide to DeepSeek Models](https://www.bentoml.com/blog/the-complete-guide-to-deepseek-models-from-v3-to-r1-and-beyond)
- Architecture Deep Dive: [LLM Architecture Explained](https://langcopilot.com/posts/2025-07-22-from-deepseek-v3-to-kimi-k2-eight-modern-llm-architectures)
- Open-Source Architectures: [ByteByteGo Analysis](https://blog.bytebytego.com/p/the-architecture-behind-open-source)

---

## Conclusion

The LLM architecture landscape of 2024-2026 reveals that while the core transformer architecture remains dominant, **implementation details matter**:

- **GQA** is the industry standard attention mechanism
- **MLA** offers advanced memory optimization for specific use cases
- **MoE** enables efficient scaling to massive parameter counts
- **Dataset quality** and **training recipes** are more important than architectural complexity
- **Specialization** (domain, language, task) beats general scaling
- **Simple architectures** with good training can compete with complex designs

For practitioners:
- **Start with standard architecture** (GQA + RoPE + SwiGLU)
- **Focus on data quality** above all else
- **Specialize** for your use case rather than building general models
- **Use MoE** if you need scale with limited compute
- **Consider MLA** only if memory is the primary constraint

The field is moving fast, with 10+ new architectures in early 2026 alone, but the fundamentals remain: **good data, good training, appropriate architecture for your use case.**

---

**Document Version**: 1.0
**Last Updated**: March 2026
**Based on**: Sebastian Raschka's LLM Architecture Gallery and related publications

**License**: Educational use - Please cite original sources
