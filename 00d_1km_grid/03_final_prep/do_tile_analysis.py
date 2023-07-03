#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:46:52 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import geopandas as gpd
import numpy as np
import statistics as st
import pandas as pd

logger = logging.getLogger(__name__)

class DoTileAnalysis(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='do_tile_analysis.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['file']
        out_file = self.params['out_file']

        df = gpd.read_file(file)
        new = df.astype({'tile_name':'str'})
        km = list(np.unique(new['tile_name']))
        
        results = pd.DataFrame(columns=['1km', '1deg', '5deg', 'mean_h', 'mean_cd', 'footprints'])
        for i in km:
            df_km = new.loc[new['tile_name']==i]
            df_km = df_km.dropna()
            #calculate canopy density
            rv = df_km['rv']
            rg = df_km['rg']
            cd = rv/(rv + rg)
            footprints = len(cd)
            
            if footprints<=30:
                continue
            #convert height to metres
            incm = df_km['rh100']
            h = incm/100
            
            #calculate means
            mean_cd = st.mean(cd)
            mean_h = st.mean(h)
            
            onedeg = list(df_km['tile_1deg'])[0]
            fivedeg = list(df_km['tile_5deg'])[0]
            
            results = results._append({'1km': i, '1deg':onedeg, '5deg':fivedeg,
                                      'mean_h': mean_h, 'mean_cd': mean_cd,
                                      'footprints':footprints}, 
                            ignore_index=True)
            
            results.to_csv(out_file)

    def required_fields(self, **kwargs):
        return ["file", "out_file"]


    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    DoTileAnalysis().std_run()