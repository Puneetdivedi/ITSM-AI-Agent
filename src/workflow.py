from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.schemas import SupportAgentState
from src.nodes import (
    retrieve_knowledge_node, 
    draft_new_article_node, 
    update_existing_article_node, 
    route_ticket_workflow
)

def compile_support_workflow():
    """Builds and compiles the ITSM support knowledge graph."""
    workflow = StateGraph(SupportAgentState)
    
    # 1. Register Action Nodes
    workflow.add_node("retrieve_knowledge", retrieve_knowledge_node)
    workflow.add_node("draft_new_article", draft_new_article_node)
    workflow.add_node("update_existing_article", update_existing_article_node)

    # 2. Add entry point
    workflow.set_entry_point("retrieve_knowledge")

    # 3. Add conditional router logic
    workflow.add_conditional_edges(
        "retrieve_knowledge",
        route_ticket_workflow,
        {
            "draft_new_article": "draft_new_article",
            "update_existing_article": "update_existing_article"
        }
    )

    # 4. End paths
    workflow.add_edge("draft_new_article", END)
    workflow.add_edge("update_existing_article", END)
    
    # 5. Adding industry-level state persistence checkpoints 
    # (Allows the execution to be paused for Human-in-The-Loop review or resumed on failure)
    memory = MemorySaver()
    
    return workflow.compile(checkpointer=memory)
