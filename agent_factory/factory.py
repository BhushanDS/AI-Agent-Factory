"""
AI Agent Factory - The Meta-Agent that creates other AI Agents
"""
import os
import re
from pathlib import Path
from typing import Optional
from jinja2 import Template
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .config import AgentConfig, AgentCapability
from .templates import AGENT_TEMPLATE, AGENT_INIT_TEMPLATE, AGENT_README_TEMPLATE

load_dotenv()
console = Console()


class AgentFactory:
    """
    The Meta-Agent: An AI that creates other AI agents.
    
    This agent can:
    1. Understand user requirements for a new agent
    2. Design the agent's capabilities and behavior
    3. Generate the agent code from templates
    4. Create runnable agent files
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.conversation_history: list[dict] = []
        
        # System prompt for the factory agent
        self.system_prompt = """You are an AI Agent Factory - a meta-agent that designs and creates other AI agents.

Your role is to:
1. Understand what kind of AI agent the user wants to create
2. Ask clarifying questions if needed
3. Design the agent's configuration including:
   - A descriptive name (in PascalCase, e.g., "CodeAssistant")
   - A clear description of the agent's purpose
   - An effective system prompt that defines the agent's personality and behavior
   - Appropriate capabilities from: chat, code_generation, data_analysis, web_search, file_operations, api_integration, task_planning, memory, tool_use, reasoning
   - Model selection (gpt-4o, gpt-4o-mini, etc.)
   - Temperature setting (0.0-2.0)

When you have enough information, output the agent configuration in this EXACT JSON format:
```json
{
    "name": "AgentName",
    "description": "What the agent does",
    "system_prompt": "The full system prompt for the agent",
    "capabilities": ["chat", "reasoning"],
    "model": "gpt-4o",
    "temperature": 0.7,
    "max_tokens": 4096,
    "tools": []
}
```

Be creative but practical. Design agents that are useful, well-defined, and have clear purposes.
Always wrap the final configuration in ```json``` code blocks so it can be parsed."""

    def _to_snake_case(self, name: str) -> str:
        """Convert PascalCase or camelCase to snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    def _to_pascal_case(self, name: str) -> str:
        """Convert string to PascalCase"""
        # Remove special characters and split
        words = re.split(r'[_\s-]+', name)
        return ''.join(word.capitalize() for word in words)
    
    def _extract_json_config(self, text: str) -> Optional[dict]:
        """Extract JSON configuration from LLM response"""
        import json
        
        # Look for JSON in code blocks
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', text)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find raw JSON
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        
        return None
    
    def design_agent(self, user_request: str) -> tuple[str, Optional[AgentConfig]]:
        """
        Have a conversation with the LLM to design an agent based on user request.
        
        Args:
            user_request: What kind of agent the user wants
            
        Returns:
            Tuple of (response text, AgentConfig if complete)
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_request
        })
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=4096
        )
        
        response_text = response.choices[0].message.content or ""
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        # Try to extract configuration
        config_dict = self._extract_json_config(response_text)
        if config_dict:
            try:
                config = AgentConfig(**config_dict)
                return response_text, config
            except Exception as e:
                console.print(f"[yellow]Warning: Could not parse config: {e}[/yellow]")
        
        return response_text, None
    
    def generate_agent(self, config: AgentConfig) -> Path:
        """
        Generate agent code from configuration.
        
        Args:
            config: The agent configuration
            
        Returns:
            Path to the generated agent directory
        """
        # Prepare template variables
        class_name = self._to_pascal_case(config.name)
        module_name = self._to_snake_case(config.name)
        
        template_vars = {
            "agent_name": config.name,
            "class_name": class_name,
            "module_name": module_name,
            "description": config.description,
            "system_prompt": config.system_prompt.replace('"""', '\\"\\"\\"'),
            "capabilities": config.capabilities,
            "model": config.model,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "tools": config.tools,
        }
        
        # Create agent directory
        base_dir = Path(config.output_directory)
        agent_dir = base_dir / module_name
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate main agent file
        agent_template = Template(AGENT_TEMPLATE)
        agent_code = agent_template.render(**template_vars)
        agent_file = agent_dir / f"{module_name}.py"
        agent_file.write_text(agent_code, encoding='utf-8')
        
        # Generate __init__.py
        init_template = Template(AGENT_INIT_TEMPLATE)
        init_code = init_template.render(**template_vars)
        init_file = agent_dir / "__init__.py"
        init_file.write_text(init_code, encoding='utf-8')
        
        # Generate README
        readme_template = Template(AGENT_README_TEMPLATE)
        readme_content = readme_template.render(**template_vars)
        readme_file = agent_dir / "README.md"
        readme_file.write_text(readme_content, encoding='utf-8')
        
        return agent_dir
    
    def create_agent(self, user_request: str) -> Optional[Path]:
        """
        Main method to create an agent from a user request.
        This method handles the full conversation flow.
        
        Args:
            user_request: Description of the agent to create
            
        Returns:
            Path to generated agent or None if incomplete
        """
        console.print(Panel(
            f"[bold blue]AI Agent Factory[/bold blue]\n\n"
            f"Creating agent for: {user_request}",
            title="Agent Factory"
        ))
        
        response, config = self.design_agent(user_request)
        console.print(Markdown(response))
        
        while config is None:
            user_input = console.input("\n[bold green]You:[/bold green] ")
            if user_input.lower() in ['quit', 'exit', 'cancel']:
                console.print("[yellow]Agent creation cancelled.[/yellow]")
                return None
            
            response, config = self.design_agent(user_input)
            console.print(Markdown(response))
        
        # Generate the agent
        console.print("\n[bold green][OK] Configuration complete! Generating agent...[/bold green]")
        agent_path = self.generate_agent(config)
        
        console.print(Panel(
            f"[bold green]Agent created successfully![/bold green]\n\n"
            f"Location: {agent_path}\n"
            f"Name: {config.name}\n"
            f"Description: {config.description}\n\n"
            f"To run your agent:\n"
            f"```python\n"
            f"python {agent_path / (self._to_snake_case(config.name) + '.py')}\n"
            f"```",
            title="Agent Created"
        ))
        
        return agent_path
    
    def create_agent_from_config(self, config: AgentConfig) -> Path:
        """
        Create an agent directly from a configuration object.
        
        Args:
            config: The agent configuration
            
        Returns:
            Path to generated agent
        """
        return self.generate_agent(config)
    
    def run_interactive(self) -> None:
        """Run the factory in interactive mode"""
        console.print(Panel(
            "[bold blue]Welcome to the AI Agent Factory![/bold blue]\n\n"
            "I'm a meta-agent that creates other AI agents.\n"
            "Tell me what kind of agent you want to create, and I'll design and generate it for you.\n\n"
            "Type 'quit' to exit.",
            title="AI Agent Factory"
        ))
        
        while True:
            try:
                user_input = console.input("\n[bold green]You:[/bold green] ")
                
                if user_input.lower() in ['quit', 'exit']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if user_input.lower() == 'reset':
                    self.conversation_history = []
                    console.print("[yellow]Conversation reset.[/yellow]")
                    continue
                
                self.create_agent(user_input)
                
                # Reset for next agent
                self.conversation_history = []
                console.print("\n[dim]Ready to create another agent...[/dim]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye![/yellow]")
                break
