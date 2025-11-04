# MiniSH

A tiny, no-fuss shell for interacting with the Gemini API. Think of it as your mini command center with LLM integrated.  

## Features

- Super easy setup with a Python virtual environment  
- Handles dependencies automatically  
- Quick launch via `./your_project.sh`  
- Gemini API integration (enter your key when prompted)  
- Minimal and lightweight, no bloat  

---

## Follow these steps to get MiniSH running:

```bash
# Clone the repo
git clone https://github.com/MiniSH.git
cd MiniSH

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the startup script
./your_project.sh

If ./your_project.sh doesn’t run, make it executable first:
chmod +x your_project.sh

# Enter your Gemini API key when prompted

Wanr to use LLM:
command:
ai "your query"
