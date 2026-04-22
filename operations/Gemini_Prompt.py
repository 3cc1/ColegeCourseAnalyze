import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
from input_transcripts import load_pdf_text, find_student
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.5-flash')


pdf_path = r"C:\Users\Kostiantyn\Desktop\course_analyze\database\pdf_file.pdf"

student_name = input("Enter Student Name: ").strip()

student_data = find_student(pdf_path, student_name)
pdf_text = load_pdf_text(pdf_path)

if student_data:



    question = "Which courses does this student need to graduate and what schedule fits them best?"
    prompt_final = f"""
    You are an academic advisor.

    Here is the student's transcript:

    {student_data}

    Student's question: {question}

    Give:
    1.Missing Courses
    2.Suggested next semester schedule
    3.Graduation estimate
    4.Helpful academic advice 
    """
    response = model.generate_content(prompt_final)

    print("\n--- GEMINI RESPONSE ---\n")
    print(response.text)

else:
    print("Student not found.")