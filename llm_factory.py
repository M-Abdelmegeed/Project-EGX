from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

def get_llm(llm_name: str):
    """Factory function to return an initialized LLM instance."""
    if llm_name == "GPT-3.5":
        return ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")
    elif llm_name == "Gemini":
        return ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", verbose=True, temperature=0)
    elif llm_name == "Groq":
        return ChatGroq(temperature=0, model_name="openai/gpt-oss-120b")
    else:
        raise ValueError(f"Unsupported LLM: {llm_name}")
