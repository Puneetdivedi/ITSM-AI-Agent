import asyncio
import logging

from src.workflow import compile_support_workflow
from src.schemas import IncidentReport

# -------------------------------------------------------------------------
# Application Bootstrap Configuration
# -------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)-8s %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("ITSM_Service")

async def run_pipeline():
    logger.info("Initializing ITSM Support Resolution Workflow...")
    support_agent = compile_support_workflow()

    # The Checkpointer requires a thread configuration dictionary
    config_1 = {"configurable": {"thread_id": "ticket_11044_session"}}

    logger.info("Ingesting Webhook Event: INC-11044")
    incident_1 = IncidentReport(
        incident_id="INC-11044",
        issue_description="I can't connect to the new wifi network, getting authentication error.",
        resolution_summary="Flushed DNS cache and updated network drivers to resolve the issue."
    )
    
    res_1 = await support_agent.ainvoke({
        "incident_report": incident_1, 
        "retrieved_article": None,
        "action_log": []
    }, config=config_1)
    
    # Our graph now safely aggregates data directly into a final status block!
    logger.info(f"==> FINAL AGGREGATED PATH LOGS: {res_1['action_log']}")
    
    print("\n" + "="*80 + "\n")


    config_2 = {"configurable": {"thread_id": "ticket_11045_session"}}

    logger.info("Ingesting Webhook Event: INC-11045")
    incident_2 = IncidentReport(
        incident_id="INC-11045",
        issue_description="VPN client fails to establish a secure tunnel on startup.",
        resolution_summary="Reinstalled VPN client and rotated user certificates to fix the issue."
    )
    
    res_2 = await support_agent.ainvoke({
        "incident_report": incident_2, 
        "retrieved_article": None,
        "action_log": []
    }, config=config_2)

    logger.info(f"==> FINAL AGGREGATED PATH LOGS: {res_2['action_log']}")
    logger.info("Batch processing complete.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())