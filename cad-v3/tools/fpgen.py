"""KiCad 10 footprint writer for bingbong v3. Every footprint is built ONLY from the numbers of a
manufacturer land-pattern drawing, cited in the footprint's description. Coordinates in mm, top view,
+X right, +Y down (KiCad).
"""
import os
import uuid

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "lib", "Bingbong_v3.pretty")


def uid():
    return str(uuid.uuid4())


def _pad(num, shape, x, y, w, h, layers, rr=None, mask=None, paste=None, angle=0):
    s = f'\t(pad "{num}" smd {shape}\n\t\t(at {x:g} {y:g}{" " + str(angle) if angle else ""})\n\t\t(size {w:g} {h:g})\n\t\t(layers {layers})\n'
    if rr is not None:
        s += f'\t\t(roundrect_rratio {rr:g})\n'
    if mask is not None:
        s += f'\t\t(solder_mask_margin {mask:g})\n'
    if paste is not None:
        s += f'\t\t(solder_paste_margin {paste:g})\n'
    return s + f'\t\t(uuid "{uid()}")\n\t)\n'


def _line(a, b, layer, w):
    return f'\t(fp_line (start {a[0]:g} {a[1]:g}) (end {b[0]:g} {b[1]:g}) (stroke (width {w:g}) (type solid)) (layer "{layer}") (uuid "{uid()}"))\n'


def _rect(a, b, layer, w):
    return f'\t(fp_rect (start {a[0]:g} {a[1]:g}) (end {b[0]:g} {b[1]:g}) (stroke (width {w:g}) (type solid)) (fill no) (layer "{layer}") (uuid "{uid()}"))\n'


def _circle(c, r, layer, w, fill=False):
    return (f'\t(fp_circle (center {c[0]:g} {c[1]:g}) (end {c[0] + r:g} {c[1]:g}) (stroke (width {w:g}) (type solid)) '
            f'(fill {"yes" if fill else "no"}) (layer "{layer}") (uuid "{uid()}"))\n')


class FP:
    def __init__(self, name, descr, body_w, body_h, source):
        self.name, self.descr, self.bw, self.bh, self.src = name, descr, body_w, body_h, source
        self.items = []
        self.extent = [body_w / 2, body_h / 2]

    def _grow(self, x, y, w, h):
        self.extent[0] = max(self.extent[0], abs(x) + w / 2)
        self.extent[1] = max(self.extent[1], abs(y) + h / 2)

    def bga(self, num, x, y, d, mask, paste_sq=None, paste_rr=None):
        """NSMD ball land: copper circle d, mask opening d + 2*mask; paste as a separate square aperture."""
        self.items.append(_pad(num, "circle", x, y, d, d, '"F.Cu" "F.Mask"', mask=mask))
        if paste_sq:
            rr = (paste_rr / paste_sq) if paste_rr else 0
            self.items.append(_pad("", "roundrect", x, y, paste_sq, paste_sq, '"F.Paste"', rr=rr))
        self._grow(x, y, d + 2 * mask, d + 2 * mask)

    def smd(self, num, x, y, w, h, r=None, mask=None, paste=None, layers='"F.Cu" "F.Mask" "F.Paste"'):
        shape = "roundrect" if r else "rect"
        rr = (r / min(w, h)) if r else None
        self.items.append(_pad(num, shape, x, y, w, h, layers, rr=rr, mask=mask, paste=paste))
        self._grow(x, y, w + 2 * (mask or 0), h + 2 * (mask or 0))

    def land(self, num, x, y, w, h, mask, paste=None, paste_r=0.05):
        """Copper + NSMD mask; optional separate (smaller) paste aperture (pw, ph); paste=None -> no paste."""
        self.items.append(_pad(num, "rect", x, y, w, h, '"F.Cu" "F.Mask"', mask=mask))
        if paste:
            pw, ph = paste
            self.items.append(_pad("", "roundrect", x, y, pw, ph, '"F.Paste"', rr=paste_r / min(pw, ph)))
        self._grow(x, y, w + 2 * mask, h + 2 * mask)

    def poly(self, num, pts, layers='"F.Cu" "F.Mask"', mask=None, anchor=0.1):
        """Custom polygon pad; pts absolute (footprint coords). Anchored at the polygon's centroid."""
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        rel = " ".join(f"(xy {x - cx:g} {y - cy:g})" for x, y in pts)
        m = f"\t\t(solder_mask_margin {mask:g})\n" if mask is not None else ""
        self.items.append(f'''\t(pad "{num}" smd custom
\t\t(at {cx:g} {cy:g})
\t\t(size {anchor:g} {anchor:g})
\t\t(layers {layers})
{m}\t\t(options (clearance outline) (anchor rect))
\t\t(primitives (gr_poly (pts {rel}) (width 0) (fill yes)))
\t\t(uuid "{uid()}")
\t)
''')
        for x, y in pts:
            self._grow(x, y, 2 * (mask or 0), 2 * (mask or 0))

    def keepout(self, x0, y0, x1, y1, layers='"F.Cu"'):
        """Rule area: no tracks, no vias (pads allowed)."""
        self.items.append(f'''\t(zone (net 0) (net_name "") (layers {layers}) (uuid "{uid()}") (hatch edge 0.5)
\t\t(connect_pads (clearance 0)) (min_thickness 0.25) (filled_areas_thickness no)
\t\t(keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed))
\t\t(fill (thermal_gap 0.5) (thermal_bridge_width 0.5))
\t\t(polygon (pts (xy {x0:g} {y0:g}) (xy {x1:g} {y0:g}) (xy {x1:g} {y1:g}) (xy {x0:g} {y1:g})))
\t)
''')

    def write(self, pin1=None):
        bw, bh = self.bw / 2, self.bh / 2
        ex, ey = self.extent
        cx, cy = round(max(ex, bw) + 0.1, 2), round(max(ey, bh) + 0.1, 2)
        g = ""
        g += _rect((-bw, -bh), (bw, bh), "F.Fab", 0.05)
        g += _rect((-cx, -cy), (cx, cy), "F.CrtYd", 0.05)
        if pin1:
            g += _circle(pin1, 0.08, "F.SilkS", 0.1, fill=True)
            g += _circle((-bw + 0.12, -bh + 0.12), 0.05, "F.Fab", 0.03, fill=True)
        text = f'''(footprint "{self.name}"
\t(version 20251024)
\t(generator "bingbong_fpgen")
\t(layer "F.Cu")
\t(descr "{self.descr} | SOURCE: {self.src}")
\t(tags "bingbong v3 verified-from-datasheet")
\t(property "Reference" "REF**" (at 0 {-cy - 0.6:g} 0) (layer "F.SilkS") (uuid "{uid()}") (effects (font (size 0.5 0.5) (thickness 0.08))))
\t(property "Value" "{self.name}" (at 0 {cy + 0.6:g} 0) (layer "F.Fab") (uuid "{uid()}") (effects (font (size 0.3 0.3) (thickness 0.05))))
\t(property "Datasheet" "" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{uid()}") (effects (font (size 1 1))))
\t(property "Description" "{self.descr}" (at 0 0 0) (layer "F.Fab") (hide yes) (uuid "{uid()}") (effects (font (size 1 1))))
\t(attr smd)
{g}{"".join(self.items)}\t(embedded_fonts no)
)
'''
        os.makedirs(OUT, exist_ok=True)
        open(os.path.join(OUT, self.name + ".kicad_mod"), "w").write(text)
        return self.name
