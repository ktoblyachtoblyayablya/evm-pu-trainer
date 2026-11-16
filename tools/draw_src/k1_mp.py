import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svglib import *

M2C = "#1c6dd0"
M3C = "#2b8a3e"


def badge(g, x, y, n, c=ACC):
    g.circle(x, y, 11, c=c, fill=c, sw=1)
    g.text(x, y + 5, str(n), s=13, wt="bold", c="#fff")


def base(g, hl_cells=()):
    """simplified structure of the base 8-bit MP (i8080/8085) with memory"""
    # memory and buffers
    g.box(210, 25, 130, 70, "Память", ["(ОЗУ/ПЗУ)"], s=14, fill=FILL_GREY)
    g.box(45, 35, 95, 50, "Буфер", ["данных"], s=13)
    g.box(600, 35, 105, 50, "Буфер", ["адреса"], s=13)
    g.line(140, 60, 210, 60, w=2.4); g.text(175, 52, "ШД", s=12, wt="bold")
    g.line(340, 60, 600, 60, w=2.4); g.text(470, 52, "ША (A15–A0)", s=12, wt="bold")
    # internal bus
    g.line(30, 150, 730, 150, w=4, c="#495057")
    g.text(470, 142, "внутренняя шина данных (8 бит)", s=12, c="#495057")
    g.line(92, 85, 92, 150, w=2.2)
    # accumulator, temp, alu, flags
    g.box(55, 185, 90, 36, "A", s=14, fill="#fff")
    g.text(100, 236, "аккумулятор", s=11, c=GREY)
    g.line(100, 150, 100, 185, w=2.2)
    g.box(160, 185, 70, 36, "БРВ", s=13)
    g.line(195, 150, 195, 185, w=2.2)
    g.path([(55, 262), (230, 262), (198, 312), (87, 312)], close=True, fill="#fff")
    g.text(142, 293, "АЛУ", s=15, wt="bold")
    g.line(100, 221, 100, 262, w=1.6, arrow=True)
    g.path([(195, 221), (195, 245), (172, 245), (172, 262)], arrow=True)
    g.path([(142, 312), (142, 338), (38, 338), (38, 150)], w=1.6, arrow=True)
    g.box(255, 275, 64, 34, "RF", s=13)
    g.text(287, 324, "флаги", s=11, c=GREY)
    g.arrow(214, 291, 255, 291)
    # IR + decoder
    g.box(345, 185, 80, 36, "РК (IR)", s=13)
    g.line(385, 150, 385, 185, w=2.2)
    g.box(335, 258, 120, 62, "ДК и автомат", ["управления"], s=12)
    g.arrow(385, 221, 385, 258)
    g.arrow(319, 292, 335, 292)
    g.text(395, 340, "RD, WR, ALE, IO/M̄ …", s=11, c=GREY)
    # register block
    x0, y0 = 520, 180
    g.rect(x0, y0, 180, 16, fill=FILL_GREY); g.text(x0 + 90, y0 + 12, "блок регистров", s=11)
    rows = [("W", "Z"), ("B", "C"), ("D", "E"), ("H", "L"), ("SP",), ("PC",)]
    for i, r in enumerate(rows):
        yy = y0 + 16 + 28 * i
        if len(r) == 2:
            for j, t in enumerate(r):
                f = FILL_ACC if t in hl_cells else "#fff"
                g.rect(x0 + 90 * j, yy, 90, 28, fill=f); g.text(x0 + 90 * j + 45, yy + 19, t, s=13, wt="bold")
        else:
            f = FILL_ACC if r[0] in hl_cells else "#fff"
            g.rect(x0, yy, 180, 28, fill=f); g.text(x0 + 90, yy + 19, r[0], s=13, wt="bold")
    g.line(610, 150, 610, 180, w=2.2)
    g.box(540, 382, 140, 30, "+1 / −1", s=12)
    g.line(610, 364, 610, 382)
    # address path from registers to address buffer
    g.line(715, 60, 715, 350, w=2.2)
    g.line(705, 60, 715, 60, w=2.2)
    for yy in (294, 350):
        g.line(700, yy, 715, yy, w=2.2)
    return g


def hl(g, pts, c, w=5):
    g.path(pts, c=c, w=w)


