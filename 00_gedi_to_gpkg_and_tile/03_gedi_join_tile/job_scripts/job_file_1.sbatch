#!/bin/bash --login

#SBATCH --account=scw1403
#SBATCH --partition=compute
#SBATCH --job-name=to_gpkg_1
#SBATCH --output=/scratch/a.hek4/logs/to_gpkg_1_log.out.%J
#SBATCH --error=/scratch/a.hek4/logs/to_gpkg_1_log.err.%J
#SBATCH --time=2-23:59
#SBATCH --ntasks=5
#SBATCH --mem-per-cpu=8224

module load parallel singularity


parallel -N 1 --delay .2 -j $SLURM_NTASKS < /scratch/a.hek4/gedi_scw/00_gedi_to_gpkg_and_tile/03_gedi_join_tile/job_scripts/jobcmds.sh

