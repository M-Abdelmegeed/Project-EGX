from langchain_google_genai import ChatGoogleGenerativeAI
from tools import tools
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatVertexAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
import google.generativeai as genai
from langchain.agents import AgentType, initialize_agent, AgentExecutor, create_structured_chat_agent
from pymongo.mongo_client import MongoClient
from langchain.memory import MongoDBChatMessageHistory
import os
from dotenv import load_dotenv


load_dotenv()
def chatbot(session_id,user_input):
    gemini_llm = ChatGoogleGenerativeAI(model='gemini-pro', verbose=True, temperature=0)
    gpt_llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    uri = os.getenv('MONGODB_CONNECTION_STRING')
    client = MongoClient(uri)
    message_history = MongoDBChatMessageHistory(
        connection_string=uri, session_id=session_id, collection_name= "Chats"
    )

    # tool_names = ["google_search","stock_price","lower_case"]

    # SYSTEM_PROMPT_TEMPLATE="You are a helpful assistant, use the chat history, given tools, and your\
    #                 knowledge, to answer the user's query. You have access to the following tools: {tools},\
    #                 and these are the tool names: {tool_names}"
    # HUMAN_PROMPT_TEMPLATE="{input}"

    # prompt = ChatPromptTemplate.from_messages([
    #     SystemMessagePromptTemplate.from_template(
    #         input_variables=['tool_names', 'tools'],
    #         template=SYSTEM_PROMPT_TEMPLATE
    #     ),
    #     MessagesPlaceholder(variable_name='chat_history', optional=True),
    #     MessagesPlaceholder("agent_scratchpad"),
    #     HumanMessagePromptTemplate.from_template(
    #         input_variables=["input", "chat_history", "agent_scratchpad"],
    #         template=HUMAN_PROMPT_TEMPLATE
    #     )
    # ])
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


    # agent = initialize_agent(tools,
    #                         gemini_llm,
    #                         verbose=True)



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