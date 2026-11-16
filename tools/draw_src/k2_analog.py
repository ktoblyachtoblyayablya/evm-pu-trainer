import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from svglib import *


def zbox(g, x1, y, x2, label, vertical=False):
    """generic impedance box on a horizontal wire"""
    xm = (x1 + x2) / 2
    g.line(x1, y, xm - 20, y); g.line(xm + 20, y, x2, y)
    g.rect(xm - 20, y - 10, 40, 20, fill="#fff"); g.text(xm, y + 5, label, s=12, wt="bold")


def axes(g, x0, y0, x1, y1, xl, yl, ox=None):
    """axes with origin (x0,y0); x to x1, y up to y1"""
    g.arrow(x0 - 5 if ox is None else ox, y0, x1, y0, w=1.4)
    g.arrow(x0, y0 + 5, x0, y1, w=1.4)
    g.text(x1, y0 + 18, xl, s=13, a="end", it=True)
    g.text(x0 + 8, y1 + 6, yl, s=13, a="start", it=True)


def oa():
    g = D(760, 300)
    ti, bi, o = g.opamp(90, 125, size=110)
    g.line(30, ti[1], 90, ti[1]); g.text(26, ti[1] + 5, "U−", a="end", s=14, it=True)
    g.line(30, bi[1], 90, bi[1]); g.text(26, bi[1] + 5, "U+", a="end", s=14, it=True)
    g.line(o[0], o[1], 250, o[1]); g.text(256, o[1] + 5, "Uвых", a="start", s=14, it=True)
    g.line(135, 92, 135, 50); g.text(135, 44, "+Eп", s=13)
    g.line(135, 158, 135, 200); g.text(135, 216, "−Eп", s=13)
    g.text(150, 250, "Uвых = K·(U+ − U−),  K ≈ 10⁴…10⁶", s=14, wt="bold")
    g.text(150, 272, "Rвх → ∞, Rвых → 0", s=13, c=GREY)
    X0, Y0 = 590, 150
    axes(g, X0, Y0, 740, 25, "Uд = U+ − U−", "Uвых", ox=420)
    g.line(X0, 255, X0, 150, w=1.4)
    g.path([(430, 225), (575, 225), (605, 75), (735, 75)], c=ACC, w=2.6)
    g.path([(470, 222), (530, 210), (650, 90), (700, 80)], c=BLUE, w=1.8, dash="6 4")
    g.line(X0, 75, 605, 75, dash="3 3", c=GREY); g.line(575, 225, X0, 225, dash="3 3", c=GREY)
    g.text(X0 - 6, 70, "+Uнас", s=12, a="end"); g.text(X0 + 6, 240, "−Uнас", s=12, a="start")
    g.text(625, 180, "без ОС: доли мВ —", s=12, c=ACC, a="start")
    g.text(625, 196, "и уже насыщение", s=12, c=ACC, a="start")
    g.text(470, 200, "с ООС", s=12, c=BLUE, a="start")
    g.text(590, 290, "передаточная характеристика ОУ", s=13, c=GREY)
    g.save("sv_oa")


def stage(g, x, y, zin, zfb, cap_in=False, cap_fb=False, lin="Uвх"):
    """inverting stage: opamp left edge at x, centre y; returns node x"""
    ti, bi, o = g.opamp(x, y, size=70)
    node = x - 18
    g.line(node, ti[1], x, ti[1])
    if cap_in:
        g.capacitor(x - 95, ti[1], node, ti[1], label=zin)
    elif zin:
        g.resistor(x - 95, ti[1], node, ti[1], label=zin)
    g.text(x - 100, ti[1] + 5, lin, s=13, a="end", it=True)
    g.dot(node, ti[1])
    g.line(node, ti[1], node, y - 60)
    if cap_fb:
        g.capacitor(node, y - 60, o[0] + 15, y - 60, label=zfb)
    else:
        g.resistor(node, y - 60, o[0] + 15, y - 60, label=zfb)
    g.line(o[0] + 15, y - 60, o[0] + 15, y); g.dot(o[0] + 15, y)
    g.line(o[0], y, o[0] + 40, y); g.text(o[0] + 44, y + 5, "Uвых", s=13, a="start", it=True)
    g.line(bi[0], bi[1], bi[0] - 10, bi[1]); g.line(bi[0] - 10, bi[1], bi[0] - 10, bi[1] + 8); g.ground(bi[0] - 10, bi[1] + 8)
    return node


