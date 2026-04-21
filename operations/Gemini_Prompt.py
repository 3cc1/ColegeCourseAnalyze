import os
from dotenv import load_dotenv
import google.generativeai as genai




load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('models/gemini-2.5-flash')

question = "Which courses does this students need to graduate?"
prompt_final = f"{pdf_file}"\n\nStudent's Question: {question}"

response = model.generate_content(prompt_final)
print(response.text)