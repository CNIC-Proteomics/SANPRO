# sanpro

Programs designed for managing the iSanXoT results.


# File structure
```
├── tests
│   ├── test1
├── src
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


# Programs

## basic: programs for handling large files

* diff_tables: Retrieve the rows that differ based on specified columns from two tabular-separated files.

Usage:
```
python basic/diff_tables.py -i1 tests/test1/scan2pdm_tagged.bak.tsv -i2 tests/test1/scan2pdm_tagged.tsv -o tests/test1/diff_table.tsv
```

* filter_table: Filter the given table file based on the provided conditions (header, operator, value).

Usage:
```
python basic/filter_table.py -i tests/test2/scan2pdm_outStats.tsv -f "([tags] == 'out')" -o  tests/test2/scan2pdm_outStats.tags_out.tsv
```

* sort_table: Sort the table file (in tabular-separated format) based on the specified columns.

Usage:
```
python basic/sort_table.py -i tests/test2/scan2pdm_outStats.tsv -s "idsup,Z,tags" -o tests/test2/scan2pdm_outStats.sorted.tsv
```

* get_n_rows: Retrieve the N rows from the given file.

Usage:
```
python basic/get_n_rows.py -i tests/test2/scan2pdm_outStats.tsv -n 10 -o tests/test2/scan2pdm_outStats.n_rows.tsv
```

* cmp_val_tables: Create a scatter plot using the column values from two tables (tabular-separated files).

Usage:
```
python basic/cmp_val_tables.py -i1 tests/test3/scan2pdm_outStats.1.tsv  -i2 tests/test3/scan2pdm_outStats.2.tsv  -id1 "idsup,idinf"  -id2 "idsup,idinf"  -c1 "Z"  -c2 "Z"  -o tests/test3/scatterplot_1_vs_2.png
```

## positioner: programs that add positions

* add_pep_position: Include the peptide position within the protein in the report.

Usage:
```
python positioner/add_pep_position.py -i tests/test4/Npep2prot.tsv  -f tests/test4/mouse_202206_uni-sw-tr.target.fasta  -hp "peptide"  -hq "protein" -o tests/test4/Npep2prot.new.tsv
```