def analog():
    g = D(760, 320)
    # a) generic
    x, y = 130, 170
    ti, bi, o = g.opamp(x, y, size=70)
    node = x - 18
    zbox(g, 40, ti[1], node, "Z1"); g.text(34, ti[1] + 5, "Uвх", s=13, a="end", it=True)
    g.line(node, ti[1], x, ti[1]); g.dot(node, ti[1])
    g.line(node, ti[1], node, 110); zbox(g, node, 110, o[0] + 15, "Zос"); g.line(o[0] + 15, 110, o[0] + 15, y); g.dot(o[0] + 15, y)
    g.line(o[0], y, o[0] + 30, y); g.text(o[0] + 33, y + 5, "Uвых", s=13, a="start", it=True)
    g.line(bi[0], bi[1], bi[0] - 10, bi[1]); g.line(bi[0] - 10, bi[1], bi[0] - 10, bi[1] + 8); g.ground(bi[0] - 10, bi[1] + 8)
    g.text(140, 40, "а) обобщённое инвертирующее звено", s=13, wt="bold")
    g.text(140, 255, "Uвых = −Uвх · Zос / Z1", s=14, wt="bold")
    # b) summator
    x, y = 445, 175
    ti, bi, o = g.opamp(x, y, size=70)
    node = x - 22
    for i, (yy, r, u) in enumerate(((95, "R1", "U1"), (126, "R2", "U2"), (157.5, "R3", "U3"))):
        g.resistor(330, yy, node, yy, label=None)
        g.text(325, yy + 5, u, s=13, a="end", it=True); g.text(370, yy - 9, r, s=11)
        g.dot(node, yy) if yy != 157.5 else None
    g.line(node, 95, node, 157.5); g.line(node, 157.5, x, 157.5); g.dot(node, 157.5)
    g.line(node, 95, node, 65); g.resistor(node, 65, o[0] + 15, 65, label="Rос")
    g.line(o[0] + 15, 65, o[0] + 15, y); g.dot(o[0] + 15, y)
    g.line(o[0], y, o[0] + 25, y); g.text(o[0] + 28, y + 5, "Uвых", s=13, a="start", it=True)
    g.line(bi[0], bi[1], bi[0] - 10, bi[1]); g.line(bi[0] - 10, bi[1], bi[0] - 10, bi[1] + 8); g.ground(bi[0] - 10, bi[1] + 8)
    g.text(420, 40, "б) сумматор", s=13, wt="bold")
    g.text(425, 255, "Uвых = −Rос·(U1/R1 + U2/R2 + U3/R3)", s=13, wt="bold")
    g.text(380, 300, "в цепи ОС конденсатор C → интегратор: Uвых = −(1/RC)·∫Uвх dt;   C на входе → дифференциатор: Uвых = −RC·dUвх/dt", s=12, c=GREY)
    g.save("sv_analog")


def comparator():
    g = D(760, 290)
    ti, bi, o = g.opamp(110, 120, size=100, minus_top=False)
    g.line(30, ti[1], 110, ti[1]); g.text(26, ti[1] + 5, "Uвх", s=14, a="end", it=True)
    g.line(30, bi[1], 110, bi[1]); g.text(26, bi[1] + 5, "Uоп", s=14, a="end", it=True)
    g.line(o[0], o[1], 260, o[1]); g.text(264, o[1] + 5, "Uвых (0/1)", s=14, a="start", it=True)
    g.text(165, 220, "ОУ без обратной связи", s=13, c=GREY)
    g.text(165, 245, "Uвх > Uоп → Uвых = U¹;  Uвх < Uоп → U⁰", s=14, wt="bold")
    X0, Y0 = 450, 220
    axes(g, X0, Y0, 740, 30, "Uвх", "Uвых")
    g.path([(455, 200), (600, 200), (600, 70), (730, 70)], c=ACC, w=2.6)
    g.line(600, 220, 600, 200, dash="3 3", c=GREY); g.text(600, 238, "Uоп", s=13, it=True)
    g.line(X0, 70, 600, 70, dash="3 3", c=GREY); g.text(X0 - 6, 75, "U¹", s=13, a="end"); g.text(X0 - 6, 205, "U⁰", s=13, a="end")
    g.path([(560, 70), (640, 70)], c=BLUE, w=1.5, dash="5 4"); g.path([(560, 200), (640, 200)], c=BLUE, w=1.5, dash="5 4")
    g.path([(640, 200), (640, 70)], c=BLUE, w=1.5, dash="5 4", arrow=True); g.path([(560, 70), (560, 200)], c=BLUE, w=1.5, dash="5 4", arrow=True)
    g.text(595, 262, "передаточная характеристика компаратора", s=13, c=GREY)
    g.text(595, 280, "пунктир — с ПОС: гистерезис (триггер Шмитта)", s=12, c=BLUE)
    g.save("sv_cmp")


