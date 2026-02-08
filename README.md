# Autonomous Insurance Claims Processing Agent

## Overview

This project implements an **Autonomous Insurance Claims Processing Agent** that automatically processes First Notice of Loss (FNOL) documents in PDF and TXT formats. The agent extracts structured claim information, validates required fields, and determines the appropriate claim routing decision based on predefined business rules.

The system is designed to simulate real-world insurance claim intake automation, reducing manual workload and accelerating claim processing.

---

## Problem Statement

Insurance companies receive FNOL documents containing claim details such as policy information, incident details, asset damage, and claimant information. These documents may be incomplete, structured differently, or contain placeholder template text.

Manually reviewing each FNOL document is time-consuming and inefficient.

The goal of this project is to build an autonomous agent that can:

* Accept FNOL documents in PDF or TXT format
* Extract key claim information
* Identify missing mandatory fields
* Route claims automatically based on business logic
* Provide structured output in JSON format

---

## Key Features

* Supports both PDF and TXT FNOL files
* Extracts structured claim information automatically
* Detects missing mandatory fields
* Prevents extraction of template labels and placeholder text
* Applies automated claim routing logic
* Generates structured JSON output
* Handles blank and filled FNOL forms safely
* Works with dynamic file input

---

## Technology Stack

### Programming Language

* Python 3.10+

### Libraries Used

| Library    | Purpose                               |
| ---------- | ------------------------------------- |
| pdfplumber | Extract text from PDF FNOL documents  |
| re (regex) | Pattern matching for field extraction |
| json       | Generate structured output            |
| os         | File handling and path management     |
| sys        | Command-line input handling           |

---

## System Architecture

The agent follows a modular architecture:

```
Input FNOL File
      ↓
Text Extraction Module
      ↓
Field Extraction Module
      ↓
Missing Field Detection Module
      ↓
Routing Decision Engine
      ↓
Structured JSON Output
```

---

## Claim Routing Logic

The agent routes claims based on assignment business rules:

| Condition                      | Route             |
| ------------------------------ | ----------------- |
| Missing mandatory fields       | Manual Review     |
| Estimated damage < 25,000      | Fast-track        |
| Estimated damage ≥ 25,000      | Specialist Review |
| Fraud-related keywords present | Investigation     |

---

## Fields Extracted

### Policy Information

* Policy Number
* Policyholder Name
* Effective Dates

### Incident Information

* Date of Loss
* Time of Loss
* Location
* Description

### Involved Parties

* Claimant
* Third Parties
* Contact Details

### Asset Details

* Asset Type
* Asset ID (VIN)
* Estimated Damage

### Other Fields

* Claim Type
* Initial Estimate
* Attachments

---

## Project Structure

```
insurance-claims-agent/
│
├── src/
│   ├── main.py
│   ├── extract_text.py
│   ├── extract_fields.py
│   ├── route_claim.py
│
├── data/
│   ├── sample_fnol.pdf
│   ├── sample_fnol.txt
│   ├── fnol1.pdf
│
├── output/
│   └── (generated JSON outputs)
│
├── requirements.txt
├── README.md
├── .gitignore
```

---

## File Descriptions

### main.py

Entry point of the agent.

Responsibilities:

* Accept FNOL file path
* Run extraction pipeline
* Generate structured JSON output
* Print routing decision

---

### extract_text.py

Extracts raw text from:

* PDF files using pdfplumber
* TXT files using standard file reading

---

### extract_fields.py

Core extraction engine.

Responsibilities:

* Extract all required FNOL fields using regex
* Filter placeholder template text
* Prevent incorrect extraction from blank forms
* Identify missing mandatory fields

---

### route_claim.py

Implements routing logic.

Responsibilities:

* Analyze extracted fields
* Apply routing rules
* Return routing decision and reasoning

---

### requirements.txt

Contains project dependencies:

```
pdfplumber
```

---

### data/

Contains sample FNOL files for testing.

---

### output/

Stores generated JSON results.

---

## Installation Instructions

Clone repository:

```
git clone https://github.com/yourusername/insurance-claims-agent.git
cd insurance-claims-agent
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## How to Run

From project root:

```
python src/main.py data/sample_fnol.pdf
```

Or for TXT file:

```
python src/main.py data/sample_fnol.txt
```

---

## Example Output

```
{
  "inputFile": "sample_fnol.pdf",
  "extractedFields": {
    "policyNumber": "POL987654321",
    "policyholderName": "Rohit Kumar Janjarapu",
    "estimatedDamage": "18500",
    "claimType": "vehicle"
  },
  "missingFields": [],
  "recommendedRoute": "Fast-track",
  "reasoning": "Damage below fast-track threshold"
}
```

---

## Key Challenges Solved

* Handling blank FNOL template forms
* Preventing extraction of label text
* Extracting data from structured PDF layouts
* Supporting multiple file formats
* Ensuring robust routing logic

---

## Assumptions Made

* FNOL documents follow ACORD or similar structured format
* Asset type defaults to vehicle if not specified
* Estimated damage determines routing priority
* Fraud detection uses keyword matching

---

## Future Improvements

* Add REST API interface
* Add confidence scoring for extracted fields
* Support scanned documents using OCR
* Add batch processing support
* Add web-based interface

---

## Conclusion

This project successfully implements an autonomous insurance claims processing agent that can:

* Automatically extract FNOL data
* Validate claim completeness
* Apply routing rules
* Generate structured output

The system is robust, modular, and production-ready.

---
