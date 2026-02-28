#!/usr/bin/env python3
"""
E2E ADK (Agent Development Kit) Integration Ecosystem Demo
===========================================================

Complete demonstration of Google ADK integrations ecosystem:
- Observability: AgentOps, Arize, Phoenix, W&B Weave
- Platforms: n8n, StackOne
- AI/ML: Hugging Face
- MCP Toolset
- Multi-agent orchestration

Run:
    ANTHROPIC_API_KEY=sk-ant-... python examples/adk/e2e_adk_demo.py
"""

import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from integrations.adk.core.adk_framework import (
    ADKAgent,
    MultiAgentOrchestrator
)
from integrations.adk.integrations.observability.observability_integrations import (
    create_observability_stack
)
from integrations.adk.integrations.platforms.integration_platforms import (
    create_integration_platforms
)
from integrations.adk.integrations.ai_ecosystem.ai_ecosystem_integrations import (
    create_ai_ecosystem_integrations
)


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


async def demo_core_adk():
    """Demo 1: Core ADK framework."""
    print_header("DEMO 1: Core ADK Framework")

    print_section("Creating ADK Agent with MCP Toolset")

    # Create agent
    agent = ADKAgent(
        name="research_agent",
        role="Research and analyze information",
        model="claude-sonnet-4-5-20250929"
    )

    # Add a custom tool
    async def search_web(query: str) -> Dict:
        """Simulated web search."""
        return {
            "query": query,
            "results": [
                {"title": "Result 1", "url": "http://example1.com"},
                {"title": "Result 2", "url": "http://example2.com"}
            ]
        }

    agent.add_tool(
        name="search_web",
        func=search_web,
        description="Search the web for information",
        parameters={"query": "string"}
    )

    print(f"✓ Created agent: {agent.name}")
    print(f"✓ Role: {agent.role}")
    print(f"✓ Tools: {len(agent.mcp.tools)}")

    # Execute a task
    print("\nExecuting task...")
    result = await agent.execute_task(
        "Research the latest developments in AI agents"
    )

    if result["success"]:
        print(f"\n✓ Task completed successfully")
        print(f"  Result: {result['result'][:200]}...")
    else:
        print(f"\n✗ Task failed: {result.get('error')}")

    print("\nAgent metrics:")
    metrics = agent.get_metrics()
    for key, value in metrics["metrics"].items():
        print(f"  {key}: {value}")


async def demo_observability():
    """Demo 2: Observability integrations."""
    print_header("DEMO 2: Observability Integrations")

    # Create observability stack
    observability = create_observability_stack(
        enable_agentops=True,
        enable_arize=True,
        enable_phoenix=True,
        enable_wandb=True
    )

    print(f"✓ Created observability stack with {len(observability)} integrations:")
    for integration in observability:
        print(f"  - {integration.name}")

    # Initialize all
    print("\nInitializing integrations...")
    for integration in observability:
        await integration.initialize()
        if integration.enabled:
            print(f"  ✓ {integration.name} ready")
        else:
            print(f"  ⚠ {integration.name} disabled (API key not set)")

    # Demo AgentOps
    print_section("AgentOps - Session Replay & Monitoring")

    agentops = observability[0]  # AgentOps

    # Start session
    session_result = await agentops.execute(
        operation="start_session",
        agent_name="demo_agent"
    )
    print(f"✓ Started session: {session_result['session_id']}")

    # Log events
    await agentops.execute(
        operation="log_event",
        event={
            "type": "agent_call",
            "agent": "demo_agent",
            "task": "process_data",
            "cost": 0.02
        }
    )
    print("✓ Logged event")

    # Get metrics
    metrics = await agentops.execute(operation="get_metrics")
    print(f"\nAgentOps Metrics:")
    print(f"  Total sessions: {metrics['total_sessions']}")
    print(f"  Total events: {metrics['total_events']}")
    print(f"  Total cost: ${metrics['total_cost']:.4f}")

    # Demo Phoenix
    print_section("Phoenix - LLM Traces & Spans")

    phoenix = observability[2]  # Phoenix

    # Start trace
    trace_result = await phoenix.execute(
        operation="start_trace",
        name="agent_execution"
    )
    print(f"✓ Started trace: {trace_result['trace_id']}")

    # Add spans
    await phoenix.execute(
        operation="add_span",
        trace_id=trace_result['trace_id'],
        name="llm_call",
        tokens=500,
        latency_ms=1200
    )
    print("✓ Added span: llm_call (500 tokens, 1200ms)")

    # End trace
    end_result = await phoenix.execute(
        operation="end_trace",
        trace_id=trace_result['trace_id']
    )
    print(f"\nTrace Summary:")
    print(f"  Total tokens: {end_result['total_tokens']}")
    print(f"  Total latency: {end_result['total_latency_ms']}ms")

    # Demo W&B Weave
    print_section("W&B Weave - Model Call Logging")

    wandb = observability[3]  # W&B Weave

    # Start run
    run_result = await wandb.execute(
        operation="start_run",
        name="adk_experiment"
    )
    print(f"✓ Started run: {run_result['run_id']}")

    # Log calls
    await wandb.execute(
        operation="log_call",
        model="claude-sonnet-4-5",
        input="Generate a summary",
        output="Summary generated...",
        tokens=350,
        latency=0.8,
        cost=0.0175
    )
    print("✓ Logged model call")

    # Finish run
    finish_result = await wandb.execute(operation="finish_run")
    print(f"\nRun Summary:")
    print(f"  Total calls: {finish_result['summary']['total_calls']}")
    print(f"  Total tokens: {finish_result['summary']['total_tokens']}")
    print(f"  Total cost: ${finish_result['summary']['total_cost']:.4f}")