def dac():
    g = D(760, 330)
    bx = [("Входной", ["регистр кода N"]), ("Ключи", ["S0 … Sn−1"]), ("Резистивная", ["матрица"]), ("ОУ", ["ток → напряжение"])]
    xs = [20, 200, 380, 560]
    for (t, l), x in zip(bx, xs):
        g.box(x, 50, 150, 56, t, l, s=13)
    for i in range(3):
        g.arrow(xs[i] + 150, 78, xs[i + 1], 78)
    g.arrow(735, 78, 755, 78)
    g.line(710, 78, 740, 78); g.text(745, 70, "Uвых", s=13, a="end", it=True)
    g.text(95, 36, "n разрядов", s=12, c=GREY)
    g.box(380, 140, 150, 40, "Uоп (опорное)", s=12, wt=None); g.arrow(455, 140, 455, 106)
    X0, Y0 = 70, 300
    axes(g, X0, Y0, 360, 190, "N", "Uвых")
    st = 32; hh = 13
    pts = [(X0, Y0)]
    for k in range(8):
        pts += [(X0 + k * st, Y0 - k * hh), (X0 + (k + 1) * st, Y0 - k * hh)]
    g.path(pts, c=ACC, w=2.2)
    for k in range(8):
        g.text(X0 + k * st + st / 2, Y0 + 16, str(k), s=11, c=GREY)
    g.line(X0, Y0, X0 + 8 * st, Y0 - 8 * hh, dash="4 4", c=GREY)
    g.text(X0 + 12, 200, "шаг Δ = Uоп/2ⁿ", s=12, c=ACC, a="start")
    tx = 410
    g.text(tx, 215, "Параметры ЦАП:", s=13, a="start", wt="bold")
    for i, t in enumerate(("разрядность n и шаг (ЕМР) Δ = Uоп/2ⁿ", "время установления выхода",
                           "погрешности: смещение нуля, полной шкалы,", "нелинейность (интегральная, дифференциальная)")):
        g.text(tx, 237 + 20 * i, "• " + t, s=12, a="start")
    g.save("sv_dac")


def dac_weighted():
    g = D(760, 330)
    g.line(60, 50, 330, 50, w=2); g.text(52, 55, "Uоп", s=14, a="end", it=True)
    code = {0: 1, 1: 0, 2: 1, 3: 0}
    for i, (x, r) in enumerate(zip((100, 170, 240, 310), ("R", "2R", "4R", "8R"))):
        bit = 3 - i
        g.dot(x, 50); g.line(x, 50, x, 70)
        g.switch(x, 70, L=34, closed=bool(code[i]), vertical=True)
        g.text(x - 10, 92, f"a{bit}", s=12, a="end", wt="bold", c=BLUE)
        g.resistor(x, 104, x, 200, label=r, lpos="right")
        g.line(x, 200, x, 220); g.dot(x, 220) if x != 100 else None
    g.line(100, 220, 450, 220)
    ti, bi, o = g.opamp(470, 237.5, size=70)
    g.line(450, 220, 470, 220); g.dot(450, 220)
    g.line(450, 220, 450, 150); g.resistor(450, 150, 560, 150, label="Rос"); g.line(560, 150, 560, 237.5); g.dot(560, 237.5)
    g.line(o[0], o[1], 600, o[1]); g.text(605, o[1] + 5, "Uвых", s=14, a="start", it=True)
    g.line(bi[0], bi[1], bi[0] - 10, bi[1]); g.line(bi[0] - 10, bi[1], bi[0] - 10, bi[1] + 6); g.ground(bi[0] - 10, bi[1] + 6)
    g.text(205, 245, "I3 = Uоп/R,  I2 = Uоп/2R,  I1 = Uоп/4R,  I0 = Uоп/8R", s=12, c=GREY)
    g.text(380, 290, "Uвых = −Uоп · (Rос / R) · (a3 + a2/2 + a1/4 + a0/8)", s=15, wt="bold")
    g.text(380, 315, "на схеме код 1010: замкнуты ключи a3 и a1.  Минус — нужен широкий ряд точных номиналов R … 2ⁿ⁻¹R", s=12, c=GREY)
    g.save("sv_dacw")


