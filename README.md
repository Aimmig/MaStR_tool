This projet is intended to download and preprocess the data for german power plants,
especially renewable energy plants which is available to download from the official
'Markstammdatenregister' part of 'Bundesnetzagentur' for a possible import to openstreetmap. The data is downloaded using https://github.com/OpenEnergyPlatform/open-MaStR and processed with pandas. Note that most of the detailed data is not acutally used as it's not relevant in this context. Since 2023 the data can be used under the OSM licensing terms. As usual, no permission is granted to actually import any data using this tool without consulting the community (and me, the author) beforehand.

A template class and derived class for basic filtering of wind plants is provided. For photovoltaik this would be straight forward, but the dataset is much larger and appropriate filters would need to implemented. 

The german names for OSM relevant data are replaced with the appropriate OSM tags. Refer to OSM wiki for details. Relevant data is start/end/opening date of a plant, location, power output and e.g. the height for wind turbines, others might be added as required.
Most relevant is the 'MaStR-Nummer der Einheit' (OSM ref:mastr) in the form of SEExxxxx that can be used to cross-reference with the original data and therefore allows to update plants over their lifecycle. This is issued for every sort of generator/power plant and can serve as a unique id. 

Note there is also 'EEG-Anlagenschlüssel' (OSM ref:EEG) in the form Exxxxxxxxxxxxxxx , this is only issued for renewable energy plants and only after the validation of the grid operator which can take a few months even after the plant is already in operation, so this is not ideal to use for cross-referencing. Similar there's also 'MaStR-Nummer der EEG-Anlage' in the form EEGxxxxx which is still another identifer in the data. Non renewable plants/generators have other specific values e.g. 'KWKxxxx' for Kraft-Wärmekopplung.

So it is generally recommended to primarily use the 'SEExxx' value as this doesn't depend on the energy carrier and avoids confusion with different ids. But since ref:EEG was/is still used with OSM it is included
to potentially match existing tagging.
