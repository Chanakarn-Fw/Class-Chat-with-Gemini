import streamlit as st
import google.generativeai as genai

try:
    key = st.secrets['gemini_api_key']
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state: #work like cookies
        st.session_state.chat = model.start_chat(history=[])
    st.title('Gemini Pro Test')

    def role_to_streamlit(role: str) -> str: # we have 2 role model and user
        if role == 'model':
            return 'assistant'
        else:
            return role

    for message in st.session_state.chat.history: #if there is history in chat -> show the chat)
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("What you want to know?"): #prompt the question
        st.chat_message('user').markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(response.text)

except Exception as e: #if there is an error show the error (exception = error)
    st.error(f'An error occurred {e}')
