"""
Base Agent class - Abstract base for all generated agents
"""
import os
from abc import ABC, abstractmethod
from typing import Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class BaseAgent(ABC):
    """
    Abstract base class for all AI Agents.
    Generated agents will inherit from this class.
    """
    
    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_key: Optional[str] = None
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.conversation_history: list[dict] = []
        self.tools: list[dict] = []
        
    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this agent"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the description of this agent"""
        pass
    
    def add_tool(self, tool: dict) -> None:
        """Add a tool to the agent's toolkit"""
        self.tools.append(tool)
    
    def reset_conversation(self) -> None:
        """Clear the conversation history"""
        self.conversation_history = []
    
    def chat(self, message: str, use_tools: bool = False) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: The user's message
            use_tools: Whether to enable tool use for this request
            
        Returns:
            The agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Build messages with system prompt
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history
        ]
        
        # Make API call
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        
        if use_tools and self.tools:
            kwargs["tools"] = self.tools
            kwargs["tool_choice"] = "auto"
        
        response = self.client.chat.completions.create(**kwargs)
        
        # Extract and store response
        assistant_message = response.choices[0].message
        
        # Handle tool calls if present
        if assistant_message.tool_calls:
            return self._handle_tool_calls(assistant_message)
        
        response_text = assistant_message.content or ""
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text
        })
        
        return response_text
    
    def _handle_tool_calls(self, assistant_message: Any) -> str:
        """Handle tool calls from the assistant - override in subclasses"""
        # Default implementation - just return the content if available
        return assistant_message.content or "Tool call requested but not implemented"
    
    def run(self, initial_message: Optional[str] = None) -> None:
        """
        Run the agent in interactive mode.
        
        Args:
            initial_message: Optional first message to send
        """
        print(f"\n[Agent] {self.name} is ready!")
        print(f"   {self.description}")
        print("   Type 'quit' to exit, 'reset' to clear history\n")
        
        if initial_message:
            print(f"You: {initial_message}")
            response = self.chat(initial_message)
            print(f"\n{self.name}: {response}\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                    
                if user_input.lower() == 'reset':
                    self.reset_conversation()
                    print("Conversation history cleared.\n")
                    continue
                
                response = self.chat(user_input)
                print(f"\n{self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
