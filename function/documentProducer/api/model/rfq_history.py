from typing import Dict, Optional


def get_model(row: list) -> Optional[Dict]:

    mpn = row[6]
    mfr = row[7]
    ipn = row[12]

    if any(v is None for v in [mpn, ipn, mfr]):
        return None

    return {
        "mpn": mpn.strip(),
        "manufacturerName": mfr.strip(),
        "ipn": ipn.strip()
    }
