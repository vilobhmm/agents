"""
Co-Scientist Co-Founder Agent - Your AI Research & Startup Partner

Combines scientific research expertise with startup/business strategy.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class CoScientistAgent:
    """
    AI co-scientist and co-founder for building science-based companies.

    Capabilities:
    - Scientific research and literature review
    - Experiment design and data analysis
    - Hypothesis generation and validation
    - Research paper analysis
    - Startup strategy and business planning
    - Pitch deck creation
    - Fundraising strategy
    - Technical documentation
    - Market analysis
    - Competitive research
    """

    def __init__(self):
        """Initialize co-scientist agent."""
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        if self.anthropic_api_key:
            import anthropic
            self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.has_claude = True
        else:
            self.claude = None
            self.has_claude = False
            logger.warning("Claude API not configured")

        self.conversation_history = []
        self.project_context = {
            "name": None,
            "domain": None,
            "stage": None,  # idea, research, prototype, MVP, growth
            "hypothesis": None,
            "experiments": [],
            "findings": []
        }

        logger.info("Co-Scientist Co-Founder Agent initialized")

    # ==================== RESEARCH CAPABILITIES ====================

    async def literature_review(
        self,
        topic: str,
        depth: str = "comprehensive"
    ) -> Dict:
        """
        Conduct literature review on a scientific topic.

        Args:
            topic: Research topic or question
            depth: "quick", "moderate", or "comprehensive"

        Returns:
            {
                "summary": "Overall findings...",
                "key_papers": [...],
                "research_gaps": [...],
                "recommendations": [...]
            }
        """
        logger.info(f"Conducting literature review: {topic}")

        prompt = f"""You are a scientific research expert. Conduct a {depth} literature review on:

Topic: {topic}

Provide:
1. **Summary**: Key findings and current state of research
2. **Important Areas**: Main research areas and approaches
3. **Research Gaps**: What's missing or needs more study
4. **Methodologies**: Common experimental approaches
5. **Key Insights**: Most important takeaways
6. **Next Steps**: Recommended directions for research

Format as a structured research brief."""

        response = await self._ask_claude(prompt, system="You are an expert scientific researcher with deep knowledge across multiple domains.")

        return {
            "topic": topic,
            "depth": depth,
            "review": response,
            "timestamp": datetime.now().isoformat()
        }

    async def analyze_paper(
        self,
        paper_text: str,
        focus: Optional[str] = None
    ) -> Dict:
        """
        Analyze a research paper.

        Args:
            paper_text: Full text or abstract of paper
            focus: Specific aspect to focus on (methodology, results, etc.)

        Returns:
            Analysis including key findings, methodology, and implications
        """
        logger.info("Analyzing research paper")

        focus_text = f"Focus specifically on: {focus}" if focus else "Provide comprehensive analysis"

        prompt = f"""Analyze this research paper:

{paper_text}

{focus_text}

Provide:
1. **Key Findings**: Main results and conclusions
2. **Methodology**: Experimental approach and techniques
3. **Strengths**: What the paper does well
4. **Limitations**: Weaknesses or gaps
5. **Implications**: What this means for the field
6. **Follow-up Questions**: What should be investigated next
7. **Reproducibility**: How easy to replicate these results"""

        response = await self._ask_claude(prompt, system="You are a scientific peer reviewer with expertise in critical analysis.")

        return {
            "analysis": response,
            "focus": focus,
            "timestamp": datetime.now().isoformat()
        }

    async def generate_hypothesis(
        self,
        observation: str,
        domain: str,
        background: Optional[str] = None
    ) -> Dict:
        """
        Generate testable scientific hypotheses.

        Args:
            observation: The phenomenon or observation
            domain: Scientific domain (biology, chemistry, physics, etc.)
            background: Additional context or prior knowledge

        Returns:
            Multiple hypotheses with predictions and test methods
        """
        logger.info(f"Generating hypotheses for: {observation}")

        background_text = f"\n\nBackground: {background}" if background else ""

        prompt = f"""As a scientist in {domain}, generate testable hypotheses for this observation:

Observation: {observation}{background_text}

For each hypothesis, provide:
1. **Hypothesis Statement**: Clear, testable statement
2. **Null Hypothesis**: What would disprove it
3. **Predictions**: Expected outcomes if hypothesis is true
4. **Test Method**: How to experimentally test it
5. **Variables**: Independent, dependent, and control variables
6. **Expected Timeline**: How long to test
7. **Success Criteria**: What results would support/reject hypothesis

