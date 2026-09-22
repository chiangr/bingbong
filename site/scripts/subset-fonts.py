"""Reproducible font subset; retain weight variation, fix unused display axes."""
from pathlib import Path
import shutil
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.varLib.instancer import instantiateVariableFont

folder = Path('public/fonts')
originals = Path('qa/font-originals')
originals.mkdir(exist_ok=True)
for path in folder.glob('*.woff2'):
    source = originals / path.name
    if not source.exists():
        shutil.copy2(path, source)
    font = TTFont(source)
    if 'fvar' in font:
        axes = {a.axisTag: a.defaultValue for a in font['fvar'].axes if a.axisTag != 'wght'}
        if axes:
            font = instantiateVariableFont(font, axes, inplace=True)
    if 'gvar' in font:
        for glyph in font.getGlyphOrder():
            if glyph not in font['gvar'].variations:
                font['gvar'].variations[glyph] = []
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['kern', 'liga']
    sub = subset.Subsetter(options=options)
    sub.populate(unicodes=list(range(32, 256)) + list(range(0x2000, 0x2070)) + [0x2191, 0x2193, 0x2197, 0x21BB, 0x2212, 0x2299])
    sub.subset(font)
    font.flavor = 'woff2'
    font.save(path)
    print(f'{path.name}: {source.stat().st_size} -> {path.stat().st_size} bytes')
