# Claude Code Skills - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER                                   │
│                            │                                     │
│                            ▼                                     │
│         ┌──────────────────────────────────────┐               │
│         │     CLAUDE CODE CLI                  │               │
│         │  (Job hunting commands via skills)   │               │
│         └──────────────────┬───────────────────┘               │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │         CLAUDE CODE SKILLS                 │
        │         (.claude/skills/)                  │
        ├────────────────────────────────────────────┤
        │  • job-quick      (instant links)         │
        │  • job-search     (natural language)      │
        │  • job-track      (tracking)              │
        │  • job-dashboard  (overview)              │
        │  • job-apply      (applications)          │
        │  • job-match      (matching)              │
        │  • job-research   (research)              │
        │  • interview-prep (prep)                  │
        │  • morning-brief  (productivity)          │
        └────────────────┬───────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────────┐
        │      AGENCY MULTI-AGENT SYSTEM             │
        │         (agency/)                          │
        ├────────────────────────────────────────────┤
        │  Agents:                                   │
        │  • job_hunter    (job search)             │
        │  • cc            (productivity)            │
        │  • coordinator   (orchestration)           │
        └────────────────┬───────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────────┐
        │          JOB SEARCH TOOLS                  │
        │      (agency/tools/)                       │
        ├────────────────────────────────────────────┤
        │  • UniversalJobScraper                     │
        │  • JobSearchTools                          │
        │  • Google Tools (Gmail, Calendar, Drive)   │
        └────────────────┬───────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────────────┐
        │        JOB BOARDS & APIS                   │
        ├────────────────────────────────────────────┤
        │  • LinkedIn Jobs                           │
        │  • Indeed                                  │
        │  • Glassdoor                               │
        │  • Naukri.com (India)                      │
        │  • Google API (Gmail, Calendar, Drive)     │
        └────────────────────────────────────────────┘
```

---

## 📊 Data Flow

### Example: `/job-search "Find Java Developer at TCS in India"`

```
1. USER runs command:
   .claude/skills/job-search "Find Java Developer at TCS in India"

2. SKILL parses input:
   - Extracts: role="Java Developer", company="TCS", location="India"
   - Constructs query for agent

3. SKILL invokes agent:
   python -m agency debug test job_hunter --message "..."

4. AGENT processes query:
   - Uses UniversalJobScraper
   - Calls job board APIs
   - Formats results

5. SCRAPER generates links:
   - LinkedIn: https://linkedin.com/jobs/search/?keywords=...
   - Indeed: https://indeed.com/jobs?q=...
   - Glassdoor: https://glassdoor.com/Job/jobs.htm?...
   - Naukri: https://naukri.com/java-developer-tcs-india-jobs

6. RESULTS returned to user:
   🔗 SEARCH RESULTS FOR: Find Java Developer at TCS in India

   LinkedIn Jobs:  [link]
   Indeed:         [link]
   Glassdoor:      [link]
   Naukri:         [link]
```

---

## 🔄 Skill Types

### 1. Direct Execution Skills (Fast)
**Examples:** `job-quick`, `morning-brief`

```
User → Skill → Direct Output
       (no agent needed)
```

**Characteristics:**
- Instant execution
- No AI processing
- Direct URL generation
- Fastest option

---

### 2. Agent-Powered Skills (Intelligent)
**Examples:** `job-search`, `job-apply`, `interview-prep`

```
User → Skill → Agent → Tools → APIs → Results
```

**Characteristics:**
- Natural language processing
- Context-aware
- Smart filtering
- More powerful

---

### 3. Tracking Skills (Stateful)
**Examples:** `job-track`, `job-dashboard`

```
User → Skill → Agent → Storage → Results
                         ↓
                   ~/.agency/job_search/
                   - tracked_jobs.json
                   - applications.json
                   - preferences.json
```

**Characteristics:**
- Persistent storage
- State management
- Historical data
- Progress tracking

---

## 🛠️ Component Breakdown

### 1. Claude Code Skills (`.claude/skills/`)

**Purpose:** User-facing CLI interface

**Technology:** Python scripts (executable)

**Responsibilities:**
- Parse user commands
- Validate input
- Invoke agents
- Format output

**Example:**
```python
#!/usr/bin/env python3
import sys
import subprocess

