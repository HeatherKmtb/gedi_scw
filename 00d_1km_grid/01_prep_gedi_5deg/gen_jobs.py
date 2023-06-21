#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 13:52:32 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import glob
import rsgislib
import rsgislib.vectorattrs
import os
import geopandas as gpd

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        gedi_files = glob.glob(kwargs['gedi_tiles'])
        #grid_dir = '/scratch/a.hek4/data/1km/grids/5deg_gridded_named/'
        
        grid = '/scratch/a.hek4/data/1km/glb_land_roi_deg_tiles_named_1km.geojson'

        for gedi_file in gedi_files:
            basename = self.get_file_basename(gedi_file)
            new_gedi_file = '/scratch/a.hek4/data/1_deg_q/10-9_with_renamed_cols/{}.gpkg'.format(basename)
            out_file = os.path.join(kwargs['out_dir'], f'{basename}.gpkg')
            beams = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_file)
            for beam in beams:
                file = gpd.read_file(gedi_file, layer = beam)
                new_file = file.rename(columns={'index_left':'ind_l','index_right':'ind_r'})
                new_file.to_file(new_gedi_file, layer = beam)

            if (not os.path.exists(out_file)):
                c_dict = dict()
                c_dict['gedi_file'] = new_gedi_file
                c_dict['out_file'] = out_file
                c_dict['grid'] = grid
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gedi_tiles='/scratch/a.hek4/data/1_deg_q/9-all_joined/*.gpkg',
            out_dir='/scratch/a.hek4/data/1km/1-5deg_prepped')


        self.pop_params_db()
        self.create_slurm_sub_sh("join_lc", 8224, '/scratch/a.hek4/logs', run_script="run_exe_analysis.sh",
                                  db_info_file=None, account_name='scw1403', n_cores_per_job=5, n_jobs=5, job_time_limit='2-23:59',
                                  module_load='module load parallel singularity\n')
        #self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=25, db_info_file="pbpt_db_info_lcl_file.txt")

if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.hek4/pbpt_db_info.txt",
                           lock_file_path="/scratch/a.hek4/tmp/gedi_lock_file.txt",
                           process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()