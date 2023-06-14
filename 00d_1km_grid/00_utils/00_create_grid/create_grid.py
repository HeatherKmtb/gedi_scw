
import rsgislib.vectorutils


bbox = [-180, 180, -54, 54]
out_vec = '/scratch/a.hek4/data/1km/grid.gpkg'


rsgislib.vectorutils.createvectors.define_grid(bbox=bbox, x_size = 0.01, y_size = 0.01, 
            in_epsg_code = 4326, out_vec=out_vec, out_vec_lyr='grid', out_format='GPKG')


