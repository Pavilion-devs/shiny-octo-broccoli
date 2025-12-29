import sys
from pathlib import Path
print("=" *60)
print("Starting API Server")
print("=" * 60)
project_root=Path(__file__).parent.parent
sys.path.insert(0,str(project_root))
print(f"Project root set to : {project_root}")
print("Importing FASTAPI")
from fastapi import FastAPI,HTTPException
print("FASTAPI IMPORTED")
print("Importing UVICORN")
import uvicorn
print("UVICORN IMPORTED")
print("Loadiing environmental variables")
from dotenv import load_dotenv
load_dotenv()
print("Environment variables loaded")
print("Importing CRAG AGENT(this may take a while)")


from app.agent import app as crag_agent
print("Imported CRAG AGENT")
print("Importing schemas")
from backend.schemas import QueryRequest,QueryResponse
print("Schemas imported")

api=FastAPI(
    title="Mobolaji's CRAG API",
    description="Corrective RAG with loacl PDFs + Brave Search fallback",
    version="1.0"
)
print("FastAPI APP configured!")
@api.post("/ask",response_model=QueryResponse)
async def ask_crag(request:QueryRequest):
    try:
        result=crag_agent.invoke({"question":request.question})
        return QueryResponse(
            answer=result.get("answer","No answer generated"),
            sources=result.get("citations",[])

        )
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))
    
@api.get("/")
def root():
    return {"message":"Mobolaji's CRAG API is live. POST to /ask with {'question':'your question'}"}

if __name__=="__main__":
    uvicorn.run("api:api",host="0.0.0.0",port=8000,reload=False)
    