def r2r():
    g = D(760, 340)
    xs = [140, 260, 380, 500]
    g.line(60, 60, xs[0], 60); g.text(52, 65, "Uоп", s=14, a="end", it=True)
    for i in range(3):
        g.resistor(xs[i], 60, xs[i + 1], 60, label="R")
    g.resistor(xs[3], 60, 590, 60, label="2R"); g.line(590, 60, 590, 75); g.ground(590, 75)
    code = [1, 0, 1, 1]
    for i, x in enumerate(xs):
        g.dot(x, 60)
        g.resistor(x, 60, x, 150, label="2R", lpos="right")
        g.line(x, 150, x, 165); g.dot(x, 165, r=2.6)
        g.dot(x - 16, 195, r=2.6); g.dot(x + 16, 195, r=2.6)
        if code[i]:
            g.line(x, 165, x - 15, 192)
        else:
            g.line(x, 165, x + 15, 192)
        g.line(x - 16, 195, x - 16, 225); g.dot(x - 16, 225) if i else None
        g.line(x + 16, 195, x + 16, 262); g.dot(x + 16, 262) if i < 3 else None
        g.text(x + 22, 175, f"a{3 - i}", s=12, a="start", wt="bold", c=BLUE)
    g.line(xs[0] - 16, 225, 600, 225); g.text(xs[0] - 22, 229, "к ОУ", s=11, a="end", c=GREY)
    g.line(xs[0] + 16, 262, 560, 262); g.line(560, 262, 560, 270); g.ground(560, 270)
    ti, bi, o = g.opamp(620, 242.5, size=70)
    g.line(600, 225, 620, 225); g.dot(600, 225)
    g.line(600, 225, 600, 150); g.resistor(600, 150, 710, 150, label="Rос = R"); g.line(710, 150, 710, 242.5); g.dot(710, 242.5)
    g.line(o[0], o[1], 740, o[1]); g.text(745, o[1] - 8, "Uвых", s=13, a="end", it=True)
    g.line(bi[0], bi[1], bi[0] - 8, bi[1]); g.line(bi[0] - 8, bi[1], bi[0] - 8, bi[1] + 10); g.ground(bi[0] - 8, bi[1] + 10)
    g.text(380, 305, "Ток делится пополам в каждом узле: I = Uоп/2R, Uоп/4R, Uоп/8R, Uоп/16R", s=13, c=GREY)
    g.text(380, 330, "Uвых = −Uоп · N / 2ⁿ   (код 1011 → −11/16·Uоп);  нужны всего два номинала: R и 2R", s=14, wt="bold")
    g.save("sv_r2r")


def adc():
    g = D(760, 340)
    names = [("Дискретизация", ["по времени (УВХ)"]), ("Квантование", ["по уровню"]), ("Кодирование", ["→ двоичный код"])]
    xs = [120, 330, 540]
    g.text(20, 70, "Uвх(t)", s=14, a="start", it=True); g.arrow(70, 78, 120, 78)
    for (t, l), x in zip(names, xs):
        g.box(x, 50, 170, 56, t, l, s=13)
    g.arrow(290, 78, 330, 78); g.arrow(500, 78, 540, 78); g.arrow(710, 78, 750, 78)
    g.text(728, 70, "N", s=14, wt="bold")
    X0, Y0 = 60, 310
    axes(g, X0, Y0, 740, 135, "t", "U")
    D_ = 18
    for k in range(1, 9):
        g.line(X0, Y0 - k * D_, 735, Y0 - k * D_, c="#e9ecef", w=1)
        g.text(X0 - 6, Y0 - k * D_ + 4, str(k), s=10, a="end", c=GREY)
    f = lambda x: 4.2 + 2.9 * math.sin((x - X0) / 95.0) + 0.9 * math.sin((x - X0) / 37.0)
    pts = [(x, Y0 - f(x) * D_) for x in range(X0 + 2, 731, 4)]
    g.path(pts, c=BLUE, w=2)
    T = 45
    q = []
    for i in range(1, 15):
        x = X0 + i * T
        v = f(x); n = round(v)
        g.line(x, Y0, x, Y0 - v * D_, c="#adb5bd", w=1, dash="2 3")
        g.dot(x, Y0 - v * D_, c=BLUE, r=3)
        q.append((x, n))
    pts = []
    for i, (x, n) in enumerate(q):
        x2 = q[i + 1][0] if i + 1 < len(q) else x + T
        pts += [(x, Y0 - n * D_), (x2, Y0 - n * D_)]
    g.path(pts, c=ACC, w=2.4)
    g.text(X0 + T, Y0 + 18, "T", s=12, it=True); g.text(X0 + 2 * T, Y0 + 18, "2T", s=12, it=True)
    g.line(700, 150, 730, 150, c=BLUE, w=2); g.text(695, 155, "сигнал", s=12, a="end", c=BLUE)
    g.line(700, 170, 730, 170, c=ACC, w=2.4); g.text(695, 175, "квантованный", s=12, a="end", c=ACC)
    g.text(380, 125, "Шаг квантования Δ = Uмакс/2ⁿ, ошибка ±Δ/2;  частота отсчётов fд ≥ 2·fмакс (теорема Котельникова)", s=12, c=GREY)
    g.save("sv_adc")