query = " ".join(sys.argv[1:])
subprocess.run([
    "python", "-m", "agency", "debug", "test", "job_hunter",
    "--message", query
], cwd="/home/user/agents")
```

---

### 2. Agency System (`agency/`)

**Purpose:** Multi-agent orchestration

**Technology:** Python (asyncio)

**Components:**
- `config.json` - Agent configuration
- `processor.py` - Message processing
- `agent.py` - Agent execution
- `conversation.py` - Conversation management

**Agents:**
- `job_hunter` - Job search specialist
- `cc` - Productivity assistant
- `coordinator` - Team orchestrator

---

### 3. Job Search Tools (`agency/tools/`)

**Purpose:** Core job search functionality

**Files:**
- `job_search_tools.py` - Main tools API
- `universal_job_scraper.py` - Universal job board scraper
- `job_scraper.py` - Company-specific scrapers
- `google_tools.py` - Google API integration

**Features:**
- Universal job search across all boards
- Company-specific career page scraping
- Application tracking
- Preference matching

---

### 4. Data Storage (`~/.agency/job_search/`)

**Purpose:** Persistent job hunting data

**Files:**
- `tracked_jobs.json` - Jobs you're tracking
- `applications.json` - Application history
- `preferences.json` - Your job preferences

**Schema:**
```json
{
  "tracked_jobs": [
    {
      "id": "unique-id",
      "company": "TCS",
      "title": "Java Developer",
      "location": "Bangalore",
      "status": "applied",
      "tracked_date": "2026-02-17",
      "notes": "Looks promising"
    }
  ]
}
```

---

## 🎯 Design Principles

### 1. Simplicity First
- Easy to use: One command, one purpose
- Easy to understand: Clear naming
- Easy to extend: Simple Python scripts

### 2. Progressive Enhancement
- Basic: Direct links (`job-quick`)
- Advanced: AI-powered (`job-search`)
- Expert: Full tracking (`job-dashboard`)

### 3. Separation of Concerns
- **Skills** - User interface
- **Agents** - Intelligence
- **Tools** - Functionality
- **Storage** - Persistence

### 4. Flexibility
- CLI + Telegram support
- Standalone or integrated
- Customizable per user

---

## 🔌 Integration Points

### With Claude Code:
```
User types: /job-search "Find jobs"
           ↓
Claude Code invokes: .claude/skills/job-search
           ↓
Skill executes
```

### With Multi-Agent System:
```
Skill calls: python -m agency debug test job_hunter
           ↓
Agency processor handles message
           ↓
Agent executes with tools
```

### With Job Boards:
```
Tool generates: https://linkedin.com/jobs/search/?keywords=...
              ↓
User clicks link
              ↓
Job board opens
```

---

## 📈 Scalability

### Adding New Skills

1. Create skill file:
```bash
touch .claude/skills/my-skill
chmod +x .claude/skills/my-skill
```

2. Implement logic:
```python
#!/usr/bin/env python3
import sys
import subprocess

query = " ".join(sys.argv[1:])
subprocess.run([
    "python", "-m", "agency", "debug", "test", "job_hunter",
    "--message", query
])
```

3. Document:
```bash
# Update README.md with usage examples
```

### Adding New Tools

1. Add to `job_search_tools.py`:
```python
async def my_new_tool(self, ...):
    # Implementation
    pass
```

2. Register in `tools.py`:
```python
registry.register("my_new_tool", my_new_tool)
```

3. Document in agent config

### Adding New Agents

1. Add to `config.json`:
```json
{
  "agent_id": "my_agent",
  "role": "Specialist for...",
  "capabilities": [...]
}
```

2. Create skill interface
3. Document usage

---

## 🔒 Security Considerations

### API Keys
- Stored in environment variables
- Never committed to git
- Per-user authentication

### Data Privacy
- Local storage only
- User controls all data
- No external tracking

### Safe Execution
- Scripts run in user context
- No elevated privileges
- Sandboxed operations

---

## 📊 Performance

### Skill Execution Times

| Skill | Type | Avg Time | Notes |
|-------|------|----------|-------|
| job-quick | Direct | <100ms | Instant links |
| job-search | Agent | 1-3s | AI processing |
| job-track | Storage | 100-500ms | DB lookup |
| job-dashboard | Complex | 2-5s | Multiple queries |
| morning-brief | API | 3-7s | External APIs |

### Optimization Strategies
- Cache job board results (15 min TTL)
- Parallel API calls where possible
- Lazy loading for dashboards
- Incremental updates for tracking

---

## 🎓 Future Enhancements

### Planned Features
- [ ] Resume optimization skill
- [ ] Cover letter generation skill
- [ ] LinkedIn outreach skill
- [ ] Salary negotiation helper
- [ ] Interview feedback tracker
- [ ] Networking contact manager

### Technical Improvements
- [ ] Async skill execution
- [ ] Background job scraping
- [ ] Real-time notifications
- [ ] ML-based job matching
- [ ] Browser automation for applications

---

## 📖 Related Documentation

- [Main Guide](../CLAUDE_SKILLS_GUIDE.md)
- [Quick Start](QUICKSTART.md)
- [Full README](README.md)
- [Multi-Agent System](../../README.md)

---

*Architecture designed for simplicity, scalability, and user control*
