singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif rsgischkgdalfile.py -i "/scratch/a.hek4/data/1_deg_q/1.filter_for_quality/GEDI02_B_2019_Q2/*.gpkg" --vec --rmerr --printerr --epsg 4326 --chkproj

