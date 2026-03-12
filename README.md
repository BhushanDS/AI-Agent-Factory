# AI Agent Factory

<div align="center">

**A Meta-Agent System that Creates AI Agents**

*Describe what you need - Get a fully functional AI agent*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Interactive Mode](#1-interactive-mode)
  - [CLI Commands](#2-cli-commands)
  - [Programmatic API](#3-programmatic-api)
- [Generated Agent Structure](#generated-agent-structure)
- [Available Capabilities](#available-capabilities)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AI Agent Factory** is a revolutionary meta-agent system - an AI that creates other AI agents. Instead of manually coding AI assistants, simply describe what you need in natural language, and the factory will:

1. **Understand** your requirements through intelligent conversation
2. **Design** the perfect agent configuration (personality, capabilities, behavior)
3. **Generate** clean, production-ready Python code
4. **Create** a fully functional, immediately runnable AI agent

This project demonstrates the power of **agentic AI** - AI systems that can autonomously perform complex tasks, including creating other AI systems.

---

## How It Works

```
+------------------------------------------------------------------+
|                      AI AGENT FACTORY                            |
+------------------------------------------------------------------+
|                                                                  |
|   User Input          Meta-Agent            Generated Agent      |
|   -----------         ----------            ---------------      |
|                                                                  |
|   "I need an    -->   [Factory]     -->    agents/assistant/     |
|    agent that         (GPT-4)              +-- __init__.py       |
|    helps with                              +-- assistant.py      |
|    coding"                                 +-- README.md         |
|                                                                  |
|                           |                        |             |
|                           v                        v             |
|                    +--------------+        +--------------+      |
|                    | Understands  |        | Ready to Run |      |
|                    | Requirements |        | python agent |      |
|                    | Designs Config|       |              |      |
|                    | Generates Code|       | Chat with    |      |
|                    +--------------+        | your agent   |      |
|                                            +--------------+      |
+------------------------------------------------------------------+
```

### The Process

1. **You describe** what kind of agent you want
2. **The Factory** (powered by GPT-4) asks clarifying questions if needed
3. **It designs** a complete agent configuration including:
   - Name and description
   - System prompt (personality & behavior)
   - Capabilities (reasoning, code generation, etc.)
   - Model settings (temperature, max tokens)
4. **Code is generated** using Jinja2 templates
5. **Your agent is ready** to use immediately!

---

## Features

| Feature | Description |
|---------|-------------|
| **Conversational Design** | Describe your agent in plain English - no coding required |
| **Smart Configuration** | Automatically generates optimal system prompts and settings |
| **Template-Based Generation** | Produces clean, consistent, maintainable Python code |
| **Multiple Capabilities** | Support for chat, coding, reasoning, planning, and more |
| **CLI Interface** | Easy command-line usage with rich formatting |
| **Programmatic API** | Integrate agent creation into your own applications |
| **Auto Documentation** | Each generated agent includes its own README |
| **Extensible** | Easy to add new capabilities and templates |

---

## Installation

### Prerequisites

- **Python 3.10** or higher
- **OpenAI API key** with available credits
- **pip** package manager

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-agent-factory.git
cd ai-agent-factory
```

#### 2. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `openai` - OpenAI API client
- `pydantic` - Data validation
- `jinja2` - Template engine
- `rich` - Beautiful terminal output
- `typer` - CLI framework
- `python-dotenv` - Environment variable management

---

## Configuration

### Setting Up Your API Key

#### Option 1: Environment File (Recommended)

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=your-api-key-here
```

#### Option 2: Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Getting an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **"Create new secret key"**
4. Copy the key and save it securely
5. Add billing at [Billing Settings](https://platform.openai.com/settings/organization/billing/overview)

> **Note:** OpenAI API requires credits. New accounts may get free credits; otherwise, add a payment method.

---

## Usage

### 1. Interactive Mode

The easiest way to create agents:

```bash
python main.py
```

**Example Session:**
```
+------------------- AI Agent Factory --------------------+
| Welcome to the AI Agent Factory!                        |
|                                                         |
| I'm a meta-agent that creates other AI agents.          |
| Tell me what kind of agent you want to create.          |
|                                                         |
| Type 'quit' to exit.                                    |
+---------------------------------------------------------+

You: I need an agent that helps me write professional emails

Creating agent...

I'll create an EmailAssistant for you! Here's the configuration:
- Name: EmailAssistant  
- Capabilities: chat, reasoning
- Temperature: 0.7

[OK] Agent created successfully!
Location: agents/email_assistant
Name: EmailAssistant

To run your agent:
python agents/email_assistant/email_assistant.py
```

### 2. CLI Commands

#### Create Agent via Conversation
```bash
python cli.py create "A coding assistant that helps with Python and debugging"
```

#### Quick Create (No Conversation)
```bash
python cli.py quick "DataAnalyst" "Analyzes data and provides insights" \
    --cap chat \
    --cap data_analysis \
    --cap reasoning
```

#### Interactive Mode
```bash
python cli.py interactive
```

#### List Available Capabilities
```bash
python cli.py list-capabilities
```

### 3. Programmatic API

#### Basic Usage
```python
from agent_factory import AgentFactory

# Create factory instance
factory = AgentFactory()

# Create agent through conversation
agent_path = factory.create_agent(
    "I need an agent that helps with project management and task planning"
)

print(f"Agent created at: {agent_path}")
```

#### With Explicit Configuration
```python
from agent_factory import AgentFactory, AgentConfig, AgentCapability

# Define configuration
config = AgentConfig(
    name="ProjectManager",
    description="Helps manage projects and plan tasks effectively",
    system_prompt="""You are ProjectManager, an expert project management assistant.

Your expertise includes:
- Breaking down complex projects into manageable tasks
- Creating realistic timelines and milestones
- Identifying risks and dependencies
- Providing progress tracking strategies

Be organized, practical, and encouraging. Use bullet points and numbered lists.""",
    capabilities=[
        AgentCapability.CHAT,
        AgentCapability.TASK_PLANNING,
        AgentCapability.REASONING
    ],
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=4096
)

# Generate the agent
factory = AgentFactory()
agent_path = factory.create_agent_from_config(config)
```

#### Using Generated Agents
```python
# Import the generated agent
from agents.project_manager import ProjectManager

# Create instance
agent = ProjectManager()

# Chat with it
response = agent.chat("Help me plan a website redesign project")
print(response)

# Continue the conversation
response = agent.chat("What should be the first milestone?")
print(response)

# Or run in interactive mode
agent.run()
```

---

## Generated Agent Structure

When you create an agent, the factory generates a complete package:

```
agents/
+-- your_agent_name/
    +-- __init__.py           # Package initialization
    +-- your_agent_name.py    # Main agent class
    +-- README.md             # Agent documentation
```

### Generated Agent Features

Each generated agent includes:

- [x] **Inherits from BaseAgent** - Consistent interface
- [x] **Configured System Prompt** - Defines personality
- [x] **Conversation History** - Maintains context
- [x] **Interactive Mode** - `agent.run()` for CLI chat
- [x] **Capability Methods** - Based on selected capabilities
- [x] **Documentation** - README with usage instructions

### Example Generated Code

```python
class ProjectManager(BaseAgent):
    """
    Helps manage projects and plan tasks effectively
    
    Capabilities: chat, task_planning, reasoning
    Model: gpt-4o-mini
    """
    
    @property
    def name(self) -> str:
        return "ProjectManager"
    
    @property
    def system_prompt(self) -> str:
        return """You are ProjectManager, an expert..."""
    
    def plan_task(self, task: str) -> str:
        """Create a detailed plan for a task"""
        return self.chat(f"Create a plan for: {task}")
    
    def reason(self, problem: str) -> str:
        """Apply step-by-step reasoning"""
        return self.chat(f"Reason through: {problem}")
```

---

## Available Capabilities

| Capability | Description | Added Methods |
|------------|-------------|---------------|
| `chat` | Basic conversation abilities | Default `chat()` method |
| `code_generation` | Generate code from specifications | `generate_code(spec, language)` |
| `reasoning` | Step-by-step problem solving | `reason(problem)` |
| `task_planning` | Break down complex tasks | `plan_task(task)` |
| `data_analysis` | Analyze and interpret data | `analyze_data(data)` |
| `web_search` | Web search capabilities | *Requires implementation* |
| `file_operations` | File system operations | *Requires implementation* |
| `api_integration` | External API calls | *Requires implementation* |
| `memory` | Persistent context | *Requires implementation* |
| `tool_use` | External tool usage | *Requires implementation* |

---

## Project Structure

```
ai-agent-factory/
│
├── agent_factory/              # Core module
│   ├── __init__.py            # Package exports
│   ├── base_agent.py          # BaseAgent class (parent for all agents)
│   ├── config.py              # Pydantic models (AgentConfig, etc.)
│   ├── factory.py             # AgentFactory (the meta-agent)
│   └── templates.py           # Jinja2 templates for code generation
│
├── agents/                     # Generated agents directory
│   └── __init__.py            # Package marker
│
├── examples/                   # Example scripts
│   ├── create_agents.py       # Programmatic creation examples
│   └── use_agent.py           # Usage examples
│
├── .github/
│   └── copilot-instructions.md # AI coding assistant instructions
│
├── .vscode/
│   ├── launch.json            # Debug configurations
│   └── tasks.json             # Build tasks
│
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore rules
├── cli.py                     # Command-line interface
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
└── README.md                  # This file
```

---

## Examples

### Example 1: Code Review Agent

```python
from agent_factory import AgentFactory, AgentConfig, AgentCapability

config = AgentConfig(
    name="CodeReviewer",
    description="Reviews code for bugs, best practices, and improvements",
    system_prompt="""You are CodeReviewer, an expert code review assistant.

When reviewing code, you:
- Identify bugs and potential issues
- Suggest performance improvements
- Check for security vulnerabilities
- Recommend best practices
- Provide constructive, educational feedback

Be thorough but kind. Explain the 'why' behind your suggestions.""",
    capabilities=[
        AgentCapability.CHAT,
        AgentCapability.CODE_GENERATION,
        AgentCapability.REASONING
    ],
    temperature=0.3  # Lower for more precise analysis
)

factory = AgentFactory()
factory.create_agent_from_config(config)
```

### Example 2: Study Buddy

```python
config = AgentConfig(
    name="StudyBuddy",
    description="A friendly tutor that helps with learning any subject",
    system_prompt="""You are StudyBuddy, a patient and encouraging tutor.

Your teaching style:
- Break complex concepts into simple parts
- Use analogies and real-world examples
- Ask questions to check understanding
- Celebrate progress and encourage persistence
- Adapt explanations to the student's level

Make learning fun and engaging!""",
    capabilities=[
        AgentCapability.CHAT,
        AgentCapability.REASONING,
        AgentCapability.TASK_PLANNING
    ],
    temperature=0.8  # Higher for more creative explanations
)
```

### Example 3: Using a Generated Agent

```python
from agents.study_buddy import StudyBuddy

# Initialize
tutor = StudyBuddy()

# Start a learning session
print(tutor.chat("I want to learn about machine learning. Where should I start?"))

# Ask follow-up questions
print(tutor.chat("Can you explain neural networks with a simple analogy?"))

# Use the reasoning capability
print(tutor.reason("Why does gradient descent work for training neural networks?"))

# Get a study plan
print(tutor.plan_task("Learn the basics of Python in 2 weeks"))
```

---

## Troubleshooting

### Common Issues

#### 1. `ModuleNotFoundError: No module named 'agent_factory'`

**Solution:** Run from the project root directory:
```bash
cd path/to/ai-agent-factory
python main.py
```

Or set PYTHONPATH:
```bash
$env:PYTHONPATH = "C:\path\to\ai-agent-factory"  # Windows
export PYTHONPATH="/path/to/ai-agent-factory"   # Linux/macOS
```

#### 2. `openai.AuthenticationError: Incorrect API key`

**Solution:** Check your `.env` file:
```bash
# Make sure it contains:
OPENAI_API_KEY=sk-your-actual-key-here

# No quotes, no spaces around the =
```

#### 3. `openai.RateLimitError: You exceeded your current quota`

**Solution:** 
- Add billing: https://platform.openai.com/settings/organization/billing
- Add at least $5 in credits
- Or use a different API key with credits

#### 4. Virtual Environment Not Activated

**Symptoms:** `ModuleNotFoundError` for installed packages

**Solution (Windows):**
```powershell
# If activation script is blocked:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
.\.venv\Scripts\Activate.ps1

# Or use python directly:
.\.venv\Scripts\python.exe main.py
```

#### 5. Interactive Mode Not Working in VS Code

**Symptoms:** Terminal doesn't accept input

**Solution:** Use an external terminal:
- Open Windows Terminal or Command Prompt
- Navigate to project folder
- Run: `.\.venv\Scripts\python.exe main.py`

---

## Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

- **Report bugs** - Open an issue with details
- **Suggest features** - Share your ideas
- **Improve docs** - Fix typos, add examples
- **Submit PRs** - Add new capabilities, fix issues

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-agent-factory.git
cd ai-agent-factory

# Create branch
git checkout -b feature/your-feature

# Install dev dependencies
pip install -r requirements.txt

# Make changes and test
python main.py

# Commit and push
git commit -m "Add your feature"
git push origin feature/your-feature

# Open a Pull Request
```

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - You are free to:
[x] Use commercially
[x] Modify
[x] Distribute
[x] Use privately
```

---

## Acknowledgments

- **OpenAI** for the GPT models
- **Pydantic** for data validation
- **Rich** for beautiful terminal output
- **Jinja2** for templating

---

## Star This Project

If you find this useful, please give it a star!

It helps others discover the project and motivates continued development.

---

<div align="center">

**Built with Python and OpenAI**

[Report Bug](https://github.com/yourusername/ai-agent-factory/issues) | 
[Request Feature](https://github.com/yourusername/ai-agent-factory/issues) | 
[Contribute](https://github.com/yourusername/ai-agent-factory/pulls)

</div>
