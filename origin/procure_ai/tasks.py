from origin.procure_ai.celery_worker import celery_app
from origin.procure_ai.llm import extract_requirements
from origin.procure_ai.rfq_builder import build_rfq


@celery_app.task(bind=True)
def process_requirement_task(self, user_input: str):
    print("TASK RECEIVED:", user_input)

    data = extract_requirements(user_input)
    print("LLM OUTPUT:", data)

    # Handle LLM failure
    if "error" in data:
        return {
            "status": "llm_error",
            "details": data
        }

    # Handle low confidence
    if data.get("confidence", 0) < 0.7:
        return {
            "status": "low_confidence",
            "message": "Low confidence in requirement. Please refine input.",
            "data": data
        }

    # Build RFQ
    rfq = build_rfq(data)

    result = {
        "status": "success",
        "rfq": rfq
    }

    print("FINAL RESULT:", result)

    return result