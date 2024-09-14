import os
from PyPDF2 import PdfReader, PdfWriter

def compress_pdf(input_path):
    output_path = input_path.replace('.pdf', ' - compressed.pdf')
    
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)

    for page in writer.pages:
        page.compress_content_streams()  # This is CPU intensive!

    # Use 256-bit encryption (security handler of revision 5)
    writer.encrypt(user_password='', owner_password=None, 
                   use_128bit=False, allow_printing=True,
                   allow_commenting=True, allow_modifying=True,
                   allow_copying=True, allow_form_filling=True)

    with open(output_path, 'wb') as out_file:
        writer.write(out_file)

    print(f"Compressed PDF saved as {output_path}")

input_file = input("PDF to compress (full path): ")
compress_pdf(input_file)