# KIPE - KiCad Parser and Editor

>Project will be translated to english and migrated to the GIT in few weeks.

The project is aimed for usage of KiCad (version 7) to drawing of industrial electric diagrams.

Project is derived from KIPE for version 4 and was actively developed and used since year 2016 (for example see figure below).

__KIPE is intended to run above the KiCad's project file and edit KiCad's schematic file to:__
* create the references for global labels
* create the references for the components (eg. relays)
* create pin number of the "subcomponents" (eg. contacts of the relay, input block of PLC etc.)
* check symbol duplicities
* generate table of content 
* generate BOM
* fill repository changeset to the header of the schematics

__There are few limitations to usage of the whole KIPE system:__
* schematics shall be flat, hierarchical structure is not possible (hierarchic sheets are allowed, but only one instance per sheet/file)
* hieararchical pins are not allowed
* library component shall have special fileds

__Example created by KIPE for KiCad 4:__

![kicad4_example](https://user-images.githubusercontent.com/124931409/222565988-7076cebb-986b-4b37-a39e-b1f20e59036f.png)
