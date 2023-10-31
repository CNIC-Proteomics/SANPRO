
# Installation

## Download the repository

Download the SANPRO programs from the GitHub repository located at 
<br/><a href='https://github.com/CNIC-Proteomics/SANPRO'>https://github.com/CNIC-Proteomics/SANPRO</a>.

<img src='docs/github_sanpro_1.png'/>

Next, decompress the zip file.

<!--
## Can I run a Python script without typing "python" before the script name?

On Unix-based systems, you can add a shebang (#!/usr/bin/env python3) at the top of your script and make the script executable using the **chmod +x script.py** command.

On Windows, you can associate the .py extension with the Python interpreter.

Then, include the path of scripts into PATH environment variable.

On Unix-based systems:
```
export PATH=${PATH}:/U_Proteomica/UNIDAD/SANPRO/basic
```

On Windows:
```
SETX PATH "%PATH%;S:\U_Proteomica\UNIDAD\SANPRO\basic"
```

Retrieve the environment variables
```
SET
```
-->

## Prerequisities

You need to install the Python programming language and the following packages. To install these packages, you can use the pip module in Python:

```
pip install -r python_requirements.txt
```

## Requirements for the "get_appris" program

The "get_appris" service requires the APPRIS data files. To obtain these files for a specific species, you need to execute the following bash script:
```bash
./create_appris_dbs.sh
```

This bash script contains the following programs:

The following script downloads annotations for the APPRIS methods that locate annotations in specific regions of the protein:
```bash
python download_appris.py    -s human     -o test/appris       -vv  &> logs/download_apprishuman.log
```

Additionally, to convert the method annotations in GTF format to another GTF format that references the protein region, you can use:
```bash
python  convert_appris.py  -ia "test/appris/*.gtf"  -iu "test/human_202306.uniprot.tsv" -o "test/appris/human_202306.appris.gtf"
```
