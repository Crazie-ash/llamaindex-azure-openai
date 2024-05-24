from fastapi import APIRouter, Depends, HTTPException
from app.controllers.embeddings_controller import create_embeddings
from app.models.embeddings import EmbeddingsRequest, EmbeddingsResponse
from app.services.elasticsearch_service import get_elasticSearch

router = APIRouter()

@router.post("/embeddings", response_model=EmbeddingsResponse)
def create_embeddings_endpoint(request: EmbeddingsRequest, es= Depends(get_elasticSearch)):
    try:
        result = create_embeddings(es, request.index_name)
        return result
    except HTTPException as e:
        raise e
    
