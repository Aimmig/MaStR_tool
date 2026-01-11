This projet is intended to download and preprocess the data for german power plants,
especially renewable energy plants which is available to download from the official
Markstammdatenregister (see https://www.marktstammdatenregister.de/MaStR ) part of 
Bundesnetzagentur for a possible import to openstreetmap. The data is downloaded using
https://github.com/OpenEnergyPlatform/open-MaStR and can processed with pandas e.g.
like in the given examples using custom query strings.
Note that most of the detailed data is not acutally used as it's not relevant in this context.
Since 2023 the data can be used under the OSM licensing terms.
As usual, no permission is granted to actually import any data using this toolwithout 
consulting the community (and me, the author) beforehand.

A template class and examples for wind, gsgk, hydro and biomass are provided.
Note that the dataset for solar and storage is very large and takes a long time download,
because it also includes millions of small home installtions.
The full data can also be viewed after downloading using e.g. a regular sqlite viewer
etc where all columns and possible values can be investigated.
Also see documention of open-MaStR and of MaStR for reference.

This script mainly uses the german names, but these can be replaced with appropriate english
terms if required. Refer to OSM wiki and the documentation of
Markstammdatenregister for matching the names/tags between them.
Relevant data is start/end/opening date of a plant, location, power output and
e.g. the height for wind turbines, others can be added/removed as required.
Most relevant is the 'MaStR-Nummer der Einheit' (OSM ref:mastr) in the form of SEExxxxx
that can be used to cross-reference with the original data and therefore allows to update
plants over their lifecycle.
This is issued for every individual generator(!) and can serve as a unique id.

Note there's also 'EEG-Anlagenschlüssel' (OSM ref:EEG) in the form Exxxxxxxxxxxxxxx,
this is only issued for renewable energy plants and only after the validation of the
grid operator which can take a few months even after the plant is already in operation,
so this is not ideal to use for cross-referencing.
Similar there's also 'MaStR-Nummer der EEG-Anlage' in the form EEGxxxxx which is used to
identify the whole plant e.g. to group multiple generators at the same location together.

Some plants e.g biomass, waste and non-renewable have other specific values e.g. 'KWKxxxx'
for Kraft-Wärmekopplung.

So it is generally recommended to primarily use the 'SEExxx' value as this doesn't depend
on the energy carrier and avoids confusion with different ids.
But since ref:EEG was/is still used with OSM can be included to potentially match existing tagging.
For plants where only the whole plant is mapped e.g. biomass plants often have multiple generators
which are not obvious to differentiate on the ground this might be included too. These plants
then have multiple "SEExxx" numbers attached to it in the dataset.
Also latitude/longitude are always included, as these are the most relevant tags for matching.

To execute the examples provided first add the cloned directory to your path e.g.
export PYTHONPATH=/path/to/cloned_dir
