import streamlit as st
from streamlit_option_menu import option_menu
import os
from gemini_utlities import (load_gemini_ai_model, load_gemini_vision_model,embedding_model,ask_gemini_model)
from PIL import Image

# Set working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Configure Streamlit page
st.set_page_config(
    page_title="AI BRAIN",
    page_icon="🧠",
    layout="centered"
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="AI BRAIN",
        options=["CHATBOT", "IMAGE BOT", "EMBED TEXT", "ASK ANYTHING"],
        menu_icon='robot',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0
    )
def translate_role_for_streamlit(user_role):
    if user_role =="model":
        return "assitant"
    else:
        return user_role
# Chatbot section
if selected == "CHATBOT":
    model = load_gemini_ai_model()
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    st.title("🤖 ChatBot")
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    user_prompt = st.chat_input("Ask your question")
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        output = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(output.text)

# Image Captioning section
elif selected == "IMAGE BOT":
    st.title("📸 Ask About the Image")

    if "upload_image" not in st.session_state:
        st.session_state.upload_image = None

    if "prompt" not in st.session_state:
        st.session_state.prompt = ""

    upload_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if upload_image is not None:
        st.session_state.upload_image = upload_image

    prompt = st.text_input("Enter Your Prompt", st.session_state.prompt)
    if prompt:
        st.session_state.prompt = prompt

    if st.button("Generate Caption"):
        if st.session_state.upload_image is not None:
            image = Image.open(st.session_state.upload_image)
            col1, col2 = st.columns(2)

            with col1:
                resized_image = image.resize((800, 500))
                st.image(resized_image)

            # Call the model with the prompt and image
            result = load_gemini_vision_model(st.session_state.prompt, image)

            with col2:
                st.info(result)
        else:
            st.error("Please upload an image.")
if selected == "EMBED TEXT":
    st.title("🔠 Embeded Text")
    input_text = st.text_area(label=" ", placeholder="Enter the command")
    if st.button("Get Embeding"):
        response = embedding_model(input_text)
        st.markdown(response)
if selected == "ASK ANYTHING":
    st.title("❔ ASK ANYTHING")
    prompt = st.text_area(label="",placeholder="Ask Your Question")
    if st.button("Generate"):
        response =ask_gemini_model(prompt)

        st.markdown(response.parts[0].text)