Generate 3-5 different hypotheses with varying approaches."""

        response = await self._ask_claude(prompt, system="You are a creative scientist skilled at hypothesis generation and experimental design.")

        # Store in project context
        self.project_context["hypothesis"] = response

        return {
            "observation": observation,
            "domain": domain,
            "hypotheses": response,
            "timestamp": datetime.now().isoformat()
        }

    async def design_experiment(
        self,
        hypothesis: str,
        constraints: Optional[Dict] = None
    ) -> Dict:
        """
        Design a scientific experiment.

        Args:
            hypothesis: The hypothesis to test
            constraints: Budget, time, equipment, etc.

        Returns:
            Complete experimental protocol
        """
        logger.info("Designing experiment")

        constraints_text = ""
        if constraints:
            constraints_text = f"\n\nConstraints:\n"
            for key, value in constraints.items():
                constraints_text += f"- {key}: {value}\n"

        prompt = f"""Design a rigorous scientific experiment to test this hypothesis:

Hypothesis: {hypothesis}{constraints_text}

Provide a complete experimental protocol:

1. **Objective**: Clear goal of the experiment
2. **Materials**: All required equipment and reagents
3. **Protocol**: Step-by-step procedure
4. **Sample Size**: How many samples/replicates
5. **Controls**: Positive and negative controls
6. **Variables**: What to measure and how
7. **Data Collection**: How to record observations
8. **Statistical Analysis**: How to analyze results
9. **Timeline**: Estimated duration for each step
10. **Safety Considerations**: Risks and precautions
11. **Expected Results**: What results would look like
12. **Troubleshooting**: Common issues and solutions

Make it detailed enough for a researcher to execute."""

        response = await self._ask_claude(prompt, system="You are an experimental scientist skilled at designing rigorous, reproducible experiments.")

        # Store experiment
        experiment = {
            "hypothesis": hypothesis,
            "protocol": response,
            "status": "designed",
            "created": datetime.now().isoformat()
        }
        self.project_context["experiments"].append(experiment)

        return experiment

    async def analyze_data(
        self,
        data_description: str,
        analysis_type: str = "comprehensive"
    ) -> Dict:
        """
        Analyze experimental data.

        Args:
            data_description: Description of the data and results
            analysis_type: Type of analysis needed

        Returns:
            Statistical analysis and interpretation
        """
        logger.info(f"Analyzing data: {analysis_type}")

        prompt = f"""Analyze this experimental data:

{data_description}

Provide:
1. **Descriptive Statistics**: Mean, median, std dev, etc.
2. **Statistical Tests**: Appropriate tests to use (t-test, ANOVA, etc.)
3. **Significance**: Are results statistically significant?
4. **Visualization**: Suggested plots and graphs
5. **Interpretation**: What do the results mean?
6. **Confidence**: Level of confidence in conclusions
7. **Limitations**: Data quality issues or biases
8. **Next Steps**: Follow-up experiments or analysis

Be rigorous and scientifically accurate."""

        response = await self._ask_claude(prompt, system="You are a biostatistician and data scientist with expertise in experimental data analysis.")

        return {
            "data": data_description,
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }

    # ==================== STARTUP/BUSINESS CAPABILITIES ====================

    async def business_strategy(
        self,
        idea: str,
        market: str,
        stage: str = "early"
    ) -> Dict:
        """
        Develop business strategy for science-based startup.

        Args:
            idea: Business/product idea
            market: Target market or industry
            stage: early, growth, or scale

        Returns:
            Comprehensive business strategy
        """
        logger.info(f"Developing business strategy for: {idea}")

        prompt = f"""Develop a business strategy for this science-based startup:

Idea: {idea}
Market: {market}
Stage: {stage}

Provide:
1. **Value Proposition**: What problem does this solve?
2. **Market Analysis**:
   - Market size (TAM, SAM, SOM)
   - Target customers
   - Customer pain points
3. **Competitive Landscape**:
   - Direct competitors
   - Indirect competitors
   - Competitive advantages
4. **Business Model**:
   - Revenue streams
   - Pricing strategy
   - Unit economics
5. **Go-to-Market Strategy**:
   - Customer acquisition channels
   - Sales strategy
   - Marketing approach
