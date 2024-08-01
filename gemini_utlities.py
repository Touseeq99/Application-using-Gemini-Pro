import os
import json
import google.generativeai as genai
from PIL import Image
working_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = f'{working_directory}/config.json'
config_data = json.load(open(config_file_path))
Google_API_key = config_data["Google_API_key"]
genai.configure(api_key=Google_API_key)

def load_gemini_ai_model():
    gemini_ai_model = genai.GenerativeModel("gemini-pro")
    return gemini_ai_model

def load_gemini_vision_model(prompt, image):
    gemini_vision_model = genai.GenerativeModel("gemini-1.5-flash")
    # Ensure the method call matches the signature of `generate_content`
    response = gemini_vision_model.generate_content([prompt, image])
    result = response.text
    return result


def embedding_model(input_text):
    embedding_model = "models/embedding-001"
    embedding = genai.embed_content(model=embedding_model,content=input_text,task_type="retrieval_document")
    embeding_list = embedding["embedding"]
    return embeding_list
def ask_gemini_model(input_text):
    gemini_ai_model = genai.GenerativeModel("gemini-pro")
    response  = gemini_ai_model.generate_content(input_text)
    return response