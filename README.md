# AI Research Agent

An AI-powered research assistant built with **FastAPI, Groq LLM, and web-based tools**. The agent can understand a research query, search the web, read relevant webpages, perform calculations when required, and generate a structured research report.

## 🚀 Features

* 🤖 AI-powered research using Groq LLM
* 🔎 Web search for real-time information
* 🌐 Webpage content extraction
* 🧮 Calculator tool for mathematical operations
* 🔄 Multi-turn tool execution
* 📑 Structured research reports
* ⚡ FastAPI REST API
* 🛠️ Tool-calling based agent architecture
* 🔐 Environment-based API key configuration

## 🏗️ Architecture

```text
                    User Query
                        │
                        ▼
              ┌──────────────────┐
              │   FastAPI API     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Research Agent  │
              │   Groq LLM       │
              └────────┬─────────┘
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          Web Search  Web Reader  Calculator
              │        │        │
              └────────┼────────┘
                       ▼
              Research Information
                       │
                       ▼
              Structured AI Report
```

## 📂 Project Structure

```text
ai-research-agent/
│
├── app/
│   ├── agents/
│   │   └── research_agent.py
│   │
│   ├── models/
│   │   └── research.py
│   │
│   ├── prompts/
│   │   └── research_prompt.py
│   │
│   ├── services/
│   │   └── groq_service.py
│   │
│   ├── tools/
│   │   ├── calculator.py
│   │   ├── search_tool.py
│   │   ├── tool_schemas.py
│   │   └── web_reader.py
│   │
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

| Technology            | Purpose                |
| --------------------- | ---------------------- |
| Python                | Core development       |
| FastAPI               | REST API               |
| Groq                  | LLM inference          |
| OpenAI-compatible API | LLM integration        |
| Requests              | HTTP requests          |
| BeautifulSoup         | Web content extraction |
| Pydantic              | Data validation        |
| Uvicorn               | ASGI server            |

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git
cd ai-research-agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```powershell
Copy-Item .env.example .env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

**Never commit your `.env` file or expose your API key publicly.**

## ▶️ Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API Usage

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "AI Research Agent API is running"
}
```

### Research

```http
POST /research
```

Request:

```json
{
  "query": "What are the latest trends in AI automation?"
}
```

The agent processes the query, uses available tools when required, and generates a structured research report.

Example response structure:

```json
{
  "title": "AI Automation Trends",
  "summary": "A summary of the research findings.",
  "key_findings": [
    "Finding 1",
    "Finding 2",
    "Finding 3"
  ],
  "sources": [
    {
      "title": "Source title",
      "url": "https://example.com"
    }
  ],
  "conclusion": "Final conclusion based on the research."
}
```

## 🧠 How It Works

1. User submits a research query.
2. FastAPI receives the request.
3. The Research Agent sends the query to the Groq LLM.
4. The LLM decides which tools are required.
5. The agent executes tools such as:

   * Web Search
   * Webpage Reader
   * Calculator
6. Tool results are returned to the LLM.
7. The agent can perform additional tool calls when required.
8. The collected information is processed.
9. A structured research report is generated.
10. FastAPI returns the final response.

## 🔧 Available Tools

### Web Search

Searches the web for relevant information and returns titles, URLs, and snippets.

### Webpage Reader

Reads and extracts useful content from webpages.

### Calculator

Performs mathematical calculations when required by the research query.

## 🔄 Multi-Turn Agent Execution

The research agent supports multiple reasoning/tool-execution cycles instead of relying on a single LLM call.

This allows the agent to:

```text
Query
  ↓
LLM
  ↓
Tool Call
  ↓
Tool Result
  ↓
LLM
  ↓
Additional Tool Call
  ↓
Tool Result
  ↓
Final Research Report
```

This improves the agent's ability to gather sufficient information before generating the final answer.

## 🔐 Environment Variables

The project uses environment variables for sensitive configuration.

```env
GROQ_API_KEY=your_groq_api_key_here
```

The actual `.env` file is excluded from Git using `.gitignore`.

## 📌 Future Improvements

* Add persistent research history
* Add source credibility scoring
* Add citation verification
* Add parallel web searches
* Add asynchronous tool execution
* Add database support
* Add authentication
* Add research export to PDF/Markdown
* Add additional research tools

## 👨‍💻 Author

Developed as a Generative AI / AI Agent project using Python and modern LLM tooling.
