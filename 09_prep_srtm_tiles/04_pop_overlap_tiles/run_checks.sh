#singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif python gen_jobs.py --check


singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.hek4/gedi_files_2021_12_16/data/srtm/srtm_overlap_tiles/*.kea" --rmerr --printerrs \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum

