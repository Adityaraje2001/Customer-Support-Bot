from fastapi import UploadFile
import uuid
from pathlib import Path
class FileService:
    def __init__(self):
        pass

    #method upload_file to which when triggered should return filename and status as completed

    async def upload_file(self,file:UploadFile):
        try:
            validate_pdf = await self.validate_pdf(file)
            if validate_pdf["status"] == "failed":
                return validate_pdf
            else:
                filename = await self.generate_unique_filename(file.filename)
                save_file = await self.save_file(file,filename)
                if save_file["status"] == "failed":
                    return save_file
                status = "completed"
                return {"filename":filename,"status":status,"file_path":save_file["file_path"]} 
        except Exception as e:
            return {"status":"failed","error":str(e)}   
    
    async def validate_pdf(self,file:UploadFile):
        if file.content_type != "application/pdf":
            return {"status":"failed","error":"Invalid file type. Please upload a PDF file."}
        return {"status":"completed"} 

    async def generate_unique_filename(self, filename: str) -> str:
        stem, ext = filename.rsplit(".", 1)
        return f"{stem}_{uuid.uuid4()}.{ext}"
    
    async def save_file(self,file:UploadFile,filename:str)->str:
        try:
            uploads_dir = Path("storage/uploads")
            uploads_dir.mkdir(parents=True, exist_ok=True)
            upload_path = uploads_dir / filename  # internal path — not exposed in response
            file_content = await file.read()
            upload_path.write_bytes(file_content)
            return {"status":"completed","file_path":str(upload_path)}
        except Exception as e:
            return {"status":"failed","error":str(e)}  