import re


def parse_name(name):
    # Expected incoming format: "Last, First Middle" or "Last, First"
    parts = name.split(", ")
    
    if len(parts) != 2:
        return "", "", parts[0] if parts else ""
    
    last_name = parts[0].strip()

    first_middle = parts[1].strip().split()
    first_name = first_middle[0] if first_middle else ""
    
    middle_name = first_middle[1] if len(first_middle) > 1 else ""

    return first_name, middle_name, last_name

def parse_address(address):

    # Expected incoming format: "123 Main St Apt 42, Springfield, CA, 90210"
    parts = address.rsplit(", ", 2)

    if len(parts) < 3:
        return address, "", "", "", "", ""
    
    city_state_zip = parts[-1].strip()
    city_state = parts[-2].strip()
    address_lines = parts[0].strip()
    
    # Extract zip
    zip_match = re.search(r"\d{5}", city_state_zip)
    zip_code = zip_match.group(0) if zip_match else ""
    
    # Extract state (assume 2-letter code before zip)
    state_match = re.search(r"[A-Z]{2}", city_state_zip)
    state = state_match.group(0) if state_match else ""
    
    # City is what's left in city_state
    city = city_state
    
    # Split address_lines into address1, address2, address3
    addr_parts = address_lines.split(" Apt ")
    address1 = addr_parts[0].strip()
    address2 = f"Apt {addr_parts[1].strip()}" if len(addr_parts) > 1 else ""
    address3 = ""
    
    return address1, address2, address3, city, state, zip_code