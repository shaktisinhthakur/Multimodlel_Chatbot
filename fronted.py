# Ui Setup with streamlit model provider , model, system prompt
import streamlit as st

st.set_page_config(page_title="LangGraph Agent ui", layout="centered")
st.title("AI Chatbot Agentic")
st.write("Create and interact with the Ai Agentic")

system_prompt = st.text_area("Define your AI agentic :",height = 70, placeholder = "Type your system prompt here")

MODEL_NAMES_GROOQ = ["llama-3.1-8b-instant", "mixtral-8x7b-32768", "llama-3.3-70b-versatile"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:",("Groq","OpenAI"))

if provider == "Groq":
    Select_model = st.selectbox("Select goroq model:",MODEL_NAMES_GROOQ)
elif provider == "OpenAI":
    Select_model = st.selectbox("Select Openai Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query =  st.text_area("Enter your query :",height = 150, placeholder = "Ask anything")

API_URl = "http://127.0.0.1:8000/chat"
if st.button("Ask Agentic"):
    if user_query.strip(): 
        import requests 
        payload={
            "model_name": Select_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages" : [user_query],
            "allow_search": allow_web_search   
        }
        try:
            response = requests.post(API_URl, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("status") == "error":
                    st.error(response_data.get("error", "An error occurred in the agent."))
                else:
                    st.subheader("Agent Response")
                    st.markdown(f"**Final Response:**\n\n{response_data.get('response', '')}")
            else:
                st.error(f"Backend Server Error: Status Code {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the backend server. Please make sure that 'backed.py' is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
           
            
        
        


 
