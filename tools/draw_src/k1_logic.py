import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svglib import *

OV = "̄"  # combining overline (macron)


def neumann():
    g = D(760, 300)
    g.box(295, 20, 170, 50, "Устройство", ["управления (УУ)"], s=14)
    g.box(30, 125, 170, 60, "Устройство", ["ввода"], s=14)
    g.box(295, 125, 170, 60, "Память (ЗУ)", ["программы и данные"], s=14, fill=FILL_BLUE)
    g.box(560, 125, 170, 60, "АЛУ", ["арифметика и логика"], s=14)
    g.box(560, 232, 170, 50, "Устройство", ["вывода"], s=14)
    g.arrow(200, 155, 293, 155)
    g.line(465, 155, 558, 155, arrow=True, arrow2=True)
    g.path([(380, 185), (380, 257), (558, 257)], arrow=True)
    g.arrow(345, 125, 345, 72)
    g.text(340, 105, "команды", s=12, a="end", c=GREY)
    # control (dashed)
    g.path([(295, 45), (115, 45), (115, 123)], dash="6 4", arrow=True)
    g.arrow(415, 70, 415, 123, dash="6 4")
    g.path([(465, 32), (745, 32), (745, 257), (732, 257)], dash="6 4", arrow=True)
    g.path([(680, 32), (680, 123)], dash="6 4", arrow=True)
    g.dot(680, 32)
    g.path([(610, 125), (610, 58), (467, 58)], c=GREY, arrow=True)
    g.text(540, 52, "признаки результата", s=12, c=GREY)
    g.line(30, 230, 70, 230); g.text(78, 234, "данные и команды", s=12, a="start")
    g.line(30, 255, 70, 255, dash="6 4"); g.text(78, 259, "управляющие сигналы", s=12, a="start")
    g.text(30, 285, "Одна память на программы и данные, команды выполняются по очереди", s=12, a="start", c=GREY)
    g.save("sv_neumann")


def decoder():
    g = D(760, 330)
    X1, NX1, X0, NX0 = 150, 175, 200, 225
    for xb in (X1, NX1, X0, NX0):
        g.line(xb, 28, xb, 300)
    g.text(20, 36, "x1", a="start", wt="bold"); g.line(40, 40, X1, 40); g.dot(X1, 40)
    g.dot(48, 40); g.path([(48, 40), (48, 85), (60, 85)])
    ins, out = g.gate(60, 65, "1", n=1, inv=True)
    g.line(out[0], 85, NX1, 85); g.dot(NX1, 85)
    g.text(20, 146, "x0", a="start", wt="bold"); g.line(40, 150, X0, 150); g.dot(X0, 150)
    g.dot(48, 150); g.path([(48, 150), (48, 195), (60, 195)])
    ins, out = g.gate(60, 175, "1", n=1, inv=True)
    g.line(out[0], 195, NX0, 195); g.dot(NX0, 195)
    for xb, t in ((X1, "x1"), (NX1, "x̄1"), (X0, "x0"), (NX0, "x̄0")):
        g.text(xb, 22, t, s=12, c=GREY)
    names = ["y0 = x̄1 · x̄0", "y1 = x̄1 · x0", "y2 = x1 · x̄0", "y3 = x1 · x0"]
    for k in range(4):
        c = 60 + 70 * k
        ins, out = g.gate(290, c - 22, "&", n=2, h=44)
        b1 = X1 if k & 2 else NX1
        b0 = X0 if k & 1 else NX0
        g.line(b1, ins[0][1], 290, ins[0][1]); g.dot(b1, ins[0][1])
        g.line(b0, ins[1][1], 290, ins[1][1]); g.dot(b0, ins[1][1])
        g.line(out[0], c, 372, c)
        g.text(380, c + 5, names[k], s=14, a="start")
    # УГО
    x, y = 560, 70
    g.rect(x, y, 130, 200)
    g.line(x + 30, y, x + 30, y + 200); g.line(x + 100, y, x + 100, y + 200)
    g.text(x + 65, y + 26, "DC", s=16, wt="bold")
    for i, (t, w) in enumerate((("x0", "1"), ("x1", "2"))):
        yy = y + 70 + 50 * i
        g.line(x - 30, yy, x, yy); g.text(x - 34, yy + 5, t, s=13, a="end"); g.text(x + 15, yy + 5, w, s=13)
    for i in range(4):
        yy = y + 40 + 40 * i
        g.line(x + 130, yy, x + 165, yy); g.text(x + 115, yy + 5, str(i), s=13); g.text(x + 170, yy + 5, f"y{i}", s=13, a="start")
    g.text(625, 300, "б) УГО дешифратора 2→4", s=13)
    g.text(250, 322, "а) схема на элементах НЕ и И (одна единица на выходе)", s=13)
    g.save("sv_dc")


