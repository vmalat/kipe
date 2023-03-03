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

## Short description

KIPE consists of 3 parts

### Part 1: kipe.py

Main script for automatic functions. It allows to run ```command``` automatically from command line or activates console mode (like python console).
Script is parsing and editting the schematic source files via ```toolsmod``` modules and calls the "higher" functions from ```check``` modules.

__Example 1:__

Running:
```
python3 kipe.py console
```
activates console and you can write ```command``` manually (example below shows running command ```help``` which lists all commands for KIPE and ```exit``` for termination of the KIPE):
```
>>>help
chkdup
mkcontent
mksubs
mkrefs
chkrepo
mkrepoid
mkrev
pquestion
ptodos
mkbom
mktitle
mkpgnum
mkflat
findcr
load
save
save-force
help
exit
console
lang-en
lang-cz
>>>exit
Exitting
```


__Example 2:__

Running:
```
python3 kipe.py load ../../../kicad7.kicad_pro mkpgnum save
```
will load the project, set the page numbers of the sheet (rewrites page number setted manually in the KiCad), save project and exit (exit is automatic when not ```console``` command specified)
```
Loading project... OK
Setting numbers of pages... OK
Saving project... OK
```

### Part 2: toolsmod

Modules for parsing and editing schematic source files (*.kicad_sch etc.) 

### Part 3: check

Modules for definition of automated functions via ```kipe.py```. 

Eg. ```mkpgnum``` from Example 2 above is realized by calling ```check/pagenum.py``` by ```kipe.py```.

