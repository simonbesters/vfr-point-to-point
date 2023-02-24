## Plot visual flight rules on map based on 2 GPS points or IGC-based flight track


TODO/WIP:

Regels over hoogte opnemen:

300 meter boven het hoogste punt van de bebouwde kom met een straal van 600 m.
150 m boven de grond of het water met een minimale afstand van 150 m van obstakels;

Afkortingen

'MSL' QNH
Altitude. The distance measured from mean sea level.

'SFC' = QFE
Height. The distance is measured from the surface of the Earth. Also referred to as "AGL" (Above Ground Level)

'STD' 1013,2 = flight level
The vertical distance is measured with a pressure altimeter set to the standard atmosphere.

## TODO Layers

- Minimal height = AHN source, 150m above ground/water + Grey fill_between
- Objects = api source needed, object height + 150m and 150m wide - red fill_between
- City limits = api source needed, 300m above + 600m before and after
- Clouds = based on weather report, 300m below, but only if higher than 900m for IFR planes
- TMA = upper limit for gliders depending on the region: Hard line with fill up to the highest point in graph
- Actual flight path