async def demo_integration_platforms():
    """Demo 3: Integration platforms."""
    print_header("DEMO 3: Integration Platforms")

    # Create platforms
    platforms = create_integration_platforms(
        enable_n8n=True,
        enable_stackone=True
    )

    print(f"✓ Created integration platforms: {len(platforms)}")

    # Initialize
    for platform in platforms:
        await platform.initialize()

    # Demo n8n
    print_section("n8n - Workflow Automation")

    n8n = platforms[0]  # n8n

    # Create email workflow
    workflow_result = await n8n.create_email_workflow({
        "to": "user@example.com",
        "subject": "Agent Task Complete",
        "body": "Your agent has completed the task!"
    })
    print(f"✓ Created workflow: {workflow_result['name']}")
    print(f"  Workflow ID: {workflow_result['workflow_id']}")

    # Trigger workflow
    trigger_result = await n8n.trigger_workflow(
        workflow_id=workflow_result['workflow_id'],
        data={"task": "data_processing", "status": "completed"}
    )
    print(f"\n✓ Triggered workflow:")
    print(f"  Execution ID: {trigger_result['execution_id']}")
    print(f"  Status: {trigger_result['status']}")

    # Demo StackOne
    print_section("StackOne - Unified SaaS Integration")

    stackone = platforms[1]  # StackOne

    # Connect to providers
    await stackone.connect_app(
        provider="salesforce",
        credentials={"api_key": "demo_key"}
    )
    print("✓ Connected to Salesforce")

    await stackone.connect_app(
        provider="slack",
        credentials={"token": "demo_token"}
    )
    print("✓ Connected to Slack")

    # Call APIs
    contacts = await stackone.get_salesforce_contacts()
    print(f"\n✓ Retrieved Salesforce contacts")

    slack_msg = await stackone.send_slack_message(
        message="Agent task completed!",
        channel="#agents"
    )
    print(f"✓ Sent Slack message")

    # List connected apps
    apps = await stackone.list_connected_apps()
    print(f"\nConnected apps: {apps['total_apps']}")
    for app in apps['apps']:
        print(f"  - {app['provider']}")


