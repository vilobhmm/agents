#!/usr/bin/env python3
"""
E2E Co-Scientist Co-Founder Demo
=================================

Complete demonstration of research-to-startup workflow.

Run:
    ANTHROPIC_API_KEY=sk-ant-... python examples/co_scientist/e2e_co_scientist_demo.py
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agents.co_scientist.co_scientist_agent import CoScientistAgent


def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_section(title):
    """Print section title."""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}\n")


async def demo_research_capabilities():
    """Demo research capabilities."""
    print_header("DEMO 1: Research Capabilities")

    agent = CoScientistAgent()

    # Literature Review
    print_section("📚 Literature Review")
    print("Topic: CRISPR gene editing for cancer therapy\n")

    result = await agent.literature_review(
        topic="CRISPR gene editing for cancer therapy",
        depth="quick"
    )

    print(result["review"])
    print(f"\n✓ Literature review completed")

    # Generate Hypotheses
    print_section("💡 Hypothesis Generation")
    print("Observation: Some cancer cells develop resistance to CRISPR-based treatments\n")

    result = await agent.generate_hypothesis(
        observation="Some cancer cells develop resistance to CRISPR-based treatments",
        domain="oncology"
    )

    print(result["hypotheses"])
    print(f"\n✓ Generated testable hypotheses")

    # Design Experiment
    print_section("🧪 Experiment Design")
    print("Designing validation experiment...\n")

    result = await agent.design_experiment(
        hypothesis="Resistance develops through DNA repair pathway upregulation",
        constraints={
            "budget": "$50,000",
            "timeline": "3 months",
            "equipment": "Standard cell culture + flow cytometry"
        }
    )

    print(result["protocol"][:1000] + "...\n")
    print(f"✓ Complete experimental protocol designed")


async def demo_business_capabilities():
    """Demo business/startup capabilities."""
    print_header("DEMO 2: Business & Startup Capabilities")

    agent = CoScientistAgent()

    # Business Strategy
    print_section("💼 Business Strategy")
    print("Idea: CRISPR-based cancer therapy platform\n")

    result = await agent.business_strategy(
        idea="CRISPR-based precision cancer therapy platform",
        market="oncology therapeutics",
        stage="early"
    )

    print(result["strategy"])
    print(f"\n✓ Business strategy developed")

    # Market Analysis
    print_section("📊 Market Analysis")
    print("Analyzing oncology therapeutics market...\n")

    result = await agent.market_analysis(
        product="CRISPR cancer therapy",
        industry="oncology"
    )

    print(result["analysis"][:1000] + "...\n")
    print(f"✓ Market analysis completed")

    # Pitch Deck
    print_section("🎯 Pitch Deck Creation")
    print("Creating investor pitch deck...\n")

    result = await agent.create_pitch_deck(
        company_info={
            "name": "GeneCure Therapeutics",
            "problem": "Cancer treatments have low specificity and high toxicity",
            "solution": "CRISPR-based precision targeting with 95% specificity",
            "market": "Oncology",
            "traction": "Successful in-vitro validation, 2 patents pending"
        },
        target_audience="seed_investors"
    )

    print(result["deck_content"][:1000] + "...\n")
    print(f"✓ 12-slide pitch deck created")


async def demo_complete_workflow():
    """Demo complete research-to-startup workflow."""
    print_header("DEMO 3: Complete Research-to-Startup Workflow")

    agent = CoScientistAgent()

    print("Research Idea: Novel mRNA delivery mechanism for targeted therapy")
    print("Domain: Biotechnology\n")
    print("Running complete workflow (this takes a few minutes)...\n")

    result = await agent.research_to_startup_workflow(
        research_idea="Novel lipid nanoparticle design for targeted mRNA delivery",
        domain="biotechnology"
    )

    # Show summary of each step
    print_section("📚 Step 1: Literature Review")
    print("✓ Analyzed current state of mRNA delivery research")
    print("✓ Identified key research gaps")
    print("✓ Found opportunities for innovation\n")

    print_section("💡 Step 2: Hypothesis Generation")
    print("✓ Generated 3-5 testable hypotheses")
    print("✓ Defined success criteria")
    print("✓ Outlined experimental approaches\n")

    print_section("💼 Step 3: Business Strategy")
    print("✓ Defined value proposition")
    print("✓ Analyzed market opportunity")
    print("✓ Outlined go-to-market strategy\n")

    print_section("📊 Step 4: Market Analysis")
    print("✓ Calculated TAM/SAM/SOM")
    print("✓ Identified customer segments")
    print("✓ Mapped competitive landscape\n")

    print_section("🎯 Step 5: Pitch Deck")
    print("✓ Created 12-slide investor deck")
    print("✓ Structured problem-solution-opportunity")
    print("✓ Ready for seed fundraising\n")

    print_section("📁 Results")
    print("Complete research-to-startup package ready!")
    print(f"- Literature review")
    print(f"- Scientific hypotheses")
    print(f"- Business strategy")
    print(f"- Market analysis")
    print(f"- Investor pitch deck")

    # Save project
    output_file = agent.save_project("research_to_startup_demo.json")
    print(f"\n✓ All results saved to: {output_file}")


async def demo_interactive_examples():
    """Show interactive usage examples."""
    print_header("DEMO 4: Interactive Usage Examples")

    agent = CoScientistAgent()

    # Example 1: Paper Analysis
    print_section("📄 Example 1: Analyze Research Paper")

    paper_abstract = """
    We developed a novel approach to protein structure prediction using
    transformer-based language models. Our method achieves 95% accuracy
    on benchmark datasets, surpassing previous methods by 15%. The model
    was trained on 200,000 protein sequences and validated on independent
    test sets. Applications include drug discovery and protein engineering.
    """

    print(f"Paper Abstract:\n{paper_abstract}\n")
    print("Analyzing commercial potential...\n")

    result = await agent.analyze_paper(
        paper_text=paper_abstract,
        focus="commercial potential"
    )

    print(result["analysis"][:800] + "...\n")
    print("✓ Commercial potential analyzed")

    # Example 2: Fundraising Strategy
    print_section("💰 Example 2: Fundraising Strategy")

    print("Planning seed round fundraising...\n")

    result = await agent.fundraising_strategy(
        stage="seed",
        amount="2M",
        use_of_funds="Product development (60%), team expansion (30%), operations (10%)"
    )

    print(result["strategy"][:800] + "...\n")
    print("✓ Fundraising strategy developed")


async def main():
    """Run complete demo."""
    print("\n" + "=" * 70)
    print("  🔬 Co-Scientist Co-Founder Agent - E2E Demo")
    print("=" * 70)
    print("\n  Demonstrates research-to-startup capabilities:")
    print("  • Scientific research and analysis")
    print("  • Experiment design and validation")
    print("  • Business strategy and planning")
    print("  • Market analysis and competitive research")
    print("  • Pitch deck creation and fundraising")
    print("  • Complete research-to-startup workflows")
    print("\n" + "=" * 70)

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set.")
        print("   Set it to use Claude AI: export ANTHROPIC_API_KEY=sk-ant-...")
        return

    input("\n  Press Enter to start demo...")

    # Run demos
    await demo_research_capabilities()
    input("\n  Press Enter to continue...")

    await demo_business_capabilities()
    input("\n  Press Enter to continue...")

    await demo_interactive_examples()
    input("\n  Press Enter for complete workflow demo...")

    await demo_complete_workflow()

    # Summary
    print_header("DEMO COMPLETE")

    print("✅ Demonstrated all capabilities:")
    print("   • Literature review and paper analysis")
    print("   • Hypothesis generation")
    print("   • Experiment design")
    print("   • Business strategy development")
    print("   • Market analysis")
    print("   • Pitch deck creation")
    print("   • Fundraising planning")
    print("   • Complete research-to-startup workflow")

    print("\n📚 Next steps:")
    print("   1. Try interactive mode:")
    print("      python -m agency.agents.co_scientist.co_scientist_agent")
    print("\n   2. Use in your code:")
    print("      from agents.co_scientist import CoScientistAgent")
    print("      agent = CoScientistAgent()")
    print("      result = await agent.literature_review('your topic')")
    print("\n   3. Run complete workflow for your research idea")

    print("\n📖 Documentation:")
    print("   agency/agents/co_scientist/README.md")

    print("\n" + "=" * 70)
    print("  🔬 From research to funded startup!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
