"""
CLI interface for the AI Agent Factory
"""
import typer
from pathlib import Path
from rich.console import Console

from agent_factory.factory import AgentFactory
from agent_factory.config import AgentConfig, AgentCapability

app = typer.Typer(
    name="agent-factory",
    help="AI Agent Factory - Create AI agents that create AI agents"
)
console = Console()


@app.command()
def create(
    description: str = typer.Argument(
        ...,
        help="Description of the agent you want to create"
    ),
    output_dir: str = typer.Option(
        "agents",
        "--output", "-o",
        help="Output directory for generated agents"
    ),
    model: str = typer.Option(
        "gpt-4o",
        "--model", "-m",
        help="LLM model to use for agent design"
    )
):
    """Create a new AI agent based on your description."""
    factory = AgentFactory(model=model)
    factory.create_agent(description)


@app.command()
def interactive():
    """Run the agent factory in interactive mode."""
    factory = AgentFactory()
    factory.run_interactive()


@app.command()
def quick(
    name: str = typer.Argument(..., help="Name for the agent"),
    description: str = typer.Argument(..., help="What the agent does"),
    system_prompt: str = typer.Option(
        None,
        "--prompt", "-p",
        help="System prompt for the agent"
    ),
    capabilities: list[str] = typer.Option(
        ["chat"],
        "--cap", "-c",
        help="Capabilities (can specify multiple)"
    ),
    output_dir: str = typer.Option(
        "agents",
        "--output", "-o",
        help="Output directory"
    )
):
    """Quickly create an agent with explicit parameters (no LLM design)."""
    # Use default system prompt if not provided
    if not system_prompt:
        system_prompt = f"You are {name}, an AI assistant. {description}"
    
    # Parse capabilities
    caps = []
    for cap in capabilities:
        try:
            caps.append(AgentCapability(cap))
        except ValueError:
            console.print(f"[yellow]Warning: Unknown capability '{cap}', skipping[/yellow]")
    
    if not caps:
        caps = [AgentCapability.CHAT]
    
    config = AgentConfig(
        name=name,
        description=description,
        system_prompt=system_prompt,
        capabilities=caps,
        output_directory=output_dir
    )
    
    factory = AgentFactory()
    agent_path = factory.create_agent_from_config(config)
    console.print(f"[green][OK] Agent created at: {agent_path}[/green]")


@app.command()
def list_capabilities():
    """List all available agent capabilities."""
    console.print("\n[bold]Available Agent Capabilities:[/bold]\n")
    for cap in AgentCapability:
        console.print(f"  - [cyan]{cap.value}[/cyan]")
    console.print()


if __name__ == "__main__":
    app()
