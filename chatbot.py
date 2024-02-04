from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import MongoDBChatMessageHistory, ConversationSummaryBufferMemory
import os
from dotenv import load_dotenv


load_dotenv()
def chatbot(session_id,user_input,llm):
    """ The LLM parameter is either 'GPT-3.5' or 'Gemini' """
    gemini_llm = ChatGoogleGenerativeAI(model='gemini-pro', verbose=True, temperature=0, convert_system_message_to_human=True)
    gpt_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    uri = os.getenv('MONGODB_CONNECTION_STRING')
    message_history = MongoDBChatMessageHistory(
        connection_string=uri, session_id=session_id, collection_name= "Chats"
    )
    
    
    summarized_memory= ConversationSummaryBufferMemory(
    llm=gemini_llm,
    chat_memory=message_history,
    memory_key='chat_history',
    return_messages=True,
    max_token_limit=50
    )
    print(summarized_memory)
    
    prompt = hub.pull("abdelmegeed/chat_agent")
    print(f"Prompt: {prompt}")

    
    if(llm=="GPT-3.5"): 
        chat_agent = create_structured_chat_agent(llm=gpt_llm, tools=tools, prompt=prompt)  
    elif(llm=="Gemini"):
        chat_agent = create_structured_chat_agent(llm=gemini_llm, tools=tools, prompt=prompt)
        
    agent_executor = AgentExecutor.from_agent_and_tools(
            agent=chat_agent, 
            tools=tools, 
            verbose=True, 
            handle_parsing_errors=True,
            return_intermediate_steps=True,
    )
    
    response = agent_executor.invoke(
                {
                    "input": f"{user_input}",
                    "chat_history": message_history.messages
                }
            )
    # print(f"Response {response}")
    message_history.add_user_message(user_input)
    if 'text' in response["output"]:
        message_history.add_ai_message(response['output']['text'])
        return response['output']['text']
    else:
        message_history.add_ai_message(response['output'])
        return response['output']