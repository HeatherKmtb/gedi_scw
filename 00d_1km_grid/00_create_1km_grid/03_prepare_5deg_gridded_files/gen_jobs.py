from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib
import rsgislib.vectorattrs
import geopandas as gpd

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        grid_files = glob.glob(kwargs['tiles_vec_file'])
                 
        for file in grid_files:
            basename = self.get_file_basename(file)
            out_file = os.path.join(kwargs['out_dir'], f'{basename}.gpkg')

            if (not os.path.exists(out_file)):            
                c_dict = dict()
                c_dict['grid_file'] = file
                c_dict['grid_lyr'] = basename
                c_dict['out_file'] = out_file
                c_dict['out_lyr'] = basename
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            tiles_vec_file='/scratch/a.hek4/data/1km/grids/5deg_gridded/*.geojson',
            out_dir='/scratch/a.hek4/data/1km/grids/grids/5deg_gridded_named')


        self.pop_params_db()
        self.create_slurm_sub_sh("to_gpkg", 8224, '/scratch/a.hek4/logs', run_script="exe_analysis.sh",
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
