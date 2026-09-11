# TamBOT AI

Created by itzz_thammi.

A cross-device starter for a fast, multimodal AI assistant. The included app provides:
- TamBOT AI branding
- fast streaming text chat
- persistent browser conversation history
- a memory panel
- voice input/output hooks
- image upload hooks
- responsive UI for phones, tablets and desktops
- safe system instructions
- server-side OpenAI API key handling

## Run

1. Install Python 3.10+.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Set your API key as an environment variable:
   - macOS/Linux: `export OPENAI_API_KEY="your_key"`
   - Windows PowerShell: `$env:OPENAI_API_KEY="your_key"`
4. Run:
   `python server.py`
5. Open the address printed by the server.

Do NOT put your API key into `static/app.js`.

This is a real working starter, not a trained foundation model. It uses an AI API for the heavy model work and is structured so realtime voice, image generation, web search, authentication and cloud memory can be added behind the same interface.