6. **Milestones**:
   - 6-month goals
   - 12-month goals
   - 18-month goals
7. **Risks & Mitigation**:
   - Technical risks
   - Market risks
   - Execution risks
8. **Team Needs**:
   - Key hires
   - Advisors needed

Be specific and actionable."""

        response = await self._ask_claude(prompt, system="You are a startup strategy consultant with expertise in deep tech and life sciences companies.")

        self.project_context["name"] = idea
        self.project_context["domain"] = market

        return {
            "idea": idea,
            "market": market,
            "strategy": response,
            "timestamp": datetime.now().isoformat()
        }

    async def create_pitch_deck(
        self,
        company_info: Dict,
        target_audience: str = "seed_investors"
    ) -> Dict:
        """
        Create pitch deck outline and content.

        Args:
            company_info: Company details (name, problem, solution, etc.)
            target_audience: seed_investors, series_a, corporate, etc.

        Returns:
            Complete pitch deck structure and content
        """
        logger.info(f"Creating pitch deck for: {target_audience}")

        info_text = json.dumps(company_info, indent=2)

        prompt = f"""Create a compelling pitch deck for {target_audience}:

Company Information:
{info_text}

Provide content for each slide:

1. **Cover Slide**:
   - Company name and tagline
   - One-liner description

2. **Problem**:
   - The specific problem
   - Why it matters (market size, impact)
   - Current solutions and their limitations

3. **Solution**:
   - Your unique approach
   - Why it's better/faster/cheaper
   - Scientific/technical innovation

4. **Product/Technology**:
   - How it works (simple explanation)
   - Key innovations
   - Demo or proof points

5. **Market Opportunity**:
   - TAM/SAM/SOM
   - Market trends
   - Why now?

6. **Business Model**:
   - Revenue streams
   - Pricing
   - Unit economics

7. **Traction**:
   - Key milestones achieved
   - Metrics
   - Customer validation

8. **Competition**:
   - Competitive landscape
   - Unique advantages
   - Barriers to entry

9. **Go-to-Market**:
   - Customer acquisition strategy
   - Partnerships
   - Sales approach

10. **Team**:
    - Founders and key team
    - Relevant expertise
    - Advisors

11. **Financials**:
    - Revenue projections (3-5 years)
    - Key assumptions
    - Path to profitability

12. **Ask**:
    - Funding amount
    - Use of funds
    - Milestones to achieve

For each slide, provide:
- Headline
- Key points (bullet format)
- Supporting data/numbers
- Visual suggestions"""

        response = await self._ask_claude(prompt, system="You are a pitch deck expert who has helped deep tech and biotech startups raise over $500M.")

        return {
            "audience": target_audience,
            "deck_content": response,
            "timestamp": datetime.now().isoformat()
        }

    async def fundraising_strategy(
        self,
        stage: str,
        amount: str,
        use_of_funds: str
    ) -> Dict:
        """
        Develop fundraising strategy.

        Args:
            stage: pre-seed, seed, series-a, etc.
            amount: Target raise amount
            use_of_funds: What the money will be used for

        Returns:
            Fundraising strategy and investor targets
        """
        logger.info(f"Developing fundraising strategy: {stage}, ${amount}")

        prompt = f"""Develop a fundraising strategy:

Stage: {stage}
Target Amount: ${amount}
Use of Funds: {use_of_funds}

Provide:
1. **Fundraising Strategy**:
   - Realistic funding goal
   - Round structure (SAFE, priced round, convertible)
   - Valuation guidance
   - Timeline

2. **Investor Targeting**:
   - Types of investors (angels, VCs, corporate, grants)
   - Specific firms/individuals to target
   - Why they're a good fit
   - Warm intro strategies

3. **Fundraising Materials**:
   - Pitch deck requirements
   - Financial model needs
   - Data room essentials
   - One-pager

4. **Fundraising Process**:
   - Week-by-week plan
   - Meeting cadence
   - Follow-up strategy
   - Negotiation tactics

5. **Terms to Negotiate**:
   - Valuation
   - Board seats
   - Pro-rata rights
   - Liquidation preferences

6. **Founder Preparation**:
   - Questions to expect
   - Objections to address
   - Due diligence prep

7. **Alternative Funding**:
   - Grants (NSF, NIH, SBIR, etc.)
   - Non-dilutive funding
   - Strategic partnerships

