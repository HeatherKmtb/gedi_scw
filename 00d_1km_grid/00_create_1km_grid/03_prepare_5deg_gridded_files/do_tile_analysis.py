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
        grid_file = self.params['grid_file']
        grid_lyr = self.params['grid_lyr']
        out_file = self.params['out_file']
        out_lyr = self.params['out_lyr']
        
        rsgislib.vectorattrs.pop_bbox_cols(grid_file, grid_lyr, x_min_col='xmin',
                                   x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')


        rsgislib.vectorattrs.create_name_col(grid_file, grid_lyr, out_file, out_lyr,
                                     out_format='GeoJSON', out_col='tile_name', x_col='xmin', y_col='ymax',
                                     prefix='grid_', coords_lat_lon=True, int_coords=True, zero_x_pad=4, zero_y_pad=4,
                                     round_n_digts=5, non_neg=True)

    def required_fields(self, **kwargs):
        return ["grid_file", "grid_lyr", "out_file", "out_lyr"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print('No outputs to remove')

if __name__ == "__main__":
    DoTileAnalysis().std_run()
