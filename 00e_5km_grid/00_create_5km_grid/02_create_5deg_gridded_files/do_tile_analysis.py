"splitting into 5 degree tiles and creating a 1km grid for each of these"

from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import tqdm
import rsgislib.vectorutils.createvectors
import rsgislib.vectorattrs
import rsgislib.tools.utils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        bbox = self.params['bbox']
        out_file = self.params['out_file']
        out_lyr = self.params['out_lyr']
        
        rsgislib.vectorutils.createvectors.define_grid(bbox=bbox, x_size = 0.01, y_size = 0.01, 
                    in_epsg_code = 4326, out_vec=out_file, out_vec_lyr=out_lyr, out_format='GPKG')


    def required_fields(self, **kwargs):
        return ["bbox", "out_file", "out_lyr"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print('No outputs to remove')

if __name__ == "__main__":
    DoTileAnalysis().std_run()
