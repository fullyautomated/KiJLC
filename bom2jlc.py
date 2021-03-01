import csv
import pcbnew
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

top_bom = dict()
bot_bom = dict()
layer_map = dict()

ref_ignore = ["TP", "T", "NT", "REF***", "G", "H"]

def parse_pcb(fn):
    pcb_fn = str(Path(fn).with_suffix("")) + ".kicad_pcb"
    board = pcbnew.LoadBoard(pcb_fn)
    modules = board.GetModules()

    for mod in modules:
        ref = mod.GetReference()
        layer = board.GetLayerName(mod.GetLayer())
        layer_map[ref] = layer

def write_bom(fn, components):
    with open(fn, 'w', newline='') as csvfile:
        bw = csv.writer(csvfile, delimiter=',',
                        quotechar='"', quoting=csv.QUOTE_ALL)
        bw.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        for comp in components.values():
            designators = ""
            for o in comp:
                designators += o["ref"] + " "
            bw.writerow([comp[0]["value"], designators.rstrip(),
                        comp[0]["jlc"], comp[0]["lcsc"]])


# input files
netlist = sys.argv[1]
out = sys.argv[2]

# open the netlist xml file
tree = ET.parse(netlist)
root = tree.getroot()

# try parsing the pcb for footprint to layer association
parse_pcb(netlist)

for comp in root.iter("comp"):
    skip = False
    ref = comp.attrib["ref"]

    # ignore some common prefixes we don't want
    for prefix in ref_ignore:
        if ref.startswith(prefix):
            skip = True
    
    if skip:
        continue

    value = comp.find("value").text

    footprint = comp.find("footprint").text

    o = comp.find("fields/field[@name='MPN']")
    mpn = "" if o is None else o.text

    if mpn.lower() == "dnp":
        continue

    o = comp.find("fields/field[@name='JLC']")
    jlc = "" if o is None else o.text

    o = comp.find("fields/field[@name='LCSC']")
    lcsc = "" if o is None else o.text

    k = str(value) + "_" + str(footprint) + "_" + str(lcsc)
    o = {"ref": ref, "value": value, "mpn": mpn,
         "footprint": footprint, "jlc": jlc, "lcsc": lcsc}

    if layer_map[ref] == "F.Cu":
        if k in top_bom and top_bom[k] is not None:
            top_bom[k].append(o)
        else:
            top_bom[k] = [o]
    elif layer_map[ref] == "B.Cu":
        if k in bot_bom and bot_bom[k] is not None:
            bot_bom[k].append(o)
        else:
            bot_bom[k] = [o]


# write separate bom files
write_bom("{}_bom_top.csv".format(out), top_bom)
write_bom("{}_bom_bot.csv".format(out), bot_bom)
