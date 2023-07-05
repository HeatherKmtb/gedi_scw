#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
from os import path
from scipy.stats import gaussian_kde
import geopandas
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import glob
from rsgislib import vectorutils
from sklearn.metrics import mean_squared_error

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_fig_dir = self.params['out_fig_dir']
        out_csv_file = self.params['out_csv_file']
        out_check_file = self.params['out_check_file']        #out_gpkg_file = self.params['out_gpkg_file']
        #quarter = self.params['quarter']
        #create df for results
        results = pd.DataFrame(columns = ['Grid', 'eco', 'qout_gedi', 'deg_free_g', 'mse_g',
                                           'mean_h_g', 'mean_cd_g', 'max_h_g'])


        hd, tl = path.split(file)
        shp_lyr_name = path.splitext(tl)[0]
        name_comp = shp_lyr_name.split('_')
        name = name_comp[1] 
        eco = name_comp[3]
        print(name)
        print(eco)
        
        layers = vectorutils.get_vec_lyrs_lst(file)
            
        df_list = [geopandas.read_file(file, layer=layer) for layer in layers]
        df = pd.concat(df_list)
         
        #calculate canopy density
        rv = df['rv']
        rg = df['rg']
        cd = rv/(rv + rg)
        
        rhov = df['rhov']
        rhog = df['rhog'] 
        f = rhov/rhog
        
        stepone = cd+f
        steptwo = 1-cd
        stepthree = stepone * steptwo
        new_cd = cd/stepthree
        #new_cd = cd/((cd+f)*(1-cd))
        
        df['cd'] = new_cd
        final = df.dropna(subset = ['cd'])
        
        df['f'] = f
        df['cd+f'] = stepone
        df['1-cd'] = steptwo
        df['(cd+f)(1-cd)'] = stepthree
        
        df.to_csv(out_check_file)
        
        
        #final.to_file(out_gpkg_file, layer = 'layer', driver='GPKG', crs='EPSG:4326')
        #convert height to metres
        incm = final['rh100']
        x = incm/100
        final['h100']=x 
        #final = final2[final2['h100']<=12]
        
        del x, rv, rg
                
        footprints = len(final['h100'])
        
        #regression 
        def f(x,q):
           return 1- np.exp(-q * x)
    
        x = final['h100'].to_numpy()
        y = final['cd'].to_numpy() 

        qout, qcov = curve_fit(f, x, y, 0.04)
        qout = qout.round(decimals=4)
        
        y_predict = f(x, qout)
            
        mse = mean_squared_error(y, y_predict)
        mse = round(mse, 3)        

        meanh = np.mean(x)
        meancd = np.mean(y)
        maxh = np.max(x)
        
        new_row = pd.Series({'Grid': name, 'eco':eco, 'qout_gedi': qout, 
                                    'deg_free_g': footprints, 
                                    'mse_g': mse,
                                    'mean_h_g': meanh, 'mean_cd_g': meancd, 
                                    'max_h_g': maxh})
        
        results = pd.concat([results, new_row.to_frame().T], 
                                    ignore_index=True)       

        results.to_csv(out_csv_file)

        xy = np.vstack([x,y])
        z = gaussian_kde(xy)(xy)

        fig, ax = plt.subplots()
        ax.scatter(x, y, c=z, s=10)
        plt.rcParams.update({'font.size':12}) 

        ax.set_title('Ecoregion ' + eco + 'in grid square ' + name)
        ax.set_ylabel('Canopy Density')
        ax.set_xlabel('Height - h100 (m)')
        ax.set_xlim([0, 60])
        ax.set_ylim([0,1])
        #plotting regression
        #putting x data in an order, cause that's what the code needs
        xdata = np.linspace(0, 60)
        #for each value of x calculating the corresponding y value
        ycurve = [f(t, qout) for t in xdata]
        #plotting the curve
        ax.plot(xdata, ycurve, linestyle='-', color='red')
        #adding qout, mse and deg_free to plot
        #ax.annotate('adj_r2 = ' + str(adj_r2[0]), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('q = ' + str(qout[0]), xy=(0.975,0.15), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('MSE = ' + str(mse), xy=(0.975,0.10), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        ax.annotate('No of footprints = ' + str(footprints),xy=(0.975,0.05), xycoords='axes fraction', fontsize=12, horizontalalignment='right', verticalalignment='bottom')
        plt.savefig(out_fig_dir + 'fig{}_{}.png'.format(name, eco))
        plt.close 

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_fig_dir", "out_csv_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()