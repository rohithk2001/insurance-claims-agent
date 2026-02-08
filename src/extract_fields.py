import re


# Words that indicate labels, headers, or invalid values
INVALID_LABEL_WORDS = [
    "CONTACT",
    "INSURED",
    "ADDRESS",
    "LOCATION",
    "DESCRIPTION",
    "LOSS",
    "DATE",
    "PHONE",
    "EMAIL",
    "LINE OF BUSINESS",
    "REPORT NUMBER",
    "POLICE",
    "VEHICLE",
    "OWNER",
    "DRIVER",
    "PRIMARY",
    "SECONDARY",
    "CITY",
    "STATE",
    "ZIP",
    "COUNTRY",
    "ACORD",
    "SCHEDULE",
    "REMARKS",
    "DETAILS",
    "INFORMATION",
    "FAX",
    "PAGE",
    "FORM",
    "NAIC"
]


# Optional fields (missing allowed)
OPTIONAL_FIELDS = [
    "effectiveDates",
    "timeOfLoss",
    "thirdParties",
    "contactDetails",
    "assetType",
    "attachments"
]


def is_valid_value(value):
    """
    Validates extracted value.
    Rejects placeholder text, labels, and blank-form helper text.
    """

    if value is None:
        return False

    value = value.strip()

    if value == "" or value == ":":
        return False

    upper_value = value.upper()

    # Reject placeholder text
    if "(" in value or ")" in value:
        return False

    if "#" in value:
        return False

    # Reject labels
    if ":" in value:
        return False

    # Reject ACORD footer/header
    if "ACORD" in upper_value or "PAGE" in upper_value:
        return False

    # Reject known label words
    for word in INVALID_LABEL_WORDS:
        if word in upper_value:
            return False

    # Reject lines with many uppercase words (likely labels)
    words = value.split()
    uppercase_words = sum(1 for w in words if w.isupper())

    if uppercase_words >= 3:
        return False

    # Reject lines with excessive spacing (form placeholders)
    if "  " in value:
        return False

    return True

    """
    Validates extracted value.
    Rejects labels, headers, and junk values.
    """

    if value is None:
        return False

    value = value.strip()

    if value == "":
        return False

    if value == ":":
        return False

    upper_value = value.upper()

    # Reject footer/header junk
    if "ACORD" in upper_value:
        return False

    if "PAGE" in upper_value:
        return False

    # Reject exact label matches
    if upper_value in INVALID_LABEL_WORDS:
        return False

    # Reject label-like values
    for word in INVALID_LABEL_WORDS:
        if upper_value == word:
            return False

    # Reject colon-only or label-only lines
    if ":" in value and len(value.split()) <= 2:
        return False

    # Reject very short junk
    if len(value) < 2:
        return False

    return True


def extract_regex_patterns(text, patterns):
    """
    Extract values safely from same line or next line.
    Prevents capturing label lines like 'LOCATION OF LOSS: ...'
    """

    lines = text.splitlines()

    for i, line in enumerate(lines):

        for pattern in patterns:

            match = re.search(pattern, line, re.IGNORECASE)

            if match:

                # Case 1: value exists on same line
                if match.lastindex:

                    value = match.group(1).strip()

                    if is_valid_value(value):
                        return value

                # Case 2: check next line safely
                if i + 1 < len(lines):

                    next_line = lines[i + 1].strip()

                    # IMPORTANT FIX:
                    # Reject if next line contains colon (likely another label)
                    if ":" in next_line:
                        continue

                    # Reject if next line contains label keywords
                    upper_next = next_line.upper()
                    if any(word in upper_next for word in INVALID_LABEL_WORDS):
                        continue

                    if is_valid_value(next_line):
                        return next_line

    return None


def extract_fields(text):
    """
    Extract all FNOL required fields.
    """

    fields = {}

    # Policy Information

    fields["policyNumber"] = extract_regex_patterns(text, [
        r"POLICY NUMBER[:\s]*([A-Z0-9\-]+)",
        r"Policy Number[:\s]*([A-Z0-9\-]+)"
    ])

    fields["policyholderName"] = extract_regex_patterns(text, [
        r"NAME OF INSURED[:\s]*(.+)",
        r"Policyholder Name[:\s]*(.+)"
    ])

    fields["effectiveDates"] = extract_regex_patterns(text, [
        r"Effective Dates[:\s]*(.+)"
    ])

    # Incident Information

    fields["dateOfLoss"] = extract_regex_patterns(text, [
        r"DATE OF LOSS[:\s]*([0-9\-\/]+)",
        r"Date of Loss[:\s]*([0-9\-\/]+)"
    ])

    fields["timeOfLoss"] = extract_regex_patterns(text, [
        r"TIME OF LOSS[:\s]*([0-9:\sAPMapm]+)",
        r"Time of Loss[:\s]*([0-9:\sAPMapm]+)"
    ])

    fields["location"] = extract_regex_patterns(text, [
        r"LOCATION OF LOSS[:\s]*(.+)",
        r"Location of Loss[:\s]*(.+)"
    ])

    fields["description"] = extract_regex_patterns(text, [
        r"DESCRIPTION OF ACCIDENT[:\s]*(.+)",
        r"Description of Accident[:\s]*(.+)"
    ])

    # Involved Parties

    fields["claimant"] = extract_regex_patterns(text, [
        r"CLAIMANT NAME[:\s]*(.+)",
        r"Claimant Name[:\s]*(.+)",
        r"NAME OF INSURED[:\s]*(.+)"
    ])

    fields["thirdParties"] = extract_regex_patterns(text, [
        r"Third Parties[:\s]*(.+)"
    ])

    fields["contactDetails"] = extract_regex_patterns(text, [
        r"PHONE[:\s]*(.+)",
        r"EMAIL[:\s]*(.+)"
    ])

    # Asset Details

    fields["assetID"] = extract_regex_patterns(text, [
        r"VIN[:\s]*([A-Z0-9]+)",
        r"Asset ID[:\s]*([A-Z0-9]+)"
    ])

    asset_type = extract_regex_patterns(text, [
        r"Asset Type[:\s]*(.+)"
    ])

    if asset_type is None:
        asset_type = "vehicle"

    fields["assetType"] = asset_type

    fields["estimatedDamage"] = extract_regex_patterns(text, [
        r"ESTIMATE AMOUNT[:\s]*\$?([0-9,]+)",
        r"Estimated Damage Amount[:\s]*([0-9,]+)"
    ])

    # Claim Information

    claim_type = extract_regex_patterns(text, [
        r"CLAIM TYPE[:\s]*(vehicle|injury|property)",
        r"Claim Type[:\s]*(vehicle|injury|property)"
    ])

    if claim_type is None:
        claim_type = "vehicle"

    fields["claimType"] = claim_type

    initial_estimate = extract_regex_patterns(text, [
        r"Initial Estimate[:\s]*([0-9,]+)"
    ])

    if initial_estimate is None:
        initial_estimate = fields["estimatedDamage"]

    fields["initialEstimate"] = initial_estimate

    fields["attachments"] = extract_regex_patterns(text, [
        r"Attachments[:\s]*(.+)"
    ])

    return fields


def find_missing_fields(fields):
    """
    Identify mandatory missing fields.
    """

    missing = []

    for key, value in fields.items():

        if value is None and key not in OPTIONAL_FIELDS:
            missing.append(key)

    return missing
