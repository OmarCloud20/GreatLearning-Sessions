# Extract Texts from PDFs and Images


A. Extract using Apache Tika as a Lambda layer

B. Extract using AWS TexTract service

---

The folder contains:

1. lambda layer - Apache Tika zip file: **appbase.zip**
2. Python code to utilize the Apache Tika: **PDFExtractor.py**
3. Lambda test event json file for the PDF Extractor: **PDFExtractorTest.json**
4. Python code for Textract service: **TexTract.py**

### Architecture Diagram - TexTract

<br>

![diagram](textract.png)