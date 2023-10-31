#!/usr/bin/bash

# Declare variables
CODEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd -P)"
DATE="$(date +"%Y%m")" # create date
TMPDIR="${CODEDIR}/tmp/${DATE}"
DATDIR="${CODEDIR}/data/${DATE}"
SPECIES_LIST=(human mouse rat pig zebrafish chicken)
XREFDATE="202306"
XREFDIR="/mnt/tierra/U_Proteomica/UNIDAD/iSanXoT_DBs/${XREFDATE}"
APPRIS_DAT="${DATDIR}/appris.gtf"

# Function that executes the input command
run_cmd () {
  echo "-- $1"
  echo ""
  eval $1
}


echo "preparing workspace..."
run_cmd "mkdir -p '${TMPDIR}'"
run_cmd "mkdir -p '${DATDIR}'"
run_cmd "rm '${APPRIS_DAT}'"


echo "going through the species..."
for SPECIES in "${SPECIES_LIST[@]}"
do
    # get local variables
    XREFFILE="${XREFDIR}/${SPECIES}/categories/${SPECIES}_${XREFDATE}.uniprot.tsv"
    APPRISDIR="${TMPDIR}/${SPECIES}"
    OUTFILE="${DATDIR}/${SPECIES}_${DATE}.appris.gtf"
    LOGFILE="${TMPDIR}/appris_db.${SPECIES}.log"

    # execute the program:
    # The following script downloads the annotations for the APPRIS methods that locate the annotation in a specific region of the protein.
    CMD1="python '${CODEDIR}/positioner/download_appris.py' -s ${SPECIES} -o '${APPRISDIR}' -vv  &> '${LOGFILE}' "
    # Convert the method annotations in GTF format to another GTF that references the protein region
    CMD2="python '${CODEDIR}/positioner/convert_appris.py' -ia '${APPRISDIR}/*.gtf' -iu '${XREFFILE}' -o ${OUTFILE} -vv  &>> '${LOGFILE}' "
    run_cmd "${CMD1} && ${CMD2}"

    # concatenate the APPRIS annotations
    if [ -f "${APPRIS_DAT}" ]; then
      CMD3="tail -n +2 '${OUTFILE}' >> '${APPRIS_DAT}'"
    else
      CMD3="cat '${OUTFILE}' > '${APPRIS_DAT}'"
    fi
    run_cmd "${CMD3}"
done