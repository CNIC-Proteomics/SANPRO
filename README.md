# sanpro

Programs designed for managing the iSanXoT results.


# File structure
```
|
├── basic
│   ├── diff_tables.py
│   ├── filter_table.py
│   ├── sort_table.py
│   ├── get_n_rows.py
├── positioner
│   ├── add_pep_position.py
├── potpurri
│   ├── convert_bed_to_fasta.py
├── README.md
└── .gitignore
```

**tests** folder contains test files. Note: This folder may not exist.

**potpourri** is a folder for discarding. It is a mixture of programs without an objective.


# Installation

## Download the repository

Download the SANPRO programs from the GitHub repository located at 
<br/><a href='https://github.com/CNIC-Proteomics/sanpro'>https://github.com/CNIC-Proteomics/sanpro</a>.

<img src='docs/github_sanpro_1.png'/>

Next, decompress the zip file.


## Can I run a Python script without typing "python" before the script name?

On Unix-based systems, you can add a shebang (#!/usr/bin/env python3) at the top of your script and make the script executable using the **chmod +x script.py** command.

On Windows, you can associate the .py extension with the Python interpreter.

Then, include the path of scripts into PATH environment variable.

On Unix-based systems:
```
export PATH=${PATH}:/U_Proteomica/UNIDAD/sanpro/basic
```

On Windows:
```
SETX PATH "%PATH%;S:\U_Proteomica\UNIDAD\sanpro\basic"
```

Retrieve the environment variables
```
SET
```

# Programs

## basic: programs for handling large files

* diff_tables: Retrieve the rows that differ based on specified columns from two tabular-separated files.

Usage:
```
python diff_tables.py -i1 tests/test1/scan2pdm_tagged.bak.tsv -i2 tests/test1/scan2pdm_tagged.tsv -o tests/test1/diff_table.tsv
```

* filter_table: Filter the given table file based on the provided conditions (header, operator, value).

Usage:
```
python filter_table.py -i tests/test2/scan2pdm_outStats.tsv -f "([tags] == 'out')" -o  tests/test2/scan2pdm_outStats.tags_out.tsv
```

* sort_table: Sort the table file (in tabular-separated format) based on the specified columns.

Usage:
```
python sort_table.py -i tests/test2/scan2pdm_outStats.tsv -s "idsup,Z,tags" -o tests/test2/scan2pdm_outStats.sorted.tsv
```

* get_n_rows: Retrieve the N rows from the given file.

Usage:
```
python get_n_rows.py -i tests/test2/scan2pdm_outStats.tsv -n 10 -o tests/test2/scan2pdm_outStats.n_rows.tsv
```

* remove_cols: Remove the specified columns from the table.

Usage:
```
python remove_cols.py -i tests/test2/scan2pdm_outStats.tsv -o tests/test2/scan2pdm_outStats.removed_cols.tsv -c "idinf,Xinf,Vinf"
```

* select_cols: Select the specified columns from the table.

Usage:
```
python select_cols.py -i tests/test2/scan2pdm_outStats.tsv -o tests/test2/scan2pdm_outStats.selected_cols.tsv -c "idsup , Xsup , Vsup , n , Z , FDR, tags"
```

* cmp_val_tables: Create a scatter plot using the column values from two tables (tabular-separated files).

Usage:
```
python cmp_val_tables.py -i1 tests/test3/scan2pdm_outStats.1.tsv  -i2 tests/test3/scan2pdm_outStats.2.tsv  -id1 "idsup,idinf"  -id2 "idsup,idinf"  -c1 "Z"  -c2 "Z"  -o tests/test3/scatterplot_1_vs_2.png
```


## positioner: programs that add positions

* add_pep_position: Include the peptide position within the protein in the report.

Usage:
```
python add_pep_position.py -i tests/test4/Npep2prot.tsv  -f tests/test4/mouse_202206_uni-sw-tr.target.fasta  -hp "peptide"  -hq "protein" -o tests/test4/Npep2prot.new.tsv
```



