#!/bin/bash
#PBS -P xe2
#PBS -q normal
#PBS -l walltime=36:00:00
#PBS -l ncpus=2
#PBS -l mem=2G
#PBS -l jobfs=1G
#PBS -l storage=scratch/xf3+gdata/xf3
#PBS -l wd

source /home/106/ht5438/DE_analysis_snake/norm_cov/gadimod.sh

conda activate snakemake


set -ueo pipefail
logdir=gadi/log
mkdir -p $logdir
export TMPDIR=${PBS_JOBFS:-$TMPDIR}
TARGET=${TARGET:-all}

QSUB="qsub -q {cluster.queue} -l ncpus={cluster.threads} -l jobfs={cluster.jobfs}"
QSUB="$QSUB -l walltime={cluster.time} -l mem={cluster.mem} -N {cluster.name} -l storage=scratch/xf3+gdata/xf3"
QSUB="$QSUB -l wd -j oe -o $logdir -P {cluster.project}" 


snakemake																	    \
	-j 1000																	    \
	--max-jobs-per-second 2													    \
	--cluster-config /home/106/ht5438/DE_analysis_snake/norm_cov/cluster.yaml	\
	--local-cores ${PBS_NCPUS:-1}											    \
	--js /home/106/ht5438/DE_analysis_snake/norm_cov/jobscript.sh			    \
	--nolock																    \
	--keep-going															    \
	--rerun-incomplete														    \
	--use-envmodules														    \
	--cluster "$QSUB"														    \
	"$TARGET"


# snakemake																	    \
	# -j 1000																	    \
	# --max-jobs-per-second 2													    \
	# --cluster-config /home/106/ht5438/DE_analysis_snake/norm_cov/cluster.yaml	\
	# --local-cores ${PBS_NCPUS:-1}											    \
	# --js /home/106/ht5438/DE_analysis_snake/norm_cov/jobscript.sh			    \
	# --nolock																    \
	# --keep-going															    \
	# --rerun-incomplete														    \
	# --use-envmodules														    \
	# --cluster "$QSUB"														    \
	# "$TARGET"