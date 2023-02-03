#!/bin/bash --login

#SBATCH --account=scw1403
#SBATCH --partition=compute
#SBATCH --job-name=join_lc_4
#SBATCH --output=/scratch/a.hek4/logs/join_lc_4_log.out.%J
#SBATCH --error=/scratch/a.hek4/logs/join_lc_4_log.err.%J
#SBATCH --time=2-23:59
#SBATCH --ntasks=5
#SBATCH --mem-per-cpu=8224

module load parallel singularity


parallel -N 1 --delay .2 -j $SLURM_NTASKS < /scratch/a.hek4/gedi_scw/01b_1_degree_q/03_remove_lc_cats/job_scripts/jobcmds.sh