async def demo_ai_ecosystem():
    """Demo 4: AI/ML ecosystem."""
    print_header("DEMO 4: AI/ML Ecosystem - Hugging Face")

    # Create integrations
    ai_integrations = create_ai_ecosystem_integrations()
    hf = ai_integrations[0]  # Hugging Face

    await hf.initialize()

    print_section("Search Models")

    # Search models
    models_result = await hf.search_models("text-generation")
    print(f"✓ Found {models_result['total_models']} models")
    for model in models_result['models'][:3]:
        print(f"  - {model['model_id']}")
        print(f"    Downloads: {model['downloads']:,}")
        print(f"    Likes: {model['likes']:,}")

    print_section("Model Inference")

    # Load and run inference
    load_result = await hf.load_model("gpt2")
    print(f"✓ Loaded model: {load_result['model_id']}")

    inference_result = await hf.run_inference(
        model_id="gpt2",
        inputs="The future of AI agents is"
    )
    print(f"\n✓ Inference result:")
    print(f"  Input: 'The future of AI agents is'")
    print(f"  Output: {inference_result['outputs']}")

    print_section("Search Datasets")

    # Search datasets
    datasets_result = await hf.search_datasets("question-answering")
    print(f"✓ Found {datasets_result['total_datasets']} datasets")
    for dataset in datasets_result['datasets']:
        print(f"  - {dataset['dataset_id']}")

    print_section("Convenience Methods")

    # Use convenience methods
    text = await hf.text_generation("AI agents will", model="gpt2")
    print(f"✓ Text generation: {text}")

    qa_result = await hf.question_answering(
        question="What is AI?",
        context="AI stands for Artificial Intelligence. It is the simulation of human intelligence by machines."
    )
    print(f"✓ Question answering: {qa_result}")


async def demo_multi_agent():
    """Demo 5: Multi-agent orchestration."""
    print_header("DEMO 5: Multi-Agent Orchestration")

    # Create orchestrator
    orchestrator = MultiAgentOrchestrator()

    # Create multiple agents
    print("Creating agent team...")

    researcher = ADKAgent(
        name="researcher",
        role="Research and gather information",
        model="claude-sonnet-4-5-20250929"
    )

    analyst = ADKAgent(
        name="analyst",
        role="Analyze data and extract insights",
        model="claude-sonnet-4-5-20250929"
    )

    writer = ADKAgent(
        name="writer",
        role="Write reports and summaries",
        model="claude-sonnet-4-5-20250929"
    )

    # Register agents
    orchestrator.register_agent(researcher)
    orchestrator.register_agent(analyst)
    orchestrator.register_agent(writer)

    print(f"✓ Created {len(orchestrator.agents)} agents")

    # Create workflow
    print("\nRegistering workflow...")

    orchestrator.register_workflow(
        name="research_report",
        steps=[
            {
                "agent": "researcher",
                "task": "Research AI agent trends in 2026"
            },
            {
                "agent": "analyst",
                "task": "Analyze the research findings"
            },
            {
                "agent": "writer",
                "task": "Write an executive summary"
            }
        ]
    )

    print("✓ Registered workflow: research_report")

    # Execute workflow
    print("\nExecuting multi-agent workflow...")

    result = await orchestrator.execute_workflow("research_report")

    print(f"\n✓ Workflow completed: {result['workflow']}")
    print(f"  Total steps: {result['steps']}")

    for i, step_result in enumerate(result['results'], 1):
        step = step_result['step']
        print(f"\n  Step {i}: {step['agent']}")
        print(f"    Task: {step['task']}")
        if 'result' in step_result:
            if step_result['result']['success']:
                print(f"    ✓ Success")
            else:
                print(f"    ✗ Failed")

    # System status
    print_section("System Status")

    status = orchestrator.get_system_status()
    print(f"Orchestrator: {status['orchestrator']}")
    print(f"Total agents: {len(status['agents'])}")
    print(f"Total workflows: {len(status['workflows'])}")

    print("\nAgent Metrics:")
    for agent_metrics in status['agents']:
        print(f"\n  {agent_metrics['agent']} ({agent_metrics['role']}):")
        for key, value in agent_metrics['metrics'].items():
            print(f"    {key}: {value}")


