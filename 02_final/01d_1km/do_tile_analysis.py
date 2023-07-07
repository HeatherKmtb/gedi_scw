#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 11:13:39 2022

@author: heatherkay
"""
from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
from scipy.stats import gaussian_kde
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

logger = logging.getLogger(__name__)

class ProcessJob(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='perform_processing.py', descript=None)

    def do_processing(self, **kwargs):
        file = self.params['gedi_file']
        out_fig_dir = self.params['out_fig_dir']
        out_csv_file = self.params['out_csv_file']
        #out_gpkg_file = self.params['out_gpkg_file']
        #quarter = self.params['quarter']
        #create df for results
        results = pd.DataFrame(columns = ['Grid', 'eco', 'qout_gedi', 'deg_free_gedi', 'mse_gedi',
                                           'mean_h_gedi', 'mean_cd_gedi'])

        #hd, tl = path.split(file)
        #shp_lyr_name = path.splitext(tl)[0]
        #name_comp = shp_lyr_name.split('_')
        #grid = name_comp[1] 
        #print(grid)

        df = pd.read_csv(file)
        new = df.astype({'1deg':'str'})
        tile = list(np.unique(new['1deg']))
        
        for i in tile:
            dfi = new.loc[new['1deg']==i]
                 
            #extra code to remove 1km squares without sufficient footprints to make a mean
            final = dfi[dfi['footprints']>=10]
            if final.empty:
                continue
            
            
            footprints = len(final['mean_cd'])
            
            if footprints < 50:
                continue
        
            #regression 
            def f(x,q):
               return 1- np.exp(-q * x)
    
            x = final['mean_h'].to_numpy()
            y = final['mean_cd'].to_numpy() 

            qout, qcov = curve_fit(f, x, y, 0.04)
            qout = qout.round(decimals=4)
        
            y_predict = f(x, qout)
            
            mse = mean_squared_error(y, y_predict)
            mse = round(mse, 3)        

            meanh = np.mean(x)
            meancd = np.mean(y)
        
            new_row = pd.Series({'Grid': i, 'qout_gedi': qout, 
                                    'deg_free_g': footprints, 
                                    'mse_g': mse,
                                    'mean_h_g': meanh, 'mean_cd_g': meancd})
            results = pd.concat([results, new_row.to_frame().T], 
                                    ignore_index=True)

            results.to_csv(out_csv_file)

            #xy = np.vstack([x,y])
            #z = gaussian_kde(xy)(xy)

            fig = plt.figure()
            ax = fig.add_sublot(1, 1, 1, projection='scatter_density')
            ax.scatter(x, y)
            plt.rcParams.update({'font.size':12}) 

            ax.set_title('Grid square ' + i)
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
            plt.savefig(out_fig_dir + 'fig{}.png'.format(i))
            plt.close 

    def required_fields(self, **kwargs):
        return ["gedi_file", "out_fig_dir", "out_csv_file"]

    def outputs_present(self, **kwargs):
        return True, dict()

    def remove_outputs(self, **kwargs):
        print("No outputs to remove")

if __name__ == "__main__":
    ProcessJob().std_run()