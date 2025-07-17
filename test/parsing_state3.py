import csv

def export_codesys_mapping(tags, filename):
  with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header comment lines
        writer.writerow(["//CoDeSys Mapping Export V1.2"])
        writer.writerow(["//Mapped variable,//Parameter name @ counter in device,//Unit,//Description,//IEC address,//Device name"])
        writer.writerow(["//Important: change only first, third or fourth column in Excel or add variable name before first"])

        # Group tags by Channel (0 or 1)
        channels = {}
        for tag in tags:
            ch = tag['Channel']
            channels.setdefault(ch, []).append(tag)

        # Write each channel block
        for ch in sorted(channels.keys()):
            # Write channel main line
            rw1 = ['', f'Channel {ch}', '', 'Read Discrete Inputs' if ch == 0 else 'Write Multiple Coils', f'%I{"B" if ch == 0 else "Q"}{ch}0', 'Modbus_TCP_Server']
            if ch == 1:
                rw1[3] = 'Write Multiple Coils'
            else:
                rw1[3] = 'Read Discrete Inputs'
            writer.writerow(rw1)

            # Write channel bit array line
            rw2 = ['', f'Channel {ch}[0]', '', rw1[3], rw1[4], rw1[5]]
            writer.writerow(rw2)

            # Write each tag in channel
            for tag in channels[ch]:
                var_name = tag['Variable']
                bit_index = tag['BitIndex']
                bit_counter = f"Bit{bit_index}"
                if ch == 1:
                    bit_counter += "@1"  # output channel bit suffix
                
                # Address: use %IX or %QX with byte.bit notation
                iec_address = tag['IEC_Address']  # e.g. %IX0.0 or %QX0.0
                
                # Compose CSV row
                row = [
                    var_name,
                    bit_counter,
                    '',  # Unit empty (you can customize if needed)
                    f"0x{bit_index:04X}",  # Description as hex address string
                    iec_address,
                    'Modbus_TCP_Server'
                ]
                writer.writerow(row)

# Example tag data for testing
tags = [
    # Inputs channel 0
    {"Variable": "ItemEntry", "Type": "Input", "Data Type": "Bool", "BitIndex": 0, "Channel": 0, "IEC_Address": "%IX0.0"},
    {"Variable": "ItemExit", "Type": "Input", "Data Type": "Bool", "BitIndex": 1, "Channel": 0, "IEC_Address": "%IX0.1"},
    {"Variable": "MovingX", "Type": "Input", "Data Type": "Bool", "BitIndex": 2, "Channel": 0, "IEC_Address": "%IX0.2"},
    {"Variable": "MovingZ", "Type": "Input", "Data Type": "Bool", "BitIndex": 3, "Channel": 0, "IEC_Address": "%IX0.3"},
    {"Variable": "Itemdet", "Type": "Input", "Data Type": "Bool", "BitIndex": 4, "Channel": 0, "IEC_Address": "%IX0.4"},
    {"Variable": "Start", "Type": "Input", "Data Type": "Bool", "BitIndex": 5, "Channel": 0, "IEC_Address": "%IX0.5"},
    {"Variable": "Reset", "Type": "Input", "Data Type": "Bool", "BitIndex": 6, "Channel": 0, "IEC_Address": "%IX0.6"},
    {"Variable": "Stop", "Type": "Input", "Data Type": "Bool", "BitIndex": 7, "Channel": 0, "IEC_Address": "%IX0.7"},

    # Outputs channel 1
    {"Variable": "EntryCon", "Type": "Output", "Data Type": "Bool", "BitIndex": 0, "Channel": 1, "IEC_Address": "%QX0.0"},
    {"Variable": "ExitCon", "Type": "Output", "Data Type": "Bool", "BitIndex": 1, "Channel": 1, "IEC_Address": "%QX0.1"},
    {"Variable": "MoveX", "Type": "Output", "Data Type": "Bool", "BitIndex": 2, "Channel": 1, "IEC_Address": "%QX0.2"},
    {"Variable": "MoveY", "Type": "Output", "Data Type": "Bool", "BitIndex": 3, "Channel": 1, "IEC_Address": "%QX0.3"},
    {"Variable": "Grab", "Type": "Output", "Data Type": "Bool", "BitIndex": 4, "Channel": 1, "IEC_Address": "%QX0.4"},
    {"Variable": "SLight", "Type": "Output", "Data Type": "Bool", "BitIndex": 5, "Channel": 1, "IEC_Address": "%QX0.5"},
    {"Variable": "RLight", "Type": "Output", "Data Type": "Bool", "BitIndex": 6, "Channel": 1, "IEC_Address": "%QX0.6"},
    {"Variable": "StopLight", "Type": "Output", "Data Type": "Bool", "BitIndex": 7, "Channel": 1, "IEC_Address": "%QX0.7"},
]

# Export to CSV file
export_codesys_mapping(tags, "codesys_mapping_export.csv")
print("Export complete.")

# This code defines a function to export a mapping of tags to a CSV file in a format suitable for CoDeSys.
# It includes example tag data for testing and demonstrates how to write the CSV file with appropriate headers and data.
# This structure is designed to match the expected format for CoDeSys, with channels and bit addressing. I got this structure from exporting a CoDeSys project to CSV.
# What is left is to see how we can format the data from factoryio to match this structure.
