
# Programs

* convert_bed_to_fasta: Convert BED file to FASTA.

Usage:
```
python  src/potpourri/convert_bed_to_fasta.py -i  tests/test5/Ribo-seq_ORFs.bed -o  tests/test5/Ribo-seq_ORFs.fasta
```

Bed format:
http://genome.ucsc.edu/FAQ/FAQformat.html#format1

The first three required BED fields are:

  1. chrom - The name of the chromosome (e.g. chr3, chrY, chr2_random) or scaffold (e.g. scaffold10671).

  2. chromStart - The starting position of the feature in the chromosome or scaffold. The first base in a chromosome is numbered 0.

  3. chromEnd - The ending position of the feature in the chromosome or scaffold. The chromEnd base is not included in the display of the feature, however, the number in position format will be represented. For example, the first 100 bases of chromosome 1 are defined as chrom=1, chromStart=0, chromEnd=100, and span the bases numbered 0-99 in our software (not 0-100), but will represent the position notation chr1:1-100. Read more here.
  chromStart and chromEnd can be identical, creating a feature of length 0, commonly used for insertions. For example, use chromStart=0, chromEnd=0 to represent an insertion before the first nucleotide of a chromosome.

The 9 additional optional BED fields are:

  4.  name - Defines the name of the BED line. This label is displayed to the left of the BED line in the Genome Browser window when the track is open to full display mode or directly to the left of the item in pack mode.

  5.  score - A score between 0 and 1000. If the track line useScore attribute is set to 1 for this annotation data set, the score value will determine the level of gray in which this feature is displayed (higher numbers = darker gray). This table shows the Genome Browser's translation of BED score values into shades of gray:
  shade                  
  score in range    ≤ 166 167-277 278-388 389-499 500-611 612-722 723-833 834-944 ≥ 945

  6.  strand - Defines the strand. Either "." (=no strand) or "+" or "-".

  7.  thickStart - The starting position at which the feature is drawn thickly (for example, the start codon in gene displays). When there is no thick part, thickStart and thickEnd are usually set to the chromStart position.

  8.  thickEnd - The ending position at which the feature is drawn thickly (for example the stop codon in gene displays).

  9.  itemRgb - An RGB value of the form R,G,B (e.g. 255,0,0). If the track line itemRgb attribute is set to "On", this RBG value will determine the display color of the data contained in this BED line. NOTE: It is recommended that a simple color scheme (eight colors or less) be used with this attribute to avoid overwhelming the color resources of the Genome Browser and your Internet browser.

  10. blockCount - The number of blocks (exons) in the BED line.

  11. blockSizes - A comma-separated list of the block sizes. The number of items in this list should correspond to blockCount.

  12. blockStarts - A comma-separated list of block starts. All of the blockStart positions should be calculated relative to chromStart. The number of items in this list should correspond to blockCount.
  
