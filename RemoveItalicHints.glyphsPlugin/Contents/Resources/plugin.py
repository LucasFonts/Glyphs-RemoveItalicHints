from __future__ import annotations

import objc

from AppKit import NSError
from GlyphsApp import Glyphs, GSCallbackHandler, STEM
from GlyphsApp.plugins import GeneralPlugin
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from GlyphsApp import GSGlyph, GSLayer


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
        self, layer: GSLayer, glyph: GSGlyph, interpolation, error
    ) -> Tuple[bool, None | NSError]:
        success = True
        err = None

        # Interpolate the italic angle
        angle = 0
        for master_id, factor in interpolation.items():
            angle += factor * glyph.parent.masters[master_id].italicAngle

        # If the font is italic, delete vertical hints
        if abs(angle) > 0.1:
            for i in reversed(range(len(layer.hints))):
                hint = layer.hints[i]
                if not hint.isPostScript:
                    continue

                if not hint.horizontal and hint.type == STEM:
                    del layer.hints[i]

        return success, err

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
