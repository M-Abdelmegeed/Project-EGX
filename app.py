from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, AgentExecutor, create_structured_chat_agent
from langchain.memory import MongoDBChatMessageHistory
import os
from dotenv import load_dotenv


load_dotenv()
def chatbot(session_id,user_input):
    gemini_llm = ChatGoogleGenerativeAI(model='gemini-pro', verbose=True, temperature=0)
    gpt_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    uri = os.getenv('MONGODB_CONNECTION_STRING')
    message_history = MongoDBChatMessageHistory(
        connection_string=uri, session_id=session_id, collection_name= "Chats"
    )
    
    prompt = hub.pull("hwchase17/structured-chat-agent")
    print(f"Prompt: {prompt}")

    chat_agent = create_structured_chat_agent(llm=gpt_llm, tools=tools, prompt=prompt)
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
                    "chat_history": message_history
                }
            )
    message_history.add_user_message(user_input)
    message_history.add_ai_message(response.output)
    return response.output

print(chatbot("1222", "Hello my name is Bob"))