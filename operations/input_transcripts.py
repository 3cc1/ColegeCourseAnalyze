import pandas as pd
import re
import pdfplumber


def load_pdf_data(pdf_file):
    text = ""

    # -----------------------------
    # 1. READ PDF TEXT
    # -----------------------------
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # Split into student blocks
    students = text.split("Student ")

    rows = []

    # -----------------------------
    # 2. PARSE EACH STUDENT BLOCK
    # -----------------------------
    for block in students:
        if not block.strip():
            continue

        try:
            # Name + Year
            name_match = re.search(r"\d+:\s(.+?) — CS Major,\s(.+)", block)

            # Progress %
            progress_match = re.search(r"Progress:\s*(\d+)%", block)

            # -----------------------------
            # COMPLETED COURSES
            # -----------------------------
            completed_match = re.search(
                r"Completed:\s*(.*?)In Progress:",
                block,
                re.DOTALL
            )

            # -----------------------------
            # IN PROGRESS COURSES
            # -----------------------------
            in_progress_match = re.search(
                r"In Progress:\s*(.*?)Remaining:",
                block,
                re.DOTALL
            )

            # -----------------------------
            # REMAINING COURSES
            # -----------------------------
            remaining_match = re.search(
                r"Remaining:\s*(.*)",
                block,
                re.DOTALL
            )

            # -----------------------------
            # CLEAN DATA
            # -----------------------------
            name = name_match.group(1).strip()
            year = name_match.group(2).strip()
            progress = int(progress_match.group(1))

            def clean_courses(match):
                if not match:
                    return []
                raw = match.group(1).replace("\n", " ")
                return [c.strip() for c in raw.split(",") if c.strip()]

            completed = clean_courses(completed_match)
            in_progress = clean_courses(in_progress_match)
            remaining = clean_courses(remaining_match)

            # -----------------------------
            # STORE ROW
            # -----------------------------
            rows.append({
                "Name": name,
                "Year": year,
                "Progress": progress,
                "Completed": completed,
                "In Progress": in_progress,
                "Remaining": remaining
            })

        except Exception as e:
            print("Error parsing block:", e)
            continue

    return pd.DataFrame(rows)


# -----------------------------
# 3. LOAD PDF (CHANGE PATH HERE)
# -----------------------------
pdf_path = r"C:\Users\Kostiantyn\Desktop\course_analyze\database\pdf_file.pdf"
df = load_pdf_data(pdf_path)

# -----------------------------
# 4. PRINT RESULTS
# -----------------------------
print("\n=== FULL DATAFRAME ===\n")
print(df.to_string(index=False))

# Optional: nicer structured preview
print("\n=== SIMPLE VIEW ===\n")
for _, row in df.iterrows():
    print(f"\nStudent: {row['Name']} ({row['Year']})")
    print(f"Progress: {row['Progress']}%")
    print(f"Completed ({len(row['Completed'])}): {row['Completed']}")
    print(f"In Progress ({len(row['In Progress'])}): {row['In Progress']}")
    print(f"Remaining ({len(row['Remaining'])}): {row['Remaining']}")


search_name = input("\nEnter student name to search: ").strip().lower()

# Find matching student(s)
filtered_df = df[df["Name"].str.lower().str.contains(search_name)]

# -----------------------------
# OUTPUT
# -----------------------------
if filtered_df.empty:
    print("\nNo student found.")
else:
    for _, row in filtered_df.iterrows():
        print(f"\nStudent: {row['Name']} ({row['Year']})")
        print(f"Progress: {row['Progress']}%")
        print(f"Completed ({len(row['Completed'])}): {row['Completed']}")
        print(f"In Progress ({len(row['In Progress'])}): {row['In Progress']}")
        print(f"Remaining ({len(row['Remaining'])}): {row['Remaining']}")