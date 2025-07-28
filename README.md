# adobe-hackathon-submission
"Connecting the Dots" Challenge Submission
This repository contains the complete solution for both Round 1A and Round 1B of the "Connecting the Dots" hackathon. The project is designed as a cohesive system that first understands document structure (1A) and then uses that intelligence to provide persona-driven insights (1B).

1. Project Structure
The project is organized into two main directories, one for each round of the challenge.

.
├── round1A/
│   ├── input/                # Place PDFs for Round 1A here
│   │   ├── file01.pdf
│   │   └── ...
│   ├── output/               # JSON outlines from Round 1A will be saved here
│   ├── process_pdfs.py       # Main script for Round 1A
│   ├── Dockerfile            # Docker configuration for Round 1A
│   └── requirements.txt
│
├── round1B/
│   ├── collection1/          # Test case 1 for Round 1B
│   │   ├── input.json
│   │   └── (PDFs for collection 1...)
│   ├── collection2/          # Test case 2 for Round 1B
│   │   ├── input.json
│   │   └── (PDFs for collection 2...)
│   ├── collection3/          # Test case 3 for Round 1B
│   │   ├── input.json
│   │   └── (PDFs for collection 3...)
│   ├── output/               # JSON results from Round 1B will be saved here
│   ├── batch_run_collections.py # Script to run all 1B test cases
│   ├── main.py               # Core logic for Round 1B
│   ├── Dockerfile            # Docker configuration for Round 1B
│   └── requirements.txt
│
└── README.md                 # This file

2. Methodology
Round 1A: Understand Your Document
The goal of Round 1A is to extract a structured outline from a raw PDF.

Approach: The process_pdfs.py script uses the PyMuPDF library to analyze the document. It does not simply rely on font sizes. Instead, it creates a profile of all text elements on each page, considering font size, weight (bold), and spatial layout. It identifies the most common "body text" font size and then uses a relative threshold to classify larger and bolder text as H1, H2, and H3 headings, thus creating a hierarchical outline.

Round 1B: Persona-Driven Document Intelligence
The goal of Round 1B is to act as an intelligent analyst, extracting the most relevant sections from multiple documents based on a user persona.

Approach: The solution (main.py) uses a generic, scalable model that avoids hardcoding keywords for each persona.

Dynamic Keyword Analysis: It first parses the persona and job_to_be_done to extract core concepts (e.g., "HR," "forms," "vegetarian," "travel").

Scalable Concept Expansion: It then uses a generic "concept map" to expand these core terms into a rich set of related keywords (e.g., "form" expands to "fillable," "signature," "interactive"). This makes the system adaptable to new, unseen personas without code changes.

Intelligent Scoring: Sections are scored based on the density of these keywords. A heavy bonus is applied if keywords appear in a section's title. The system also supports negative constraints, heavily penalizing sections with non-vegetarian terms if the persona requires a vegetarian menu.

3. How to Build and Run
Prerequisites:

Docker must be installed and running.

Python 3.x must be installed to run the batch script.

Running Round 1A
Navigate to the Directory:

cd round1A

Add PDFs: Place all the PDF files you want to process into the round1A/input/ folder.

Build the Docker Image:

docker build -t pdf-processor-1a .

Run the Processor:

docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" pdf-processor-1a

The JSON outlines will be generated in the round1A/output/ directory.

Running Round 1B
Navigate to the Directory:

cd round1B

Set up Collections: Ensure each test case (collection1, collection2, etc.) has its own folder containing an input.json file and all its associated PDFs.

Run the Batch Processor: The batch_run_collections.py script automates everything (building the Docker image and running each collection).

python batch_run_collections.py

The script will build the Docker image (document-intelligence-1b) and then process each collection one by one. All final JSON reports will be saved in the round1B/output/ directory, named appropriately (e.g., collection1_output.json).
