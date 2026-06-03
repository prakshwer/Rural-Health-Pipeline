import pandas as pd
import re

def fetch_from_google_sheets(sheet_url: str) -> pd.DataFrame:
    """
    Fetch data from a public Google Sheet.
    The sheet must be set to 'Anyone with link can view'.
    No API key needed for public sheets.
    """
    # Convert the Google Sheets URL to a CSV export URL
    # Works for any public Google Sheet
    pattern = r"https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)"
    match = re.search(pattern, sheet_url)

    if not match:
        raise ValueError(
            "Invalid Google Sheets URL. "
            "Make sure you paste the full URL."
        )

    sheet_id = match.group(1)

    # Check if specific sheet/gid is mentioned
    gid_match = re.search(r"gid=(\d+)", sheet_url)
    gid = gid_match.group(1) if gid_match else "0"

    # Build the CSV export URL
    csv_url = (
        f"https://docs.google.com/spreadsheets/d/"
        f"{sheet_id}/export?format=csv&gid={gid}"
    )

    print(f"Fetching from: {csv_url}")

    # Read directly into pandas — no API key needed!
    df = pd.read_csv(csv_url)

    # Clean column names — remove spaces and lowercase
    df.columns = [col.strip().lower().replace(" ", "_")
                  for col in df.columns]

    print(f"Fetched {len(df)} rows with columns: {list(df.columns)}")
    return df