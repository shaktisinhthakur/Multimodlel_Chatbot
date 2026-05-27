import os
from dotenv import load_dotenv
load_dotenv()

# step 2 : Setup  LLM & Tools

from langchain_groq import ChatGroq
from langchain_community.tools import TavilySearchResults
from groq import Groq



# Step 3 : Setup AI Agent wiht Search tool Fucntionality 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# ✅ Auto model detection

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY") # here we define our key so the Chagroq  or Openai can direct access it 

# Search Tool 

#response = client.invoke("Explain the importance of fast language models")
#print(response.content)

# Step 3 : Setup AI Agent wiht Search tool Fucntionality 
from langgraph.checkpoint.memory import MemorySaver
def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    provider_lower = provider.lower()
    if provider_lower == "groq":
        llm = ChatGroq(model=llm_id,
                       api_key=GROQ_API_KEY)                        
    elif provider_lower == "openai":
        llm = ChatOpenAI(model=llm_id,
                         api_key=OPENAI_API_KEY)
    else:
        raise ValueError(f"Unsupported model provider: {provider}")

    tools = [TavilySearchResults(
        max_results=2,
        tavily_api_key=TAVILY_API_KEY
    )] if allow_search else []

    memory = MemorySaver()
    # In LangGraph 1.x, we configure the system prompt using prompt=system_prompt as a keyword argument.
    agent_executor = create_react_agent(llm, tools, prompt=system_prompt, checkpointer=memory)

    # Extract the query string from the query (which might be passed as a list of strings)
    query_str = query[-1] if isinstance(query, list) else query

    state = {
        "messages": [
            HumanMessage(content=query_str)
        ]
    }
    
    # Configure the thread_id for MemorySaver checkpointing
    config = {"configurable": {"thread_id": "default_thread"}}
    response = agent_executor.invoke(state, config=config) #invoke method go and search and predict
    messages = response.get("messages")
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    return (ai_messages[-1])# -1 because we want last object 
 









