# FIO-CODESYS Automation Tags Converter Tool

## Project Overview

This small Python-based tool is built to automate the conversion and management of automation tags for Factory I/O (FIO) when integrated with CODESYS. Its primary function is to parse CSV tag files, modify device configurations, and significantly streamline the setup process for PLC automation projects.

The tool was created out of necessity—to eliminate the repetitive and error-prone manual task of configuring each input and output channel based on the exported mappings from Factory I/O.

In addition to the core automation functionality, the project includes:

- Project Architecture Overview

- Data State Definitions for improved understanding and easier troubleshooting

- Detailed Explanation of IEC Addressing, Channels, and Bit Positions—how they are derived and used

These resources are included to help users understand the logic behind the automated data tagging and facilitate easier debugging or future expansion.

The export format for CODESYS, as well as for Factory I/O, is subject to change with new updates. This means frequent adjustments to any integration scripts or tools may be necessary. A more sustainable and robust solution would be to acquire the official CODESYS SDK.

If anyone has access to the SDK or is willing to collaborate, feel free to reach out. With the right resources, we can develop a proper long-term tool—this current solution is only a temporary workaround.



---

## Features

- Parses CSV files containing automation tags with attributes such as name, type, data type, and address.
- Automatically infers data types when not explicitly specified.
- Uploades Factory IO mappings and automatically tags them or infers them if not explicitly specified.
- Edits and updates said CSV configuration files for CODESYS devices based on parsed tag data.
- GUI supported created with Tkinter GUI toolkit.

---

## Architecture and Data States

<!-- Insert Draw.io architecture diagram here -->

![Architecture Diagram](https://github.com/Sofre/FIO-CODESYS-Automation-Tags-Converter/blob/main/docs/Architecture%20of%20CodesysFIOMapper.drawio%20(1).png)

---

## Explanation for IEC Address , Channels and Bit Positions 


### IEC Addresses

IEC (International Electrotechnical Commission) defines a standard for addressing and accessing memory areas in PLCs and industrial controllers.

- **IEC Addresses** specify memory areas such as Inputs, Outputs, Memory, Timers, Counters, etc.
- Typical IEC address format includes a prefix that indicates the memory area, followed by an address specifying the byte or word location, and optionally a bit position for bit-level access.

### Common IEC Address Prefixes

| Prefix | Memory Area                 | Description                      |
|--------|-----------------------------|---------------------------------|
| `%I`   | Input                       | Digital Inputs                  |
| `%Q`   | Output                      | Digital Outputs                 |
| `%M`   | Memory                      | Internal memory bits or bytes  |
| `%T`   | Timer                       | Timer variables                |
| `%C`   | Counter                     | Counter variables              |

---

### Channels and Bit Positions

- **Channels** typically refer to the byte or word offset within a given memory area.
- **Bit Positions** specify the bit inside the byte or word (0 to 7 for a byte, 0 to 15 for a word).

### Addressing Examples

| IEC Address   | Explanation                                  |
|---------------|----------------------------------------------|
| `%IX0.0`      | Input byte 0, bit 0 (Channel 0, Bit 0)      |
| `%QX2.3`      | Output byte 2, bit 3 (Channel 2, Bit 3)     |
| `%MW10`       | Memory word at byte offset 10 (no bit level)|
| `%MX5.7`      | Memory byte 5, bit 7                         |

- `%IX` and `%QX` indicate input and output **bits**.
- `%IW` and `%QW` indicate input and output **words** (16 bits).
- `%MX` and `%MW` refer to internal memory bits and words.

---

## Summary

| Term          | Meaning                                  |
|---------------|------------------------------------------|
| IEC Address   | Standardized way to reference PLC memory areas, including bit-level addressing |
| Channel       | The byte or word number within a memory area |
| Bit Position  | The specific bit (0–7 or 0–15) within a byte or word |

---

---
## Usage

- Export Factory IO .csv file.
- Open src/app.py and attach the file.
- The file will automaticly be downloaded and opened with the folder dir in the background to let you know where it has been saved.
- Import the new .csv file into CODESYS.
- NOTE : Make sure beforehand that you have set up your channels purpose and lenght as they count as array data structures for the mappings. 



## Future Upgrades

- Add in options to set up channel configuration automaticly or in a easier and faster way than the more complicated way in CODESYS.
- Runnable .exe file and file saving choice for the user or a bare bone web application for easier usage.
  

---

## Contributing

- Feel free to contribute

  
## Contact
- Email: dukisofronievski@gmail.com
- Linkdin : https://www.linkedin.com/in/dushko-sofronievski-19044021b

---
