#!/bin/bash
#
#  usage: $0 [ --PU ] [ --events N ] job  /store/path/output_file.root 
#
TMPDIR=$PWD
#### ENV
SRC=$1; shift
CMSSWNANO=$1; shift
STEP5=Run18_106X_step5Nano_13010_cfg.py

FILESPY=$1
shift;

if [[ "$1" == "--events" ]]; then
    EVNUM=$2; shift; shift;
fi;

JOB=$1
shift;

OUTFILE=$1

OUTBASE=$(basename $OUTFILE .root)
echo "Will write to $OUTFILE";
shift;

## Create output directories
OUTDIR=/eos/cms$(dirname $OUTFILE)
eos ls $OUTDIR || eos mkdir -p $OUTDIR

### ENVIRONMENT STEP
cd $SRC/$CMSSWNANO; 
export SCRAM_ARCH=el8_amd64_gcc11
if [[ "$LD_LIBRARY_PATH" == "" ]] ; then
    CMSSW_BASE_VERSION=${CMSSW_VERSION%_patch*}
    if [[ "$CMSSW_BASE_VERSION" != "$CMSSW_VERSION" ]]; then # patch release
        export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/${SCRAM_ARCH}/cms/cmssw-patch/${CMSSW_VERSION}/external/${SCRAM_ARCH}/lib ;
    else
        export LD_LIBRARY_PATH=/cvmfs/cms.cern.ch/${SCRAM_ARCH}/cms/cmssw/${CMSSW_VERSION}/external/${SCRAM_ARCH}/lib ;
    fi;
fi
eval $(scramv1 runtime -sh)
cd $TMPDIR;

echo "All the parameters"
echo $FILESPY
echo $SRC
echo $OUTBASE
echo $OUTDIR
echo $JOB
echo $OUTFILE
echo $EVNUM
echo $FIRSTLUMI


echo "Step NanoAOD"

cat $SRC/$STEP5 > $OUTBASE.step5_cfg.py
echo -n "process.source.fileNames = " >> $OUTBASE.step5_cfg.py
sed -n '/^files = \[/,/\]/p' "$SRC/$FILESPY" | sed 's/^files = //' >> $OUTBASE.step5_cfg.py

cat >> $OUTBASE.step5_cfg.py <<_EOF_
## Input and output
process.maxEvents.input = cms.untracked.int32($EVNUM)
process.source.skipEvents = cms.untracked.uint32($JOB*$EVNUM)
## Scramble
import random
rnd = random.SystemRandom()
for X in process.RandomNumberGeneratorService.parameterNames_(): 
    if X != 'saveFileName': getattr(process.RandomNumberGeneratorService,X).initialSeed = rnd.randint(1,99999999)
_EOF_
cp $OUTBASE.step5_cfg.py $SRC/ciaociaonano.py
cmsRun $OUTBASE.step5_cfg.py 
STEP5OUT=step5.root
test -f $TMPDIR/${STEP5OUT}  || exit 41
edmFileUtil --ls file:$TMPDIR/${STEP5OUT} | grep events        || exit 42
edmFileUtil --ls file:$TMPDIR/${STEP5OUT} | grep ', 0 events'  && exit 43


echo "making directory /eos/cms/${OUTFILE}/Nano"

mkdir -p /eos/cms/${OUTFILE}/Nano
ls /eos/cms/${OUTFILE}/

cp ${STEP5OUT} /eos/cms/${OUTFILE}/Nano/job_${JOB}_${STEP5OUT}
echo "copied ${STEP5OUT} into /eos/cms/${OUTFILE}/Nano/job_${JOB}_${STEP5OUT}"


