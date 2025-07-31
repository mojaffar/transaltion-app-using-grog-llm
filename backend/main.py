import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from langserve import add_routes
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="LangServe Translation API",
    version="1.0",
    description="Translate text using llama-3.3-70b-versatile via Groq + LangServe"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define LLM + prompt + chain
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the following text to {language}:"),
    ("user", "{text}")
])

chain = prompt | llm | StrOutputParser()

# Add LangServe routes with explicit path
add_routes(
    app,
    chain,
    path="/api/translate",
    enabled_endpoints=["invoke"],
)

# Debug endpoint to verify routing
@app.post("/api/translate/invoke")
async def debug_translate(request: Request):
    body = await request.json()
    return JSONResponse({"message": "Debug endpoint working", "received": body})

# Serve frontend - ensure this comes after API routes
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)