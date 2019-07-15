#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import platform

from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder(pure_c=True)

    items = []
    for item in builder.items:
        if item.options["libxslt:shared"] == True:
            # add msys2 and mingw as a build requirement for mingw builds
            if platform.system() == "Windows" and item.settings["compiler"] == "gcc" and \
                    not item.options.get("libxslt:shared", False):
                new_build_requires = copy.copy(item.build_requires)
                new_build_requires["*"] = new_build_requires.get("*", []) + \
                    ["mingw_installer/1.0@conan/stable",
                     "msys2_installer/latest@bincrafters/stable"]
                items.append([item.settings, item.options, item.env_vars,
                              new_build_requires, item.reference])
            else:
                items.append(item)
    builder.items = items

    builder.run()