Be specific and tactical."""

        response = await self._ask_claude(prompt, system="You are a fundraising advisor specializing in deep tech and life sciences startups.")

        return {
            "stage": stage,
            "amount": amount,
            "strategy": response,
            "timestamp": datetime.now().isoformat()
        }

    async def market_analysis(
        self,
        product: str,
        industry: str
    ) -> Dict:
        """
        Conduct market analysis.

        Args:
            product: Product or service description
            industry: Target industry

        Returns:
            Comprehensive market analysis
        """
        logger.info(f"Conducting market analysis: {industry}")

        prompt = f"""Conduct a market analysis:

Product/Service: {product}
Industry: {industry}

Analyze:
1. **Market Size**:
   - TAM (Total Addressable Market)
   - SAM (Serviceable Addressable Market)
   - SOM (Serviceable Obtainable Market)
   - Market growth rate

2. **Customer Segments**:
   - Primary target customers
   - Secondary targets
   - Customer needs and pain points
   - Willingness to pay

3. **Market Trends**:
   - Current trends driving the market
   - Regulatory changes
   - Technology shifts
   - Consumer behavior changes

4. **Competitive Analysis**:
   - Direct competitors
   - Indirect competitors
   - Substitute products
   - Competitive positioning

5. **Market Entry Strategy**:
   - Beachhead market
   - Entry barriers
   - First mover advantages
   - Partnership opportunities

6. **Market Risks**:
   - Technology risks
   - Regulatory risks
   - Competition risks
   - Market timing risks

