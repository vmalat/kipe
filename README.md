# KIPE - KiCad Parser and Editor

>Project will be translated to english and migrated to the GIT in few weeks.

The project is aimed for usage of KiCad (version 7) to drawing of industrial electric diagrams. There are probably more suitable and powerful applications for this job, but KiCad (eeschema) has been chosen from these reasons:
* is free
* the source files are pure texts, so additionaly parsing, tracking changes via versioning system is very easy

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

## Command description

Here is the list of functions and the possibility of running them without special conditions (eg. library with special fields)
| Command | Function | Runs without special conditions |
| --- | --- | --- |
| chkdup  | Checking of the duplicity symbols - the references | :heavy_check_mark:
| mkcontent | Creating the TOC | :x: |
| mksubs | Creating the link between symbols and "subsymbol". Eg. between relay's coil and it's contacts. | :x:
| mkrefs | Creating the link (page number and section) between global labels. | :heavy_check_mark:
| chkrepo | Checking the status of the repository which is KIPE called from. | :x: Only Mercurial repository is supported.
| mkrepoid | Sets the project variable ```${DOC_CHANGESET}``` according to the repository changeset. | :x: Only Mercurial repository is supported.
| mkrev REV | Sets the project variable ```${DOC_REV}```  according to REV. | :heavy_check_mark:
| pquestion | Open points. Lists all text which contains ```#?``` | :heavy_check_mark:
| ptodos | TODO. Lists all text which contains ```#TODO``` | :heavy_check_mark:
| mkbom | Prints the BOM. | :x: Will provide a list of symbol references, but without special fields inside the library the detais related to vendor etc. will not be accessible.
| mktitle | Adds the "KIPE standard" title block to each schematic file.| :heavy_check_mark:
| mkpgnum | Sets the number of pages inside the project. | :heavy_check_mark:|
| mkflat | Creates the "flat" structure of the project. Removes duplicity sheet, adapts symbol instances. | :heavy_check_mark:|
| findcr REGEXP | Finds the location of symbol(s) given by the REGEXP. Eg. ```findcr -K.*``` will print all symbol with references start by -K | :heavy_check_mark:|
| load PRO | Loads the project given by PRO from \*.kicad_pro file. Eg. load ../my_project.kicad_pro | :heavy_check_mark:|
| save | Saves changes in project done by KIPE.  The shall be no error in previously executed command. <br>:exclamation: backup the project before saving project.| :heavy_check_mark: 
|save-force |  Saves changes in project done by KIPE even if there were any error in executed commands. <br>:exclamation: backup the project before saving project. | :heavy_check_mark:|
| help | Prints all command. | :heavy_check_mark:
| exit | Exits the console. | :heavy_check_mark:|
| console | Start console mode | :heavy_check_mark:| 
| lang-en | Switching to english language | :heavy_check_mark:|
| lang-cz | Switching to czech language | :heavy_check_mark:|

