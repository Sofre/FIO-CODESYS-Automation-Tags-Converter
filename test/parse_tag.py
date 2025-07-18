import csv

def factoryio_to_codesys_tag(name, type_, data_type, address):
    # Parse 'Input 0', 'Input 1' etc.
    parts = address.strip().split()
    if len(parts) != 2:
        raise ValueError(f"Invalid address format: {address}")
    direction, index_str = parts
    index = int(index_str)

    byte = index // 8
    bit = index % 8

    # Compose CODESYS address for BOOLs
    if data_type.lower() == 'bool':
        if direction.lower() == 'input':
            codesys_address = f"%IX{byte}.{bit}"
        elif direction.lower() == 'output':
            codesys_address = f"%QX{byte}.{bit}"
        else:
            codesys_address = address  # fallback
    else:
        # For non-BOOLs, word level addressing
        if direction.lower() == 'input':
            codesys_address = f"%IW{byte}"
        elif direction.lower() == 'output':
            codesys_address = f"%QW{byte}"
        else:
            codesys_address = address

    variable_name = f"{name.strip().replace(' ', '_')}_{direction}_{bit}"

    channel = bit
    comment = f"{direction} bit {bit} for {name.strip()}"

    return {
        "Variable": variable_name,
        "Type": type_,
        "Data Type": data_type,
        "Address": codesys_address,
        "Channel": channel,
        "Comment": comment
    }

def parse_csv_tags(csv_file):
    tags = []
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            print("Detected headers:", headers)

            for row in reader:
                try:
                    tag = factoryio_to_codesys_tag(
                        row['Name'],
                        row['Type'],
                        row['Data Type'],
                        row['Address']
                    )
                    tags.append(tag)
                except Exception as e:
                    print(f"Skipping row due to error: {e}")

    except Exception as e:
        print(f"CSV Parse Error: {e}")

    return tags

if __name__ == '__main__':
    csv_file = 'C:/Users/Duki/codesys-xml-autogen/data/tags.csv'  # Adjust path as needed
    tags = parse_csv_tags(csv_file)
    for tag in tags:
        print(tag)
