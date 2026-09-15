from INGESTION.pipeline import process_pdf


pdf_path = input("Enter your PDF path: ")
course_name = input("Enter your course name: ")
lesson_name = input("Enter your lesson name: ")


result = process_pdf(
    pdf_path,
    course_name,
    lesson_name
)

print(f"Stored records: {result}")