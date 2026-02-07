import re


# Words that indicate labels (NOT actual values)
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
    "ACORD",        # ← ADD THIS
    "SCHEDULE",     # ← ADD THIS
    "REMARKS"       # ← ADD THIS
]


# Optional fields that do NOT trigger Manual Review if missing
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
    Reject label text and accept only real values.
    """

    if value is None:
        return False

    value = value.strip()

    if value == "":
        return False

    # Reject if ALL uppercase (likely label)
    if value.isupper():
        return False

    # Reject if contains known label words
    for word in INVALID_LABEL_WORDS:
        if word in value.upper():
            return False

    # Reject very short values
    if len(value) < 3:
        return False

    return True


def extract_regex_patterns(text, patterns):
    """
    Try multiple patterns and return first valid extracted value.
    """

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            value = match.group(1).strip()

            if is_valid_value(value):
                return value

    return None


def extract_fields(text):
    """
    Extract all FNOL fields required by assignment.
    """

    fields = {}

    # --------------------
    # Policy Information
    # --------------------

    fields["policyNumber"] = extract_regex_patterns(text, [
        r"POLICY NUMBER[:\s]+([A-Z0-9\-]+)",
        r"Policy Number[:\s]+([A-Z0-9\-]+)"
    ])

    fields["policyholderName"] = extract_regex_patterns(text, [
        r"NAME OF INSURED[:\s]+(.+)",
        r"Policyholder Name[:\s]+(.+)"
    ])

    fields["effectiveDates"] = extract_regex_patterns(text, [
        r"Effective Dates[:\s]+(.+)"
    ])

    # --------------------
    # Incident Information
    # --------------------

    fields["dateOfLoss"] = extract_regex_patterns(text, [
        r"DATE OF LOSS[:\s]+([0-9\-]+)",
        r"Date of Loss[:\s]+([0-9\-]+)"
    ])

    fields["timeOfLoss"] = extract_regex_patterns(text, [
        r"TIME OF LOSS[:\s]+(.+)",
        r"Time of Loss[:\s]+(.+)"
    ])

    fields["location"] = extract_regex_patterns(text, [
        r"LOCATION OF LOSS[:\s]+(.+)",
        r"Location of Loss[:\s]+(.+)"
    ])

    fields["description"] = extract_regex_patterns(text, [
        r"DESCRIPTION OF ACCIDENT[:\s]+(.+)",
        r"Description of Accident[:\s]+(.+)"
    ])

    # --------------------
    # Involved Parties
    # --------------------

    fields["claimant"] = extract_regex_patterns(text, [
        r"CLAIMANT NAME[:\s]+(.+)",
        r"Claimant Name[:\s]+(.+)",
        r"NAME OF INSURED[:\s]+(.+)"
    ])

    fields["thirdParties"] = extract_regex_patterns(text, [
        r"Third Parties[:\s]+(.+)"
    ])

    fields["contactDetails"] = extract_regex_patterns(text, [
        r"PHONE[:\s]+(.+)",
        r"EMAIL[:\s]+(.+)"
    ])

    # --------------------
    # Asset Details
    # --------------------

    fields["assetID"] = extract_regex_patterns(text, [
        r"VIN[:\s]+([A-Z0-9]+)",
        r"Asset ID[:\s]+(.+)"
    ])

    asset_type = extract_regex_patterns(text, [
        r"Asset Type[:\s]+(.+)"
    ])

    # Default for automobile FNOL
    if asset_type is None:
        asset_type = "vehicle"

    fields["assetType"] = asset_type

    fields["estimatedDamage"] = extract_regex_patterns(text, [
        r"ESTIMATE AMOUNT[:\s]+\$?([0-9,]+)",
        r"Estimated Damage Amount[:\s]+([0-9,]+)"
    ])

    # --------------------
    # Other Mandatory Fields
    # --------------------

    fields["claimType"] = extract_regex_patterns(text, [
        r"CLAIM TYPE[:\s]+(.+)",
        r"Claim Type[:\s]+(.+)"
    ])

    initial_estimate = extract_regex_patterns(text, [
        r"Initial Estimate[:\s]+([0-9,]+)"
    ])

    if initial_estimate is None:
        initial_estimate = fields["estimatedDamage"]

    fields["initialEstimate"] = initial_estimate

    fields["attachments"] = extract_regex_patterns(text, [
        r"Attachments[:\s]+(.+)"
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