Provide specific data points and sources where possible."""

        response = await self._ask_claude(prompt, system="You are a market research analyst specializing in deep tech and life sciences markets.")

        return {
            "product": product,
            "industry": industry,
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }

    # ==================== INTEGRATED WORKFLOWS ====================

    async def research_to_startup_workflow(
        self,
        research_idea: str,
        domain: str
    ) -> Dict:
        """
        Complete workflow from research idea to startup plan.

        Steps:
        1. Literature review
        2. Generate hypotheses
        3. Design validation experiments
        4. Business strategy
        5. Market analysis
        6. Pitch deck outline

        Args:
            research_idea: The scientific research idea
            domain: Scientific domain

        Returns:
            Complete research-to-startup plan
        """
        logger.info(f"Running research-to-startup workflow: {research_idea}")

        workflow_results = {}

        # Step 1: Literature Review
        print("\n📚 Step 1: Conducting literature review...")
        lit_review = await self.literature_review(research_idea, depth="comprehensive")
        workflow_results["literature_review"] = lit_review

        # Step 2: Generate Hypotheses
        print("\n💡 Step 2: Generating hypotheses...")
        hypotheses = await self.generate_hypothesis(
            observation=research_idea,
            domain=domain,
            background=lit_review["review"][:500]  # Brief context
        )
        workflow_results["hypotheses"] = hypotheses

        # Step 3: Business Strategy
        print("\n💼 Step 3: Developing business strategy...")
        strategy = await self.business_strategy(
            idea=research_idea,
            market=domain,
            stage="early"
        )
        workflow_results["business_strategy"] = strategy

        # Step 4: Market Analysis
        print("\n📊 Step 4: Analyzing market...")
        market = await self.market_analysis(
            product=research_idea,
            industry=domain
        )
        workflow_results["market_analysis"] = market

        # Step 5: Pitch Deck Outline
        print("\n🎯 Step 5: Creating pitch deck outline...")
        pitch = await self.create_pitch_deck(
            company_info={
                "name": research_idea,
                "problem": "Based on research gaps",
                "solution": "Scientific innovation",
                "market": domain
            },
            target_audience="seed_investors"
        )
        workflow_results["pitch_deck"] = pitch

        return {
            "research_idea": research_idea,
            "domain": domain,
            "workflow_results": workflow_results,
            "timestamp": datetime.now().isoformat()
        }

    # ==================== HELPER METHODS ====================

    async def _ask_claude(
        self,
        prompt: str,
        system: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929"
    ) -> str:
        """Ask Claude a question."""
        if not self.has_claude:
            return "Claude API not configured. Please set ANTHROPIC_API_KEY."

        try:
            messages = [{"role": "user", "content": prompt}]

            response = self.claude.messages.create(
                model=model,
                max_tokens=4000,
                system=system or "You are a helpful AI assistant.",
                messages=messages
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error: {e}"

    def save_project(self, output_file: str = "co_scientist_project.json"):
        """Save project context and conversation history."""
        data = {
            "project": self.project_context,
            "conversation": self.conversation_history,
            "saved_at": datetime.now().isoformat()
        }

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Project saved to {output_file}")

        return output_file


# CLI interface
async def co_scientist_cli():
    """
    CLI for co-scientist agent.

    Usage:
        python -m agency.agents.co_scientist.co_scientist_agent
    """
    agent = CoScientistAgent()

    print("🔬 Co-Scientist Co-Founder Agent")
    print("=" * 60)
    print("Research & Startup Capabilities:")
    print("\nResearch:")
    print("  1 - Literature review")
    print("  2 - Analyze paper")
    print("  3 - Generate hypotheses")
    print("  4 - Design experiment")
    print("  5 - Analyze data")
    print("\nBusiness:")
    print("  6 - Business strategy")
    print("  7 - Create pitch deck")
    print("  8 - Fundraising strategy")
    print("  9 - Market analysis")
    print("\nWorkflows:")
    print("  10 - Research-to-startup (complete workflow)")
    print("\nOther:")
    print("  s - Save project")
    print("  q - Quit")
    print("=" * 60)

    while True:
        choice = input("\n> ").strip()

        if choice == "1":
            topic = input("Research topic: ").strip()
            print("\n📚 Conducting literature review...")
            result = await agent.literature_review(topic, depth="comprehensive")
            print(f"\n{result['review']}\n")

        elif choice == "2":
            paper_text = input("Paste paper abstract or full text: ").strip()
            print("\n📄 Analyzing paper...")
            result = await agent.analyze_paper(paper_text)
            print(f"\n{result['analysis']}\n")

        elif choice == "3":
            observation = input("Observation/phenomenon: ").strip()
            domain = input("Scientific domain: ").strip()
            print("\n💡 Generating hypotheses...")
            result = await agent.generate_hypothesis(observation, domain)
            print(f"\n{result['hypotheses']}\n")

        elif choice == "4":
            hypothesis = input("Hypothesis to test: ").strip()
            print("\n🧪 Designing experiment...")
            result = await agent.design_experiment(hypothesis)
            print(f"\n{result['protocol']}\n")

        elif choice == "5":
            data_desc = input("Describe your data: ").strip()
            print("\n📊 Analyzing data...")
            result = await agent.analyze_data(data_desc)
            print(f"\n{result['analysis']}\n")

        elif choice == "6":
            idea = input("Business idea: ").strip()
            market = input("Target market: ").strip()
            print("\n💼 Developing business strategy...")
            result = await agent.business_strategy(idea, market)
            print(f"\n{result['strategy']}\n")

        elif choice == "7":
            print("\nCompany info (press Enter to use defaults):")
            name = input("  Company name: ").strip() or "Science Startup"
            problem = input("  Problem: ").strip() or "TBD"
            solution = input("  Solution: ").strip() or "TBD"

            print("\n🎯 Creating pitch deck...")
            result = await agent.create_pitch_deck({
                "name": name,
                "problem": problem,
                "solution": solution
            })
            print(f"\n{result['deck_content']}\n")

        elif choice == "8":
            stage = input("Fundraising stage (seed/series-a): ").strip()
            amount = input("Target amount ($M): ").strip()
            use = input("Use of funds: ").strip()
            print("\n💰 Developing fundraising strategy...")
            result = await agent.fundraising_strategy(stage, amount, use)
            print(f"\n{result['strategy']}\n")

        elif choice == "9":
            product = input("Product/service: ").strip()
            industry = input("Industry: ").strip()
            print("\n📊 Conducting market analysis...")
            result = await agent.market_analysis(product, industry)
            print(f"\n{result['analysis']}\n")

        elif choice == "10":
            idea = input("Research idea: ").strip()
            domain = input("Scientific domain: ").strip()
            print("\n🚀 Running complete research-to-startup workflow...")
            print("This will take a few minutes...\n")
            result = await agent.research_to_startup_workflow(idea, domain)
            print("\n✅ Workflow complete! Check the output above.")
            print("\nTip: Use 's' to save all results to a file.")

        elif choice == "s":
            output = agent.save_project()
            print(f"\n✅ Project saved to {output}")

        elif choice.lower() == "q":
            print("\nGoodbye! Keep building!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(co_scientist_cli())
