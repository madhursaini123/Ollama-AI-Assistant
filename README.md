# Ollama-AI-Assistant
# 🧠 Local AI Assistant (Ollama + Mistral)  A terminal-based AI assistant that runs **completely offline** using Ollama and the Mistral model.   Built by Madhur Saini – demonstrates LLM integration, conversation memory, and Python skills.

## Features
- 💬 Full conversation memory (context-aware)
- 🧠 Runs locally – no data leaves your computer
- 💾 Save conversations to file (`/save`)
- 🔄 Clear history (`/clear`)
- 🤖 Custom system prompt (acts as a helpful, witty AI)

## Requirements
- [Ollama](https://ollama.com) installed
- Mistral model pulled: `ollama pull mistral`
- Python 3.8+

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/ollama-ai-assistant.git
cd ollama-ai-assistant
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Commands inside the chat:
/save – save conversation to Desktop
/clear – reset conversation history
/exit – quit