def sar():
    g = D(760, 340)
    ti, bi, o = g.opamp(150, 95, size=64, minus_top=False)
    g.line(40, ti[1], 150, ti[1]); g.text(36, ti[1] + 5, "Uвх", s=14, a="end", it=True)
    g.text(182, 140, "компаратор", s=11, c=GREY)
    g.box(250, 55, 120, 80, "РПП", ["регистр", "последоват.", "приближения"], s=12)
    g.line(o[0], o[1], 250, o[1], arrow=True)
    g.arrow(310, 25, 310, 55); g.text(318, 30, "ГТИ, Пуск", s=12, a="start")
    g.box(95, 185, 120, 44, "ЦАП", s=14)
    g.path([(310, 135), (310, 207), (215, 207)], arrow=True, w=2.2); g.bus_label(270, 207, "n")
    g.path([(95, 207), (75, 207), (75, bi[1]), (150, bi[1])], arrow=True)
    g.arrow(155, 265, 155, 229); g.text(155, 282, "Uоп", s=13, it=True)
    g.path([(370, 95), (405, 95)], arrow=True, w=2.2); g.text(388, 86, "N", s=14, wt="bold")
    g.arrow(345, 135, 345, 170); g.text(352, 168, "Готов", s=12, a="start")
    # plot
    X0, Y0 = 450, 270
    axes(g, X0, Y0, 745, 35, "такт", "U")
    k = 12.5
    uin = 11.3
    yin = Y0 - uin * k
    g.line(X0, yin, 740, yin, c=BLUE, dash="6 4", w=1.8); g.text(456, yin - 6, "Uвх = 11,3", s=12, a="start", c=BLUE)
    vals = [(8, "1000", True), (12, "1100", False), (10, "1010", True), (11, "1011", True)]
    for i, (v, code, ok) in enumerate(vals):
        x = X0 + 15 + i * 68
        y = Y0 - v * k
        g.rect(x, y, 52, Y0 - y, c=ACC if ok else GREY, fill=FILL_ACC if ok else FILL_GREY, sw=1.4)
        g.text(x + 26, y - 8, code, s=12, wt="bold")
        g.text(x + 26, y + 30, ("<Uвх" if ok else ">Uвх"), s=11, c=INK)
        g.text(x + 26, y + 46, ("1" if ok else "0"), s=13, wt="bold", c=ACC if ok else GREY)
        g.text(x + 26, Y0 + 16, str(i + 1), s=11, c=GREY)
    g.text(595, 310, "N = 1011₂ = 11 (Uоп = 16 В, 4 разряда)", s=13, wt="bold")
    g.text(380, 333, "каждый такт решает один разряд, от старшего к младшему: n разрядов — n тактов", s=12, c=GREY)
    g.save("sv_sar")


