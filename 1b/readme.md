Persona-Driven Document Intelligence System
1. Overview
This system acts as an intelligent document analyst. It processes a collection of PDF documents and, based on a specific user persona and their job-to-be-done, it extracts and ranks the most relevant sections. The entire process is containerized with Docker for consistent and reliable execution.

2. Project Structure
For the system to work correctly, your files must be organized in the following structure. Each test case (collection) should have its own folder containing its specific input.json and all related PDF documents.

.
├── collection1/
│   ├── input.json
│   └── (all PDFs for test case 1...)
│
├── collection2/
│   ├── input.json
│   └── (all PDFs for test case 2...)
│
├── collection3/
│   ├── input.json
│   └── (all PDFs for test case 3...)
│
├── output/                 <-- All results will be saved here
│
├── batch_run_collections.py  <-- The script to run all tests
├── Dockerfile
├── main.py                   <-- The core document analysis logic
└── requirements.txt

3. Methodology
<details>
<summary>Click to expand the technical approach</summary>

The system operates in a three-stage process:

Dynamic Keyword Generation: Instead of using hardcoded keywords for each persona, the system analyzes the persona and job_to_be_done from the input.json. It extracts core concepts (e.g., "HR," "forms," "onboarding") and uses a generic concept map to expand these into a rich set of relevant keywords. This makes the system highly scalable and adaptable to new, unseen personas without changing the code.

Intelligent Section Scoring: The system parses each PDF, breaking it down into titled sections. Each section is then scored based on the density of the generated keywords. Sections with titles that match the keywords are given a significantly higher score, mimicking how a human expert would prioritize information. For specific negative constraints (e.g., a "vegetarian" persona), the system heavily penalizes sections containing non-vegetarian terms.

Extractive Summarization: For the top-ranked sections, the system performs a final analysis. It breaks the section's content into individual sentences and scores each one against the keyword profile. The most relevant sentences are then extracted and combined to create a concise, actionable summary (refined_text).

</details>

4. Setup and Installation
You only need to perform this step once.

Prerequisite: You must have Docker installed and running on your machine.

Build the Docker Image:
Open your terminal in the project's root directory and run the following command. This will build the Docker image and tag it as document-intelligence.

docker build -t document-intelligence .

5. Execution: Running All Test Collections
After the image is built, you can process all your test collections (collection1, collection2, collection3, etc.) with a single command.

The batch_run_collections.py script automates the entire process. It will:

Loop through each collection folder.

Copy the necessary PDFs and the correct input.json for the container to use.

Run the document analysis inside the Docker container.

Save the result in the output folder, correctly named (e.g., collection1_output.json).

Clean up the temporary files before processing the next collection.

To run the batch process, execute this command in your terminal:

python batch_run_collections.py

After the script finishes, you will find all the generated output files inside the output/ directory.