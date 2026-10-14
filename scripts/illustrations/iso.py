"""Tiny isometric SVG kit for the DataMatrix site illustrations (styles 9d light / 9e night).

World units: x runs down-right, y runs down-left, z up. Projection:
    X = ox + (x - y) * cos30 * s,   Y = oy + (x + y) * 0.5 * s - z * s
Visible box faces: top, "left" = plane y+d (faces lower-left), "right" = plane x+w (faces lower-right).
Scenes are functions f(S) run twice: pass 1 measures the bounding box at s=40, pass 2 renders fitted
into the viewBox. Screen-space overlays (`S.at`) are authored at s=40 and scale with the scene.
Draw order is the caller's job (painter: back = small x+y first).
"""
import math

C30 = math.cos(math.pi / 6)
FONT = "Segoe UI,system-ui,-apple-system,Helvetica,Arial,sans-serif"

ANIM_CSS = """@keyframes draw{from{stroke-dashoffset:var(--l,60)}to{stroke-dashoffset:0}}
@keyframes flow{to{stroke-dashoffset:-36}}
@keyframes bob{50%{transform:translateY(-6px)}}
@keyframes twinkle{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.7)}}
@keyframes blink{0%,60%,100%{opacity:1}70%,90%{opacity:.25}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
@keyframes ring{0%,60%,100%{transform:rotate(0)}65%{transform:rotate(12deg)}75%{transform:rotate(-10deg)}85%{transform:rotate(6deg)}}
@keyframes rise{0%{opacity:0;transform:translateY(6px)}40%{opacity:1}100%{opacity:0;transform:translateY(-10px)}}
@keyframes pop{0%,15%{transform:scale(0)}25%{transform:scale(1.12)}32%,100%{transform:scale(1)}}
@keyframes slidein{0%{opacity:0;transform:translateX(-14px)}100%{opacity:1;transform:none}}
@keyframes nudge{0%,55%,100%{transform:none}70%,85%{transform:translate(var(--nx,5px),var(--ny,3px))}}
.draw{stroke-dasharray:var(--l,60);animation:draw .7s cubic-bezier(.6,0,.2,1) both}
.flow{animation:flow 1.6s linear infinite}
.bob{animation:bob 4s ease-in-out infinite}
.tw{transform-box:fill-box;transform-origin:center;animation:twinkle 2.6s ease-in-out infinite}
.blink{animation:blink 2.4s ease-in-out infinite}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-in-out infinite}
.ring{transform-box:fill-box;transform-origin:50% 0;animation:ring 3.2s ease-in-out infinite}
.rise{animation:rise 2.8s ease-out infinite}
.pop{transform-box:fill-box;transform-origin:center;animation:pop 4s ease-out infinite}
.slide{animation:slidein .6s ease-out both}
.nudge{animation:nudge 4.5s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}"""


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(c, d, t):
    a, b = _hex(c), _hex(d)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def plen(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


class Scene:
    def __init__(self, W, H, mode="light", margin=18, label=""):
        self.W, self.H, self.mode, self.margin, self.label = W, H, mode, margin, label
        self.s, self.ox, self.oy = 40.0, 0.0, 0.0
        self.out, self.grads, self.bbox = [], {}, [1e9, 1e9, -1e9, -1e9]
        self.defs_extra = []
        if mode == "light":
            self.edge = 'stroke="#FFFFFF" stroke-opacity=".35" stroke-width=".8" stroke-linejoin="round"'
            self.lift = .28
        else:
            self.edge = 'stroke="#8FB8FF" stroke-opacity=".28" stroke-width=".8" stroke-linejoin="round"'
            self.lift = .14

    # ---------- projection / bookkeeping
    @property
    def k(self):
        return self.s / 40.0

    def P(self, x, y, z=0.0):
        X = self.ox + (x - y) * C30 * self.s
        Y = self.oy + (x + y) * 0.5 * self.s - z * self.s
        self._grow(X, Y)
        return X, Y

    def _grow(self, X, Y):
        b = self.bbox
        b[0], b[1], b[2], b[3] = min(b[0], X), min(b[1], Y), max(b[2], X), max(b[3], Y)

    def add(self, s):
        self.out.append(s)

    def fill(self, c, horiz=False):
        if c.startswith("url") or c == "none":
            return c
        gid = ("h" if horiz else "g") + c.lstrip("#")
        if gid not in self.grads:
            hi = mix(c, "#FFFFFF", self.lift)
            if horiz:
                self.grads[gid] = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
                                   f'<stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{c}"/>'
                                   f'<stop offset="1" stop-color="{mix(c, "#000000", .12)}"/></linearGradient>')
            else:
                self.grads[gid] = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
                                   f'<stop offset="0" stop-color="{hi}"/><stop offset="1" stop-color="{c}"/></linearGradient>')
        return f"url(#{gid})"

    # ---------- primitives
    def poly(self, pts3, color, attrs="", edge=True):
        pts = " ".join("%.2f,%.2f" % self.P(*p) for p in pts3)
        e = self.edge if edge else ""
        self.add(f'<polygon points="{pts}" fill="{self.fill(color)}" {e} {attrs}/>')

    def box(self, x, y, z, w, d, h, top, left, right, attrs="", edge=True, cls=None, style=""):
        if cls:
            self.add(f'<g class="{cls}" style="{style}">')
        if attrs:
            self.add(f"<g {attrs}>")
        self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top, edge=edge)
        self.poly([(x, y + d, z + h), (x + w, y + d, z + h), (x + w, y + d, z), (x, y + d, z)], left, edge=edge)
        self.poly([(x + w, y, z + h), (x + w, y + d, z + h), (x + w, y + d, z), (x + w, y, z)], right, edge=edge)
        if attrs:
            self.add("</g>")
        if cls:
            self.add("</g>")

    def face(self, kind, x0, y0, z0, inner, attrs=""):
        """kind 'left' (plane y=y0, u along +x, v down), 'right' (plane x=x0, u along -y, v down),
        'top' (plane z=z0, u along +x, v along +y). Content in world units."""
        X0, Y0 = self.P(x0, y0, z0)
        s = self.s
        m = {"left": (C30 * s, .5 * s, 0, s), "right": (C30 * s, -.5 * s, 0, s),
             "top": (C30 * s, .5 * s, -C30 * s, .5 * s)}[kind]
        self.add(f'<g transform="matrix({m[0]:.3f},{m[1]:.3f},{m[2]:.3f},{m[3]:.3f},{X0:.2f},{Y0:.2f})" {attrs}>{inner}</g>')

    def cyl(self, cx, cy, z, r, h, side, top, attrs=""):
        X, Yb = self.P(cx, cy, z)
        _, Yt = self.P(cx, cy, z + h)
        rx, ry = 1.2247 * r * self.s, .7071 * r * self.s
        self._grow(X - rx, Yb + ry)
        self._grow(X + rx, Yt - ry)
        self.add(f'<g {attrs}><path d="M{X - rx:.2f} {Yt:.2f} V{Yb:.2f} A{rx:.2f} {ry:.2f} 0 0 0 {X + rx:.2f} {Yb:.2f} V{Yt:.2f} Z" '
                 f'fill="{self.fill(side, True)}"/>'
                 f'<ellipse cx="{X:.2f}" cy="{Yt:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{self.fill(top)}" {self.edge}/></g>')

    def path3(self, pts3, attrs):
        pts = [self.P(*p) for p in pts3]
        d = "M" + " L".join("%.2f %.2f" % p for p in pts)
        self.add(f'<path d="{d}" fill="none" {attrs}/>')
        return plen(pts)

    def at(self, x, y, z, inner, ext=(-30, -30, 30, 30), cls=None, style=""):
        """Screen-space group anchored at world point, authored at s=40. ext = bbox in authored px."""
        X, Y = self.P(x, y, z)
        k = self.k
        self._grow(X + ext[0] * k, Y + ext[1] * k)
        self._grow(X + ext[2] * k, Y + ext[3] * k)
        c = f' class="{cls}"' if cls else ""
        st = f' style="{style}"' if style else ""
        self.add(f'<g transform="translate({X:.2f} {Y:.2f}) scale({k:.4f})"><g{c}{st}>{inner}</g></g>')

    def sparkle(self, x, y, z, delay=0, color="#F2A541", size=8):
        self.at(x, y, z, f'<path class="tw" style="animation-delay:{delay}s" d="M0 -{size} v{2*size} M-{size} 0 h{2*size}" '
                         f'stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>', ext=(-size, -size, size, size))

    # ---------- shared objects
    def b2_logo(self, x, y, z, e=0.6, animate=True):
        """DataMatrix B2 mark as a real iso object: 2x2 blocks, white one sliding out (+x)."""
        p = e * 1.14
        blue = ("#6E9BF0", "#2F6FDB", "#1E4FA6")
        self.box(x, y, z, e, e, e, *blue)            # back
        self.box(x + p, y, z, e, e, e, *blue)        # right
        self.box(x, y + p, z, e, e, e, *blue)        # left
        nx, ny = C30 * .35 * e * self.s, .5 * .35 * e * self.s
        cls = "nudge" if animate else None
        self.box(x + p + .2 * e, y + p, z - .0 * e, e, e, e, "#FFFFFF", "#E4E8EF", "#C3CAD6",
                 cls=cls, style=f"--nx:{nx:.1f}px;--ny:{ny:.1f}px")

    def person(self, x, y, z, body="#2F6FDB", head="#FFD9B0", hair="#2A4470", scale=1.0):
        r = .26 * scale
        self.cyl(x, y, z, r, .62 * scale, body, mix(body, "#FFFFFF", .25))
        X, Y = self.P(x, y, z + .62 * scale)
        hr = .24 * scale * self.s
        hy = Y - hr * 1.15
        self._grow(X - hr, hy - hr)
        self.add(f'<circle cx="{X:.2f}" cy="{hy:.2f}" r="{hr:.2f}" fill="{self.fill(head)}"/>'
                 f'<path d="M{X - .97*hr:.2f} {hy - .25*hr:.2f} A{hr:.2f} {hr:.2f} 0 0 1 {X + .97*hr:.2f} {hy - .25*hr:.2f} '
                 f'Q{X + .2*hr:.2f} {hy - .62*hr:.2f} {X - .97*hr:.2f} {hy - .25*hr:.2f}z" fill="{hair}"/>')

    # ---------- render
    def svg(self, extra_defs=""):
        defs = "".join(self.grads[k] for k in sorted(self.grads)) + extra_defs + "".join(self.defs_extra)
        lab = f' role="img" aria-label="{self.label}"' if self.label else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W} {self.H}"{lab}>'
                f"<defs>{defs}</defs><style>{ANIM_CSS}</style>" + "\n".join(self.out) + "</svg>\n")


def render(W, H, scene_fn, mode="light", margin=18, label="", extra_defs="", bg="", fit_box=None):
    """Run scene_fn twice: measure, then fit into viewBox. fit_box=(x0,y0,x1,y1) overrides target area."""
    m = Scene(W, H, mode, margin, label)
    scene_fn(m)
    bx0, by0, bx1, by1 = m.bbox
    tx0, ty0, tx1, ty1 = fit_box or (margin, margin, W - margin, H - margin)
    k = min((tx1 - tx0) / (bx1 - bx0), (ty1 - ty0) / (by1 - by0))
    S = Scene(W, H, mode, margin, label)
    S.s = 40 * k
    S.ox = (tx0 + tx1) / 2 - k * (bx0 + bx1) / 2
    S.oy = (ty0 + ty1) / 2 - k * (by0 + by1) / 2
    if bg:
        S.add(bg)
    scene_fn(S)
    return S.svg(extra_defs)
