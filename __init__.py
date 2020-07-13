import csv
import os
import pcbnew
import wx
from decimal import Decimal
from pathlib import Path

ref_ignore = ["TP", "J", "NT", "SW"]

class JLCSMTPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "Generate JLCSMT Placement Files"
        self.category = "Fabrication Outputs"
        self.description = "Generates the CPL placement files as expected by JLCSMT"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'KiJLC_32x32.png')

    def Run(self):
        board = pcbnew.GetBoard()
        modules = board.GetModules()

        fn = Path(board.GetFileName()).with_suffix("")

        bot = open("{}_bot.cpl".format(fn), "w", newline='')
        top = open("{}_top.cpl".format(fn), "w", newline='')
        botw = csv.writer(bot, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        topw = csv.writer(top, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        hdr = ["Ref","PosX","PosY","Rot","Side"]
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
            mid_x = Decimal(pos[0]) / Decimal(100000)
            mid_y = Decimal(pos[1]) / Decimal(100000)

            if layer == "F.Cu":
                layer = "top"
                topw.writerow([ref, mid_x, mid_y, rot, layer])
            elif layer == "B.Cu":
                layer = "bottom"
                botw.writerow([ref, mid_x, mid_y, rot, layer])
        
        bot.close()
        top.close()
        wx.MessageBox("Placement files generated.", 'Done', wx.OK | wx.ICON_INFORMATION)

JLCSMTPlugin().register()
