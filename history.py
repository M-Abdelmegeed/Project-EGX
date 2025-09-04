import os
from langchain_mongodb import MongoDBChatMessageHistory

def get_message_history(session_id: str, collection_name: str = "Chats"):
    uri = os.getenv("MONGODB_CONNECTION_STRING")
    return MongoDBChatMessageHistory(
        connection_string=uri,
        session_id=session_id,
        collection_name=collection_name
    )