def movam():
    g = D(760, 560)
    base(g, hl_cells=("H", "L"))
    # M1 fetch
    hl(g, [(700, 350), (715, 350), (715, 60), (705, 60)], ACC)
    hl(g, [(600, 60), (340, 60)], ACC)
    hl(g, [(210, 60), (140, 60)], ACC)
    hl(g, [(92, 85), (92, 150), (385, 150), (385, 185)], ACC)
    # M2 read via HL
    hl(g, [(700, 294), (722, 294), (722, 66), (705, 66)], M2C)
    hl(g, [(600, 67), (340, 67)], M2C)
    hl(g, [(210, 67), (140, 67)], M2C)
    hl(g, [(99, 85), (99, 156), (107, 156), (107, 185)], M2C)
    badge(g, 735, 340, 1); badge(g, 410, 172, 2, ACC); badge(g, 322, 247, 3, ACC)
    badge(g, 740, 290, 4, M2C); badge(g, 175, 85, 5, M2C); badge(g, 125, 175, 6, M2C)
    g.text(395, 247, "7E → MOV A,M", s=11, c=ACC, wt="bold")
    ly = 440
    g.text(30, ly, "MOV A,M — код 7E, 1 байт, 2 машинных цикла (M1 — 4 такта, M2 — 3 такта)", s=14, a="start", wt="bold")
    g.line(30, ly + 18, 60, ly + 18, c=ACC, w=5); g.text(68, ly + 23, "M1 — выборка кода команды", s=13, a="start")
    g.line(330, ly + 18, 360, ly + 18, c=M2C, w=5); g.text(368, ly + 23, "M2 — чтение операнда из памяти по адресу HL", s=13, a="start")
    steps = ["① PC → буфер адреса → ША: адрес команды; PC := PC + 1",
             "② память → ШД → буфер данных → внутренняя шина → РК (код 7E)",
             "③ ДК расшифровывает код: нужен цикл чтения памяти, адрес в паре HL",
             "④ H, L → буфер адреса → ША;  ⑤ память → ШД → буфер данных;  ⑥ → внутренняя шина → A"]
    for i, t in enumerate(steps):
        g.text(30, ly + 50 + 20 * i, t, s=13, a="start")
    g.save("sv_movam")


def jnz():
    g = D(760, 580)
    base(g, hl_cells=("W", "Z", "PC"))
    hl(g, [(700, 350), (715, 350), (715, 60), (705, 60)], ACC)
    hl(g, [(600, 60), (340, 60)], ACC)
    hl(g, [(210, 60), (140, 60)], ACC)
    hl(g, [(92, 85), (92, 150), (385, 150), (385, 185)], ACC)
    hl(g, [(99, 85), (99, 156), (604, 156), (604, 180)], M2C)
    hl(g, [(287, 309), (287, 330), (330, 330), (335, 300)], M3C, w=4)
    g.d("M 520 202 C 470 230, 470 330, 520 350", c=M3C, w=3.5, dash="7 5", arrow=True)
    badge(g, 735, 340, 1); badge(g, 410, 172, 2); badge(g, 322, 247, 3)
    badge(g, 560, 168, 4, M2C); badge(g, 300, 346, 5, M3C); badge(g, 470, 300, 6, M3C)
    g.text(483, 268, "WZ→PC", s=11, c=M3C, wt="bold", a="end")
    ly = 440
    g.text(30, ly, "JNZ 1004 — код C2 04 10, 3 байта, 3 машинных цикла (4 + 3 + 3 = 10 тактов)", s=14, a="start", wt="bold")
    g.line(30, ly + 18, 60, ly + 18, c=ACC, w=5); g.text(68, ly + 23, "M1 — выборка кода", s=13, a="start")
    g.line(230, ly + 18, 260, ly + 18, c=M2C, w=5); g.text(268, ly + 23, "M2, M3 — чтение адреса в W, Z", s=13, a="start")
    g.line(510, ly + 18, 540, ly + 18, c=M3C, w=5); g.text(548, ly + 23, "проверка Z и переход", s=13, a="start")
    steps = ["① PC → ША (адрес кода);  ② память → РК: код C2;  ③ ДК: нужны ещё 2 байта (адрес перехода)",
             "④ M2: PC → ША, память → Z (04, младший байт);  M3: PC → ША, память → W (10, старший байт)",
             "⑤ автомат управления проверяет флаг Z в регистре признаков RF",
             "⑥ Z = 0 (результат не ноль) → WZ = 1004 → PC, переход;  Z = 1 → PC уже указывает",
             "    на следующую команду (адрес команды + 3), переход не выполняется"]
    for i, t in enumerate(steps):
        g.text(30, ly + 50 + 20 * i, t, s=13, a="start")
    g.save("sv_jnz")


