"Connecting the Dots" Challenge - Our Approach
This document explains the methodology used to solve Round 1A and Round 1B.

Round 1A: Understanding Document Structure
Goal: To extract a structured outline (Title, H1, H2, H3 headings) from a PDF file.

Our Solution:

We built a Python script that utilizes the PyMuPDF library. Our system does not solely rely on font sizes but uses a smarter approach:

Text Analysis: The script analyzes every text block in the PDF—considering its font size, weight (bold or not), and its position on the page.

Heading Detection: The script first determines the average font size of "normal" body text. Then, it classifies larger and bolder text as H1, H2, or H3 headings.

Outline Creation: In this way, the script prepares a complete hierarchical outline of the document and saves it into a clean JSON file.

Round 1B: Persona-Driven Information Extraction
Goal: To extract the most essential sections from multiple PDF documents based on different users (personas) and their tasks (jobs-to-be-done).

Our Solution:

We have built a generic and scalable system that eliminates the need to hardcode new keywords for every new persona.

Dynamic Keyword Analysis: The system understands core concepts (like "HR," "forms," "vegetarian," "travel") by reading the user's persona and job_to_be_done.

Scalable Concept Expansion: After this, the system uses a "concept map" to generate more keywords related to these core concepts (e.g., "form" expands to "fillable," "signature," "interactive"). This makes the system ready for new personas without any code changes.

Intelligent Scoring: Each section is scored based on these keywords. If a keyword is found in the section's title, it receives extra points. The system also handles negative constraints—for example, if the user is "vegetarian," it gives a negative score to sections with non-veg dishes to push them down in the ranking.

With this approach, our system delivers smart, adaptable, and relevant results for all types of users.
