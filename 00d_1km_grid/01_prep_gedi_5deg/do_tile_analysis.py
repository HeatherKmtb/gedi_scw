#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas
from rasterstats import zonal_stats
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        gedi_file = self.params['gedi_file']
        out_file = self.params['out_file']
        grid = self.params["grid"]
                       
        beams = rsgislib.vectorutils.get_vec_lyrs_lst(gedi_file)
        stats = 'median'
        for beam in beams:
            vector = geopandas.read_file(gedi_file, layer=beam)
            
            result = zonal_stats(vector, grid, stats=stats, geojson_out=True)
            geostats = geopandas.GeoDataFrame.from_features(result, crs='EPSG:4326')
    
            geostats.to_file(out_file, layer = beam, driver='GPKG')



    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file", "grid"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()