def alu():
    g = D(760, 340)
    g.line(20, 40, 740, 40, w=4, c="#495057"); g.text(380, 30, "внутренняя шина данных", s=12, c="#495057")
    g.box(80, 75, 110, 40, "Аккумулятор A", s=13, fill=FILL_BLUE)
    g.line(135, 40, 135, 75, w=2.2)
    g.box(80, 145, 110, 36, "БРА", s=13); g.arrow(135, 115, 135, 145)
    g.box(270, 145, 110, 36, "БРВ", s=13); g.line(325, 40, 325, 145, w=2.2)
    g.path([(60, 215), (400, 215), (350, 285), (110, 285)], close=True, fill=FILL_ACC, c=ACC)
    g.text(230, 245, "АЛУ", s=17, wt="bold")
    g.text(230, 267, "+, −, И, ИЛИ, ⊕, сдвиг, сравнение", s=12)
    g.arrow(135, 181, 135, 215); g.arrow(325, 181, 325, 215)
    g.path([(230, 285), (230, 310), (30, 310), (30, 40)], arrow=True, w=2)
    g.text(120, 326, "результат → шина → A", s=12, c=GREY)
    g.box(470, 145, 150, 36, "десятичный", ["корректор (DAA)"], s=12, wt=None)
    g.arrow(400, 163, 470, 163); g.line(545, 40, 545, 145, w=1.6)
    # flags register
    fx, fy = 460, 240
    for i, t in enumerate(("S", "Z", "0", "AC", "0", "P", "1", "CY")):
        g.rect(fx + 34 * i, fy, 34, 30, fill="#fff"); g.text(fx + 17 + 34 * i, fy + 20, t, s=12, wt="bold")
    g.text(fx + 136, fy + 50, "регистр признаков RF (F)", s=12, c=GREY)
    g.arrow(380, 250, 460, 255)
    g.path([(700, 240), (700, 70), (700, 40)], w=1.6)
    g.text(692, 120, "PUSH PSW", s=11, c=GREY, a="end")
    g.arrow(452, 212, 394, 228, c=GREY, dash="5 4")
    g.text(458, 216, "код операции (от ДК)", s=11, c=GREY, a="start")
    g.save("sv_alu")


def cu():
    g = D(760, 330)
    g.box(30, 30, 110, 40, "РК (IR)", s=13)
    g.box(30, 110, 110, 56, "дешифратор", ["команд"], s=12, wt=None)
    g.arrow(85, 70, 85, 110)
    g.box(30, 220, 110, 40, "RF (флаги)", s=12)
    g.box(220, 20, 140, 44, "генератор", ["тактов (CLK)"], s=12, wt=None)
    g.box(390, 20, 170, 44, "счётчик тактов T1–T6", ["и циклов M1–M5"], s=12, wt=None)
    g.arrow(360, 42, 390, 42)
    g.box(220, 100, 340, 140, "Автомат управления", ["комбинационная схема:", "код команды + номер такта + условия", "→ управляющие сигналы"], s=13, fill=FILL_ACC, c=ACC)
    g.arrow(475, 64, 475, 100)
    g.arrow(140, 138, 220, 138); g.path([(140, 240), (180, 240), (180, 200), (220, 200)], arrow=True)
    for i, t in enumerate(("READY", "HOLD", "INTR", "RESET IN")):
        x = 250 + 85 * i
        g.arrow(x, 300, x, 240); g.text(x, 318, t, s=12, wt="bold")
    g.arrow(560, 140, 592, 140); g.text(598, 134, "внутренние сигналы:", s=12, a="start")
    g.text(598, 152, "регистры, АЛУ, буферы", s=12, a="start", c=GREY)
    g.arrow(560, 200, 592, 200); g.text(598, 194, "на шину управления:", s=12, a="start")
    g.text(598, 212, "RD, WR, ALE, IO/M̄,", s=12, a="start", c=GREY)
    g.text(598, 228, "S0, S1, INTA, HLDA", s=12, a="start", c=GREY)
    g.text(220, 280, "", s=12)
    g.save("sv_cu")


