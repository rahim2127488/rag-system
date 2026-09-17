from INGESTION.pipeline import process_pdf


pdf_path = input("Enter the PDF path: ")
course_name = input("Enter course name: ")
course_code = input("Enter course code:")
lesson_name = input("Enter lesson name: ")


result = process_pdf(
    pdf_path,
    course_name,
    lesson_name
)

print(f"Stored records: {result}")