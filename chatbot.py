from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.agents import AgentExecutor
from llm_factory import get_llm
from history import get_message_history
from tools import tools
from dotenv import load_dotenv



load_dotenv()

def build_agent(llm, tools):
    prompt = hub.pull("abdelmegeed/project-egx-chatbot")
    print(f"Prompt: {prompt}")
    return create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)


def chatbot(session_id: str, user_input: str, llm: str):
    """Handles chatbot interaction using chosen LLM and MongoDB for chat history."""

    # --- Setup ---
    llm_instance = get_llm(llm)
    message_history = get_message_history(session_id)
    chat_agent = build_agent(llm=llm_instance, tools=tools)

    # --- Executor ---
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=chat_agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    # --- Run ---
    response = agent_executor.invoke({
        "input": user_input,
        "chat_history": message_history.messages
    })

    print(f"Response: {response}")

    # --- Update history ---
    message_history.add_user_message(user_input)
    output = response["output"]
    if isinstance(output, dict) and "text" in output:
        message_history.add_ai_message(output["text"])
        return output["text"]
    else:
        message_history.add_ai_message(str(output))
        return output

# print(chatbot('825417', "What is EFIH's stock price?", 'Groq'))