def mux():
    g = D(760, 370)
    A1, NA1, A0, NA0 = 230, 255, 280, 305
    for xb in (A1, NA1, A0, NA0):
        g.line(xb, 15, xb, 355)
    g.text(18, 25, "A1", a="start", wt="bold"); g.line(40, 20, A1, 20); g.dot(A1, 20)
    g.dot(90, 20); g.path([(90, 20), (90, 55), (120, 55)])
    _, o = g.gate(120, 35, "1", n=1, inv=True); g.line(o[0], 55, NA1, 55); g.dot(NA1, 55)
    g.text(18, 90, "A0", a="start", wt="bold"); g.line(40, 85, A0, 85); g.dot(A0, 85)
    g.dot(90, 85); g.path([(90, 85), (90, 115), (120, 115)])
    _, o = g.gate(120, 95, "1", n=1, inv=True); g.line(o[0], 115, NA0, 115); g.dot(NA0, 115)
    outs = []
    for k in range(4):
        c = 140 + 65 * k
        ins, out = g.gate(360, c - 30, "&", n=3, h=60, pitch=18)
        b1 = A1 if k & 2 else NA1
        b0 = A0 if k & 1 else NA0
        g.line(b1, ins[0][1], 360, ins[0][1]); g.dot(b1, ins[0][1])
        g.line(b0, ins[1][1], 360, ins[1][1]); g.dot(b0, ins[1][1])
        g.line(40, ins[2][1], 360, ins[2][1]); g.text(18, ins[2][1] + 5, f"D{k}", a="start", wt="bold")
        outs.append(out)
    ins, o = g.gate(470, 237.5 - 35, "1", n=4, h=70, pitch=16)
    vx = [450, 440, 440, 450]
    for k in range(4):
        (ox, oy) = outs[k]
        g.path([(ox, oy), (vx[k], oy), (vx[k], ins[k][1]), (470, ins[k][1])])
    g.line(o[0], o[1], 545, o[1]); g.text(552, o[1] + 6, "Y", a="start", wt="bold", s=16)
    g.text(600, 40, "Y = Ā1·Ā0·D0 + Ā1·A0·D1 +", s=14, a="start")
    g.text(612, 62, "+ A1·Ā0·D2 + A1·A0·D3", s=14, a="start")
    # УГО
    x, y = 610, 120
    g.rect(x, y, 100, 200); g.line(x + 30, y, x + 30, y + 200); g.line(x + 30, y + 130, x, y + 130)
    g.text(x + 65, y + 26, "MS", s=16, wt="bold")
    for i in range(4):
        yy = y + 22 + 27 * i
        g.line(x - 18, yy, x, yy); g.text(x + 15, yy + 5, str(i), s=12); g.text(x - 22, yy + 5, f"D{i}", s=12, a="end")
    for i, t in enumerate(("A0", "A1")):
        yy = y + 152 + 27 * i
        g.line(x - 18, yy, x, yy); g.text(x + 15, yy + 5, str(1 << i), s=12); g.text(x - 22, yy + 5, t, s=12, a="end")
    g.line(x + 100, y + 100, x + 125, y + 100); g.text(x + 130, y + 105, "Y", s=13, a="start")
    g.text(660, 345, "УГО мультиплексора 4→1", s=13)
    g.save("sv_mux")


