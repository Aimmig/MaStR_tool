source env/bin/activate
### Update geofabrik extract
# pyosmium-up-to-date osm_extracts/germany-latest.osm.pbf
### Remove old filtered file
# rm osm_extracts/germany-latest-filtered.osm.pbf
### Create map for newly finished construction
### Implicitly download MaStR data and create osm extract
python tools/check_osm_construction.py
### Create map for permanently shut down
python tools/check_osm_disused.py
