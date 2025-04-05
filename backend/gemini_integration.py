import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-001')

def generate_gemini_response_with_pdfs(system_prompt, pdf_files):
    contents = [system_prompt]
    for pdf_file in pdf_files:
        contents.append({"mime_type": "application/pdf", "data": pdf_file.stream.read()})

    try:
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        return f"Error generating response from Gemini: {e}"

def generate_gemini_response(prompt, history=None):
    prompt_parts = []
    if history:
        for item in history:
            if item['role'] == 'user':
                prompt_parts.append({"text": f"User: {item['content']}"})
            elif item['role'] == 'model':
                prompt_parts.append({"text": f"Assistant: {item['content']}"})
    prompt_parts.append({"text": f"User: {prompt}"})

    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"Error generating response from Gemini: {e}"

if __name__ == '__main__':
    system_prompt_from_file = __import__('system_prompt').SYSTEM_PROMPT
    try:
        with open("dummy1.pdf", "rb") as f1, open("dummy2.pdf", "rb") as f2:
            pdf_files_to_process = [f1, f2]
            response = generate_gemini_response_with_pdfs(system_prompt_from_file, pdf_files_to_process)
            print("Initial Response (Gemini 1.5 Flash):\n", response)
    except FileNotFoundError:
        print("Please create dummy1.pdf and dummy2.pdf files in the backend directory for testing.")
