import os
import shutil
import json
import subprocess

collections = [
    {
        "name": "collection1",
        "input": "collection1/challenge1b_input.json",
        "output": "output/collection1_output.json"
    },
    {
        "name": "collection2",
        "input": "collection2/challenge1b_input.json",
        "output": "output/collection2_output.json"
    },
    {
        "name": "collection3",
        "input": "collection3/challenge1b_input.json",
        "output": "output/collection3_output.json"
    }
]

def get_pdf_list(input_json_path):
    with open(input_json_path, "r") as f:
        data = json.load(f)
    return [doc["filename"] for doc in data["documents"]]

def copy_pdfs(pdf_list, collection_dir):
    for pdf in pdf_list:
        src = os.path.join(collection_dir, pdf)
        dst = pdf
        if not os.path.exists(dst):
            shutil.copy(src, dst)

def remove_pdfs(pdf_list):
    for pdf in pdf_list:
        if os.path.exists(pdf):
            os.remove(pdf)

def run_main():
    subprocess.run(["python", "main.py"], check=True)

os.makedirs("output", exist_ok=True)

for col in collections:
    print(f"\n=== Running {col['name']} ===")
    # Copy input file
    shutil.copy(col["input"], "challenge1b_input.json")
    # Get PDF list from input
    pdfs = get_pdf_list(col["input"])
    # Copy PDFs to root
    copy_pdfs(pdfs, col["name"])
    # Run main.py
    run_main()
    # Move output to collection-specific file
    shutil.copy("output/challenge1b_output_generated.json", col["output"])
    # Clean up PDFs
    remove_pdfs(pdfs)

print("\nAll collections processed! Outputs are in the output/ folder.")