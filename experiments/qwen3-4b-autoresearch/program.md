# AutoResearch Program: Qwen3-4B on TinyStories

## Objective

Optimize the Qwen3-4B language model training on the TinyStories dataset through autonomous hyperparameter search and architecture exploration.

**Primary Goal:** Minimize validation loss
**Secondary Goals:**
- Stable training (no NaN/exploding gradients)
- Efficient convergence (< 5 minutes per experiment)
- Discover optimal hyperparameter combinations

---

## Model Architecture

**Qwen3-4B Specifications:**
- 36 transformer layers
- 4.0B total parameters (3.6B non-embedding)
- Grouped Query Attention (32 query heads, 8 KV heads)
- SwiGLU activation function
- RMSNorm with pre-normalization
- RoPE (Rotary Positional Embeddings)
- QK-Normalization (Qwen3 innovation)

**Dataset:** TinyStories (karpathy/tinystories-gpt4-clean)
- Small-scale language modeling
- Perfect for rapid experimentation
- Allows 100+ experiments overnight

---

## Research Areas to Explore

### 1. Learning Rate Optimization

**Key Questions:**
- What's the optimal peak learning rate?
- How long should warmup be?
- What should the minimum LR ratio be?

**Experiments to Try:**
```
learning_rate: [3e-4, 6e-4, 1e-3, 2e-3, 4e-3]
warmup_iters: [500, 1000, 2000, 4000]
min_lr (as ratio): [0.01, 0.05, 0.1, 0.2]
```

**Expected Insights:**
- Qwen3 likely prefers moderate LR (around 6e-4)
- Longer warmup helps with 4B model
- Cosine schedule usually outperforms linear

---

### 2. Batch Size & Gradient Accumulation

**Key Questions:**
- What effective batch size is optimal?
- How to balance memory and gradient quality?

**Experiments to Try:**
```
Effective Batch Size = batch_size * gradient_accumulation_steps

Configurations to test:
- 32  = 4 * 8
- 64  = 8 * 8  (baseline)
- 128 = 8 * 16
- 256 = 16 * 16
- 512 = 32 * 16
```

**Expected Insights:**
- Larger batches → more stable gradients
- But diminishing returns after certain size
- Memory constraints on single GPU

---

### 3. Optimizer Configuration

**Key Questions:**
- What Adam beta values work best?
- How much weight decay?
- Does gradient clipping threshold matter?

**Experiments to Try:**
```
beta1: [0.9, 0.95]
beta2: [0.9, 0.95, 0.99]
weight_decay: [0.0, 0.01, 0.05, 0.1, 0.2]
grad_clip: [0.5, 1.0, 2.0, 5.0]
```

**Expected Insights:**
- Beta2 = 0.95 often works well (Qwen3 default)
- Weight decay around 0.1 for regularization
- Gradient clipping prevents instability

---

### 4. Architecture Features

**Key Questions:**
- Does QK-Normalization help on TinyStories?
- Should we tie input/output embeddings?
- Is gradient checkpointing worth the speed cost?

**Experiments to Try:**
```
qk_norm: [true, false]
tie_weights: [true, false]
gradient_checkpointing: [true, false]
```

**Expected Insights:**
- QK-Norm: Stability vs. slight overhead
- Tied weights: Memory savings, but does it hurt quality?
- Grad checkpointing: Essential for 4B model on single GPU

---

### 5. Learning Rate Schedule Variations

**Advanced experiments once basics are optimized:**

**Linear Warmup + Cosine Decay (baseline)**
```
warmup: linear increase
main: cosine decay
min_lr: 10% of peak
```

**Alternative Schedules:**
```
1. No warmup (risky but faster)
2. Longer warmup (more stable)
3. Different min_lr ratios
4. Constant LR (ablation)
```

---

## Experimental Strategy

### Phase 1: Baseline Establishment (Experiments 1-5)
- Run with default configuration
- Establish reproducible baseline
- Check for any immediate issues

**Default Config:**
```python
learning_rate = 6e-4
batch_size = 8
gradient_accumulation_steps = 8
warmup_iters = 2000
weight_decay = 0.1
beta1 = 0.9
beta2 = 0.95
```

### Phase 2: Single-Variable Exploration (Experiments 6-30)
- Vary ONE hyperparameter at a time
- Keep others at baseline
- Identify most impactful parameters

**Priority order:**
1. Learning rate (highest impact expected)
2. Batch size (second highest)
3. Warmup steps
4. Weight decay
5. Optimizer betas

### Phase 3: Combination Search (Experiments 31-60)
- Combine best settings from Phase 2
- Test interactions between hyperparameters
- Example: Best LR + Best batch size

