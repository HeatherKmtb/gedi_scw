"adding 5 degree tile name to 1 degree file naming"

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
from pathlib import Path

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params['gedi_file']
        out_dir = self.params['out_dir']
        temp_file = self.params["temp_file"]
        basename = self.params["basename"]
                       
        beams = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_file)
        
        for beam in beams:
            df = gpd.read_file(gedi_file, layer = beam)
            tiles = df['tile_name_right']
            tile = tiles[0]
        
            df.to_file(out_dir + basename + '_' + tile + '.gpkg', layer = beam)
            
        Path(temp_file)    

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_dir", "temp_file", "basename"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()