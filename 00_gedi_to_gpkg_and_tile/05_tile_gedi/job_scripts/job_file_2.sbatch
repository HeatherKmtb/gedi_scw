#!/bin/bash --login

#SBATCH --partition=compute
#SBATCH --job-name=tile_gedi_data_2
#SBATCH --output=/scratch/a.hek4/logs/tile_gedi_data_2_log.out.%J
#SBATCH --error=/scratch/a.hek4/logs/tile_gedi_data_2_log.err.%J
#SBATCH --time=2-23:59
#SBATCH --ntasks=10
#SBATCH --mem-per-cpu=16448

module load parallel singularity


parallel -N 1 --delay .2 -j $SLURM_NTASKS < /scratch/a.hek4/gedi_scw/00_gedi_to_gpkg_and_tile/05_tile_gedi/job_scripts/jobcmds.sh

