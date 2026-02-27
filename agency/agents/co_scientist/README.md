# 🔬 Co-Scientist Co-Founder Agent

**Your AI partner for building science-based companies**

Combines deep scientific research expertise with startup strategy and business acumen. From research hypothesis to funded startup.

---

## 🎯 What It Does

The Co-Scientist Co-Founder Agent is your AI partner that can:

### 🔬 **Scientific Research**
- Conduct literature reviews
- Analyze research papers
- Generate testable hypotheses
- Design rigorous experiments
- Analyze experimental data
- Identify research gaps

### 💼 **Startup & Business**
- Develop business strategy
- Create pitch decks
- Plan fundraising
- Conduct market analysis
- Competitive research
- Go-to-market strategy

### 🚀 **Integrated Workflows**
- Research → Startup pipeline
- Hypothesis → Validation → Business
- Complete research-to-fundraising journey

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install dependencies
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY=sk-ant-...
```

### Run Interactive Mode

```bash
python -m agency.agents.co_scientist.co_scientist_agent

# Choose from menu:
# 1-5: Research capabilities
# 6-9: Business capabilities
# 10: Complete research-to-startup workflow
```

---

## 💻 Using the Agent

### In Code

```python
from agency.agents.co_scientist import CoScientistAgent

agent = CoScientistAgent()

# Literature review
result = await agent.literature_review(
    topic="CRISPR gene editing for cancer therapy",
    depth="comprehensive"
)

# Generate hypotheses
result = await agent.generate_hypothesis(
    observation="Cells show increased resistance after treatment",
    domain="oncology"
)

# Business strategy
result = await agent.business_strategy(
    idea="AI-powered drug discovery platform",
    market="pharmaceutical",
    stage="early"
)

