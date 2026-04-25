import operator
from typing import TypedDict, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field

# Pydantic validates API/Webhook payloads
class IncidentReport(BaseModel):
    # Added strict production limiters for data cleanliness
    incident_id: str = Field(..., description="Unique identifier for the support ticket", min_length=3)
    issue_description: str = Field(..., description="Original user reported problem", min_length=10)
    resolution_summary: str = Field(..., description="Description of the action taken to resolve the issue", min_length=5)

# Standard typing for the Graph's internal memory
class SupportAgentState(TypedDict):
    incident_report: IncidentReport
    retrieved_article: Optional[Dict[str, Any]]
    
    # State Reducers: Annotated[list, operator.add] tells LangGraph 
    # to APPPEND to this list gracefully instead of resetting it per node!
    action_log: Annotated[list[str], operator.add]
    
    # Store the actual generated text from our LLM Agent
    llm_output: Optional[str]
