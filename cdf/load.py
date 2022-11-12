import os
from django.contrib.gis.utils import LayerMapping
from cdf.models import CdfProjects,Boundary

cdfprojects_mapping = {
    'project': 'project',
    'descrition': 'descrition',
    'remarks': 'remarks',
    'sectors': 'sectors',
    'amount': 'Amount',
    'status': 'status',
    # 'lat': 'Lat',
    'county_nam': 'county_nam',
    'location': 'location',
    # 'lon': 'lon',
    # 'geom': 'MULTIPOINT',
}

boundary_mapping = {
    'objectid_1': 'OBJECTID_1',
    'objectid': 'objectid',
    'province': 'province',
    'const_nam': 'const_nam',
    'elec_area_field': 'elec_area_',
    'local_auth': 'local_auth',
    'st_area_sh': 'st_area_sh',
    'st_length_field': 'st_length_',
    'const_no': 'const_no',
    'county_nam': 'county_nam',
    'county_no': 'county_no',
    'st_length1': 'st_length1',
    'votes': 'votes',
    'st_lengt_1': 'st_lengt_1',
    'globalid': 'globalid',
    'shape_leng': 'Shape_Leng',
    'shape_area': 'Shape_Area',
    'geom': 'MULTIPOLYGON',
}



cdf_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'cdf.shp'),
)

def run(verbose=True):
    lm = LayerMapping(CdfProjects, cdf_shp, cdfprojects_mapping,transform=False, encoding='iso-8859-1',)
    lm.save(strict=True, verbose=verbose)


boundary_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'WARDS_Output.shp'),
)

def run1(verbose=True):
    lm = LayerMapping(Boundary, boundary_shp, boundary_mapping,transform=False, encoding='iso-8859-1',)
    lm.save(strict=True, verbose=verbose)