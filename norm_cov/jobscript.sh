#!/bin/bash

source /home/106/ht5438/DE_analysis_snake/norm_cov/gadimod.sh

export TMPDIR=$PBS_JOBFS

set -ueo pipefail
{exec_job}