def triggers():
    g = D(760, 300)
    _, o1 = g.gate(120, 40, "1", n=2, h=50, inv=True)
    _, o2 = g.gate(120, 170, "1", n=2, h=50, inv=True)
    g.line(40, 55, 120, 55); g.text(34, 60, "R", a="end", wt="bold")
    g.line(40, 205, 120, 205); g.text(34, 210, "S", a="end", wt="bold")
    g.line(o1[0], 65, 300, 65); g.text(308, 70, "Q", a="start", wt="bold")
    g.line(o2[0], 195, 300, 195); g.otext(312, 200, "Q", a="middle", wt="bold")
    g.dot(210, 65); g.path([(210, 65), (210, 118), (90, 152), (90, 185), (120, 185)])
    g.dot(235, 195); g.path([(235, 195), (235, 142), (102, 108), (102, 75), (120, 75)])
    g.text(170, 255, "а) RS-триггер на ИЛИ-НЕ", s=13)
    g.text(170, 275, "S=1 → Q=1;  R=1 → Q=0;  S=R=0 — хранение", s=12, c=GREY)

    def tr(x, ins, name, dyn=None):
        y = 50
        g.rect(x, y, 70, 120); g.line(x + 24, y, x + 24, y + 120)
        g.text(x + 47, y + 24, "T", s=16, wt="bold")
        n = len(ins)
        for i, t in enumerate(ins):
            yy = y + 30 + i * (60 if n == 2 else 30)
            g.line(x - 22, yy, x, yy); g.text(x + 13, yy + 5, t, s=13, wt="bold")
            if dyn == i:
                g.path([(x, yy - 6), (x + 7, yy), (x, yy + 6)], w=1.3)
        g.line(x + 70, y + 30, x + 90, y + 30); g.text(x + 94, y + 35, "Q", s=13, a="start")
        g.bubble(x + 70, y + 90); g.line(x + 78, y + 90, x + 90, y + 90); g.otext(x + 99, y + 95, "Q", s=13)
        g.text(x + 35, y + 150, name, s=13)

    tr(370, ["D", "C"], "D-триггер")
    tr(510, ["J", "C", "K"], "JK-триггер", dyn=1)
    tr(650, ["T"], "T-триггер", dyn=0)
    g.text(560, 255, "б) условные обозначения (ГОСТ 2.743)", s=13)
    g.text(560, 275, "▷ на входе — срабатывание по фронту (динамический вход)", s=12, c=GREY)
    g.save("sv_trig")


def register():
    g = D(760, 410)
    y = 55
    for i, x in enumerate((90, 255, 420, 585)):
        g.rect(x, y, 70, 80); g.line(x + 20, y, x + 20, y + 80); g.text(x + 45, y + 22, "T", s=15, wt="bold")
        g.text(x + 10, y + 30, "D", s=12, wt="bold"); g.text(x + 10, y + 63, "C", s=12, wt="bold")
        g.path([(x - 25, 22), (x - 25, y + 25), (x, y + 25)]); g.text(x - 25, 17, f"D{i}", s=13, wt="bold")
        g.path([(x - 45, 165), (x - 45, y + 58), (x, y + 58)]); g.dot(x - 45, 165)
        g.path([(x + 70, y + 25), (x + 85, y + 25), (x + 85, 190)]); g.text(x + 85, 205, f"Q{i}", s=13, wt="bold")
    g.line(20, 165, 540, 165); g.text(20, 158, "C (запись)", s=12, a="start")
    g.text(380, 232, "а) параллельный регистр: по сигналу C все разряды записываются одновременно", s=13)
    y = 285
    xs = (110, 265, 420, 575)
    for i, x in enumerate(xs):
        g.rect(x, y, 70, 75); g.line(x + 20, y, x + 20, y + 75); g.text(x + 45, y + 22, "T", s=15, wt="bold")
        g.text(x + 10, y + 26, "D", s=12, wt="bold"); g.text(x + 10, y + 58, "C", s=12, wt="bold")
        g.path([(x, y + 47), (x + 7, y + 53), (x, y + 59)], w=1.3)
        g.path([(x - 30, 380), (x - 30, y + 53), (x, y + 53)]); g.dot(x - 30, 380)
        g.line(x + 70, y + 21, x + 100, y + 21); g.dot(x + 100, y + 21)
        g.line(x + 100, y + 21, x + 100, y - 18); g.text(x + 100, y - 23, f"Q{i}", s=13, wt="bold")
        if i < 3:
            g.line(x + 100, y + 21, xs[i + 1], y + 21)
    g.line(20, y + 21, xs[0], y + 21); g.text(20, y + 14, "DI", s=13, a="start", wt="bold")
    g.line(20, 380, 545, 380); g.text(20, 375, "C (сдвиг)", s=12, a="start")
    g.text(380, 403, "б) сдвиговый регистр: с каждым фронтом C данные сдвигаются на разряд вправо", s=13)
    g.save("sv_reg")


