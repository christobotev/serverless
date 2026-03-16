from typing import Dict, Optional


def get_model(row: list) -> Optional[Dict]:
    cust_no, cust_name, cust_po, trx_date, item_desc, order_no, lin_no, trx_qty, unit_price,\
    unit_cost, addt_cost, whse_cd, slsman_1, item_no, manu_no, cust_itmno, ship_no, lot_no,\
    ship_via, ship_method, shp_trck_no, invoice_no, country = row

    if any(v is None for v in [cust_name, order_no, cust_itmno, item_no]):
        return None

    return {
        "customer": {
            "name": cust_name.strip(),
            "number": cust_no.strip()
        },
        "order": {
            "orderNumber": to_int(order_no),
            "transactionDate": trx_date.strip(),
            "transactionQuantity": to_int(trx_qty),
            "unitPrice": to_float(unit_price),
            "unitCost": to_float(unit_cost),
            "additionalCost": to_float(addt_cost),
            "lineNumber": to_int(lin_no),
            "customerPurchaseOrder": _strip(cust_po),
            "warehouseCode": whse_cd,
            "salesman": _strip(slsman_1),
            "lotNumber": to_int(lot_no),
            "shipmentNumber": to_int(ship_no),
            "shipmentVia": to_int(ship_via),
            "shipmentTrackingNumber": _strip(shp_trck_no),
            "shipmentMethod": _strip(ship_method),
            "invoiceNumber": to_int(invoice_no),
            "country": _strip(country),
            "ipn": {
                "ipn": _strip(cust_itmno)
            }
        },
        "item": {
            "description": _strip(item_desc),
            "mpn": {
                "mpn": _strip(item_no),
                "manufacturerName": _strip(manu_no)
            }
        }
    }


def to_int(value):
    return int(value) if value is not None else value


def to_float(value):
    return float(value) if value is not None else value


def _strip(value):
    return value.strip() if value is not None else value
