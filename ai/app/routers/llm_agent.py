"""
LLM Agent router
Decision support using LLM with RAG
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import httpx

router = APIRouter()

class LLMRequest(BaseModel):
    query: str
    context: Optional[Dict] = None
    equipment_id: Optional[str] = None

class LLMResponse(BaseModel):
    response: str
    actions: List[Dict]
    confidence: float

@router.post("/llm-agent", response_model=LLMResponse)
async def query_llm(request: LLMRequest):
    """
    Query LLM agent for decision support
    Uses local Ollama or Groq API
    """
    try:
        # Build context
        context_str = build_context(request.context, request.equipment_id)
        
        # Try local Ollama first
        try:
            response = await query_ollama(request.query, context_str)
        except:
            # Fallback to Groq if Ollama fails
            response = await query_groq(request.query, context_str)
        
        # Parse response
        parsed = parse_llm_response(response)
        
        return LLMResponse(**parsed)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def build_context(context: Dict, equipment_id: str) -> str:
    """Build context string for LLM"""
    if not context:
        return ""
    
    ctx_parts = []
    
    if equipment_id:
        ctx_parts.append(f"Equipment: {equipment_id}")
    
    if "anomaly_score" in context:
        ctx_parts.append(f"Anomaly Score: {context['anomaly_score']}")
    
    if "sensor_values" in context:
        for sensor, value in context["sensor_values"].items():
            ctx_parts.append(f"{sensor}: {value}")
    
    if "severity" in context:
        ctx_parts.append(f"Severity: {context['severity']}")
    
    return "\n".join(ctx_parts)

async def query_ollama(query: str, context: str) -> str:
    """Query local Ollama instance"""
    from app.config import settings
    
    prompt = f"""You are an expert maintenance engineer for a stainless steel plant.

Context:
{context}

User Query: {query}

Provide a helpful response in Indonesian language."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": settings.LLM_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "")
        else:
            raise Exception("Ollama query failed")

async def query_groq(query: str, context: str) -> str:
    """Query Groq API as fallback"""
    from app.config import settings
    
    if not settings.GROQ_API_KEY:
        raise Exception("Groq API key not configured")
    
    prompt = f"""You are an expert maintenance engineer for a stainless steel plant.

Context:
{context}

User Query: {query}

Provide a helpful response in Indonesian language."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": settings.GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=30.0
        )
        
        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            raise Exception("Groq query failed")

def parse_llm_response(response: str) -> Dict:
    """Parse LLM response into structured format"""
    # Simple parsing - in production, use structured output
    return {
        "response": response,
        "actions": [
            {
                "type": "log_observation",
                "description": "AI analysis recorded"
            }
        ],
        "confidence": 0.85
    }
