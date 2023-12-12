import os
from src.datamodels.chat_model import (
   InitiateRequest,
   ConverseRequest,
   InitiateResponse,
   ConverseResponse,
   EndpointErrorResponse
)
from src.endpoints.assistant_logic import (
   create_new_thread_for_user,
   converse_conversation
   )
from src.endpoints.content_extractor import get_website_content

assistant_id = os.environ.get('ASSISTANT_ID')

# this is only for initiate endpoint as it helps set context that following is the web content
message_prefix = "following is the content that you need to review if its compliant or not. \n\n\n\n Content:\n "
#for any failure
error_message = "Something went wrong in the API"

async def initiate(request_body: InitiateRequest):
   """
   This endpoint is to be used when you need to submit a URL for 
   compliance check to the assistant. this will yeild primary 
   response and a thread_id. to communicate with the assistant to 
   elaborate or discuss in detail with the assistant, use the converse 
   endpoint to communicate and provide the same thread_id to maintain context.
   """

   try:
      thread_id = await create_new_thread_for_user(user_id=request_body.userid)
      website_content = get_website_content(url=request_body.url)
      complete_message = message_prefix+website_content
      message = await converse_conversation(thread_id=thread_id, 
                                          assistant_id=assistant_id,
                                          text=complete_message)
      return InitiateResponse(message=message, 
                              thread_id=thread_id)
   except Exception as e:
      return EndpointErrorResponse(error_message=error_message,
                                    error_stack=e)

async def converse(request_body: ConverseRequest):
   """
   to be used only when a conversation has began with the 
   assistant and need to discuss in detail with the assistant.
   Use thread_id to maintain context.
   """
   try:
      message =  await converse_conversation(thread_id=request_body.thread_id, 
                                             assistant_id=assistant_id, 
                                             text= request_body.text)
      return ConverseResponse(original_text=request_body.text,
                              response=message)
   except Exception as e:
      return EndpointErrorResponse(error_message=error_message, 
                                    error_stack=e)


   