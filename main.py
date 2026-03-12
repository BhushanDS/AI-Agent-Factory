"""
Main entry point for the AI Agent Factory
"""
from agent_factory import AgentFactory


def main():
    """Run the Agent Factory in interactive mode"""
    factory = AgentFactory()
    factory.run_interactive()


if __name__ == "__main__":
    main()
