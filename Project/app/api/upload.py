from fastapi import APIRouter, UploadFile, File

router = APIRouter()

#ensure the service is alive and reachable
@router.post("/upload", tags=["upload"])

async def uploadFile(file: UploadFile = File(...)):
    contents = await file.read()

    #just logging for now to ensure file was successful received 
    print(f"Received file: {file.filename}")

    # TODO: actual processing of the file here
    return {"filename": file.filename, "size": len(contents)}
    