def counter():
    g = D(760, 400)
    y = 40
    xs = (130, 330, 530)
    for i, x in enumerate(xs):
        g.rect(x, y, 70, 80); g.line(x + 20, y, x + 20, y + 80); g.text(x + 45, y + 22, "T", s=15, wt="bold")
        g.text(x + 10, y + 45, "T", s=12, wt="bold"); g.path([(x, y + 34), (x + 7, y + 40), (x, y + 46)], w=1.3)
        g.line(x + 70, y + 18, x + 100, y + 18); g.line(x + 100, y + 18, x + 100, 12); g.dot(x + 100, y + 18)
        g.text(x + 108, 20, f"Q{i}", s=13, a="start", wt="bold"); g.text(x + 108, 36, f"(вес {1 << i})", s=11, a="start", c=GREY)
        g.bubble(x + 70, y + 62)
        if i < 2:
            g.path([(x + 78, y + 62), (xs[i + 1] - 30, y + 62), (xs[i + 1] - 30, y + 40), (xs[i + 1], y + 40)])
    g.line(20, y + 40, xs[0], y + 40); g.text(20, y + 32, "C (импульсы)", s=12, a="start")
    g.text(380, 150, "Каждый следующий триггер переключается, когда предыдущий переходит 1 → 0", s=13, c=GREY)
    rows = [("C", 205), ("Q0", 255), ("Q1", 305), ("Q2", 355)]
    dx, x0, N = 36, 90, 18
    lev = {}
    lev["C"] = [s % 2 for s in range(N)]
    cnt = [(s + 1) // 2 for s in range(N)]
    lev["Q0"] = [n % 2 for n in cnt]; lev["Q1"] = [(n // 2) % 2 for n in cnt]; lev["Q2"] = [(n // 4) % 2 for n in cnt]
    for name, yy in rows:
        g.text(40, yy - 6, name, s=13, wt="bold")
        g.wave(x0, yy, lev[name], dx, h=24, c=ACC if name != "C" else INK)
    for s in range(1, N, 2):
        g.line(x0 + s * dx, 175, x0 + s * dx, 360, c="#ced4da", w=1, dash="3 3")
    for s in range(1, N - 1, 2):
        n = cnt[s]
        g.text(x0 + (s + 1) * dx, 388, str(n % 8), s=13, wt="bold", c=BLUE)
    g.text(x0 - 20, 388, "счёт:", s=12, a="end", c=BLUE)
    g.save("sv_cnt")


def adder():
    g = D(760, 270)
    g.text(18, 60, "a", a="start", wt="bold"); g.line(35, 55, 150, 55)
    g.text(18, 80, "b", a="start", wt="bold"); g.line(35, 75, 150, 75)
    _, x1 = g.gate(150, 40, "=1", n=2, h=50)
    g.dot(95, 55); g.path([(95, 55), (95, 175), (150, 175)])
    g.dot(112, 75); g.path([(112, 75), (112, 195), (150, 195)])
    _, a1 = g.gate(150, 160, "&", n=2, h=50)
    g.line(x1[0], 65, 250, 65); g.dot(250, 65)
    _, x2 = g.gate(330, 50, "=1", n=2, h=50)
    g.line(250, 65, 330, 65)
    g.text(18, 125, "p", a="start", wt="bold"); g.line(35, 120, 300, 120); g.dot(300, 120)
    g.path([(300, 120), (300, 85), (330, 85)])
    _, a2 = g.gate(330, 135, "&", n=2, h=50)
    g.path([(250, 65), (250, 150), (330, 150)])
    g.path([(300, 120), (300, 170), (330, 170)])
    _, orr = g.gate(480, 150, "1", n=2, h=50)
    g.path([(a2[0], 160), (440, 160), (440, 165), (480, 165)])
    g.path([(a1[0], 185), (220, 185), (220, 230), (450, 230), (450, 185), (480, 185)])
    g.line(x2[0], 75, 545, 75); g.text(552, 80, "S", a="start", wt="bold", s=15)
    g.line(orr[0], 175, 545, 175); g.text(552, 180, "P", a="start", wt="bold", s=15)
    g.text(270, 60, "a⊕b", s=11, c=GREY)
    x, y = 625, 55
    g.rect(x, y, 90, 130); g.line(x + 22, y, x + 22, y + 130); g.line(x + 68, y, x + 68, y + 130)
    g.text(x + 45, y + 24, "SM", s=15, wt="bold")
    for i, t in enumerate(("a", "b", "p")):
        yy = y + 40 + 35 * i
        g.line(x - 15, yy, x, yy); g.text(x + 11, yy + 5, t, s=12, wt="bold")
    for i, t in enumerate(("S", "P")):
        yy = y + 50 + 45 * i
        g.line(x + 90, yy, x + 105, yy); g.text(x + 79, yy + 5, t, s=12, wt="bold")
    g.text(670, 210, "УГО", s=13)
    g.text(160, 262, "S = a ⊕ b ⊕ p", s=15, wt="bold")
    g.text(420, 262, "P = a·b + p·(a ⊕ b)", s=15, wt="bold")
    g.save("sv_sum")


def kmap():
    g = D(760, 320)
    cs, x0, y0 = 58, 150, 70
    gray = ["00", "01", "11", "10"]
    ones = {0, 2, 8, 10, 5, 7, 13, 15}
    for i, t in enumerate(gray):
        g.text(x0 + cs * i + cs / 2, y0 - 12, t, s=14, wt="bold")
        g.text(x0 - 12, y0 + cs * i + cs / 2 + 5, t, s=14, a="end", wt="bold")
    # groups
    g.rect(x0 + cs + 6, y0 + cs + 6, 2 * cs - 12, 2 * cs - 12, c=ACC, fill=FILL_ACC, sw=2.4, rx=14)
    for (cx, cy) in ((0, 0), (3, 0), (0, 3), (3, 3)):
        xx = x0 + cx * cs + (6 if cx == 0 else 6)
        yy = y0 + cy * cs + 6
        g.rect(xx - (30 if cx == 0 else 0), yy - (30 if cy == 0 else 0), cs - 12 + 30, cs - 12 + 30, c=BLUE, fill=FILL_BLUE, sw=2.4, rx=14)
    g.rect(x0 - 2, y0 - 2, 4 * cs + 4, 4 * cs + 4, c="#fff", fill="none", sw=0)
    # mask overflow of corner groups
    g.rect(x0 - 40, y0 - 40, 4 * cs + 80, 38, c="#fff", fill="#fff", sw=0)
    g.rect(x0 - 40, y0 + 4 * cs + 2, 4 * cs + 80, 40, c="#fff", fill="#fff", sw=0)
    g.rect(x0 - 40, y0 - 2, 38, 4 * cs + 4, c="#fff", fill="#fff", sw=0)
    g.rect(x0 + 4 * cs + 2, y0 - 2, 38, 4 * cs + 4, c="#fff", fill="#fff", sw=0)
    for i, t in enumerate(gray):
        g.text(x0 + cs * i + cs / 2, y0 - 12, t, s=14, wt="bold")
        g.text(x0 - 12, y0 + cs * i + cs / 2 + 5, t, s=14, a="end", wt="bold")
    g.text(x0 - 12, y0 - 14 - 18, "ab \\ cd", s=13, a="end", c=GREY)
    for r in range(4):
        for c in range(4):
            a, b = int(gray[r][0]), int(gray[r][1]); cc, d = int(gray[c][0]), int(gray[c][1])
            m = 8 * a + 4 * b + 2 * cc + d
            x, y = x0 + c * cs, y0 + r * cs
            g.rect(x, y, cs, cs, fill="none", sw=1.2)
            g.text(x + cs / 2, y + cs / 2 + 7, "1" if m in ones else "0", s=20, wt="bold" if m in ones else None, c=INK if m in ones else "#adb5bd")
            g.text(x + cs - 5, y + 13, str(m), s=10, a="end", c=GREY)
    tx = 425
    g.text(tx, 90, "Карта Карно для f(a,b,c,d) = Σ(0,2,5,7,8,10,13,15)", s=13, a="start")
    g.rect(tx, 112, 16, 16, c=ACC, fill=FILL_ACC, sw=2, rx=4); g.text(tx + 24, 125, "центр 2×2: b = 1, d = 1 → b·d", s=14, a="start")
    g.rect(tx, 142, 16, 16, c=BLUE, fill=FILL_BLUE, sw=2, rx=4); g.text(tx + 24, 155, "4 угла (карта «замкнута»): b = 0, d = 0", s=14, a="start")
    g.text(tx + 24, 175, "→ b̄·d̄", s=14, a="start")
    g.text(tx, 220, "f = b̄·d̄ + b·d", s=22, a="start", wt="bold", c=ACC)
    g.text(tx, 252, "Соседние клетки отличаются одной переменной;", s=13, a="start", c=GREY)
    g.text(tx, 270, "группа из 2^k единиц убирает k переменных.", s=13, a="start", c=GREY)
    g.save("sv_kmap")


def basis():
    g = D(760, 260)

    def half(dx, nand):
        sym = "&"
        _, o1 = g.gate(dx + 100, 40, sym, n=2, h=44, inv=nand)
        _, o2 = g.gate(dx + 100, 120, sym, n=2, h=44, inv=nand)
        for t, yy in (("a", 52), ("b", 72), ("c", 132), ("d", 152)):
            g.line(dx + 50, yy, dx + 100, yy); g.text(dx + 42, yy + 5, t, s=14, a="end", wt="bold")
        _, o3 = g.gate(dx + 220, 80, "&" if nand else "1", n=2, h=44, inv=nand)
        g.path([(o1[0], 62), (dx + 190, 62), (dx + 190, 92), (dx + 220, 92)])
        g.path([(o2[0], 142), (dx + 190, 142), (dx + 190, 112), (dx + 220, 112)])
        g.line(o3[0], 102, dx + 320, 102); g.text(dx + 328, 107, "f", s=15, a="start", wt="bold")

    half(0, False)
    half(390, True)
    g.text(190, 195, "а) базис И, ИЛИ: f = a·b + c·d", s=14)
    g.text(580, 195, "б) базис И-НЕ (Шеффер)", s=14)
    g.text(380, 235, "f = a·b + c·d  =  ¬¬(a·b + c·d)  =  ¬( ¬(a·b) · ¬(c·d) )   — двойное отрицание + закон де Моргана", s=14, wt="bold")
    g.save("sv_basis")


def fpe():
    g = D(760, 215)
    # NOT
    g.text(20, 85, "x", s=14, a="start", wt="bold"); g.line(35, 80, 75, 80); g.dot(75, 80)
    g.path([(75, 80), (75, 70), (100, 70)]); g.path([(75, 80), (75, 90), (100, 90)])
    _, o = g.gate(100, 58, "&", n=2, h=44, inv=True); g.line(o[0], 80, 180, 80); g.text(186, 85, "x̄", s=15, a="start", wt="bold")
    g.text(110, 160, "НЕ: ¬(x·x) = x̄", s=14)
    # AND
    g.text(240, 75, "a", s=14, a="start", wt="bold"); g.line(255, 70, 300, 70)
    g.text(240, 95, "b", s=14, a="start", wt="bold"); g.line(255, 90, 300, 90)
    _, o = g.gate(300, 58, "&", n=2, h=44, inv=True)
    g.dot(372, 80); g.path([(o[0], 80), (372, 80)]); g.path([(372, 80), (372, 70), (390, 70)]); g.path([(372, 80), (372, 90), (390, 90)])
    _, o = g.gate(390, 58, "&", n=2, h=44, inv=True); g.line(o[0], 80, 470, 80); g.text(476, 85, "a·b", s=15, a="start", wt="bold")
    g.text(370, 160, "И: ¬(¬(a·b))", s=14)
    # OR
    for t, yy, cy in (("a", 40, 40), ("b", 120, 120)):
        g.text(525, yy + 5, t, s=14, a="start", wt="bold"); g.line(540, yy, 560, yy); g.dot(560, yy)
        g.path([(560, yy), (560, yy - 10), (575, yy - 10)]); g.path([(560, yy), (560, yy + 10), (575, yy + 10)])
        g.gate(575, yy - 22, "&", n=2, h=44, inv=True)
    _, o = g.gate(660, 58, "&", n=2, h=44, inv=True)
    g.path([(625, 40), (645, 40), (645, 70), (660, 70)]); g.path([(625, 120), (645, 120), (645, 90), (660, 90)])
    g.line(o[0], 80, 742, 80); g.text(712, 70, "a+b", s=14, a="start", wt="bold")
    g.text(640, 160, "ИЛИ: ¬(ā·b̄) = a + b", s=14)
    g.text(380, 200, "Из одних элементов И-НЕ строится любая функция — поэтому И-НЕ функционально полный элемент", s=13, c=GREY)
    g.save("sv_fpe")


if __name__ == "__main__":
    for f in (neumann, decoder, mux, triggers, register, counter, adder, kmap, basis, fpe):
        f(); print("ok", f.__name__)
