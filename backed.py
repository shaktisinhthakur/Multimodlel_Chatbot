#Phase 2 

#step 1: Setup pydantic model (Schema Validation)
from pydantic import BaseModel
from typing import List
from ai_agent_new import get_response_from_ai_agent

class RequestState(BaseModel):
    model_name:str
    model_provider:str
    system_prompt: str
    messages : list[str]
    allow_search:bool

ALLOWED_MODEL_NAMES=["llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

#step 2: setup Ai agent from Frontend Request
from fastapi import FastAPI
app = FastAPI(title="langraph AI Agent")
@app.post("/chat")
def cha_endpoint(request : RequestState): 
    """APi Endpoint to interact with the chatbot using langchain and search tools.
    It dynamically selects the model specified in the request.
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"status": "error", "error": f"Model name '{request.model_name}' is not allowed."}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    try:
        # Create Ai Agent and get response from it
        response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "error": str(e)}

#step 3 : Run app & explore swagger ui docs 
if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1",port= 8000)