# Complete workflow
result = await agent.research_to_startup_workflow(
    research_idea="Novel mRNA delivery mechanism",
    domain="biotechnology"
)
```

---

## 🔬 Research Capabilities

### 1. Literature Review

Conducts comprehensive literature reviews on any scientific topic.

```python
result = await agent.literature_review(
    topic="quantum computing for drug discovery",
    depth="comprehensive"  # or "quick", "moderate"
)
```

**Output:**
- Summary of current research
- Key research areas
- Research gaps and opportunities
- Common methodologies
- Recommended next steps

---

### 2. Paper Analysis

Analyzes research papers with critical evaluation.

```python
result = await agent.analyze_paper(
    paper_text="[paste abstract or full text]",
    focus="methodology"  # optional: methodology, results, etc.
)
```

**Output:**
- Key findings
- Methodology evaluation
- Strengths and limitations
- Implications for the field
- Follow-up questions
- Reproducibility assessment

---

### 3. Hypothesis Generation

Generates multiple testable hypotheses.

```python
result = await agent.generate_hypothesis(
    observation="Treatment X shows variable efficacy across patients",
    domain="personalized medicine",
    background="Previous studies show genetic factors..."
)
```

**Output (3-5 hypotheses):**
- Hypothesis statement
- Null hypothesis
- Predictions
- Test methods
- Variables to measure
- Timeline and success criteria

---

### 4. Experiment Design

Designs rigorous experimental protocols.

```python
result = await agent.design_experiment(
    hypothesis="Gene Y regulates response to Treatment X",
    constraints={
        "budget": "$50K",
        "timeline": "6 months",
        "equipment": "Standard molecular biology lab"
    }
)
```

**Output:**
- Objective and rationale
- Complete materials list
- Step-by-step protocol
- Sample size calculation
- Controls and variables
- Data collection methods
- Statistical analysis plan
- Timeline and safety considerations

---

### 5. Data Analysis

Analyzes experimental data with statistical rigor.

```python
result = await agent.analyze_data(
    data_description="""
    Measured cell viability across 3 treatment groups (n=30 each):
    - Control: 95% ± 3%
    - Treatment A: 78% ± 8%
    - Treatment B: 45% ± 12%
    """,
    analysis_type="comprehensive"
)
```

**Output:**
- Descriptive statistics
- Appropriate statistical tests
- Significance levels
- Visualization recommendations
- Interpretation
- Limitations and next steps

---

## 💼 Business Capabilities

### 1. Business Strategy

Develops comprehensive startup strategy.

```python
result = await agent.business_strategy(
    idea="AI-powered protein folding prediction SaaS",
    market="pharmaceutical R&D",
    stage="early"  # early, growth, or scale
)
```

**Output:**
- Value proposition
- Market analysis (TAM/SAM/SOM)
- Competitive landscape
- Business model and revenue streams
- Go-to-market strategy
- Milestones (6/12/18 months)
- Risk mitigation
- Team needs

---

### 2. Pitch Deck Creation

Creates complete pitch deck content.

```python
result = await agent.create_pitch_deck(
    company_info={
        "name": "BioInnovate",
        "problem": "Drug discovery takes 10+ years and $2B",
        "solution": "AI reduces time to 2 years, cost to $100M"
    },
    target_audience="seed_investors"  # or series_a, corporate
)
```

**Output (12-slide deck):**
1. Cover - Company name and tagline
2. Problem - Market pain points
3. Solution - Your innovation
4. Product/Technology - How it works
5. Market Opportunity - TAM/SAM/SOM
6. Business Model - Revenue and pricing
7. Traction - Milestones and metrics
8. Competition - Landscape and advantages
9. Go-to-Market - Customer acquisition
10. Team - Founders and expertise
11. Financials - 3-5 year projections
12. Ask - Funding and use of funds

---

### 3. Fundraising Strategy

Plans complete fundraising approach.

```python
result = await agent.fundraising_strategy(
    stage="seed",  # pre-seed, seed, series-a
    amount="2M",
    use_of_funds="Product development and first hires"
)
```

**Output:**
- Fundraising strategy and timeline
- Investor targeting (specific firms/angels)
- Required materials
- Week-by-week process
- Terms to negotiate
- Founder preparation
- Alternative funding (grants, non-dilutive)

---

### 4. Market Analysis

Conducts comprehensive market research.

```python
result = await agent.market_analysis(
    product="Point-of-care diagnostic device",
    industry="medical diagnostics"
)
```

**Output:**
- Market size (TAM/SAM/SOM)
- Customer segments and pain points
- Market trends
- Competitive analysis
- Market entry strategy
- Risks and opportunities

---

## 🚀 Complete Workflow: Research → Startup

The most powerful feature - automated research-to-startup pipeline:

```python
result = await agent.research_to_startup_workflow(
    research_idea="Novel CRISPR delivery mechanism using nanoparticles",
    domain="gene therapy"
)
```

**This runs:**
1. **Literature Review** - What's known about CRISPR delivery?
2. **Hypothesis Generation** - What could make it better?
3. **Business Strategy** - How to commercialize?
4. **Market Analysis** - Who needs this? How big is the market?
5. **Pitch Deck** - How to present to investors?

**Output:**
Complete package with all research and business materials ready to go!

---

## 📊 Real-World Examples

### Example 1: Research Idea → Startup Plan

```bash
python -m agency.agents.co_scientist.co_scientist_agent

> 10  # Research-to-startup workflow

Research idea: AI-powered early cancer detection from blood tests
Scientific domain: liquid biopsy

📚 Step 1: Conducting literature review...
[Analyzes current research in liquid biopsy and early detection]

💡 Step 2: Generating hypotheses...
[Creates testable hypotheses about biomarker combinations]

💼 Step 3: Developing business strategy...
[Market: $5B liquid biopsy market, 15% CAGR]
[Target: Oncologists and cancer screening centers]

📊 Step 4: Analyzing market...
[TAM: $10B, SAM: $2B, SOM: $200M in 5 years]

🎯 Step 5: Creating pitch deck outline...
[12-slide deck ready for seed investors]

✅ Workflow complete!
```

---

### Example 2: Analyze Breakthrough Paper

```python
paper_text = """
Abstract: We demonstrate a novel approach to protein design using
large language models trained on protein sequences...
[full abstract]
"""

result = await agent.analyze_paper(paper_text, focus="commercial potential")

# Output analyzes:
# - Technical innovation
# - Competitive advantages
# - Patent landscape
# - Market applications
# - Commercialization strategy
```

---

### Example 3: Design Validation Experiment

```python
# After generating hypothesis
result = await agent.design_experiment(
    hypothesis="Combining biomarkers A, B, and C increases early detection sensitivity to >95%",
    constraints={
        "budget": "$100K",
        "timeline": "3 months",
        "samples": "100 patient samples available"
    }
)

