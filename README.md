This projet is intended to download and preprocess the data for german power plants,
especially renewable energy plants which is available to download from the official
Markstammdatenregister (see https://www.marktstammdatenregister.de/MaStR ) part of 
Bundesnetzagentur for a possible import to openstreetmap. The data is downloaded using
https://github.com/OpenEnergyPlatform/open-MaStR and can processed with pandas e.g.
like in the given examples using custom query strings.
Note that most of the detailed data is not acutally used as it's not relevant in this context.
Since 2023 the data can be used under the OSM licensing terms,
see https://wiki.openstreetmap.org/wiki/DE:Permissions/Marktstammdatenregister.
As usual, no permission is granted to actually import any data using this tool without
consulting the community (and me, the author) beforehand.

Note that the dataset for solar and storage is very large and takes a long time to download,
because it also includes millions of small home installations.
The full data can also be viewed after downloading using e.g. a regular sqlite viewer
etc where all columns and possible values can be investigated.
Also see documention of open-MaStR and of MaStR for reference.

This script mainly uses the german names, but these can be translated if required.
Refer to OSM wiki and the documentation of
Markstammdatenregister for matching the names/tags between them.
Relevant data is start/end/opening date of a plant, location, power output and
for wind turbines e.g. manufacturere, height, rotor diameter.
Others can be added/removed as required.
Most relevant is the 'MaStR-Nummer der Einheit' (OSM ref:mastr) in the form of SEExxxxx
that can be used to cross-reference with the original data and therefore allows to update
plants over their lifecycle.
This is issued for every individual generator(!) and can serve as a unique id.

Note there's also 'EEG-Anlagenschlüssel' (OSM ref:EEG) in the form Exxxxxxxxxxxxxxx,
but this is only issued for renewable energy plants and only after the validation of the
grid operator which can take a few months even after the plant is already in operation,
so this is not ideal to use for cross-referencing.
Similar there's also 'MaStR-Nummer der EEG-Anlage' in the form EEGxxxxx which is used to
identify the whole plant e.g. to group multiple generators at the same location together.

Some plants e.g biomass, waste and non-renewable have even more additional specific
values e.g. 'KWKxxxx' for Kraft-Wärmekopplung.

So it is generally recommended to primarily use the 'SEExxx' value as this doesn't depend
on the energy carrier and avoids confusion with different ids.
But since ref:EEG was/is still used with OSM it can be included to potentially match existing tagging.
For plants where only the whole plant is mapped because it is not obvious how to differentiate
on the ground this might be included, too (e.g. biomass plants often have multiple generators
in the same building).
These plants have multiple "SEExxx" numbers attached to it in the dataset.

To execute the examples provided first add the cloned directory to your path e.g.
export PYTHONPATH=/path/to/cloned_dir

The workflow usage is something like the following:
- Download data for one energy carrier using the provided Mastrdata class
- define additional columns and their translations as dict depending on the energy carrier
- define and apply custom query string filter depending on the energy carrier
- using the provided DataFilter to apply general filters not depending on the energy carrier
- using the provided PostProcessing to e.g. adjust names of manufactureres, format power values
  as needed and in the last step rename the columns to match OSM
  
Some filters can be used (see the help page of script) directly as options,
others can be added via custom query strings "key1 = 'value1' and/or key2 = 'value2' and/or ...."

Optionally the queried data can plotted on a map, to compare the data with existing OSM data.
Another option is to plot the distance of the MaStR-Data compared to existing OSM data
(this should be a local file prefilterd with osmium to only contain appropriate elements)
and additionally with matching on a selected column.
