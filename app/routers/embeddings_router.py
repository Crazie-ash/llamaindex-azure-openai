from fastapi import APIRouter, HTTPException
from app.controllers.embeddings_controller import create_embeddings
from app.models.embeddings import EmbeddingsResponse

router = APIRouter()

@router.get("/embeddings", response_model=EmbeddingsResponse)
def create_embeddings_endpoint():
    try:
        result = create_embeddings()
        return result
    except HTTPException as e:
        raise e
    
