import streamlit as st
import openai
#from dotenv import load_dotenv
import os
#load_dotenv()

# Set your OpenAI key
#openai.api_key = 'your-api-key'
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]

client = openai.AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version="2023-07-01-preview")

# Streamlit UI
st.title('Azure OpenAI Chatbot')

# Chat history
chat_history = []


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        initial_assistant_message = {"role": "assistant", "content": "Hello, I am your AI assistant. How can I help you today?"}
        messages_for_openai = [initial_assistant_message] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        for response in client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})




