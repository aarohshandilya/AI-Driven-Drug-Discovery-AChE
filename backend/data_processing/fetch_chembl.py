"""Fetch human AChE IC50 records from the public ChEMBL API.

This script writes source records, not a curated benchmark. Inspect assay type,
confidence, units, duplicates, salts, and structure quality before modeling.
"""
import argparse
from pathlib import Path
import requests
import pandas as pd

URL = "https://www.ebi.ac.uk/chembl/api/data/activity.json"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/raw/chembl_human_ache_ic50.csv")
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()
    params = {"target_chembl_id": "CHEMBL220", "standard_type": "IC50",
              "limit": min(args.limit, 1000), "format": "json"}
    rows, url = [], URL
    while url and len(rows) < args.limit:
        response = requests.get(url, params=params if url == URL else None, timeout=45)
        response.raise_for_status()
        payload = response.json()
        rows.extend(payload.get("activities", []))
        url = payload.get("page_meta", {}).get("next")
        if url and url.startswith("/"):
            url = "https://www.ebi.ac.uk" + url
        params = None
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("ChEMBL returned no activity rows; no file written.")
    keep = [c for c in ["activity_id", "assay_chembl_id", "document_chembl_id", "target_chembl_id",
             "assay_type", "standard_type", "standard_relation", "standard_value", "standard_units",
             "standard_flag", "pchembl_value", "canonical_smiles", "molecule_chembl_id"] if c in df]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    df[keep].to_csv(args.out, index=False)
    print(f"Saved {len(df)} source activity records to {args.out}. These are uncurated records, not model-ready labels.")

if __name__ == "__main__": main()
