import csv
import os
import pcbnew
import re
import wx
from decimal import Decimal
from pathlib import Path

ref_ignore = ["TP", "J", "NT", "SW"]

# original rotation db from:
# https://github.com/matthewlai/JLCKicadTools/blob/master/jlc_kicad_tools/cpl_rotations_db.csv
rotations = {
    "^SOT-223": 180,
    "^SOT-23": 180,
    "^SOT-353": 180,
    "^QFN-": 270,
    "^LQFP-": 90,
    "^TQFP-": 270,
    "^SOP-(?!18_)": 270,
    "^TSSOP-": 270,
    "^DFN-": 270,
    "^SOIC-": 90,
    "^SOP-18_": 0,
    "^VSSOP-10_": 270,
    "^CP_EIA-3216-18_": 180,
    "^CP_Elec_8x10.5": 180,
    "^CP_Elec_6.3x7.7": 180,
    "^CP_Elec_8x6.7": 180,
    "^(.*?_|V)?QFN-(16|20|24|28|40)(-|_|$)": 270,
    "^MSOP-10_": 90,
    "^R_Array_Convex_4x0603": 90,
}

class JLCSMTPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Generate JLCSMT Placement Files"
        self.category = "Fabrication Outputs"
        self.description = "Generates the CPL placement files as expected by JLCSMT"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), 'KiJLC_32x32.png')

    def Run(self):
        board = pcbnew.GetBoard()
        modules = board.GetModules()

        fn = Path(board.GetFileName()).with_suffix("")

        bot = open("{}_cpl_bot.csv".format(fn), "w", newline='')
        top = open("{}_cpl_top.csv".format(fn), "w", newline='')
        botw = csv.writer(bot, delimiter=',', quotechar='"',
                          quoting=csv.QUOTE_ALL)
        topw = csv.writer(top, delimiter=',', quotechar='"',
                          quoting=csv.QUOTE_ALL)

        hdr = ["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]
        botw.writerow(hdr)
        topw.writerow(hdr)

        for mod in modules:
            skip = False
            ref = mod.GetReference()

            for prefix in ref_ignore:
                if ref.startswith(prefix):
                    skip = True

            if skip:
                continue

            pos = mod.GetPosition()
            rot = mod.GetOrientationDegrees()
            desc = mod.GetDescription()
            layer = board.GetLayerName(mod.GetLayer())
            mid_x = str(Decimal(pos[0]) / Decimal(1000000)) + "mm"
            mid_y = str(Decimal(pos[1]) / Decimal(-1000000)) + "mm"
            footprint = str(mod.GetFPID().GetLibItemName())


            for exp in rotations:
                if re.match(exp, footprint):
                    new_rot =  (rot + rotations[exp]) % 360
                    print("rotating {} ({}): prev {}, new {}".format(ref, footprint, rot, new_rot))
                    rot = new_rot

            if layer == "F.Cu":
                layer = "top"
                topw.writerow([ref, mid_x, mid_y, layer, rot])
            elif layer == "B.Cu":
                layer = "bottom"
                botw.writerow([ref, mid_x, mid_y, layer, rot])

        bot.close()
        top.close()
        wx.MessageBox("Placement files generated.",
                      'Done', wx.OK | wx.ICON_INFORMATION)


JLCSMTPlugin().register()
