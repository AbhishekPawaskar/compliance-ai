from src.connector.openai_connector import OpenAIConnection

# Instructions to assistant to prvent going out of context. Internal Guardrail.
internal_instructions="for given content, find compliance issues as per rules in initial instructions during setup only, you may help the user in explaining compliance issues using initial rules mentioned in instruction as reference"

assistant = OpenAIConnection()

#creates a thread, this helps hold context for a conversation of a user
async def create_new_thread_for_user(user_id:str):
    thread = assistant.client.beta.threads.create()
    return thread.id

#helps to check if the status of the run is completed so that i can retrive the response 
async def run_status_complete(thread_id:str,run_id:str):
    status = 'completed'
    current_status = 'queued'
    while(status!=current_status):
        current_status = assistant.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id).status
    return True

#used to converse with the assistant    
async def converse_conversation(thread_id:str,assistant_id:str, text:str):
    message = assistant.client.beta.threads.messages.create(thread_id=thread_id,
                                                  role="user",
                                                  content=text)
    run = assistant.client.beta.threads.runs.create(thread_id=thread_id,
                                          assistant_id=assistant_id,
                                          instructions=internal_instructions)
    status = await run_status_complete(thread_id=thread_id,run_id=run.id)
    message_data= assistant.client.beta.threads.messages.list(thread_id=thread_id).data[0]
    if message_data.role == 'assistant' and message_data.content[0].text.value!= ' ':
        return message_data.content[0].text.value
    else:
        return ' '
    