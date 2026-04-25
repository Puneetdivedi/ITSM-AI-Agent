import logging
from src.schemas import SupportAgentState
from src.services import retrieve_knowledge_base_article

logger = logging.getLogger(__name__)

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
    logger.info("[Draft Node] ACTION: Drafting new Knowledge Base article.")
    
    log = [f"Drafted NEW article derived from {report.incident_id}."]
    return {"action_log": log}

async def update_existing_article_node(state: SupportAgentState):
    report = state["incident_report"]
    article = state["retrieved_article"]
    
    logger.info("[Update Node] ACTION: Flagging existing article for revision.")
    log = [f"Flagged EXISTING article {article['article_id']} for revision based on {report.incident_id}."]
    return {"action_log": log}
