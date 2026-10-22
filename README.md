# 🤖 AI Studio: Multi-Tool Generative AI Application

AI Studio is a Streamlit-based Generative AI application that brings multiple AI-powered text tools into a single interface. Built with Python and powered by Groq's LLaMA 3.3 70B model, it supports text summarization, content generation, and conversational assistance.

## ✨ Features

- 💬 **AI Chat:** talk to an LLM through a conversational interface
- 📝 **Text Summarization:** turn long text into concise summaries
- ✍️ **Content Generation:** generate text from your own prompts
- 🧠 **Session Memory:** keeps conversational context during a session
- ⚡ **Fast inference:** Groq API with the LLaMA 3.3 70B model
- 🖥️ **Interactive UI:** all tools available in one Streamlit interface

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| Frontend / UI | Streamlit |
| LLM Provider | Groq API |
| AI Model | LLaMA 3.3 70B |
| Configuration | Environment variables (`.env`) |

## ⚙️ How It Works

1. The user selects an AI tool and enters a prompt or text.
2. Streamlit prepares the request along with the session context.
3. The request is sent to the Groq API.
4. LLaMA 3.3 70B generates a response.
5. The response is displayed in the interface.

## 🏗️ Architecture

```text
User Input → Streamlit Interface → Groq API → LLaMA 3.3 70B
                    ↑                               │
                    └──────── Generated Response ◀──┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Groq API key](https://console.groq.com)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/AI-Studio.git
cd AI-Studio

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate           # Windows
# source venv/bin/activate      # macOS / Linux

# 3. Install dependencies
pip install streamlit groq python-dotenv
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the App

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

## 🔐 Security

- Keep your API key in `.env` and never commit it to GitHub.
- Make sure `.env` and `venv/` are listed in `.gitignore`.

## ⚠️ Limitations

- Conversation memory lasts only for the current session.
- Responses depend on the LLM and may be inaccurate or incomplete.

## 🗺️ Future Enhancements

- Export generated content
- Support for additional LLM providers
- Document-based question answering
- Better conversation history management
- Automated tests and deployment configuration

## 📄 Disclaimer

AI Studio generates responses using a large language model. Outputs may contain inaccurate or incomplete information and should be reviewed before use.
