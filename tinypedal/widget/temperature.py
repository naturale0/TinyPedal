#  TinyPedal is an open-source overlay application for racing simulation.
#  Copyright (C) 2022  Xiang
#
#  This file is part of TinyPedal.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Temperature Widget
"""

import tkinter as tk
import tkinter.font as tkfont

from .. import calculation as calc
from .. import readapi as read_data
from ..base import Widget, MouseEvent

WIDGET_NAME = "temperature"


class Draw(Widget, MouseEvent):
    """Draw widget"""

    def __init__(self, config):
        # Assign base setting
        Widget.__init__(self, config, WIDGET_NAME)

        # Config size & position
        bar_gap = self.wcfg["bar_gap"]
        self.geometry(f"+{self.wcfg['position_x']}+{self.wcfg['position_y']}")

        # Config style & variable
        text_def = "n/a"
        fg_color_tyre = self.wcfg["font_color_tyre"]
        bg_color_tyre = self.wcfg["bkg_color_tyre"]
        fg_color_brake = self.wcfg["font_color_brake"]
        bg_color_brake = self.wcfg["bkg_color_brake"]
        font_temp = tkfont.Font(family=self.wcfg["font_name"],
                                size=-self.wcfg["font_size"],
                                weight=self.wcfg["font_weight"])

        # Draw label
        bar_style = {"text":text_def, "bd":0, "height":1, "width":5,
                     "padx":0, "pady":0, "font":font_temp}

        self.bar_ttemp_fl = tk.Label(self, bar_style, fg=fg_color_tyre, bg=bg_color_tyre)
        self.bar_ttemp_fr = tk.Label(self, bar_style, fg=fg_color_tyre, bg=bg_color_tyre)
        self.bar_ttemp_rl = tk.Label(self, bar_style, fg=fg_color_tyre, bg=bg_color_tyre)
        self.bar_ttemp_rr = tk.Label(self, bar_style, fg=fg_color_tyre, bg=bg_color_tyre)
        self.bar_btemp_fl = tk.Label(self, bar_style, fg=fg_color_brake, bg=bg_color_brake)
        self.bar_btemp_fr = tk.Label(self, bar_style, fg=fg_color_brake, bg=bg_color_brake)
        self.bar_btemp_rl = tk.Label(self, bar_style, fg=fg_color_brake, bg=bg_color_brake)
        self.bar_btemp_rr = tk.Label(self, bar_style, fg=fg_color_brake, bg=bg_color_brake)

        if self.wcfg["layout"] == "0":
            # Vertical layout, tyre above brake
            self.bar_ttemp_fl.grid(row=0, column=0, padx=0, pady=0)
            self.bar_ttemp_fr.grid(row=0, column=1, padx=0, pady=0)
            self.bar_ttemp_rl.grid(row=1, column=0, padx=0, pady=(0, bar_gap))
            self.bar_ttemp_rr.grid(row=1, column=1, padx=0, pady=(0, bar_gap))
            self.bar_btemp_fl.grid(row=2, column=0, padx=0, pady=0)
            self.bar_btemp_fr.grid(row=2, column=1, padx=0, pady=0)
            self.bar_btemp_rl.grid(row=3, column=0, padx=0, pady=0)
            self.bar_btemp_rr.grid(row=3, column=1, padx=0, pady=0)
        elif self.wcfg["layout"] == "1":
            # Vertical layout, brake above tyre
            self.bar_btemp_fl.grid(row=0, column=0, padx=0, pady=0)
            self.bar_btemp_fr.grid(row=0, column=1, padx=0, pady=0)
            self.bar_btemp_rl.grid(row=1, column=0, padx=0, pady=(0, bar_gap))
            self.bar_btemp_rr.grid(row=1, column=1, padx=0, pady=(0, bar_gap))
            self.bar_ttemp_fl.grid(row=2, column=0, padx=0, pady=0)
            self.bar_ttemp_fr.grid(row=2, column=1, padx=0, pady=0)
            self.bar_ttemp_rl.grid(row=3, column=0, padx=0, pady=0)
            self.bar_ttemp_rr.grid(row=3, column=1, padx=0, pady=0)
        elif self.wcfg["layout"] == "2":
            # Horizontal layout, tyre outside of brake
            self.bar_ttemp_fl.grid(row=0, column=0, padx=(0, bar_gap), pady=0)
            self.bar_ttemp_fr.grid(row=0, column=3, padx=(bar_gap, 0), pady=0)
            self.bar_ttemp_rl.grid(row=1, column=0, padx=(0, bar_gap), pady=0)
            self.bar_ttemp_rr.grid(row=1, column=3, padx=(bar_gap, 0), pady=0)
            self.bar_btemp_fl.grid(row=0, column=1, padx=0, pady=0)
            self.bar_btemp_fr.grid(row=0, column=2, padx=0, pady=0)
            self.bar_btemp_rl.grid(row=1, column=1, padx=0, pady=0)
            self.bar_btemp_rr.grid(row=1, column=2, padx=0, pady=0)
        else:
            # Horizontal layout, brake outside of tyre
            self.bar_btemp_fl.grid(row=0, column=0, padx=(0, bar_gap), pady=0)
            self.bar_btemp_fr.grid(row=0, column=3, padx=(bar_gap, 0), pady=0)
            self.bar_btemp_rl.grid(row=1, column=0, padx=(0, bar_gap), pady=0)
            self.bar_btemp_rr.grid(row=1, column=3, padx=(bar_gap, 0), pady=0)
            self.bar_ttemp_fl.grid(row=0, column=1, padx=0, pady=0)
            self.bar_ttemp_fr.grid(row=0, column=2, padx=0, pady=0)
            self.bar_ttemp_rl.grid(row=1, column=1, padx=0, pady=0)
            self.bar_ttemp_rr.grid(row=1, column=2, padx=0, pady=0)

        self.update_data()

        # Assign mouse event
        MouseEvent.__init__(self)

    def update_data(self):
        """Update when vehicle on track"""
        if read_data.state() and self.wcfg["enable"]:

            # Read average tyre & brake temperature data
            ttemp, btemp = read_data.temperature()

            # Start updating
            # Set up display temps
            ttemp_d = tuple(map(self.temp_units, ttemp))
            btemp_d = tuple(map(self.temp_units, btemp))

            # Temperature update
            if self.wcfg["color_swap_tyre"] == "0":
                self.bar_ttemp_fl["fg"] = self.color_ttemp(ttemp[0])
                self.bar_ttemp_fr["fg"] = self.color_ttemp(ttemp[1])
                self.bar_ttemp_rl["fg"] = self.color_ttemp(ttemp[2])
                self.bar_ttemp_rr["fg"] = self.color_ttemp(ttemp[3])
            else:
                self.bar_ttemp_fl["bg"] = self.color_ttemp(ttemp[0])
                self.bar_ttemp_fr["bg"] = self.color_ttemp(ttemp[1])
                self.bar_ttemp_rl["bg"] = self.color_ttemp(ttemp[2])
                self.bar_ttemp_rr["bg"] = self.color_ttemp(ttemp[3])

            if self.wcfg["color_swap_brake"] == "0":
                self.bar_btemp_fl["bg"] = self.color_btemp(btemp[0])
                self.bar_btemp_fr["bg"] = self.color_btemp(btemp[1])
                self.bar_btemp_rl["bg"] = self.color_btemp(btemp[2])
                self.bar_btemp_rr["bg"] = self.color_btemp(btemp[3])
            else:
                self.bar_btemp_fl["fg"] = self.color_btemp(btemp[0])
                self.bar_btemp_fr["fg"] = self.color_btemp(btemp[1])
                self.bar_btemp_rl["fg"] = self.color_btemp(btemp[2])
                self.bar_btemp_rr["fg"] = self.color_btemp(btemp[3])

            self.bar_ttemp_fl.config(text=ttemp_d[0])
            self.bar_ttemp_fr.config(text=ttemp_d[1])
            self.bar_ttemp_rl.config(text=ttemp_d[2])
            self.bar_ttemp_rr.config(text=ttemp_d[3])

            self.bar_btemp_fl.config(text=btemp_d[0])
            self.bar_btemp_fr.config(text=btemp_d[1])
            self.bar_btemp_rl.config(text=btemp_d[2])
            self.bar_btemp_rr.config(text=btemp_d[3])

        # Update rate
        self.after(self.wcfg["update_delay"], self.update_data)

    # Additional methods
    def temp_units(self, temp):
        """Temperature units"""
        return f" {calc.conv_temperature(temp, self.wcfg['temp_unit']):02.0f}°"

    @staticmethod
    def color_ttemp(temp):
        """Tyre temperature color"""
        if temp < 40:
            color = "#44F"  # blue
        elif 40 <= temp < 60:
            color = "#84F"
        elif 60 <= temp < 80:
            color = "#F4F"  # purple
        elif 80 <= temp < 100:
            color = "#F48"
        elif 100 <= temp < 120:
            color = "#F44"  # red
        elif 120 <= temp < 140:
            color = "#F84"
        else:
            color = "#FF4"  # yellow
        return color

    @staticmethod
    def color_btemp(temp):
        """Brake temperature color"""
        if temp < 100:
            color = "#44F"  # blue
        elif 100 <= temp < 200:
            color = "#48F"
        elif 200 <= temp < 300:
            color = "#4FF"  # cyan
        elif 300 <= temp < 400:
            color = "#4F8"
        elif 400 <= temp < 500:
            color = "#4F4"  # green
        elif 500 <= temp < 600:
            color = "#8F4"
        elif 600 <= temp < 700:
            color = "#FF4"  # yellow
        elif 700 <= temp < 800:
            color = "#F84"
        else:
            color = "#F44"  # red
        return color
