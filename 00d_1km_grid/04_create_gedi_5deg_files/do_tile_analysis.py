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
        gedi_file_list = self.params['gedi_file_list']
        out_file = self.params['out_file']

        rsgislib.vectorutils.merge_vector_files(gedi_file_list, out_file, out_format='GPKG')  

    def required_fields(self, **kwargs):
        return ["gedi_file_list", "out_file"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()