from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from ..services.rag_service import RAGService
from ..dependencies import get_rag_service 
from ..schemas.upload import URLRequest

import requests
import os, uuid
BIN_DIR = "bin"

# Ensure folder exists
os.makedirs(BIN_DIR, exist_ok=True)

def determineSuffix(file: UploadFile):
    if file.filename.endswith(".pdf"):
        return ".pdf"
    elif file.filename.endswith(".docx"):
        return ".docx"
    else:
        return ""



router = APIRouter()

#uploading a docx or pdf file
@router.post("/uploadFile", tags=["uploadFile"])
async def uploadFile(file: UploadFile = File(...), rag_service: RAGService = Depends(get_rag_service)):
    contents = await file.read()
    suffix = determineSuffix(file)
    if not suffix: return {"error": "Unsupported file type"}
    
    safe_filename = os.path.basename(file.filename)
    file_path = os.path.join(BIN_DIR, safe_filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        #handles text extraction, chunking, embedding and vector db storage 
        rag_service.upload(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    #finally:
        # Delete after processing
        #os.remove(file_path)
    
    return {"filename": file.filename, "size": len(contents)}


@router.post("/uploadUrl", tags=["uploadUrl"])
async def uploadUrl(request: URLRequest, rag_service: RAGService = Depends(get_rag_service)):
    try:
        url = request.url

        #handles text extraction, chunking, embedding and vector db storage  
        rag_service.upload(url)
        
        return {
            "url": request.url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
