PDF Structure Extraction System (Challenge 1A)
1. Overview
This system is a high-performance batch processor designed to analyze a collection of PDF documents. For each PDF, it intelligently extracts the hierarchical structure (i.e., the table of contents or outline) and saves this structured data as a corresponding JSON file. The entire workflow is containerized using Docker to ensure consistency and ease of execution.

2. Project Structure
To ensure the script runs correctly, your project must follow the directory structure below. All PDFs to be processed must be placed in the input folder.

.
├── input/
│   ├── file01.pdf
│   ├── file02.pdf
│   └── (all other PDFs to be processed...)
│
├── output/                 <-- All JSON results will be saved here
│
├── process_pdfs.py           <-- The main Python script for processing
├── Dockerfile
└── requirements.txt

3. Methodology
The core of the system is the process_pdfs.py script, which operates as follows:

Batch Processing: The script automatically scans the input/ directory to find all PDF files that need to be processed.

PDF Parsing: For each PDF, it uses the PyMuPDF library to perform a deep analysis of the document's content. It doesn't just read the text; it examines the properties of the text, such as font size, style (bold, italic), and position on the page.

Hierarchical Structure Detection: By comparing the properties of different lines of text, the script uses a set of heuristics to identify headings (H1, H2, H3, etc.). For example, text with a larger font size is typically classified as a higher-level heading.

JSON Output Generation: Once the entire document outline is reconstructed, the system formats this data into a clean JSON structure, including the heading level, text, and page number for each entry. This JSON file is then saved in the output/ directory with a matching filename.

4. Setup and Installation
This is a one-time setup step.

Prerequisite: You must have Docker installed and running on your machine.

Build the Docker Image:
Open a terminal in the project's root directory (1A/) and execute the command below. This will build the Docker image required to run the processor and tag it as pdf-processor.

docker build -t pdf-processor .

5. Execution
After building the image, you can process all the PDFs in the input folder with a single command.

The Docker command will mount your local input and output folders into the container, allowing the script inside to read your files and save the results back to your machine.

To run the PDF processing, execute this command in your terminal:

docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-processor

The script will then run, and you will see the generated .json files appear in your output directory, one for each input PDF.