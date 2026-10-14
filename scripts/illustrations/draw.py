#!/usr/bin/env python3
"""Generate the site illustrations (Hans 14 Oct 2026: style 9d for light sections, 9e for dark,
AI = the "8" diagram in 9e language). Output: public/img/ill-{hero,backup,team,ai-iso}.svg

    python3 scripts/illustrations/draw.py            # writes public/img/
    python3 scripts/illustrations/draw.py OUTDIR     # writes elsewhere (for review sheets)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iso import FONT, render, plen  # noqa: E402

PLAT = ("#DCE8FB", "#C3D6F5", "#AFC6EE")
NAVY = ("#2A4470", "#13294C", "#0B1F3A")
ORANGE = ("#FFE3B8", "#F6C27A", "#E7A34E")
WHITE = ("#FFFFFF", "#E9EEF6", "#CFD8E6")
SAND = ("#FFF1DA", "#F6D9A8", "#E9C58A")
BLUE = ("#6E9BF0", "#2F6FDB", "#1E4FA6")
GREEN = "#3FB37F"
AMBER = "#F2A541"
SHADOW = ('<filter id="sd" x="-10%" y="-10%" width="130%" height="140%"><feDropShadow dx="0" dy="12" '
          'stdDeviation="10" flood-color="#0B1F3A" flood-opacity=".20"/></filter>')

SHIELD = ('<path d="M0 -40 l30 11 v22 c0 20 -13 31 -30 36 c-17 -5 -30 -16 -30 -36 v-22 z" fill="url(#shw)"/>'
          '<path d="M0 -40 l30 11 v22 c0 20 -13 31 -30 36 z" fill="#E4E8EF" opacity=".75"/>'
          '<path class="draw" style="--l:40;animation-delay:1.4s" d="M-12 -12 l8 8 l16 -18" fill="none" '
          'stroke="#F2A541" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
SHIELD_DEF = ('<linearGradient id="shw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/>'
              '<stop offset="1" stop-color="#EEF3FB"/></linearGradient>')


def check(x, y, w, color, delay, sw=.06):
    """Check mark path in local face units, top-left at x,y, width w. Returns svg (class draw)."""
    pts = [(x, y + w * .45), (x + w * .35, y + w * .8), (x + w, y)]
    L = plen(pts) * 1.05
    d = "M%.3f %.3f L%.3f %.3f L%.3f %.3f" % (*pts[0], *pts[1], *pts[2])
    return (f'<path class="draw" style="--l:{L:.3f};animation-delay:{delay}s" d="{d}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')


def rack(S, x, y, w, d, h, units=7, leds=(GREEN, GREEN, "#6E9BF0", GREEN, AMBER, GREEN, GREEN)):
    S.box(x, y, 0, w, d, h, *NAVY)
    pitch = (h - .4) / units
    inner = ""
    for i in range(units):
        v = .25 + i * pitch
        inner += (f'<rect x=".15" y="{v:.3f}" width="{w - .3:.3f}" height="{pitch * .72:.3f}" rx=".04" fill="#1B3560" '
                  f'stroke="#6E9BF0" stroke-opacity=".55" stroke-width=".025"/>'
                  f'<path d="M.3 {v + pitch * .36:.3f} h{w * .45:.3f}" stroke="#8FB8FF" stroke-opacity=".6" stroke-width=".03" stroke-linecap="round"/>'
                  f'<circle class="blink" style="animation-delay:{(i * .37) % 2.4:.2f}s;animation-duration:{1.6 + (i % 3) * .5:.1f}s" '
                  f'cx="{w - .32:.3f}" cy="{v + pitch * .36:.3f}" r=".055" fill="{leds[i % len(leds)]}"/>')
    S.face("left", x, y + d, h, inner)
    vents = "".join(f'<path d="M.25 {.4 + i * .3:.2f} h{d - .5:.2f}" stroke="#8FB8FF" stroke-opacity=".35" stroke-width=".03" stroke-linecap="round"/>'
                    for i in range(int((h - .6) / .3)))
    S.face("right", x + w, y + d, h, vents)


def hero(S):
    S.box(0, 0, -.2, 9.6, 7.2, .2, *PLAT)
    S.path3([(7.0, 2.0, 0), (6.1, 2.0, 0), (6.1, 3.6, 0), (5.6, 3.6, 0)],
            'class="flow" stroke="#2F6FDB" stroke-opacity=".75" stroke-width="2.2" stroke-dasharray="5 7" stroke-linecap="round"')
    S.add('<g filter="url(#sd)">')
    # server rack + shield
    rack(S, 7.0, 1.0, 1.5, 1.5, 3.4)
    S.cyl(7.75, 1.75, 3.4, .45, .06, "#13294C", "#1B3560")
    S.at(7.75, 1.75, 4.55, SHIELD, ext=(-30, -40, 30, 30), cls="bob")
    # desk
    S.box(1.2, 2.4, 0, 4.4, 2.4, 1.5, *ORANGE)
    S.face("left", 1.2, 4.8, 1.5,
           '<g fill="#FFF1DA"><rect x=".3" y=".2" width="1.5" height=".5" rx=".06"/><rect x=".3" y=".82" width="1.5" height=".5" rx=".06"/></g>'
           '<path d="M.85 .45 h.4 M.85 1.07 h.4" stroke="#E7A34E" stroke-width=".06" stroke-linecap="round"/>')
    # monitor
    S.box(3.05, 3.3, 1.5, .6, .4, .05, *WHITE)
    S.box(3.29, 3.42, 1.55, .12, .12, .5, *WHITE)
    S.box(1.9, 3.25, 2.0, 2.8, .14, 1.7, *WHITE)
    chart = [(.3, .62), (.6, .46), (.9, .64), (1.2, .34), (1.5, .5), (1.85, .26)]
    scr = ('<rect x=".1" y=".1" width="2.6" height="1.5" rx=".06" fill="#0B1F3A"/>'
           '<path d="M.3 .3 h.9" stroke="#8FB8FF" stroke-opacity=".5" stroke-width=".05" stroke-linecap="round"/>'
           f'<path class="draw" style="--l:{plen(chart) * 1.05:.3f};animation-delay:.3s" d="M' +
           " L".join("%.2f %.2f" % p for p in chart) +
           '" fill="none" stroke="#6E9BF0" stroke-width=".06" stroke-linecap="round" stroke-linejoin="round"/>'
           f'<circle class="blink" cx="2.45" cy=".32" r=".08" fill="{AMBER}"/>')
    for i, (col, cls) in enumerate([(GREEN, ""), (GREEN, ""), (AMBER, "pulse")]):
        u = .3 + i * .78
        scr += f'<rect class="{cls}" x="{u:.2f}" y=".85" width=".62" height=".55" rx=".06" fill="{col}"/>'
        if i < 2:
            scr += check(u + .17, .98, .28, "#FFFFFF", .9 + i * .3, .07)
        else:
            scr += f'<path d="M{u + .31:.2f} .96 v.2 M{u + .31:.2f} 1.29 v.01" stroke="#FFFFFF" stroke-width=".08" stroke-linecap="round"/>'
    S.face("left", 1.9, 3.39, 3.7, scr)
    # keyboard, mug, phone
    S.box(2.4, 3.95, 1.5, 1.8, .5, .05, *WHITE)
    S.face("top", 2.4, 3.95, 1.55, "".join(
        f'<rect x="{.1 + c * .2:.2f}" y="{.08 + r * .14:.2f}" width=".15" height=".09" rx=".02" fill="#CFD8E6"/>'
        for r in range(3) for c in range(8)))
    S.box(4.55, 2.75, 1.5, .4, .65, .07, *NAVY)
    S.at(4.75, 3.05, 1.6, '<path class="blink" style="animation-duration:1.1s" d="M-14 -4 c-6 -6 -6 -14 0 -20 M14 -4 c6 -6 6 -14 0 -20" '
         f'fill="none" stroke="{AMBER}" stroke-width="2.4" stroke-linecap="round"/>', ext=(-20, -26, 20, 0))
    S.cyl(5.05, 4.25, 1.5, .17, .36, "#FFFFFF", "#6B4423")
    S.at(5.05, 4.25, 1.9, f'<path class="rise" d="M-4 0 c-5 -8 5 -11 0 -19 M5 0 c-5 -8 5 -11 0 -19" fill="none" stroke="{AMBER}" '
         'stroke-width="2.2" stroke-linecap="round"/>', ext=(-10, -22, 10, 0))
    # plant
    S.box(.3, 5.6, 0, .7, .7, .6, *SAND)
    S.at(.65, 5.95, .6, '<path d="M0 0 c-4 -22 -18 -32 -32 -34 c2 16 12 30 32 34z" fill="url(#leaf)"/>'
         '<path d="M0 0 c4 -24 18 -34 34 -38 c-2 18 -14 32 -34 38z" fill="url(#leaf)"/>'
         '<path d="M0 0 c-1 -14 1 -30 6 -42" stroke="#2E8B57" stroke-width="2" fill="none"/>', ext=(-34, -44, 36, 0))
    # B2 logo object
    S.b2_logo(5.9, 4.6, 0, .7)
    S.add("</g>")
    S.sparkle(0.2, 2.2, 3.4, 0)
    S.sparkle(10.2, 0.6, 2.2, 1.3)
    S.sparkle(4.4, 0.4, 3.6, .7, "#6E9BF0", 6)


FLOW = 'class="flow" stroke="#2F6FDB" stroke-opacity=".7" stroke-width="2.2" stroke-dasharray="5 7" stroke-linecap="round"'
BELL_DEF = ('<linearGradient id="bell" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8C77E"/>'
            '<stop offset="1" stop-color="#E7953A"/></linearGradient>')


def backup(S):
    S.box(0, 0, -.2, 12.0, 4.3, .2, *PLAT)
    S.path3([(1.9, 1.4, 0), (11.8, 1.4, 0)], FLOW)
    days = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]
    e, h, X0, P, Y0 = 1.15, .5, 2.3, 1.36, 2.1
    for i in range(7):
        xc = X0 + i * P + e / 2
        if i == 4:
            S.path3([(xc, 1.4, 0), (xc, Y0, 0)], f'stroke="{AMBER}" stroke-width="2.2" stroke-dasharray="2 6" stroke-linecap="round"')
        else:
            S.path3([(xc, 1.4, 0), (xc, Y0, 0)], FLOW.replace('class="flow"', f'class="flow" style="animation-delay:-{i * .3:.1f}s"'))
    S.add('<g filter="url(#sd)">')
    rack(S, 0.4, 0.5, 1.4, 1.4, 2.4, units=5)
    for i, dn in enumerate(days):
        x, y = X0 + i * P, Y0
        lab = (f'<text x="{e / 2:.2f}" y=".35" font-size=".25" text-anchor="middle" font-family="{FONT}" '
               f'font-weight="600" fill="#0B1F3A" fill-opacity=".62">{dn}</text>')
        if i == 4:
            S.add("</g>")
            top = [(x, y, h), (x + e, y, h), (x + e, y + e, h), (x, y + e, h)]
            ghost = f'fill="{AMBER}" fill-opacity=".10" stroke="{AMBER}" stroke-width="1.6" stroke-dasharray="4 4" stroke-linejoin="round"'
            pts = lambda q: " ".join("%.2f,%.2f" % S.P(*a) for a in q)
            S.add(f'<g class="pulse"><polygon points="{pts(top)}" {ghost}/>'
                  f'<polygon points="{pts([(x, y + e, h), (x + e, y + e, h), (x + e, y + e, 0), (x, y + e, 0)])}" {ghost}/>'
                  f'<polygon points="{pts([(x + e, y, h), (x + e, y + e, h), (x + e, y + e, 0), (x + e, y, 0)])}" {ghost}/></g>')
            S.at(x + e / 2, y + e / 2, h, f'<text class="pulse" y="9" font-size="28" text-anchor="middle" font-family="{FONT}" '
                 f'font-weight="700" fill="{AMBER}">?</text>', ext=(-10, -14, 10, 12))
            S.face("left", x, y + e, h, lab.replace('fill="#0B1F3A" fill-opacity=".62"', f'fill="#C77A1E"'))
            S.add('<g filter="url(#sd)">')
            continue
        S.box(x, y, 0, e, e, h, *WHITE)
        S.face("top", x, y, h, check(.28, .32, .58, "#2F6FDB", .3 + i * .22, .08))
        S.face("left", x, y + e, h, lab)
    S.add("</g>")
    # bell: the alarm for the backup that never ran
    xf = X0 + 4 * P + e / 2
    S.at(xf, Y0 + e / 2, h,
         f'<path class="flow" d="M0 -8 C 4 -40 30 -52 44 -66" fill="none" stroke="{AMBER}" stroke-width="2.2" stroke-dasharray="4 6" stroke-linecap="round"/>'
         '<g transform="translate(56 -104)"><g class="ring"><circle cx="0" cy="-2" r="3.5" fill="#E7953A"/>'
         '<path d="M-16 26 c2 -6 2 -10 2 -16 c0 -11 6 -18 14 -18 c8 0 14 7 14 18 c0 6 0 10 2 16 z" fill="url(#bell)"/>'
         '<circle cx="0" cy="31" r="4.5" fill="#E7953A"/></g>'
         f'<path class="blink" style="animation-duration:1.2s" d="M-26 4 c-5 6 -5 14 0 20 M26 4 c5 6 5 14 0 20" fill="none" stroke="{AMBER}" stroke-width="2.4" stroke-linecap="round"/></g>',
         ext=(-10, -120, 90, 0))
    # magnifier checking the week
    S.at(1.0, 3.7, 1.3,
         '<g class="bob"><path d="M14 14 L32 32" stroke="#13294C" stroke-width="8" stroke-linecap="round"/>'
         '<circle r="24" fill="#FFFFFF" fill-opacity=".85" stroke="#2F6FDB" stroke-width="6"/>'
         '<path class="draw" style="--l:36;animation-delay:2s" d="M-10 0 l7 7 l14 -15" fill="none" stroke="#2F6FDB" stroke-width="4" '
         'stroke-linecap="round" stroke-linejoin="round"/></g>', ext=(-30, -30, 36, 36))
    S.sparkle(0.2, 3.0, 3.2, .4)
    S.sparkle(11.4, 0.0, 2.0, 1.5, "#6E9BF0", 6)


UMBRELLA = ('<path d="M0 0 V-70" stroke="#13294C" stroke-width="2.4"/>'
            '<path d="M-46 -64 Q0 -104 46 -64 Q23 -58 0 -64 Q-23 -58 -46 -64z" fill="url(#bell)"/>'
            '<path d="M-15 -62 Q-12 -90 0 -91 Q12 -90 15 -62 Q8 -60 0 -64 Q-8 -60 -15 -62z" fill="#FFFFFF"/>')


def tile(S, x, y, w, d, pal=WHITE):
    S.box(x, y, 0, w, d, .14, *pal)


def team(S):
    S.box(0, 0, -.2, 8.6, 7.6, .2, *PLAT)
    hub = (4.4, 3.9)
    for a in [(1.8, 1.6), (6.6, 1.7), (1.9, 5.8), (6.4, 5.6)]:
        S.path3([(a[0], a[1], 0), (a[0], hub[1], 0), (hub[0], hub[1], 0)], FLOW)
    S.at(hub[0], hub[1], 0, '<ellipse class="pulse" rx="12" ry="7" fill="#2F6FDB" fill-opacity=".35"/>'
         '<ellipse rx="5" ry="3" fill="#2F6FDB"/>', ext=(-12, -7, 12, 7))
    S.add('<g filter="url(#sd)">')
    # monitoring corner (back): monitoring does not go on holiday
    tile(S, .5, .4, 2.6, 2.4)
    rack(S, .85, .7, 1.0, 1.0, 1.9, units=4)
    S.box(2.15, .95, .14, .75, .9, .55, *WHITE)
    hb = [(.08, .3), (.25, .3), (.33, .12), (.42, .44), (.5, .3), (.82, .3)]
    S.face("left", 2.15, 1.85, .69, f'<rect x=".05" y=".06" width=".65" height=".42" rx=".04" fill="#0B1F3A"/>'
           f'<path class="flow" style="animation-duration:2.4s" d="M' + " L".join("%.2f %.2f" % (u * .8, v) for u, v in hb) +
           f'" fill="none" stroke="{GREEN}" stroke-width=".045" stroke-dasharray=".5 .25" stroke-linejoin="round"/>')
    # colleague 2 (right)
    tile(S, 5.3, .5, 2.6, 2.4)
    colleague(S, 6.1, .9, "#1E4FA6", "#2A4470")
    # holiday (left): sand tile, umbrella, deckchair, Hans
    tile(S, .5, 4.4, 2.8, 2.7, SAND)
    S.at(1.2, 5.0, .14, UMBRELLA, ext=(-46, -100, 46, 0))
    x0, y0 = 1.9, 5.3
    S.path3([(x0 + .15, y0 + .9, .4), (x0 + .15, y0 + .9, .14)], 'stroke="#13294C" stroke-width="2.4"')
    S.path3([(x0 + 1.0, y0 + .9, .4), (x0 + 1.0, y0 + .9, .14)], 'stroke="#13294C" stroke-width="2.4"')
    S.poly([(x0 - .5, y0, 1.15), (x0, y0, .4), (x0, y0 + .9, .4), (x0 - .5, y0 + .9, 1.15)], "#F6C27A")
    S.poly([(x0, y0, .4), (x0 + 1.1, y0, .4), (x0 + 1.1, y0 + .9, .4), (x0, y0 + .9, .4)], "#FFF6E8")
    S.face("top", x0, y0, .4, "".join(f'<rect x="{.1 + i * .3:.2f}" y="0" width=".15" height=".9" fill="#F2A541" fill-opacity=".55"/>' for i in range(4)))
    S.person(x0 + .2, y0 + .45, .4, body="#F2A541", scale=.9)
    # colleague 1 (front)
    tile(S, 5.1, 4.3, 2.6, 2.5)
    colleague(S, 5.9, 4.7, "#2F6FDB", "#5A3B22", done=True)
    S.add("</g>")
    # the handover documentation travelling from Hans to the colleague
    S.add('<g class="bob">')
    S.box(3.9, 5.0, 1.15, .6, .75, .04, *WHITE)
    S.face("top", 3.9, 5.0, 1.19, '<g stroke="#2F6FDB" stroke-width=".045" stroke-linecap="round">'
           '<path d="M.1 .15 h.38 M.1 .3 h.3 M.1 .45 h.38 M.1 .6 h.22"/></g>')
    S.add("</g>")
    S.sparkle(.2, 3.4, 2.6, .9)
    S.sparkle(8.6, 3.6, 2.2, 1.8, "#6E9BF0", 6)


def colleague(S, x, y, body, hair, done=False):
    """Person behind a small desk with a laptop; x,y = person position on the tile."""
    S.person(x + .6, y + .2, .14, body=body, hair=hair)
    S.box(x, y + .7, .14, 1.4, .9, .55, *ORANGE)
    S.box(x + .4, y + .95, .69, .65, .45, .03, *NAVY)
    S.box(x + .4, y + .95, .72, .65, .04, .42, *NAVY)
    inner = '<rect x=".05" y=".05" width=".55" height=".32" rx=".02" fill="#2F6FDB" fill-opacity=".85"/>'
    if done:
        inner += check(.2, .1, .22, "#FFFFFF", 1.6, .045)
    S.face("left", x + .4, y + .99, 1.14, inner)


# ---------------- AI, night (9e) ----------------
D_PLAT = ("#183462", "#10264A", "#0B1C38")
D_CORE = ("#24477F", "#183462", "#10264A")
D_CARD = ("#203F72", "#16305A", "#10264A")
D_DOC = ("#DCE8FB", "#AFC6EE", "#8FB0E6")
GLOW_DEF = ('<filter id="gl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<filter id="dsd" x="-10%" y="-10%" width="130%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="9" '
            'flood-color="#000814" flood-opacity=".45"/></filter>'
            '<radialGradient id="rg" cx=".75" cy=".15" r=".95"><stop offset="0" stop-color="#1B3D72"/><stop offset="1" stop-color="#081629"/></radialGradient>'
            '<radialGradient id="pool" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3D7BEA" stop-opacity=".35"/><stop offset="1" stop-color="#3D7BEA" stop-opacity="0"/></radialGradient>'
            '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#5E8FE0" opacity=".28"/></pattern>')
D_FLOW = 'class="flow" stroke="#8FB8FF" stroke-width="2.2" stroke-dasharray="5 7" stroke-linecap="round" filter="url(#gl)"'


def ai(S):
    S.box(0, 0, -.25, 11.6, 3.8, .25, *D_PLAT)
    c = 1.9
    S.at(3.4, c, 0, '<ellipse rx="120" ry="60" fill="url(#pool)"/>', ext=(-10, -10, 10, 10))
    for a, b in [(1.5, 2.5), (4.3, 5.1), (6.7, 7.6), (8.8, 9.9)]:
        S.path3([(a, c, 0), (b, c, 0)], D_FLOW)
    S.add('<g filter="url(#dsd)">')
    # 1. incoming mails
    for i, (x, y, z) in enumerate([(.35, 1.0, 1.4), (.55, 1.65, .9), (.25, 2.35, .4)]):
        S.add(f'<g class="bob" style="animation-delay:-{i * 1.3:.1f}s">')
        S.box(x, y, z, 1.0, .7, .07, "#C3D6F5", "#8FB0E6", "#6E9BF0")
        S.face("top", x, y, z + .07, '<path d="M.05 .05 L.5 .38 L.95 .05" fill="none" stroke="#1E4FA6" stroke-width=".05" stroke-linejoin="round"/>')
        S.add("</g>")
    # 2. AI core with the DataMatrix mark on top
    S.box(2.6, 1.0, 0, 1.8, 1.8, 1.5, *D_CORE)
    leds = ""
    for r in range(4):
        for q in range(4):
            col = "#F2A541" if (r, q) in [(1, 2), (2, 0)] else "#8FB8FF"
            leds += (f'<rect class="blink" style="animation-delay:{((r * 4 + q) * .29) % 2.4:.2f}s;animation-duration:{1.8 + ((r + q) % 3) * .6:.1f}s" '
                     f'x="{.32 + q * .32:.2f}" y="{.28 + r * .28:.2f}" width=".18" height=".16" rx=".04" fill="{col}"/>')
    S.face("left", 2.6, 2.8, 1.5, f'<g filter="url(#gl)">{leds}</g>')
    S.face("right", 4.4, 2.8, 1.5, '<g stroke="#6E9BF0" stroke-opacity=".55" stroke-width=".035" stroke-linecap="round">' +
           "".join(f'<path d="M.3 {.3 + i * .22:.2f} h1.2"/>' for i in range(5)) + "</g>")
    S.b2_logo(3.05, 1.45, 1.5, .38)
    # 3. prioritised cards (urgent on top)
    for i, (z, col) in enumerate([(.3, "#6E9BF0"), (.75, "#F2A541"), (1.2, "#E5534B")]):
        S.add(f'<g class="pop" style="animation-delay:{.4 + (2 - i) * .25:.2f}s">')
        S.box(5.2, 1.35, z, 1.5, 1.1, .08, *D_CARD)
        S.face("top", 5.2, 1.35, z + .08, f'<rect x=".1" y=".12" width=".14" height=".86" rx=".04" fill="{col}" filter="url(#gl)"/>'
               '<path d="M.4 .3 h.8 M.4 .55 h.6 M.4 .8 h.7" stroke="#8FB8FF" stroke-opacity=".7" stroke-width=".06" stroke-linecap="round"/>')
        S.add("</g>")
    # 4. runbook: standing sheet, steps drawn one by one
    S.box(7.6, 1.8, 0, 1.3, .1, 1.7, *D_DOC)
    rb = '<rect x=".15" y=".14" width=".7" height=".12" rx=".03" fill="#1E4FA6"/>'
    for i in range(4):
        v = .45 + i * .3
        rb += (f'<rect x=".15" y="{v - .07:.2f}" width=".13" height=".13" rx=".02" fill="none" stroke="#2F6FDB" stroke-width=".03"/>'
               f'<path class="draw" style="--l:.8;animation-delay:{1.2 + i * .35:.2f}s" d="M.38 {v:.2f} h{.62 - (i % 2) * .18:.2f}" '
               f'stroke="#2F6FDB" stroke-width=".05" stroke-linecap="round"/>')
    S.face("left", 7.6, 1.9, 1.7, rb)
    # 5. the human who approves
    S.person(10.5, c, 0, body="#2F6FDB", head="#FFD9B0", hair="#5A3B22", scale=1.3)
    S.add("</g>")
    S.at(10.5, c, 2.0, '<g transform="translate(28 -32)"><g class="pop" style="animation-delay:2.6s">'
         '<circle r="15" fill="#F2A541" filter="url(#gl)"/><path d="M-9 13 l-6 9 l12 -6z" fill="#F2A541"/>'
         '<path d="M-6 0 l4 4 l8 -9" fill="none" stroke="#0B1F3A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></g>',
         ext=(-20, -50, 46, 0))
    S.sparkle(11.4, .1, 2.4, .5)
    S.sparkle(1.6, .0, 2.6, 1.6, "#8FB8FF", 6)


AI_BG = ('<rect width="600" height="420" rx="26" fill="url(#rg)"/><rect width="600" height="420" rx="26" fill="url(#dots)"/>')


LEAF = ('<linearGradient id="leaf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ED39A"/>'
        '<stop offset="1" stop-color="#3FA466"/></linearGradient>')

SCENES = {
    "ill-hero.svg": lambda: render(560, 460, hero, label="Illustration: skrivebord med overvågningsskærm, server med skjold, "
                                   "kaffe og DataMatrix-logoet", extra_defs=SHADOW + SHIELD_DEF + LEAF, margin=14),
    "ill-backup.svg": lambda: render(560, 400, backup, label="Illustration: en uges backups mandag til søndag; fredagens "
                                     "backup kørte aldrig, og en alarmklokke ringer", extra_defs=SHADOW + BELL_DEF, margin=14),
    "ill-team.svg": lambda: render(560, 420, team, label="Illustration: Hans på ferie under en parasol, mens kolleger "
                                   "tager over efter dokumentationen, og overvågningen kører videre",
                                   extra_defs=SHADOW + BELL_DEF, margin=14),
    "ill-ai-iso.svg": lambda: render(600, 420, ai, mode="dark", label="Illustration: indkommende mails sorteres og prioriteres "
                                     "af AI, som skriver en runbook, og et menneske godkender",
                                     extra_defs=GLOW_DEF, bg=AI_BG, fit_box=(26, 40, 574, 390)),
}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", "public", "img")
    os.makedirs(out, exist_ok=True)
    for name, fn in SCENES.items():
        with open(os.path.join(out, name), "w") as f:
            f.write(fn())
        print("wrote", os.path.join(out, name))
