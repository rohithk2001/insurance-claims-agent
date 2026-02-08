import pdfplumber
import os


def extract_text_from_pdf(pdf_path):

    text = ""

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page_number, page in enumerate(pdf.pages):

                page_text = page.extract_text()

                if page_text:
                    text += f"\n--- Page {page_number + 1} ---\n"
                    text += page_text

        return text

    except Exception as e:

        print(f"Error reading PDF: {e}")
        return None


def extract_text_from_txt(txt_path):

    try:

        with open(txt_path, "r", encoding="utf-8") as file:

            return file.read()

    except Exception as e:

        print(f"Error reading TXT: {e}")
        return None


def extract_text(file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".txt":
        return extract_text_from_txt(file_path)

    else:
        raise ValueError("Unsupported file format. Use PDF or TXT.")


# Test run
if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(base_dir, "../data/sample_fnol.pdf")

    text = extract_text(file_path)

    output_path = os.path.join(base_dir, "../output/extracted_text.txt")

    with open(output_path, "w", encoding="utf-8") as f:

        f.write(text)

    print("Text extracted successfully")
