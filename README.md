# AI Research Agent

An AI-powered research assistant built with **FastAPI, Groq LLM, and web-based tools**. The agent can understand a research query, search the web, read relevant webpages, perform calculations when required, and generate a structured research report.

## 🚀 Features

- 🤖 AI-powered research using Groq LLM
- 🔎 Web search for real-time information
- 🌐 Webpage content extraction
- 🧮 Calculator tool for mathematical operations
- 🔄 Multi-turn tool execution
- 📑 Structured research reports
- ⚡ FastAPI REST API
- 🛠️ Tool-calling based agent architecture
- 🔐 Environment-based API key configuration

## 🏗️ Architecture

```text
                    User Query
                        │
                        ▼
              ┌──────────────────┐
              │   FastAPI API    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  Research Agent  │
              │    Groq LLM      │
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
