
import rsgislib.vectorutils
import rsgislib.vectorattrs

glb_tiles_vec_file = "/scratch/a.hek4/data/1km/grid.gpkg"
glb_tiles_vec_lyr = "grid"
glb_land_vec_file = "/scratch/a.hek4/gadm36_levels.gpkg"
glb_land_vec_lyr = "level0"

glb_land_tiles_vec_file = "glb_land_deg_tiles.geojson"
glb_land_tiles_vec_lyr = "glb_land_deg_tiles"

roi_file = '/scratch/a.hek4/data/1km/grid_land.geojson'
roi_lyr='grid'

rsgislib.vectorutils.spatial_select(glb_tiles_vec_file, glb_tiles_vec_lyr, glb_land_vec_file, glb_land_vec_lyr,
                                    roi_file, roi_lyr, out_format='GeoJSON')


rsgislib.vectorattrs.pop_bbox_cols(roi_file, roi_lyr, x_min_col='xmin',
                                   x_max_col='xmax', y_min_col='ymin', y_max_col='ymax')

out_vec_file = "glb_land_roi_deg_tiles_named_1km.geojson"
out_vec_lyr = "grid"

rsgislib.vectorattrs.create_name_col(roi_file, roi_lyr, out_vec_file, out_vec_lyr,
                                     out_format='GeoJSON', out_col='tile_name', x_col='xmin', y_col='ymax',
                                     prefix='grid_', coords_lat_lon=True, int_coords=True, zero_x_pad=9, zero_y_pad=6,
                                     round_n_digts=5, non_neg=True)

