"""
Configuration models for AI Agents using Pydantic
"""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AgentCapability(str, Enum):
    """Available capabilities that can be assigned to an agent"""
    CHAT = "chat"
    CODE_GENERATION = "code_generation"
    DATA_ANALYSIS = "data_analysis"
    WEB_SEARCH = "web_search"
    FILE_OPERATIONS = "file_operations"
    API_INTEGRATION = "api_integration"
    TASK_PLANNING = "task_planning"
    MEMORY = "memory"
    TOOL_USE = "tool_use"
    REASONING = "reasoning"


class AgentConfig(BaseModel):
    """Configuration for creating a new AI Agent"""
    
    name: str = Field(
        ..., 
        description="The name of the agent (used for class name and file name)"
    )
    description: str = Field(
        ..., 
        description="A description of what the agent does"
    )
    system_prompt: str = Field(
        ..., 
        description="The system prompt that defines the agent's personality and behavior"
    )
    capabilities: list[AgentCapability] = Field(
        default=[AgentCapability.CHAT],
        description="List of capabilities the agent should have"
    )
    model: str = Field(
        default="gpt-4o",
        description="The LLM model to use for the agent"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Temperature for LLM responses"
    )
    max_tokens: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens for LLM responses"
    )
    tools: list[str] = Field(
        default=[],
        description="List of tool names the agent can use"
    )
    output_directory: str = Field(
        default="agents",
        description="Directory where the generated agent will be saved"
    )
    
    class Config:
        use_enum_values = True


class ToolDefinition(BaseModel):
    """Definition for a tool that an agent can use"""
    
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="What the tool does")
    parameters: dict = Field(
        default={},
        description="JSON Schema for tool parameters"
    )
    code: str = Field(
        default="",
        description="Python code implementing the tool"
    )
