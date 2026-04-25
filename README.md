# ITSM AI Agent

An industry-grade, autonomous IT Service Management (ITSM) Support Agent built using **LangGraph** and **Pydantic**. This application utilizes a state-driven knowledge graph to process incident reports, query vector knowledge bases for resolutions, and draft or update IT documentation dynamically.

## 🚀 Features
- **Stateful Workflows:** Built with LangGraph's `StateGraph` for highly reliable, memory-persistent workflows.
- **Dynamic Routing:** Intelligent routing mechanisms acting as a supervisor to dictate path execution (e.g., Drafting new KB articles vs. updating existing ones).
- **Data Integrity:** Strict input and output validation via `Pydantic` schemas.
- **Industry Standard Persistence:** Incorporates `MemorySaver` checkpointing for human-in-the-loop review capabilities and error-resilient state recovery.
- **Extensible Architecture:** Modular node, state, and routing logic allowing for seamless enterprise integration.

## 📁 Project Structure
```text
ITSM-AI-Agent/
│
├── src/
│   ├── schemas.py      # Pydantic validation & Graph state definitions
│   ├── nodes.py        # Individual workflow graph nodes (e.g., retrieve, draft, update)
│   ├── workflow.py     # Graph compilation and edge routing configuration
│   └── services.py     # External tool/DB services (e.g., Vector retrieval)
│
├── app.py              # Main application entry point (Agent runner)
├── requirements.txt    # Project dependencies
└── .gitignore          # Version control ignore list
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Puneetdivedi/ITSM-AI-Agent.git
cd ITSM-AI-Agent
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

To initialize the ITSM workflow and process a batch of mock tickets, run the main application:

```bash
python app.py
```

### Expected Output
The agent will ingest incoming webhook events (like support tickets), query the context using a simulated vector database, and print the detailed resolution aggregated action path.

```text
[2026-04-25 23:39:39] INFO     ITSM_Service - Initializing ITSM Support Resolution Workflow...
[2026-04-25 23:39:39] INFO     ITSM_Service - Ingesting Webhook Event: INC-11044
[2026-04-25 23:39:39] INFO     src.nodes - [Retrieval Node] Querying vector space for context...
[2026-04-25 23:39:39] INFO     src.nodes - [Update Node] ACTION: Flagging existing article for revision.
[2026-04-25 23:39:39] INFO     ITSM_Service - ==> FINAL AGGREGATED PATH LOGS: ['Retrieved KB Article: KB-NET-45', 'Flagged EXISTING article KB-NET-45 for revision based on INC-11044.']
...
```

## 🛡️ Enterprise Readiness
To take this implementation to full production capabilities:
1. **Vector DB Integration:** Replace the simulated lookup in `services.py` with an actual Pinecone/Qdrant/Milvus connection.
2. **LLM Invocation:** Add LangChain LLM instances in `nodes.py` to autonomously generate or summarize content rather than logging mock resolutions.
3. **Database Checkpointer:** Replace the in-memory `MemorySaver` with a production-ready PostgreSQL or Redis checkpointing mechanism for robust cross-session persistent memory.
