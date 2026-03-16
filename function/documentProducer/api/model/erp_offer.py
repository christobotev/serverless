from typing import Dict, Optional


def get_model(row: list) -> Optional[Dict]:
    mpn, mfr, qty, condition, date_code, price, vendor_no, vendor_name, uploaded, owner, notes = row

    if any(v is None for v in [mpn, mfr]):
        return None

    return {
        "mpn": _strip(mpn),
        "manufacturerName": _strip(mfr),
        "quantity": _strip(qty),
        "condition": _strip(condition),
        "dateCode": _strip(date_code),
        "price": _strip(price),
        "vendorNumber": _strip(vendor_no),
        "vendor": _strip(vendor_name),
        "uploadedAt": _strip(uploaded),
        "owner": _strip(owner),
        "notes": _strip(notes)
    }


def _strip(value) -> Optional[str]:
    return value.strip() if value is not None else value
