from pydantic import BaseModel

class InitiateRequest(BaseModel):
   userid:str
   url:str
   
class ConverseRequest(BaseModel):
   text: str
   thread_id:str

class InitiateResponse(BaseModel):
   message:str
   thread_id:str

class ConverseResponse(BaseModel):
   original_text:str
   response: str

class EndpointErrorResponse(BaseModel):
   error_message:str
   error_stack:str