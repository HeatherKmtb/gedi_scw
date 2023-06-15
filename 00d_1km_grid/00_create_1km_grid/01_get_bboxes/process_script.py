
import rsgislib.vectorutils
import rsgislib.vectorattrs

glb_tiles_vec_file = "/scratch/a.hek4/data/1km/5deg_grid.gpkg"
glb_tiles_vec_lyr = "grid"
glb_land_vec_file = "/scratch/a.hek4/gedi_scw/glb_land_roi_deg_tiles_named.geojson"
glb_land_vec_lyr = "glb_land_roi_deg_tiles_named"

#glb_land_tiles_vec_file = "glb_land_deg_tiles.geojson"
#glb_land_tiles_vec_lyr = "glb_land_deg_tiles"

roi_file = '/scratch/a.hek4/data/1km/5deg_grid_land.geojson'
roi_lyr='grid'

print('files read')

rsgislib.vectorutils.spatial_select(glb_tiles_vec_file, glb_tiles_vec_lyr, glb_land_vec_file, glb_land_vec_lyr,
                                    roi_file, roi_lyr, out_format='GeoJSON')

print('done spatial select')

rsgislib.vectorattrs.pop_bbox_cols(roi_file, roi_lyr, x_min_col='xmin',
                                   x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')

