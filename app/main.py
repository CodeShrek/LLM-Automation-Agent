from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.llm_service import llm_client
from app.dispatcher import dispatch_task
import logging

# Configure logging to see errors in terminal
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="DataWorks Automation Agent",
    version="2.1",
    description="An intelligent agent for automated data processing operations."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TaskRequest(BaseModel):
    task: str

@app.get("/")
async def read_root():
    return {"status": "running", "message": "DataWorks Automation Agent is active."}

@app.post("/run")
async def run_task(request: TaskRequest):
    try:
        # 1. Parse Intent (LLM)
        intent = await llm_client.parse_task_intent(request.task)
        logging.info(f"Parsed Intent: {intent}")
        
        # 2. Execute Task (Code)
        result_message = await dispatch_task(intent['tool'], intent['args'])
        
        return {"status": "success", "message": result_message}
        
    except ValueError as ve:
        # These are expected errors (e.g. LLM failure)
        logging.error(f"Validation Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # These are unexpected crashes (e.g. code bugs, missing tools)
        logging.error(f"Internal Error: {e}") 
        import traceback
        traceback.print_exc() # Print full crash report to terminal
        # RETURN THE ACTUAL ERROR MESSAGE TO POSTMAN
        raise HTTPException(status_code=500, detail=f"Execution Error: {str(e)}")

@app.get("/read")
async def read_file(path: str):
    from app.utils import secure_path
    try:
        file_path = secure_path(path)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        return file_path.read_text()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)