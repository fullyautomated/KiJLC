# KiJLC

![KiJLC logo](KiJLC_128x128.png)

A plugin for eeschema and pcbnew to export BOM and CPL files compliant with JLCSMT.

## Usage

Clone the repo to `~/.kicad/scripting/plugins/KiJLC` and it will load the next time pcbnew is opened.

For eeschema create a new BOM plugin entry e.g.:

`/usr/bin/python3  "~/.kicad/plugins/KiJLC/bom2jlc.py" "%I" "%O"`