# Get complete protocol:
# - Sample preparation
# - Assay protocols
# - Quality controls
# - Statistical power analysis
# - Data analysis plan
```

---

## 🎯 Use Cases

### For Researchers

**Transitioning from academia to startup:**
```python
# 1. Review existing research
lit_review = await agent.literature_review("my research area")

# 2. Find commercial opportunities
strategy = await agent.business_strategy(
    idea="My research application",
    market="target industry"
)

# 3. Create investor materials
pitch = await agent.create_pitch_deck(company_info)
```

---

### For Founders

**Building science-based company:**
```python
# 1. Validate scientific hypothesis
hypothesis = await agent.generate_hypothesis(observation, domain)

# 2. Design validation experiments
experiment = await agent.design_experiment(hypothesis)

# 3. Plan go-to-market
market = await agent.market_analysis(product, industry)

# 4. Prepare for fundraising
fundraising = await agent.fundraising_strategy(stage, amount, use)
```

---

### For Investors

**Technical due diligence:**
```python
# 1. Analyze scientific foundation
paper_analysis = await agent.analyze_paper(company_paper)

# 2. Evaluate market opportunity
market = await agent.market_analysis(product, industry)

# 3. Assess competitive position
strategy = await agent.business_strategy(idea, market)
```

---

## 🧬 Supported Domains

The agent has deep knowledge across:

- **Life Sciences**: Biology, genetics, biotech, pharma
- **Chemistry**: Drug discovery, materials science
- **Physics**: Quantum computing, photonics
- **Computer Science**: AI/ML, computational biology
- **Engineering**: Biomedical, chemical, materials
- **Medicine**: Diagnostics, therapeutics, medical devices
- **Climate**: Clean tech, carbon capture, renewables

---

## 💡 Tips & Best Practices

### For Better Results

1. **Be Specific**: "CRISPR for sickle cell" > "gene editing"
2. **Provide Context**: Include background when available
3. **Iterate**: Use outputs to refine next questions
4. **Save Work**: Use `agent.save_project()` regularly

### Workflow Recommendations

```python
# Best Practice: Iterative refinement
agent = CoScientistAgent()

# Start broad
lit_review = await agent.literature_review("cancer immunotherapy")

# Narrow focus based on gaps
hypothesis = await agent.generate_hypothesis(
    observation="[specific gap from literature]",
    domain="immuno-oncology",
    background=lit_review["review"]
)

# Design targeted experiment
experiment = await agent.design_experiment(
    hypothesis=hypothesis["hypotheses"],
    constraints={"budget": "$50K"}
)

# Build business case
strategy = await agent.business_strategy(
    idea="[based on experiment results]",
    market="oncology"
)

# Save everything
agent.save_project("my_startup_plan.json")
```

---

## 🔧 Configuration

### Customize Model

```python
# Use different Claude model
agent = CoScientistAgent()

# In individual calls
result = await agent._ask_claude(
    prompt="...",
    model="claude-opus-4-6"  # For highest quality
)
```

### Save & Load Projects

```python
# Save project state
agent.save_project("biotech_startup.json")

# Project includes:
# - All conversation history
# - Project context
# - Experiments designed
# - Findings and results
```

---

## 📚 Learn More

- **[Main README](../../../README.md)** - Project overview
- **[Examples](../../../examples/co_scientist/)** - Working examples
- **[Voice Integration](../voice/README.md)** - Use with voice agents

---

## 🎓 Example Sessions

### Session 1: Drug Discovery Startup

```
Topic: AI-powered antibody design

Literature Review:
- Current: Computational methods show 60% success rate
- Gap: Limited diversity in training data
- Opportunity: Combine physics-based + ML approaches

Hypotheses Generated:
1. Hybrid approach increases success rate to 85%
2. Novel loss function improves binding affinity prediction
3. Transfer learning from homologous proteins

Experiment Designed:
- Validate on 1000 known antibody-antigen pairs
- Compare hybrid vs pure ML vs pure physics
- 3-month timeline, $75K budget

Business Strategy:
- Market: $200B antibody therapeutics market
- Model: SaaS for pharma + licensing IP
- Go-to-Market: Partner with 3 pharma companies for validation

Pitch Deck: [Created 12-slide deck]

Fundraising: Seed round $3M from biotech VCs
```

---

**From research idea to funded startup - all in one agent.** 🔬💼✨
