# AI Research & Productivity Agent

> **MD-Based Personality Agent that tracks latest AI research and helps you stay productive**

A unique agent with personality defined by markdown files that scrapes, summarizes, and provides insights on the latest AI/ML research.

## 🌟 Key Features

### **📚 Research Tracking**
- Scrapes arXiv, HuggingFace, AI lab blogs
- Tracks latest papers in AI/ML/Agents
- Monitors trending topics
- Author and institution tracking

### **🧠 MD-Based Personality**
Agent behavior defined by 12 markdown files:
- `identity.md` - Who the agent is
- `soul.md` - Core values and principles
- `goals.md` - Agent objectives
- `memory.md` - Long-term learnings
- `knowledge.md` - Domain knowledge
- `reasoning.md` - How it thinks
- `planner.md` - Planning strategies
- `workflow.md` - Work patterns
- `tools.md` - Available capabilities
- `agents.md` - Multi-agent coordination
- `reflection.md` - Self-improvement
- `safety.md` - Safety guidelines

### **💡 Intelligent Features**
- Daily research briefings
- Personalized paper recommendations
- Trend analysis and insights
- Paper explanations in simple terms
- Knowledge base management
- Self-reflection and learning

## 🚀 Quick Start

```python
from agents.research_agent import ResearchAgent

# Initialize agent (creates personality files if needed)
agent = ResearchAgent()

# Get introduction
print(await agent.introduce())

# Get daily briefing
print(await agent.get_daily_briefing())

# Search for papers
print(await agent.search_research("multi-agent systems"))

# Track a topic
await agent.track_topic("reinforcement learning")

# Get recommendations
print(await agent.get_recommendations())

# Agent self-reflection
print(await agent.reflect())
```

## 📖 Usage Examples

### Daily Research Routine

```python
# Morning: Get daily briefing
briefing = await agent.get_daily_briefing()
print(briefing)

# Track interesting topics
await agent.track_topic("LLM agents")
await agent.track_topic("multi-modal AI")

# Get recommendations
recommendations = await agent.get_recommendations()
```

### Research Deep Dive

```python
# Search for specific papers
results = await agent.search_research("chain-of-thought reasoning")

# Explain a paper
explanation = await agent.explain_paper("2403.12345")

# Save with notes
await agent.save_paper("2403.12345", notes="Interesting approach to reasoning")

# Analyze trends
trends = await agent.analyze_trends(days=30)
```

### Ask Questions

```python
# Ask research questions
answer = await agent.ask_question("What are the latest advances in agent memory?")

# Get agent's personality
personality = await agent.get_personality_summary()
```

## 🎨 Customizing Personality

The agent's personality is fully customizable through MD files in the `personality/` directory.

### Example: Modify Identity

Edit `personality/identity.md`:

```markdown
# Agent Identity

## Who Am I?

I am your personal AI Research Assistant, specialized in cutting-edge
machine learning and agent systems research.

## My Purpose

- Keep you at the forefront of AI research
- Synthesize complex papers into actionable insights
- Connect ideas across domains
- Help you discover relevant work
```

### Example: Add to Knowledge Base

```python
# Programmatically update knowledge
agent.personality.append_to_knowledge(
    "User prefers concise summaries over detailed explanations",
    category="User Preferences"
)

# Add to memory
agent.personality.append_to_memory(
    "Discovered user is working on multi-agent coordination project"
)
```

## 📊 Features in Detail

### Research Scraping

Monitors multiple sources:
- arXiv (cs.AI, cs.LG, cs.CL)
- HuggingFace Papers
- Papers with Code
- AI lab blogs (OpenAI, Anthropic, DeepMind, etc.)

### Daily Briefing

Includes:
- New papers count
- High-priority highlights
- Trending topics
- Latest blog posts
- Personalized recommendations

### Trend Analysis

Tracks:
- Top research topics
- Emerging areas
- Growth rates
- Hot papers

### Knowledge Management

- Saves papers with notes
- Builds knowledge graph
- Tracks learnings over time
- Self-reflection and improvement

## 🔧 Advanced Usage

### Integration with LLMs

```python
# Get system prompt for Claude/GPT
system_prompt = agent.get_system_prompt()

# Use in API calls
response = anthropic.messages.create(
    model="claude-opus-4",
    system=system_prompt,
    messages=[...]
)
```

### Multi-Agent Coordination

The research agent can coordinate with other agents using patterns defined in `agents.md`:

```python
# Works with time tracker
from agents.time_tracker import TimeTrackerCoordinator

tracker = TimeTrackerCoordinator()

# Track research time
await tracker.start_activity("Reading research papers", "learning")

# Get research while tracking
briefing = await agent.get_daily_briefing()

# Stop tracking
await tracker.stop_activity()
```

## 📁 File Structure

```
agents/research_agent/
├── __init__.py
├── README.md
├── research_agent.py          # Main agent coordinator
├── personality/
│   ├── __init__.py
│   └── md_personality_loader.py  # MD file loader
├── scrapers/
│   ├── __init__.py
│   └── ai_research_scraper.py    # Research scraper
└── knowledge/
    └── __init__.py               # Knowledge management
```

## 🎯 Personality Files Location

By default, personality files are created in:
- `personality/` in the parent directory

You can specify a custom location:

```python
agent = ResearchAgent(
    personality_dir="/path/to/personality",
    knowledge_dir="/path/to/knowledge"
)
```

## 💡 Best Practices

1. **Customize Personality** - Edit MD files to match your needs
2. **Track Topics** - Tell the agent what you're interested in
3. **Daily Briefings** - Start each day with the latest research
4. **Save Papers** - Build your personal knowledge base
5. **Reflect Regularly** - Use agent reflection to improve
6. **Integrate with Workflow** - Combine with time tracker and other tools

## 🔮 Future Enhancements

- [ ] Real arXiv API integration
- [ ] PDF parsing and analysis
- [ ] Citation network analysis
- [ ] Collaborative filtering recommendations
- [ ] Voice interface integration
- [ ] Automatic paper summarization with LLMs
- [ ] Knowledge graph visualization
- [ ] Team collaboration features

## 🤖 Agent Behavior

The agent's behavior is entirely defined by its personality files:

- **Identity** defines its role and purpose
- **Soul** shapes its values and interaction style
- **Goals** drive its proactive behaviors
- **Knowledge** informs its responses
- **Reasoning** guides its analysis
- **Workflow** structures its daily patterns
- **Memory** enables learning over time
- **Reflection** drives continuous improvement

## 📚 Learn More

- See `personality/` directory for all MD files
- Check `scrapers/ai_research_scraper.py` for scraping details
- Read `research_agent.py` for full API

---

**Stay on the cutting edge of AI research!** 🚀