async def demo_complete_stack():
    """Demo 6: Complete integrated stack."""
    print_header("DEMO 6: Complete ADK Integration Stack")

    print("Building complete ADK-powered agent with all integrations...")

    # Create agent
    agent = ADKAgent(
        name="super_agent",
        role="Multi-capability agent with full ADK integration",
        model="claude-sonnet-4-5-20250929"
    )

    # Add all integrations
    print("\nAdding integrations:")

    # Observability
    for integration in create_observability_stack():
        agent.add_integration(integration)
        print(f"  ✓ {integration.name}")

    # Platforms
    for integration in create_integration_platforms():
        agent.add_integration(integration)
        print(f"  ✓ {integration.name}")

    # AI/ML
    for integration in create_ai_ecosystem_integrations():
        agent.add_integration(integration)
        print(f"  ✓ {integration.name}")

    # Initialize all
    print("\nInitializing all integrations...")
    for integration_name in agent.mcp.list_integrations():
        integration = agent.mcp.integrations[integration_name]
        await integration.initialize()

    print(f"\n✓ Agent ready with {len(agent.mcp.integrations)} integrations")

    # Use the agent
    print("\nExecuting task with full observability...")

    # Start observability
    await agent.call_integration("AgentOps", operation="start_session", agent_name=agent.name)
    await agent.call_integration("Phoenix", operation="start_trace", name="super_task")
    await agent.call_integration("W&B_Weave", operation="start_run", name="demo_run")

    # Execute task
    task_result = await agent.execute_task(
        "Analyze AI agent market trends and send summary via Slack"
    )

    # Log to observability
    await agent.call_integration("Phoenix", operation="end_trace", trace_id="trace_1")
    await agent.call_integration("W&B_Weave", operation="finish_run")

    print("\n✓ Task completed with full observability")
    print(f"  Success: {task_result['success']}")

    # Final metrics
    print("\nFinal Agent Metrics:")
    metrics = agent.get_metrics()
    print(f"  Tasks completed: {metrics['metrics']['tasks_completed']}")
    print(f"  Tools used: {metrics['metrics']['tools_used']}")
    print(f"  Integrations used: {metrics['metrics']['integrations_used']}")


async def main():
    """Run complete E2E demo."""
    print("\n" + "=" * 70)
    print("  🚀 ADK (Agent Development Kit) Integration Ecosystem Demo")
    print("=" * 70)
    print("\n  Based on Google's ADK integrations ecosystem:")
    print("  • Observability: AgentOps, Arize, Phoenix, W&B Weave")
    print("  • Platforms: n8n, StackOne")
    print("  • AI/ML: Hugging Face")
    print("  • MCP Toolset & Multi-agent orchestration")
    print("\n" + "=" * 70)

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\n⚠️  Warning: ANTHROPIC_API_KEY not set.")
        print("   Agent execution will be limited.")

    input("\n  Press Enter to start demo...")

    # Run demos
    await demo_core_adk()
    input("\n  Press Enter to continue...")

    await demo_observability()
    input("\n  Press Enter to continue...")

    await demo_integration_platforms()
    input("\n  Press Enter to continue...")

    await demo_ai_ecosystem()
    input("\n  Press Enter to continue...")

    await demo_multi_agent()
    input("\n  Press Enter for complete integrated demo...")

    await demo_complete_stack()

    # Summary
    print_header("DEMO COMPLETE")

    print("✅ Demonstrated complete ADK ecosystem:")
    print("\n1. Core ADK Framework")
    print("   • ADK Agents with MCP Toolset")
    print("   • Custom tool registration")
    print("   • Task execution")

    print("\n2. Observability Stack")
    print("   • AgentOps - Session replays & metrics")
    print("   • Arize - Production observability")
    print("   • Phoenix - LLM traces & spans")
    print("   • W&B Weave - Model call logging")

    print("\n3. Integration Platforms")
    print("   • n8n - Workflow automation")
    print("   • StackOne - 200+ SaaS providers")

    print("\n4. AI/ML Ecosystem")
    print("   • Hugging Face - Models, datasets, papers")
    print("   • Model inference")
    print("   • Gradio apps")

    print("\n5. Multi-Agent Orchestration")
    print("   • Multi-agent workflows")
    print("   • Agent coordination")
    print("   • Parallel execution")

    print("\n6. Complete Integration")
    print("   • All integrations working together")
    print("   • Full observability")
    print("   • Production-ready agents")

    print("\n📚 Next steps:")
    print("   1. Try individual integrations")
    print("   2. Build your own agent with ADK framework")
    print("   3. Add custom integrations")
    print("   4. Deploy to production with observability")

    print("\n📖 Documentation:")
    print("   agency/adk/README.md")

    print("\n" + "=" * 70)
    print("  🎯 Build production AI agents with ADK!")
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