def dual():
    g = D(760, 350)
    g.text(20, 64, "Uвх", s=13, a="start", it=True); g.line(55, 60, 92, 60); g.dot(95, 60, r=2.6)
    g.text(20, 104, "−Uоп", s=13, a="start", it=True); g.line(55, 100, 92, 100); g.dot(95, 100, r=2.6)
    g.dot(122, 80, r=2.6); g.line(122, 80, 97, 62)
    g.text(108, 128, "S", s=13, wt="bold")
    ti, bi, o = g.opamp(210, 97.5, size=70)
    g.resistor(122, 80, 190, 80, label="R"); g.line(190, 80, 210, 80); g.dot(190, 80)
    g.line(190, 80, 190, 40); g.capacitor(190, 40, 295, 40, label="C"); g.line(295, 40, 295, 97.5); g.dot(295, 97.5)
    g.line(bi[0], bi[1], bi[0] - 8, bi[1]); g.line(bi[0] - 8, bi[1], bi[0] - 8, bi[1] + 6); g.ground(bi[0] - 8, bi[1] + 6)
    g.text(245, 155, "интегратор", s=11, c=GREY)
    g.line(o[0], o[1], 320, o[1])
    t2, b2, o2 = g.opamp(320, 110, size=50, minus_top=False)
    g.line(b2[0], b2[1], b2[0] - 6, b2[1]); g.line(b2[0] - 6, b2[1], b2[0] - 6, b2[1] + 8); g.ground(b2[0] - 6, b2[1] + 8)
    g.box(245, 175, 150, 46, "Управляющая", ["логика"], s=12)
    g.path([(o2[0], o2[1]), (405, o2[1]), (405, 198), (395, 198)], arrow=True)
    g.path([(245, 198), (122, 198), (122, 90)], dash="5 4", arrow=True); g.text(130, 192, "упр. S", s=11, a="start", c=GREY)
    g.box(245, 250, 150, 40, "Счётчик", s=13)
    g.line(320, 221, 320, 250, arrow=True)
    g.arrow(180, 270, 245, 270); g.text(175, 274, "ГТИ", s=12, a="end")
    g.arrow(395, 270, 425, 270); g.text(410, 262, "N", s=13, wt="bold")
    X0, Y0 = 445, 230
    axes(g, X0, Y0, 745, 40, "t", "Uинт")
    t1 = 130
    for h, c, lab in ((60, BLUE, "Uвх1"), (110, ACC, "Uвх2")):
        g.path([(X0, Y0), (X0 + t1, Y0 - h), (X0 + t1 + h * 1.3, Y0)], c=c, w=2.4)
        g.text(X0 + t1 / 2 - 4, Y0 - h / 2 - 8, lab, s=12, c=c, a="end")
        g.line(X0 + t1 + h * 1.3, Y0, X0 + t1 + h * 1.3, Y0 + 30, c=c, dash="3 3", w=1.2)
    g.line(X0 + t1, Y0 - 115, X0 + t1, Y0 + 30, dash="3 3", c=GREY, w=1.2)
    g.text(X0 + t1 / 2, Y0 + 24, "T1 = const", s=12)
    g.text(X0 + t1 + 40, Y0 + 46, "T2 ~ Uвх", s=12)
    g.text(380, 315, "Такт 1: интегрируем Uвх фиксированное время T1 (N1 импульсов).  Такт 2: интегрируем −Uоп до нуля, считаем N2.", s=12, c=GREY)
    g.text(380, 340, "Uвх·T1 = Uоп·T2  →  N2 = N1 · Uвх / Uоп   (не зависит от R, C и частоты ГТИ)", s=14, wt="bold")
    g.save("sv_dual")


