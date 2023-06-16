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

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_file = self.params['out_file']
        grid_file = self.params["grid_file"]
                       
        beams = ['BEAM0101','BEAM0110',
                 'BEAM1000','BEAM1011']
        stats = 'tile_name'
        for beam in beams:
            vector = geopandas.read_file(file, layer=beam)
            
            result = zonal_stats(vector, grid_file, stats=stats, geojson_out=True)
            geostats = geopandas.GeoDataFrame.from_features(result, crs='EPSG:4326')
    
            geostats.to_file(out_file, layer = beam, driver='GPKG')

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_file", "grid_file"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()