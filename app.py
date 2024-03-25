from dotenv import load_dotenv

load_dotenv() ##it will load all the environment variables from .env

import streamlit as st
import os 

from PIL import Image

import google.generativeai as genai

genai.configure (api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(upload_file):
    if upload_file is not None:  # Corrected variable name here
        byte_data = upload_file.getvalue()

        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": byte_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

##streamlit app interfce basically 

st.title("Multi-language invoice extrator")
st.header("Gemini application")
input=st.text_input("Input prompt :",key="input")

upload_file =st.file_uploader("choose an image of thr invoice.....",type=["jpg","jpeg","png"])
if upload_file is not None:
    image=Image.open(upload_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit= st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices.We will uplaod image of invoices 
and you have to answer any questions asked related to the uploaded invoice. 
"""
##if  submit button is clicked -->
if submit :
    image_data=input_image_details(upload_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is ")
    st.write(response)