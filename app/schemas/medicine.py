def medicine_entity(item) -> dict:
    return {
        "smcid":str(item["smcid"]),
        "date":str(item["date"]),
        "medicine":str(item["medicine"]),
        "submission":str(item["submission"]),
        "indication":str(item["indication"]),
        "link_to":str(item["link_to"]),
    }

def medicines_entity(entity) -> list:
    return [medicine_entity(item) for item in entity]

def pricing_entity(item) -> dict:
    return {
        "smcid":str(item["smcid"]),
        "medicine":str(item["medicine"]),
        "price":float(item["price"])
    }

def pricings_entity(entity) -> list:
    return [pricing_entity(item) for item in entity]
