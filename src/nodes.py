import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.schemas import SupportAgentState
from src.services import retrieve_knowledge_base_article
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize the LLM Agent
# Uses gemini-2.5-flash for fast and intelligent text generation
# We fallback to a mock key so the application doesn't crash if the user hasn't set one yet
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logger.warning("No GOOGLE_API_KEY found in environment. LLM will use mock responses.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=api_key or "MOCK_KEY_FOR_TESTING"
)

def _invoke_llm_safely(messages: list) -> str:
    """Helper to invoke LLM and fallback gracefully if API key is missing or invalid."""
    if not os.environ.get("GOOGLE_API_KEY"):
        return "(MOCK LLM OUTPUT - Missing GOOGLE_API_KEY)\n\n**Generated KB Article**\n* Symptoms: User reported issue.\n* Resolution: Steps were taken to resolve it."
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        logger.error(f"LLM API Error: {e}")
        return f"(ERROR LLM OUTPUT) Failed to generate content: {e}"

async def retrieve_knowledge_node(state: SupportAgentState):
    try:
        issue_desc = state["incident_report"].issue_description
        logger.info(f"[Retrieval Node] Querying vector space for context: '{issue_desc[:30]}...'")
        
        article = await retrieve_knowledge_base_article(issue_desc)
        
        # We return a list to trigger the operator.add reducer in schema!
        log = [f"Retrieved KB Article: {article['article_id']}"] if article else ["No relevant KB Article found."]
        return {"retrieved_article": article, "action_log": log}
        
    except Exception as e:
        logger.error(f"[Retrieval Node] Catastrophic failure during vector query: {e}")
        return {"action_log": [f"CRITICAL ERROR on Retrieval: {e}"]}

def route_ticket_workflow(state: SupportAgentState):
    """Router logic acting as a Supervisor mapping conditional execution paths."""
    if state.get("retrieved_article") is not None:
        return "update_existing_article"
    return "draft_new_article"

async def draft_new_article_node(state: SupportAgentState):
    report = state["incident_report"]
    logger.info("[Draft Node] ACTION: Drafting new Knowledge Base article via LLM.")
    
    messages = [
        SystemMessage(content="You are an expert IT Support Engineer. Draft a concise, professional Knowledge Base (KB) article based on the incident report. Format in Markdown. Include 'Symptoms', 'Root Cause', and 'Resolution Steps'."),
        HumanMessage(content=f"Incident: {report.issue_description}\nResolution: {report.resolution_summary}")
    ]
    
    drafted_content = _invoke_llm_safely(messages)
    
    log = [f"Drafted NEW article derived from {report.incident_id} using Gemini LLM."]
    return {"action_log": log, "llm_output": drafted_content}

async def update_existing_article_node(state: SupportAgentState):
    report = state["incident_report"]
    article = state["retrieved_article"]
    
    logger.info(f"[Update Node] ACTION: Updating existing article {article['article_id']} via LLM.")
    
    messages = [
        SystemMessage(content="You are an expert IT Support Engineer. Review the existing KB article title and the new incident report. Propose an updated KB article that incorporates the new resolution. Format in Markdown."),
        HumanMessage(content=f"Existing Article: {article['title']}\nNew Incident: {report.issue_description}\nNew Resolution: {report.resolution_summary}")
    ]
    
    updated_content = _invoke_llm_safely(messages)
    
    log = [f"Updated EXISTING article {article['article_id']} based on {report.incident_id} using Gemini LLM."]
    return {"action_log": log, "llm_output": updated_content}
