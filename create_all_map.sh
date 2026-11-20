source env/bin/activate
### Update geofabrik extract
pyosmium-up-to-date osm_extracts/germany-latest.osm.pbf
### Remove old filtered file
rm osm_extracts/germany-latest-filtered.osm.pbf
### Create map for newly finished construction
### Implicitly download MaStR data and create osm extract
python tools/check_osm_construction.py --keep Hersteller Nettonennleistung --plot Hersteller
### Create map for permanently shut down
python tools/check_osm_disused.py --keep Hersteller Nettonennleistung --plot Hersteller
# -- Offshore ---
# Planned
python tools/plot_offshore_future.py -m -power MW --query "Bundesland == 'Ausschließliche Wirtschaftszone'" -future --keep Hersteller Nettonennleistung GeplantesInbetriebnahmedatum --plot Hersteller
# Active
python tools/plot_offshore_running.py -m -power MW --query "Bundesland == 'Ausschließliche Wirtschaftszone'" -currently --keep Hersteller Nettonennleistung Inbetriebnahmedatum --plot Hersteller
# All
python tools/plot_offshore_all.py -m -power MW --query "Bundesland == 'Ausschließliche Wirtschaftszone'" --keep Hersteller Nettonennleistung Inbetriebnahmedatum GeplantesInbetriebnahmedatum --plot Hersteller

# -- Onshore ---
# Match: Hersteller inside default distance
python tools/download_filter_mastr_compare_osm_match_on_tag.py --discardSmall 50 -m --onshore -power MW -currently --plot --keep Hersteller
# No machtes at all inside default distance
python tools/download_filter_mastr_compare_osm_no_match.py --discardSmall 50 -m --onshore -power MW -currently --query "Inbetriebnahmedatum >= '2020-01-01'" --plot
