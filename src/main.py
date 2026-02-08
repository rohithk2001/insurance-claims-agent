import sys
import os
import json

from extract_text import extract_text
from extract_fields import extract_fields, find_missing_fields
from route_claim import determine_route


def run_agent(file_path):

    # Extract text from PDF or TXT
    text = extract_text(file_path)

    if not text:
        print("Error: Could not extract text.")
        return

    # Extract fields
    fields = extract_fields(text)

    # Find missing fields
    missing_fields = find_missing_fields(fields)

    # Determine route
    route = determine_route(fields, missing_fields)

    # Final output
    output = {

        "inputFile": os.path.basename(file_path),

        "extractedFields": fields,

        "missingFields": missing_fields,

        "recommendedRoute": route["recommendedRoute"],

        "reasoning": route["reasoning"]
    }

    print(json.dumps(output, indent=4))

    # Save output file
    output_path = os.path.join("output", os.path.basename(file_path) + ".json")

    os.makedirs("output", exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage: python main.py <fnol_file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):

        print("Error: File not found.")
        sys.exit(1)

    run_agent(file_path)
