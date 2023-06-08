#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:10:09 2022

@author: heatherkay
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 13:52:32 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import os.path
import logging
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_fig_dir']):
            os.mkdir(kwargs['out_fig_dir'])
            
        if not os.path.exists(kwargs['out_csv_dir']):
            os.mkdir(kwargs['out_csv_dir'])

        gedi_files = glob.glob(kwargs['gedi_tiles'])
        

        for gedi_file in gedi_files:
            basename = self.get_file_basename(gedi_file)
            out_csv_file = os.path.join(kwargs['out_csv_dir'], f'{basename}.csv')
            #out_gpkg_file = os.path.join(kwargs['out_gpkg_dir'], f'{basename}.gpkg')

            if (not os.path.exists(out_csv_file)):
                c_dict = dict()
                c_dict['gedi_file'] = gedi_file
                c_dict['out_fig_dir'] = '/scratch/a.hek4/results/1_deg/figs/wwf_grid/10m'
                c_dict['out_csv_file'] = out_csv_file
                #c_dict['out_gpkg_file'] = out_gpkg_file
                #c_dict['results'] = results
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gedi_tiles='/scratch/a.hek4/data/1_deg_q/wwf/2-split_per_eco/*.gpkg',
            out_fig_dir='/scratch/a.hek4/results/1_deg/figs/wwf_grid/10m/',
            out_csv_dir='/scratch/a.hek4/results/1_deg/csvs/wwf_grid/10m/')
            #out_gpkg_dir='/scratch/a.hek4/data/1_deg_q/10-with_cd/'
            #ALSO CHANGE QUARTER AND OUT_FIG_DIR IN C_DICT ABOVE
        
        self.pop_params_db()

        self.create_slurm_sub_sh("final", 8224, '/scratch/a.hek4/logs', run_script="exe_analysis.sh",
                                  db_info_file=None, account_name='scw1403', n_cores_per_job=5, n_jobs=5, job_time_limit='2-23:59',
                                  module_load='module load parallel singularity\n')
        
if __name__ == "__main__":
    py_script = os.path.abspath("do_tile_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.hek4:/scratch/a.hek4 --bind /home/a.hek4:/home/a.hek4 /scratch/a.hek4/swimage/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'do_tile_analysis'
    process_tools_cls = 'DoTileAnalysis'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.hek4/pbpt_db_info.txt",
                           lock_file_path="/scratch/a.hek4/tmp/gedi_lock_file.txt",
                           process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)   
    create_tools.parse_cmds()