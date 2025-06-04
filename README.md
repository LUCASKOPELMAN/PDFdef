# PDF Glossary Annotator

This Python script scans a PDF for terms defined in a glossary file and automatically adds popup annotations to them with their definitions.

---

## 📄 Files Included

- `PDFdef.py` – Main script that performs the annotation.
- `definitions.json` – JSON file containing terms and their corresponding definitions.

---

## 🛠️ How to Use

### 1. Install the required dependency:

```bash
pip install pymupdf
```

### 2. Prepare your files

- Place your input PDF (e.g., `document.pdf`) in the same directory.
- Edit `definitions.json` to include the terms and definitions you want to annotate. For example:

```json
{
  "Premium": "Amount paid by the policyholder to the insurer",
  "Actual Cash Value": "Physical value minus depreciation"
}
```

### 3. Run the script

In the terminal or command line:

```bash
python PDFdef.py
```

When prompted, enter the name of the PDF (e.g., `document.pdf`).  
The script will generate an annotated version like `document_annotated.pdf`.

---

## 🔍 Features

- Fuzzy matching of terms (e.g., matches "premiums" to "premium")
- Case-insensitive and punctuation-tolerant
- Adds transparent gray boxes and tooltips with definitions
- Automatically saves an annotated copy of your PDF

---

## 📖 License

This project is released under the MIT License.

---

## 🙋 Author

Built by [Your Name] — feel free to fork or contribute!
