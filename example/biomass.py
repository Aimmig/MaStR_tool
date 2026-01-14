    query_string = "Nettonennleistung > 30"
    plants = plants.query(query_string)
    query_string = "Bundesland == 'Rheinland-Pfalz' and InstallierteLeistung > 300 and Technologie == 'Horizontalläufer'"
    plants = plants.query(query_string)
    query_string = "Technologie == 'Verbrennungsmotor' and Energietraeger == 'Klärschlamm'"
    plants = plants.query(query_string)
    query_string = "ArtDerWasserkraftanlage == 'Laufwasseranlage' and Bruttoleistung > 100"
    plants = plants.query(query_string)