def ppi_sensor():
    g = D(760, 380)
    g.box(20, 70, 90, 170, "МП", ["i8080/8085"], s=13, fill=FILL_GREY)
    g.box(265, 50, 150, 230, None, [], s=12)
    g.text(340, 40, "ППА i8255", s=13, wt="bold")
    left = [("D0–D7", 85), ("RD, WR", 125), ("A0, A1", 160), ("RESET", 195)]
    for t, y in left:
        g.text(272, y + 5, t, s=12, a="start")
    g.line(110, 85, 265, 85, w=2.6, arrow=True, arrow2=True); g.bus_label(190, 85, 8)
    g.arrow(110, 125, 265, 125); g.arrow(110, 160, 265, 160); g.arrow(110, 195, 265, 195)
    g.box(130, 285, 110, 44, "дешифратор", ["адреса"], s=11, wt=None)
    g.path([(240, 307), (330, 307), (330, 280)], arrow=True); g.otext(345, 300, "CS", s=12)
    g.arrow(65, 240, 65, 300); g.path([(65, 300), (65, 307), (130, 307)], arrow=True); g.text(72, 290, "A2–A7", s=11, a="start")
    right = [("PA0–PA7", 90), ("PC7–PC4", 150), ("PC3–PC0", 205), ("PB0–PB7", 255)]
    for t, y in right:
        g.text(408, y + 5, t, s=12, a="end")
    g.box(520, 60, 110, 100, "АЦП", s=15, fill=FILL_BLUE)
    g.line(520, 90, 415, 90, w=2.6, arrow=True); g.bus_label(470, 90, 8)
    g.path([(520, 125), (455, 125), (455, 150), (415, 150)], arrow=True); g.text(470, 120, "Готов → PC4", s=11, a="start")
    g.path([(415, 205), (485, 205), (485, 145), (520, 145)], arrow=True); g.text(492, 188, "Пуск ← PC0", s=11, a="start")
    g.box(655, 75, 90, 44, "НУ", ["усилитель"], s=12)
    g.arrow(655, 97, 630, 97)
    g.box(655, 160, 90, 44, "Датчик", ["t°, давление"], s=12)
    g.arrow(700, 160, 700, 119)
    g.arrow(575, 195, 575, 160); g.text(575, 212, "Uоп", s=12, it=True)
    g.text(20, 352, "Режим 0, УС = 1 00 1 1 0 0 0 = 98h: PA — ввод (код АЦП), PC7–4 — ввод (Готов), PB — вывод, PC3–0 — вывод (Пуск)", s=12, a="start")
    g.text(20, 372, "Цикл: импульс на PC0 (УС2: 01h → 00h), ждать PC4 = 1 (IN PC; ANI 10h), прочитать код: IN PA", s=12, a="start", c=GREY)
    g.save("sv_ppi_sensor")


def ppi_act():
    g = D(760, 360)
    g.box(20, 90, 90, 150, "МП", s=13, fill=FILL_GREY)
    g.line(110, 120, 170, 120, w=2.6, arrow=True, arrow2=True); g.bus_label(140, 120, 8); g.text(140, 106, "", s=11)
    g.arrow(110, 160, 170, 160); g.text(140, 152, "RD WR", s=10, c=GREY)
    g.arrow(110, 200, 170, 200); g.text(140, 192, "A0 A1 CS", s=10, c=GREY)
    g.box(170, 50, 120, 250, None, [])
    g.text(230, 40, "ППА i8255", s=13, wt="bold")
    rows = [("PA", 80), ("PB0", 165), ("PB1", 215), ("PC7–4", 270)]
    for t, y in rows:
        g.text(283, y + 5, t, s=12, a="end")
    g.line(290, 80, 340, 80, w=2.6, arrow=True); g.bus_label(315, 80, 8)
    g.box(340, 58, 130, 44, "дешифратор", ["7-сегм. кода"], s=11, wt=None)
    g.arrow(470, 80, 520, 80); g.box(520, 58, 120, 44, "индикатор", s=12)
    g.arrow(290, 165, 340, 165); g.box(340, 143, 130, 44, "оптрон +", ["усилитель"], s=11, wt=None)
    g.arrow(470, 165, 520, 165); g.box(520, 143, 90, 44, "реле K1", s=12)
    g.arrow(610, 165, 655, 165); g.circle(680, 165, 22); g.text(680, 171, "M", s=16, wt="bold")
    g.text(680, 205, "двигатель", s=11, c=GREY)
    g.arrow(290, 215, 340, 215); g.box(340, 193, 130, 44, "транзисторный", ["ключ"], s=11, wt=None)
    g.arrow(470, 215, 520, 215); g.box(520, 193, 120, 44, "нагреватель", s=12)
    g.arrow(340, 270, 290, 270); g.box(340, 250, 200, 40, "концевые выключатели", s=11, wt=None)
    g.text(20, 330, "Режим 0, УС = 1 00 0 1 0 0 0 = 88h: PA, PB, PC3–0 — вывод; PC7–4 — ввод (концевики)", s=12, a="start")
    g.text(20, 350, "Включить двигатель: IN PB; ORI 01h; OUT PB.  Выключить: ANI FEh.  Бит порта C: УС2 (установка/сброс)", s=12, a="start", c=GREY)
    g.save("sv_ppi_act")


if __name__ == "__main__":
    for f in (oa, analog, comparator, dac, dac_weighted, r2r, adc, sar, dual, ppi_sensor, ppi_act):
        f(); print("ok", f.__name__)
