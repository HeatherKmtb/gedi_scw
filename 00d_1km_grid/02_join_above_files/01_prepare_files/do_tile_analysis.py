#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas as gpd
from rasterstats import zonal_stats
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params['gedi_file']
        out_file = self.params['out_file']
                       
        beams = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_file)

        for beam in beams:
                file = gpd.read_file(gedi_file, layer = beam)
                new_file = file.rename(columns={'index_right':'ind_r', 'tile_name_left':
                                    'tile_1deg', 'tile_name_right':'tile_5deg'})
                new_file.to_file(out_file, layer = beam)

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()