from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import shutil
import os
import uuid

# Existing modules
from origin.procure_ai.tasks import process_requirement_task
from origin.procure_ai.llm import extract_requirements
from origin.procure_ai.vendor_pipeline import process_vendor_file
from origin.procure_ai.full_pipeline import (
    start_process,
    upload_vendor,
    finalize,
    run_full_rag_pipeline
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://origin-frontend-one.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
    requirement: str


@app.get("/")
def home():
    return {"message": "ProcureAI Backend Running 🚀"}


# ---------------------------------------------------
# REQUIREMENT PROCESSING (CELERY)
# ---------------------------------------------------
@app.post("/process")
def process_input(data: UserInput):
    task = process_requirement_task.delay(data.requirement)
    return {"status": "processing", "task_id": task.id}


@app.get("/result/{task_id}")
def get_result(task_id: str):
    from celery_worker import celery_app
    result = celery_app.AsyncResult(task_id)

    if result.state == "PENDING":
        return {"status": "processing"}

    if result.state == "FAILURE":
        return {"status": "failed", "error": str(result.result)}

    if result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}

    return {"status": result.state}


# ---------------------------------------------------
# TEST LLM EXTRACTION
# ---------------------------------------------------
@app.post("/test-llm")
def test_llm(data: UserInput):
    result = extract_requirements(data.requirement)
    return {"input": data.requirement, "llm_output": result}


# ---------------------------------------------------
# TEST SINGLE VENDOR EXTRACTION
# ---------------------------------------------------
@app.post("/test-vendor")
def test_vendor(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{uuid.uuid4()}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_vendor_file(file_path)
        os.remove(file_path)

        return result

    except Exception as e:
        return {"error": "Vendor processing failed", "details": str(e)}




# ---------------------------------------------------
# 🏆 MULTI VENDOR COMPARISON (FINAL ENDPOINT)
# ---------------------------------------------------
@app.post("/compare-vendors")
async def compare_vendors(files: List[UploadFile] = File(...)):
    try:
        vendor_list = []

        # Extract structured vendor data from files
        for file in files:
            contents = await file.read()
            file_path = f"temp_{uuid.uuid4()}_{file.filename}"

            with open(file_path, "wb") as f:
                f.write(contents)

            result = process_vendor_file(file_path)
            os.remove(file_path)

            data = result.get("structured_data", {})
            if data and "error" not in data:
                vendor_list.append(data)

        if len(vendor_list) == 0:
            return {"error": "No valid vendor data extracted"}

        # 🔥 RUN FULL GROQ RAG PIPELINE
        final_result = run_full_rag_pipeline(vendor_list)

        return {
            "vendors_processed": len(vendor_list),
            "vendors": vendor_list,
            "final_decision": final_result
        }

    except Exception as e:
        return {"error": "Comparison failed", "details": str(e)}


# ---------------------------------------------------
# EXISTING FULL PIPELINE ROUTES (KEEP)
# ---------------------------------------------------
@app.post("/start-process")
def start(data: UserInput):
    return start_process(data.requirement)


@app.post("/upload-vendor")
def upload(files: List[UploadFile] = File(...)):
    results = []
    try:
        for file in files:
            file_path = f"temp_{uuid.uuid4()}_{file.filename}"
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            result = upload_vendor(file_path)
            os.remove(file_path)
            results.append(result)

        return {"vendors_uploaded": len(results), "details": results}

    except Exception as e:
        return {"error": "Upload failed", "details": str(e)}


@app.get("/finalize")
def final():
    return finalize()