### Phase 4: Architecture Ablations (Experiments 61-80)
- Test architectural features
- QK-Norm, tied weights, grad checkpointing
- May discover efficiency wins

### Phase 5: Fine-Tuning (Experiments 81-100)
- Refine best configuration
- Small adjustments around optimal point
- Try "wild" ideas that might work

---

## Success Criteria

### Primary Metric
**Validation Loss** (lower is better)
- Target: < 3.0 (excellent for TinyStories)
- Good: 3.0 - 3.5
- Acceptable: 3.5 - 4.0

### Secondary Metrics
- **Training Stability**: No NaN losses
- **Convergence Speed**: Iterations to best loss
- **Reproducibility**: Similar results across runs

### Red Flags
- NaN or exploding losses → immediate config rejection
- Validation loss > 5.0 → poor configuration
- No improvement after 1000 iters → bad init or LR

---

## Known Good Baselines (from Qwen3 Paper)

**Qwen3 Training Insights:**
- GQA is crucial for efficiency
- SwiGLU outperforms GELU/ReLU
- RMSNorm faster than LayerNorm
- QK-Norm helps at scale (billions of params)
- Pre-normalization for stability

**Likely Optimal Ranges:**
```
learning_rate: 5e-4 to 1e-3
batch_size (effective): 64 to 256
warmup: 5-10% of total steps
weight_decay: 0.01 to 0.1
betas: (0.9, 0.95) or (0.9, 0.99)
```

---

## Things to Discover

The agent might rediscover:
1. **Optimal LR**: May find that TinyStories needs different LR than large-scale
2. **Batch Size Sweet Spot**: Balance between noise and compute
3. **Warmup Necessity**: How critical is warmup for this scale?
4. **Weight Tying**: Does it help or hurt on small dataset?
5. **Novel Combinations**: Unexpected hyperparameter interactions

**Historical ML Discoveries (that agents have found):**
- RMSNorm over LayerNorm
- Tied embeddings for efficiency
- Learning rate warmup importance
- Gradient clipping thresholds
- Optimal batch sizes for different model sizes

---

## Agent Instructions

### What to Modify
**Primary focus:** `TrainConfig` class in `train.py`
- Hyperparameters (learning_rate, batch_size, etc.)
- Architecture flags (qk_norm, tie_weights)
- Optimizer settings (betas, weight_decay)

### What NOT to Modify
- `experiment_time_limit = 300` (must stay 5 minutes)
- Core model architecture (n_layers, d_model, etc.)
- Dataset loading logic
- Evaluation procedure

### How to Decide
1. **Analyze previous results** - which changes helped?
2. **Follow the gradient** - what direction improves loss?
3. **Be systematic** - vary one thing at a time initially
4. **Be bold later** - try combinations and wild ideas
5. **Track what works** - remember successful patterns

### Expected Behavior
- **Early experiments**: Conservative changes, establish baseline
- **Middle experiments**: Explore broadly, test hypotheses
- **Late experiments**: Exploit best findings, fine-tune

---

## Monitoring & Success

### During Experiments
Watch for:
- Validation loss trend (should decrease)
- Training stability (no NaN)
- Convergence speed (faster is better)

### After Each Experiment
- Did validation loss improve?
- Was training stable?
- What changed from previous best?

### Overall Progress
- Track best loss over time
- Identify patterns in successful configs
- Document surprising findings

---

## Expected Timeline

**Overnight Run (8 hours):**
- ~12 experiments per hour
- ~100 experiments total
- Sufficient to explore major hyperparameters

**Possible Outcomes:**
- **Great**: 15-30% validation loss improvement
- **Good**: 10-15% improvement
- **Acceptable**: 5-10% improvement
- **Learning**: Even no improvement teaches us optimal range

---

## Notes for the Agent

You are an ML researcher. Your job is to:
1. Read previous experimental results
2. Form hypotheses about what might work
3. Modify `train.py` systematically
4. Learn from each experiment

You have the freedom to explore, but be smart:
- Don't make random changes
- Learn from what works and what doesn't
- Try both conservative and bold ideas
- Keep the 5-minute time limit

**Remember:** Even negative results are valuable!
Knowing what doesn't work is progress.

Good luck! 🚀

---

## References

- **Qwen3 Technical Report**: arXiv:2505.09388
- **TinyStories Dataset**: karpathy/tinystories-gpt4-clean
- **AutoResearch**: karpathy/autoresearch (630 lines of autonomous research)
- **Architectural Inspiration**: LLM Architecture Gallery (Raschka, 2026)
