# KiJLC

![KiJLC logo](img/KiJLC_128x128.png)

An inofficial plugin for eeschema and pcbnew to export BOM and CPL files compliant with JLCSMT. We're not affiliated with JLC. Please double check your data as there might still be bugs.

## BOM Fields

Right now the BOM plugin expects two fields to be present: "JLC" which should contain the JLCSMT footprint specifier and "LCSC" which should contain the part number from LCSC.

Right now KiCad footprint specifiers are not being converted to JLC ones, but this could be implemented in the future.

## Windows Compatability

Windows versions of KiCad before 6.0 were built with Python 2, which is not compatible with this plugin. This plugin requires KiCad >6.0 on Windows.

## Installation

Clone the repo to `~/.kicad/scripting/plugins/KiJLC` on Linux or `%USERPOFILE%\Documents\KiCad\6.0\scripting\plugins` on Windows and it will load the next time pcbnew is opened. Example:

Linux:

```sh
mkdir -p ~/.kicad/scripting/plugins
cd ~/.kicad/scripting/plugins
git clone https://github.com/fullyautomated/KiJLC
```

Windows:

```powershell
cd %USERPOFILE%\Documents\KiCad\6.0\scripting\plugins
git clone https://github.com/fullyautomated/KiJLC
```

For eeschema create a new BOM plugin entry under Tools->Generate Bill of Materials:

![BOM Dialog](img/BOM_dialog.png)

Linux Command line:

```sh
/usr/bin/python3  "~/.kicad/scripting/plugins/KiJLC/bom2jlc.py" "%I" "%O"
```

Windows Command Line:

```powershell
python "C:\Users\<user>\Documents\KiCad\6.0\scripting\plugins\KiJLC\bom2jlc.py" "%I" "%O"
```

## Usage

### pcbnew

Under Tools->External Plugins->Generate JLCSMT Placement Files
or via the button in the toolbar.

### eeschema

In the same configuration dialog as in Installation, just press generate and it will produce two BOM CSV files.
