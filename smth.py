import re
import json
import PyPDF2

import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)  # Use PdfReader instead of PdfFileReader
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def parse_book_structure(text):
    # Example regex to find chapters and sections
    chapters = re.split(r'(Глава\s\d+)', text)
    book_structure = []

    for i in range(1, len(chapters), 2):
        chapter_title = chapters[i].strip()
        chapter_content = chapters[i+1].strip()

        # Split sections inside the chapter
        sections = re.split(r'(\d+\.\d+)', chapter_content)
        section_list = []

        for j in range(1, len(sections), 2):
            section_title = sections[j].strip()
            section_content = sections[j+1].strip()
            section_list.append({
                "section_title": section_title,
                "text": section_content
            })
        
        book_structure.append({
            "chapter_title": chapter_title,
            "sections": section_list
        })
    
    return book_structure

def save_structure_to_json(book_structure, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(book_structure, f, indent=4, ensure_ascii=False)

# Example usage

pdf_path = r'C:\Users\User\Desktop\web-bot\Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf'
text = extract_text_from_pdf(pdf_path)
book_structure = parse_book_structure(text)
save_structure_to_json(book_structure, 'structure.json')
