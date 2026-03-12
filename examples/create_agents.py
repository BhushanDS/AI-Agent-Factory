"""
Example: Creating agents programmatically
"""
from agent_factory import AgentFactory, AgentConfig, AgentCapability


def create_coding_assistant():
    """Create a coding assistant agent"""
    config = AgentConfig(
        name="CodeWizard",
        description="An expert coding assistant that helps with programming tasks, code review, and debugging",
        system_prompt="""You are CodeWizard, an expert programming assistant.

Your expertise includes:
- Multiple programming languages (Python, JavaScript, TypeScript, Go, Rust, etc.)
- Software design patterns and best practices
- Debugging and code optimization
- Code review and refactoring

Guidelines:
- Always provide clean, well-documented code
- Explain your reasoning and approach
- Consider edge cases and error handling
- Follow language-specific best practices
- Be helpful but also teach good practices""",
        capabilities=[
            AgentCapability.CHAT,
            AgentCapability.CODE_GENERATION,
            AgentCapability.REASONING
        ],
        model="gpt-4o",
        temperature=0.3  # Lower temperature for more precise code
    )
    
    factory = AgentFactory()
    return factory.create_agent_from_config(config)


def create_research_assistant():
    """Create a research assistant agent"""
    config = AgentConfig(
        name="ResearchPro",
        description="A research assistant that helps analyze information, summarize documents, and provide insights",
        system_prompt="""You are ResearchPro, a thorough research assistant.

Your capabilities:
- Analyzing complex topics and breaking them down
- Summarizing information clearly
- Identifying key insights and patterns
- Providing balanced, well-reasoned analysis
- Citing sources when available

Guidelines:
- Be thorough but concise
- Acknowledge uncertainty when appropriate
- Consider multiple perspectives
- Organize information logically
- Ask clarifying questions when needed""",
        capabilities=[
            AgentCapability.CHAT,
            AgentCapability.REASONING,
            AgentCapability.DATA_ANALYSIS,
            AgentCapability.TASK_PLANNING
        ],
        model="gpt-4o",
        temperature=0.5
    )
    
    factory = AgentFactory()
    return factory.create_agent_from_config(config)


def create_with_conversation():
    """Create an agent through conversation with the factory"""
    factory = AgentFactory()
    
    # The factory will have a conversation to design the agent
    agent_path = factory.create_agent(
        "I need an agent that helps me plan and organize my daily tasks. "
        "It should be friendly, supportive, and help break down complex tasks "
        "into manageable steps."
    )
    
    return agent_path


if __name__ == "__main__":
    print("Creating example agents...\n")
    
    # Create agents programmatically
    print("1. Creating CodeWizard agent...")
    code_agent_path = create_coding_assistant()
    print(f"   Created at: {code_agent_path}\n")
    
    print("2. Creating ResearchPro agent...")
    research_agent_path = create_research_assistant()
    print(f"   Created at: {research_agent_path}\n")
    
    print("Done! Check the 'agents' directory for your new agents.")
