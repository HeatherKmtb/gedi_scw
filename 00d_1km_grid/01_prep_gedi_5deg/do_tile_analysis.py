#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas
import rsgislib.vectorutils
import rsgislib.vectorattrs
import geopandas as gpd

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params['gedi_file']
        out_file = self.params['out_file']
        grid = self.params["grid"]
                       
        beams = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_file)
        #stats = 'median'
        for beam in beams:
            file = gpd.read_file(gedi_file, layer = beam)
            new_file = file.rename(columns={'index_left':'ind_l','index_right':'ind_r'})
            print(new_file)
            print(beam)
            print(grid)
            print(out_file)
            rsgislib.vectorattrs.perform_spatial_join(new_file, beam, grid,
                                'glb_land_roi_deg_tiles_named_1km', out_file, beam,
                                out_format='GPKG', join_how='inner', join_op='within')

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file", "grid"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()