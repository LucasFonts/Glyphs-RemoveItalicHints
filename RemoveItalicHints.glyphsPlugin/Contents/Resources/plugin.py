from __future__ import annotations

import objc

from GlyphsApp import Glyphs, GSCallbackHandler
from GlyphsApp.plugins import GeneralPlugin


class RemoveItalicHints(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = Glyphs.localize(
            {
                "en": "Remove Italic Hints",
            }
        )

    @objc.python_method
    def start(self):
        GSCallbackHandler.addCallback_forOperation_(self, "GSPrepareLayerCallback")

    @objc.typedSelector(b"c32@:@@@o^@")
    def interpolateLayer_glyph_interpolation_error_(
        self, layer, glyph, interpolation, error
    ):
        print("__interpolateLayer", layer, glyph, interpolation)
        # if error:
        #     return False, NSError()
        return True, None

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
