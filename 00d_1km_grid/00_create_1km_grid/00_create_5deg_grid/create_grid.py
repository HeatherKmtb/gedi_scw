"create a 5 degree grid for GEDI coverage area"


import rsgislib.vectorutils.createvectors


bbox = [-180, 180, -54, 54]
out_vec = '/scratch/a.hek4/data/1km/5deg_grid.gpkg'


rsgislib.vectorutils.createvectors.define_grid(bbox=bbox, x_size = 5, y_size = 5, 
            in_epsg_code = 4326, out_vec=out_vec, out_vec_lyr='grid', out_format='GPKG')


