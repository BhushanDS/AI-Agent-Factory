"""
Example: Using a generated agent
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def example_usage():
    """Demonstrate using a generated agent"""
    try:
        # Try to import a generated agent
        from agents.code_wizard import CodeWizard
        
        agent = CodeWizard()
        
        # Use the agent
        response = agent.chat("Write a Python function to calculate fibonacci numbers")
        print(f"Agent Response:\n{response}")
        
    except ImportError:
        print("No generated agents found. Run create_agents.py first!")
        print("\nExample of how to use a generated agent:")
        print("""
from agents.code_wizard import CodeWizard

agent = CodeWizard()
response = agent.chat("Hello!")
print(response)

# Run interactively
agent.run()
        """)


if __name__ == "__main__":
    example_usage()