def pc():
    g = D(760, 300)
    g.box(265, 120, 220, 46, "PC", ["программный счётчик, 16 бит"], s=13, fill=FILL_ACC, c=ACC)
    g.box(290, 25, 170, 44, "Буфер адреса", s=13)
    g.arrow(375, 120, 375, 69)
    g.box(590, 18, 140, 58, "Память", ["команды"], s=13, fill=FILL_GREY)
    g.arrow(460, 47, 590, 47); g.text(525, 40, "ША", s=12, wt="bold")
    g.box(60, 120, 140, 46, "+1", ["после каждого байта"], s=13)
    g.path([(265, 133), (200, 133)], arrow=True); g.path([(200, 153), (265, 153)], arrow=True)
    g.box(30, 225, 160, 50, "W, Z ← адрес", ["JMP, Jcc, CALL"], s=12)
    g.box(215, 225, 150, 50, "стек → PC", ["RET, Rcc"], s=12)
    g.box(390, 225, 150, 50, "HL → PC", ["PCHL"], s=12)
    g.box(565, 225, 160, 50, "RESET → 0000", ["(RST n → 8·n)"], s=12)
    for x in (110, 290, 465, 645):
        g.path([(x, 225), (x, 200), (375, 200), (375, 166)], arrow=True if x == 465 else False)
    g.arrow(375, 200, 375, 168)
    g.box(560, 120, 170, 46, "стек", ["CALL: PC → стек"], s=12)
    g.arrow(485, 143, 560, 143)
    g.save("sv_pc")


def sp():
    g = D(760, 360)
    addrs = ["EFFB", "EFFC", "EFFD", "EFFE", "EFFF"]
    cols = [("исходно: SP = F000", {}, 5), ("после PUSH B (B=12, C=34)", {4: "12  (B)", 3: "34  (C)"}, 3),
            ("после CALL 1031 (возврат 100D)", {4: "12", 3: "34", 2: "10  (PCст)", 1: "0D  (PCмл)"}, 1)]
    for ci, (title, vals, spi) in enumerate(cols):
        x = 95 + 230 * ci
        g.text(x + 60, 30, title, s=13, wt="bold")
        for r, a in enumerate(addrs):
            y = 50 + 36 * r
            f = FILL_ACC if r in vals else "#fff"
            g.rect(x, y, 120, 36, fill=f)
            g.text(x - 6, y + 23, a, s=12, a="end", c=GREY)
            if r in vals:
                g.text(x + 60, y + 23, vals[r], s=13, wt="bold")
        g.text(x - 6, 50 + 36 * 5 + 15, "F000", s=12, a="end", c=GREY)
        g.line(x, 50 + 36 * 5, x + 120, 50 + 36 * 5, dash="4 3")
        ya = 50 + 36 * spi
        g.arrow(x + 175, ya, x + 124, ya, c=ACC, w=2.4)
        g.text(x + 178, ya + 5, "SP", s=13, wt="bold", c=ACC, a="start")
    g.arrow(36, 230, 36, 60, c=BLUE, w=2)
    g.raw('<text x="20" y="140" font-size="12" fill="#1c6dd0" text-anchor="middle" transform="rotate(-90 20 140)">рост стека</text>')
    g.text(380, 280, "PUSH rp: SP := SP−1, [SP] := старший байт; SP := SP−1, [SP] := младший байт", s=13)
    g.text(380, 302, "POP rp: младший := [SP]; SP := SP+1; старший := [SP]; SP := SP+1", s=13)
    g.text(380, 324, "CALL: адрес возврата (PC) → в стек, затем переход;  RET: PC ← из стека", s=13)
    g.text(380, 346, "Стек растёт в сторону меньших адресов, SP указывает на последний записанный байт", s=12, c=GREY)
    g.save("sv_sp")


if __name__ == "__main__":
    for f in (movam, jnz, alu, cu, pc, sp):
        f(); print("ok", f.__name__)
