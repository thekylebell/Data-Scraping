import gzip
import json
import csv
from datetime import date

# === CONFIG ===
metadata_file = "jstor_metadata_2025-09-23.jsonl.gz"  # update with your latest JSTOR file
output_file = f"succession_metadata_{date.today()}.csv"

# Consolidated search terms (excluding category labels)
search_terms = [
    # Core Keywords
    "succession planning",
    "leadership succession",
    "executive succession",
    "management succession",
    "leadership transition",
    "leadership pipeline",
    "workforce succession",
    "talent succession",
    "strategic succession",
    "organizational succession",

    # Context / Sector Keywords
    "municipal government",
    "local government",
    "city government",
    "county government",
    "public sector",
    "public administration",
    "government agencies",
    "public management",
    "local governance",
    "urban management",
    "civil service",
    "regional government",
    "state government",
    "metropolitan administration",
    "bureaucratic leadership",

    # Process / Practice Keywords
    "talent management",
    "leadership development",
    "organizational development",
    "strategic workforce planning",
    "human resource management",
    "workforce planning",
    "mentoring programs",
    "knowledge transfer",
    "leadership capacity",
    "employee retention",
    "public sector innovation",
    "performance management",
    "career paths",
    "coaching initiatives",
    "succession readiness",
    "internal promotion strategies",
    "cross-training programs",

    # Challenge & Barrier Keywords
    "political turnover",
    "budget constraints",
    "resource limitations",
    "resource constraints",
    "resistance to change",
    "leadership gaps",
    "brain drain",
    "aging workforce",
    "political appointments",
    "institutional barriers",
    "organizational culture",
    "recruitment challenges",
    "retirement wave",
    "baby boomer retirement",
    "skill shortages",
    "diversity barriers",
    "union restrictions",
    "technological adaptation issues",
    "public reception",

    # Comparative / Broader Framing Keywords
    "best practices in succession planning",
    "case studies in local government succession",
    "comparative public management",
    "comparative public administration",
    "practitioner reports",
    "public-private partnerships",
    "private sector vs. public sector succession",
    "nonprofit succession planning",
    "international public sector comparisons"
]

# === PROCESSING ===
results = []

with gzip.open(metadata_file, "rt", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        if line_number % 10000 == 0:
            print(f"\rProcessing line: {line_number}", end="", flush=True)
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            print(f"\nSkipping invalid JSON at line {line_number}")
            continue

        if data.get("review_required"):
            continue

        # Safe extraction of title
        title = (data.get("title") or "").lower()

        # Check if title contains any search term
        matched = any(term in title for term in search_terms)

        if matched:
            # Extract metadata safely
            title_out = data.get("title") or "N/A"

            authors_field = data.get("authors")
            if isinstance(authors_field, list):
                authors = ", ".join([str(a) for a in authors_field])
            elif authors_field:
                authors = str(authors_field)
            else:
                authors = "N/A"

            year = data.get("publicationYear") or "N/A"
            journal = data.get("journal") or "N/A"
            abstract_out = data.get("abstract") or "N/A"
            citation_count = data.get("citationCount") or "N/A"
            link = data.get("url") or "N/A"

            results.append([
                title_out, authors, year, journal, abstract_out, citation_count, link
            ])

print(f"\nFound {len(results)} relevant articles.")

# === EXPORT TO CSV ===
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Title", "Authors", "Year", "Journal", "Abstract", "Citation Count", "Link"
    ])
    writer.writerows(results)

print(f"Metadata saved to {output_file}")