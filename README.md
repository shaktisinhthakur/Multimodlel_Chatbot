# 🤖 Agentic Chatbot with FastAPI & LangGraph

An advanced, enterprise-ready **Agentic Chatbot** powered by **FastAPI** on the backend and **Streamlit** on the frontend. Leveraging **LangGraph** (with ReAct Agent architecture) and **LangChain**, it supports dynamic LLM provider switching (Groq & OpenAI), real-time web search integration via Tavily, custom personality tailoring (system prompts), and thread-safe conversational memory checkpointers.

---

## 🏗️ System Architecture

The following diagram illustrates the lifecycle of a request, demonstrating the separation of concerns between the user interface, backend validation layer, and the stateful agentic core:

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#e0f7fa,stroke:#00acc1,stroke-width:2px,color:#01579b;
    classDef server fill:#efebe9,stroke:#8d6e63,stroke-width:2px,color:#3e2723;
    classDef agent fill:#ede7f6,stroke:#7e57c2,stroke-width:2px,color:#311b92;
    classDef tool fill:#fff3e0,stroke:#ffb74d,stroke-width:2px,color:#e65100;
    classDef memory fill:#e8f5e9,stroke:#66bb6a,stroke-width:2px,color:#1b5e20;

    %% Nodes
    User([👤 End User])
    Streamlit[💻 Streamlit UI<br/><i>fronted.py</i>]:::client
    FastAPI[⚡ FastAPI API Layer<br/><i>backed.py</i>]:::server
    LangGraph[🧠 LangGraph Agent Core<br/><i>ai_agent_new.py</i>]:::agent
    Tavily[🔍 Tavily Search API]:::tool
    LLM[🤖 LLM Engine<br/><i>Groq / OpenAI</i>]:::tool
    Checkpointer[(💾 MemorySaver<br/><i>State Checkpoint</i>)]:::memory

    %% Relationships
    User <--> |Interacts with| Streamlit
    Streamlit <--> |POST /chat<br/>Schema Validation| FastAPI
    FastAPI <--> |Invokes| LangGraph
    LangGraph <--> |Thread Session State| Checkpointer
    LangGraph <--> |Tool Calls (conditional)| Tavily
    LangGraph <--> |Generate Completion| LLM
```

---

## ✨ Key Features

*   **⚡ Double-Engine Backend & Frontend**: Separates the API microservice (`FastAPI`) from the user interface (`Streamlit`) for horizontal scalability and independent deployment.
*   **🧠 LangGraph ReAct Architecture**: Utilizes `create_react_agent` for full reasoning-before-action execution loops.
*   **🔍 Dynamic Real-Time Web Search**: Incorporates Tavily Search API, allowing the agent to toggle web search on/off directly from the Streamlit UI to answer time-sensitive queries.
*   **💾 Thread-Safe Conversational Memory**: Utilizes LangGraph's `MemorySaver` thread-based checkpointing for robust conversation-history tracking under the `default_thread` context.
*   **🎭 Live Personality Injection**: Change the agent's behavior, instructions, and domain-expertise on the fly by customizing the system prompt directly from the UI.
*   **🔌 Multi-LLM & Provider Agnostic**: Seamlessly toggle between:
    *   **Groq**: `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `llama-3.3-70b-versatile`
    *   **OpenAI**: `gpt-4o-mini`

---

## 📂 Project Structure

```bash
Agentic-chatbot-fastapi/
│
├── backed.py          # FastAPI application server hosting the /chat endpoint
├── fronted.py         # Streamlit web interface with interactive sliders, radio buttons, and prompt boxes
├── ai_agent_new.py    # Core Agent logic, provider routing, Tavily tool binding, and LangGraph flow
├── ai_agent.py        # Prototype / historical agent file (archived/reference)
├── test.py            # Diagnostic script to test Groq connection and API keys
├── .env               # Local configuration file (contains API keys)
└── README.md          # Comprehensive documentation (this file)
```

### 📄 Detailed File Descriptions

*   **[backed.py](backed.py)**: Definess the `/chat` POST endpoint. Employs `Pydantic` schema validation (`RequestState`) to sanitize client inputs, enforces safe-model policies through `ALLOWED_MODEL_NAMES`, and handles downstream agent errors elegantly.
*   **[fronted.py](fronted.py)**: Renders the sleek web frontend. Allows users to specify LLM providers, select models, write bespoke agent personalities, toggle web search capability, compile user queries, and render markdown outputs with live error catchers.
*   **[ai_agent_new.py](ai_agent_new.py)**: Binds keys and loads models dynamically using `ChatGroq` or `ChatOpenAI`. Compiles tools into the agent state, handles thread configuration for checkpoint-based persistence, and outputs parsed target completions.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Clone and Setup Environment
Navigate to the project root directory and create a virtual environment:

```bash
# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### 3. Install Dependencies
Install all required libraries for LangGraph, FastAPI, and Streamlit:

```bash
pip install fastapi uvicorn streamlit requests langchain-groq langchain-openai langchain-community langgraph groq python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the root of the project directory and supply your API keys:

```ini
# .env
GROQ_API_KEY="your_groq_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
```

> [!WARNING]
> Keep your `.env` secure and never commit it to repository tracking systems.

---

## 🚀 How to Run

For the full application experience, you will run the backend and frontend services in parallel:

### 1. Start the Backend API (FastAPI)
Run the FastAPI web server using Uvicorn:

```bash
python backed.py
```
*   **API URL**: `http://127.0.0.1:8000`
*   **Interactive Swagger Documentation**: `http://127.0.0.1:8000/docs`

### 2. Start the Frontend UI (Streamlit)
In a separate terminal window (with virtual environment activated), start Streamlit:

```bash
streamlit run fronted.py
```
*   **Local Web Address**: `http://localhost:8501`

---

## 🔌 API Endpoint Specifications

The backend can be integrated with other frontends, CLI applications, or automated workflows.

### Endpoint: `POST /chat`

#### Request Payload Schema
```json
{
  "model_name": "llama-3.3-70b-versatile",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful data analyst. Respond in concise bullet points.",
  "messages": ["Explain what linear regression is in one sentence."],
  "allow_search": false
}
```

#### Response Payload Schema (Success)
```json
{
  "status": "success",
  "response": "Linear regression is a statistical method used to model the relationship between a dependent variable and one or more independent variables by fitting a linear equation to observed data."
}
```

#### Response Payload Schema (Invalid Model / Error)
```json
{
  "status": "error",
  "error": "Model name 'invalid-model-name' is not allowed."
}
```

---

## 💡 Best Practices Implemented

*   **Pydantic Schema Enforcement**: Ensures that all inbound API request packages match expected types (`str`, `bool`, `list`) before triggering expensive model evaluations.
*   **Agent Execution Safety Limits**: Configures `TavilySearchResults` with a safe limit of `max_results=2` to restrict prompt bloating and token consumption.
*   **Fail-Safe Architecture**: Catches network loss gracefully (e.g., when the frontend is launched but the backend API server is sleeping) and alerts the user with dynamic UI warnings.
