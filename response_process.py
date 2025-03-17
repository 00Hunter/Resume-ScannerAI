import re
import json

# Simulated Gemini API response (Your actual text)
def process_response(gemini_response):
    # Step 1: Extract Sections
    sections = re.split(r'\n\d+\.\s+\*\*(.*?)\*\*:', gemini_response)

    structured_data = []

    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        section_content = sections[i + 1].strip()

        # Extract key recommendations from bullet points
        improvements = re.findall(r'\*\*\s*(.*?)\s*\*\*:', section_content)
        improvements = [imp.strip() for imp in improvements]

        structured_data.append({
            "section": section_title,
            "improvements": improvements
        })

    # Step 2: Convert to JSON
    json_output = json.dumps(structured_data, indent=4)

    # Step 3: Print or Save the Processed JSON
    # print(json_output)

    # Optional: Save JSON to a file
    # with open("resume_analysis.json", "w") as file:
    #     file.write(json_output)
