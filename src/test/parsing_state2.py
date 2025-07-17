import csv
import re

def infer_data_type(address, data_type_field=None):
    if data_type_field:
        dt = data_type_field.lower()
        if dt in ['bool', 'boolean']:
            return "Bool"
        elif dt in ['int', 'integer']:
            return "Int"
        elif dt in ['dint', 'doubleint']:
            return "DInt"
        elif dt in ['real', 'float', 'double']:
            return "Real"
        else:
            return "Unknown"

    if address.startswith("%IX") or address.startswith("%QX"):
        return "Bool"
    elif address.startswith("%IW") or address.startswith("%QW"):
        return "Int"
    elif address.startswith("%ID") or address.startswith("%QD"):
        return "DInt"
    elif address.startswith("%MD"):
        return "Real"
    else:
        return "Unknown"

def infer_channel(address, io_type):
    if io_type.lower() == 'input':
        return 0
    elif io_type.lower() == 'output':
        return 1

    if address.startswith("%I"):
        return 0
    elif address.startswith("%Q"):
        return 1
    return -1

def parse_factoryio_csv(file_path):
    inputs = []
    outputs = []

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variable = row.get("Name") or row.get("Variable")
            io_type = row.get("Type", "").capitalize()
            data_type_field = row.get("Data Type")
            # ignore incoming address, we will reassign
            if not variable or not io_type:
                continue
            variable = variable.strip()

            data_type = infer_data_type("", data_type_field)  # ignore address on infer

            entry = {
                "Variable": variable,
                "Type": io_type,
                "Data Type": data_type,
                "Channel": 0 if io_type.lower() == 'input' else 1,
                # IEC_Address and BitIndex will be assigned later
            }

            if io_type.lower() == 'input':
                inputs.append(entry)
            elif io_type.lower() == 'output':
                outputs.append(entry)

    # Assign IEC addresses for inputs (starting %IX0.0)
    for idx, item in enumerate(inputs):
        byte = idx // 8
        bit = idx % 8
        item["BitIndex"] = bit
        item["IEC_Address"] = f"%IX{byte}.{bit}"

    # Assign IEC addresses for outputs (starting %QX0.0)
    for idx, item in enumerate(outputs):
        byte = idx // 8
        bit = idx % 8
        item["BitIndex"] = bit
        item["IEC_Address"] = f"%QX{byte}.{bit}"

    return inputs + outputs

if __name__ == "__main__":
    data = parse_factoryio_csv("C:/Users/Duki/codesys-xml-autogen/data/Tags_Production Line_Modbus TCP_IP Server_2025-07-15-11-34-56.csv")

    output_file = "C:/Users/Duki/codesys-xml-autogen/data/parsed_tags.csv"
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Variable", "Type", "Data Type", "IEC_Address", "Channel", "BitIndex"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    print(f"Parsed and re-addressed tags saved to: {output_file}")

    # Or simply use 'data' list for further processing in your app
