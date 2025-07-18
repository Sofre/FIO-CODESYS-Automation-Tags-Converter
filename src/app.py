import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk

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

def parse_factoryio_csv(file_path):
    inputs = []
    outputs = []

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            variable = row.get("Name") or row.get("Variable")
            io_type = row.get("Type", "").capitalize()
            data_type_field = row.get("Data Type")

            if not variable or not io_type:
                continue

            variable = variable.strip()
            data_type = infer_data_type("", data_type_field)

            entry = {
                "Variable": variable,
                "Type": io_type,
                "Data Type": data_type,
                "Channel": 0 if io_type.lower() == 'input' else 1,
            }

            if io_type.lower() == 'input':
                inputs.append(entry)
            elif io_type.lower() == 'output':
                outputs.append(entry)

    # Assign IEC addresses
    for idx, item in enumerate(inputs):
        byte = idx // 8
        bit = idx % 8
        item["BitIndex"] = bit
        item["IEC_Address"] = f"%IX{byte}.{bit}"

    for idx, item in enumerate(outputs):
        byte = idx // 8
        bit = idx % 8
        item["BitIndex"] = bit
        item["IEC_Address"] = f"%QX{byte}.{bit}"

    return inputs + outputs

def save_parsed_tags(tags, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Variable", "Type", "Data Type", "IEC_Address", "Channel", "BitIndex"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in tags:
            writer.writerow(item)

def export_codesys_mapping(tags, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["//CoDeSys Mapping Export V1.2"])
        writer.writerow(["//Mapped variable,//Parameter name @ counter in device,//Unit,//Description,//IEC address,//Device name"])
        writer.writerow(["//Important: change only first, third or fourth column in Excel or add variable name before first"])

        channels = {}
        for tag in tags:
            ch = tag['Channel']
            channels.setdefault(ch, []).append(tag)

        for ch in sorted(channels.keys()):
            rw1 = ['', f'Channel {ch}', '', '', f'%I{"B" if ch == 0 else "Q"}{ch}0', 'Modbus_TCP_Server']
            rw1[3] = 'Read Discrete Inputs' if ch == 0 else 'Write Multiple Coils'
            writer.writerow(rw1)

            rw2 = ['', f'Channel {ch}[0]', '', rw1[3], rw1[4], rw1[5]]
            writer.writerow(rw2)

            for tag in channels[ch]:
                var_name = tag['Variable']
                bit_index = tag['BitIndex']
                bit_counter = f"Bit{bit_index}"
                if ch == 1:
                    bit_counter += "@1"

                row = [
                    var_name,
                    bit_counter,
                    '',
                    f"0x{bit_index:04X}",
                    tag['IEC_Address'],
                    'Modbus_TCP_Server'
                ]
                writer.writerow(row)

    print(f"CoDeSys mapping exported to: {filename}")
    os.startfile(filename)  # Open the file
    os.startfile(os.path.dirname(filename))  # Open the folder

def run_parser():
    input_path = filedialog.askopenfilename(title="Select FactoryIO Tags CSV", filetypes=[("CSV Files", "*.csv")])
    if not input_path:
        return

    base_dir = os.path.dirname(input_path)
    parsed_output = os.path.join(base_dir, "new_tags.csv")
    codesys_output = os.path.join(base_dir, "codesys_mapping_export.csv")

    try:
        tags = parse_factoryio_csv(input_path)
        save_parsed_tags(tags, parsed_output)
        export_codesys_mapping(tags, codesys_output)
        messagebox.showinfo("Success", f"Exported:\n• {parsed_output}\n• {codesys_output}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
app = tk.Tk()
app.title("CodeSys -> FIO Automation Tags Converter")
app.geometry("600x300")
app.resizable(False, False)
app.configure(bg='lightblue')

base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.normpath(os.path.join(base_dir, '..', 'assets', 'bg_image.jpg'))
    
print(f"Trying to open image at: {image_path}")  # Debug print

bg_image = Image.open(image_path).convert("RGBA")
black_overlay = Image.new("RGBA", bg_image.size, (0, 0, 0, 120))
tinted_image = Image.alpha_composite(bg_image, black_overlay)
bg_photo = ImageTk.PhotoImage(tinted_image)

bg_label = tk.Label(app, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)
bg_label.image = bg_photo


label = tk.Label(app, text="Convert FactoryIO Tags to CODESYS Mapping", font=("Helvetica", 12, "bold"))
label.pack(pady=20)

btn = tk.Button(app, text="Import FactoryIO CSV", command=run_parser, height=2, width=25, bg="#4CAF50", fg="white")
btn.pack()

footer = tk.Label(app, text="Built by Sofre", font=("Helvetica", 8, "bold","italic"), fg="black", bg='white')
footer.pack(side="bottom", pady=10)

app.mainloop()
