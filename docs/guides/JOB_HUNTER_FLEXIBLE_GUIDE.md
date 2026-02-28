# 🎯 Flexible Job Hunter - Complete Configuration Guide

## Overview

The **Job Hunter multi-agent** is now **fully configurable**! You can search for:
- ✅ **ANY role** (Software Engineer, Product Manager, Research Scientist, Data Analyst, etc.)
- ✅ **ANY company** (Google, TCS, Wipro, Infosys, Anthropic, startups, etc.)
- ✅ **ANY country** (India, USA, France, UK, Germany, Remote, etc.)
- ✅ **ANY location** (Bangalore, San Francisco, London, Paris, Mumbai, etc.)
- ✅ **ANY experience level** (0-1 years, 2-3 years, 5+ years, 10+ years, etc.)
- ✅ **ANY skills** (Java, Python, Machine Learning, PyTorch, React, Kubernetes, etc.)

---

## 🚀 How It Works

The job hunter searches across **multiple job boards** simultaneously:
- **LinkedIn Jobs** (global)
- **Indeed** (multiple countries)
- **Naukri.com** (India's largest job portal)
- **Glassdoor** (with company ratings)

You get **direct search links** for all matching jobs across these platforms!

---

## 📖 Usage Examples

### Basic Command Format

```bash
python -m agency debug test job_hunter --message "YOUR FLEXIBLE SEARCH QUERY"
```

---

## 🎓 Example 1: Java Developer at TCS in India

### Query:
```bash
python -m agency debug test job_hunter --message "Find Java Developer jobs at TCS in India with 2-3 years experience"
```

### What You Get:
```
🌐 Universal Job Search Results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 LINKEDIN
Role: Java Developer
Company: TCS
Location: India
Experience: 2-3 years

🔗 Apply: https://www.linkedin.com/jobs/search?keywords=Java%20Developer%20TCS&location=India

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 INDEED (India)
Role: Java Developer
Company: TCS
Location: India

🔗 Apply: https://in.indeed.com/jobs?q=Java%20Developer%20at%20TCS&l=India

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 NAUKRI.COM
Role: Java Developer
Company: TCS
Location: India
Experience: 2 years

🔗 Apply: https://www.naukri.com/jobs-in-india?k=Java%20Developer&cmp=TCS&exp=2-4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 GLASSDOOR
Role: Java Developer
Company: TCS (★4.0 rating)

🔗 Apply: https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Java%20Developer%20TCS
```

---

## 🎓 Example 2: Product Manager at Google, Remote

### Query:
```bash
python -m agency debug test job_hunter --message "Find Product Manager roles at Google, remote positions"
```

### What You Get:
- LinkedIn search for "Product Manager Google Remote"
- Indeed search filtered for remote jobs
- Glassdoor with Google company page
- All with direct application links

---

## 🎓 Example 3: Research Scientist with ML/PyTorch Skills

### Query:
```bash
python -m agency debug test job_hunter --message "Find Research Scientist jobs with Machine Learning and PyTorch skills"
```

### What You Get:
- Search across all job boards for Research Scientist roles
- Filtered by skills: Machine Learning, PyTorch
- Any company, any location
- Direct links to matching positions

---

## 🎓 Example 4: Software Engineer in France

### Query:
```bash
python -m agency debug test job_hunter --message "Find Software Engineer jobs in France"
```

### What You Get:
- LinkedIn Jobs in France
- Indeed France
- Glassdoor France
- All major companies hiring software engineers

---

## 🎓 Example 5: Entry Level Developer at Wipro

### Query:
```bash
python -m agency debug test job_hunter --message "Find entry level Software Developer jobs at Wipro in Bangalore"
```

### What You Get:
- Entry level positions at Wipro
- Location: Bangalore
- Across multiple job boards
- Fresher-friendly applications

---

## 🎓 Example 6: Senior Data Scientist with 5+ Years Experience

### Query:
```bash
python -m agency debug test job_hunter --message "Find Senior Data Scientist roles with 5+ years experience, skills: Python, Machine Learning, TensorFlow"
```

### What You Get:
- Senior level positions
- 5+ years experience filter
- Skills: Python, ML, TensorFlow
- Top companies and startups

---

## 📋 Configuration Parameters

### All Supported Parameters:

| Parameter | Description | Examples |
|-----------|-------------|----------|
| **role** | Job title/position | "Software Engineer", "Product Manager", "Data Analyst", "Research Scientist" |
| **company** | Company name | "Google", "TCS", "Wipro", "Infosys", "Microsoft", "Anthropic", "OpenAI" |
| **location** | City/region | "Bangalore", "Mumbai", "San Francisco", "London", "Remote" |
| **country** | Country | "India", "USA", "France", "UK", "Germany" |
| **experience_level** | Years of experience | "0-1 years", "2-3 years", "5+ years", "10+ years", "Entry level", "Senior" |
| **skills** | Technical skills | "Java", "Python", "React", "Machine Learning", "PyTorch", "Kubernetes" |

---

## 🎯 Natural Language Queries

The job hunter understands natural language! Just describe what you want:

### Example Queries:

```bash
# Simple
"Find Software Engineer jobs at Microsoft"

# With location
"Find Data Scientist jobs in Bangalore, India"

# With experience
"Find Senior Java Developer roles with 5+ years experience"

# With skills
"Find ML Engineer jobs with PyTorch and Python skills"

# With multiple filters
"Find Product Manager roles at Google or Meta in USA, remote OK, 3+ years experience"

# Company + Location + Experience
"Find Full Stack Developer jobs at Infosys or TCS in Bangalore with 2-3 years experience"

# Role + Skills
"Find Research Scientist positions with Machine Learning, NLP, and Transformers skills"

# Open-ended
"Find any engineering roles at Wipro in India"

# Specific + Detailed
"Find Senior Software Engineer at Accenture in Pune, India, Java and Spring Boot skills, 5+ years experience"
```

---

## 🔍 Job Boards Covered

### 1. **LinkedIn Jobs**
- Global coverage
- Professional network
- Easy Apply feature
- Company pages and insights

### 2. **Indeed**
- Global (indeed.com)
- India (in.indeed.com)
- UK (uk.indeed.com)
- Salary information
- Company reviews

### 3. **Naukri.com** (India)
- India's #1 job portal
- Best for Indian companies (TCS, Infosys, Wipro, etc.)
- Comprehensive listings
- Easy application process

### 4. **Glassdoor**
- Company ratings and reviews
- Salary information
- Interview experiences
- Employee insights

---

## ✅ What You Get

For each search, you receive:

1. **Direct Application Links**
   - One-click access to job boards
   - Pre-filtered search results
   - Ready to apply

2. **Multiple Sources**
   - LinkedIn, Indeed, Naukri, Glassdoor
   - Maximize job discovery
   - Compare across platforms

3. **Clear Instructions**
   - How to apply on each platform
   - Filtering tips
   - Application best practices

4. **Real-Time Results**
   - Current job openings
   - Up-to-date listings
   - Active positions only

---

## 🎯 Advanced Usage

### Search Multiple Companies

```bash
python -m agency debug test job_hunter --message "Find Software Engineer jobs at Google, Microsoft, or Meta in USA"
```

### Search Multiple Locations

```bash
python -m agency debug test job_hunter --message "Find Java Developer jobs in Bangalore, Hyderabad, or Pune"
```

### Combine Multiple Skills

```bash
python -m agency debug test job_hunter --message "Find Full Stack Developer with React, Node.js, and MongoDB skills"
```

### Remote-Only Jobs

```bash
python -m agency debug test job_hunter --message "Find remote Product Manager jobs"
```

### Specific Experience Range

```bash
python -m agency debug test job_hunter --message "Find ML Engineer with exactly 3-5 years experience"
```

---

## 📊 Comparison: Old vs New System

### ❌ Old System (Hardcoded)
- Only AI companies (Anthropic, OpenAI, DeepMind)
- Only specific roles
- No flexibility
- Limited to coded companies
- Hallucinated data for unsupported companies

### ✅ New System (Fully Configurable)
- **ANY company** (Google, TCS, Wipro, startups, etc.)
- **ANY role** (Engineer, PM, Scientist, Analyst, etc.)
- **ANY location** (India, USA, France, Remote, etc.)
- **ANY skills** (Java, Python, ML, React, etc.)
- **ANY experience level** (Entry, Mid, Senior, etc.)
- Real job board links
- Multiple sources
- Always up-to-date

---

## 🚀 Quick Start Examples

### For Indian IT Companies:
```bash
# TCS Java roles
python -m agency debug test job_hunter --message "Find Java Developer at TCS in India, 2-3 years"

# Infosys Full Stack
python -m agency debug test job_hunter --message "Find Full Stack Developer at Infosys, any location in India"

# Wipro Senior roles
python -m agency debug test job_hunter --message "Find Senior Software Engineer at Wipro with 5+ years"

# Accenture in Bangalore
python -m agency debug test job_hunter --message "Find Software Developer at Accenture in Bangalore"
```

### For Global Tech Companies:
```bash
# Google in USA
python -m agency debug test job_hunter --message "Find Software Engineer at Google in USA"

# Microsoft remote
python -m agency debug test job_hunter --message "Find Product Manager at Microsoft, remote"

# Meta ML Engineer
python -m agency debug test job_hunter --message "Find ML Engineer at Meta with PyTorch skills"

# Anthropic Research
python -m agency debug test job_hunter --message "Find Research Scientist at Anthropic"
```

### For Specific Skills:
```bash
# Java + Spring Boot
python -m agency debug test job_hunter --message "Find Java Developer with Spring Boot and Microservices skills"

# Python + ML
python -m agency debug test job_hunter --message "Find Data Scientist with Python and Machine Learning"

# React + Frontend
python -m agency debug test job_hunter --message "Find Frontend Developer with React and TypeScript"

# DevOps
python -m agency debug test job_hunter --message "Find DevOps Engineer with Kubernetes and Docker"
```

---

## 🎓 Pro Tips

### Tip 1: Be Specific for Better Results
```bash
# ❌ Too vague
"Find jobs"

# ✅ Specific
"Find Java Developer jobs at TCS in Bangalore with 2-3 years experience"
```

### Tip 2: Use Multiple Skills
```bash
# Add relevant skills to filter better
"Find ML Engineer with Python, PyTorch, and TensorFlow skills"
```

### Tip 3: Specify Location for Local Results
```bash
# Better than just country
"Find Software Engineer in Bangalore, India" (not just "India")
```

### Tip 4: Include Experience Level
```bash
# Helps filter appropriate positions
"Find Senior Product Manager with 5+ years experience"
```

### Tip 5: Try Multiple Searches
```bash
# Search 1: Specific company
"Find roles at TCS in India"

# Search 2: By skills
"Find Java Developer with Spring Boot"

# Search 3: By location
"Find Software Engineer in Bangalore"
```

---

## 🔧 How to Test

### Test 1: Basic Search
```bash
python -m agency debug test job_hunter --message "Find Software Engineer jobs"
```

### Test 2: Specific Company
```bash
python -m agency debug test job_hunter --message "Find Java Developer at TCS"
```

### Test 3: Location Filter
```bash
python -m agency debug test job_hunter --message "Find jobs in Bangalore, India"
```

### Test 4: Skills Filter
```bash
python -m agency debug test job_hunter --message "Find ML Engineer with Python and PyTorch"
```

### Test 5: Full Configuration
```bash
python -m agency debug test job_hunter --message "Find Senior Java Developer at Wipro in Mumbai with 5+ years experience, Spring Boot skills"
```

---

## ✅ What Makes This Flexible?

### 1. **No Hardcoded Companies**
- Search ANY company name
- Not limited to pre-configured list
- Startups, enterprises, any organization

### 2. **No Hardcoded Roles**
- ANY job title works
- Engineering, Product, Design, Research, etc.
- Custom role names supported

### 3. **Global Coverage**
- ANY country supported
- Major job boards cover all regions
- Remote positions included

### 4. **Skill-Based Search**
- ANY technical skill
- Programming languages, frameworks, tools
- Domain expertise (ML, DevOps, Cloud, etc.)

### 5. **Experience Flexibility**
- Entry level to C-level
- Specific year ranges
- Fresher and senior positions

---

## 🎉 Get Started Now!

```bash
# Try your first flexible search
python -m agency debug test job_hunter --message "Find [YOUR ROLE] jobs at [YOUR COMPANY] in [YOUR LOCATION] with [YOUR SKILLS]"

# Examples:
python -m agency debug test job_hunter --message "Find Java Developer at TCS in India with 2-3 years"

python -m agency debug test job_hunter --message "Find Product Manager at Google, remote"

python -m agency debug test job_hunter --message "Find ML Engineer with PyTorch skills"
```

---

**Your job search is now completely flexible! 🚀**

Search for ANY role, at ANY company, in ANY location, with ANY skills!
