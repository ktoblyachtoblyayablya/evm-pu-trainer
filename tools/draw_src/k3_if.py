import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from svglib import *


def tree(g, root, rx, ry, rw, branches, y1=100, bw=None, gap=10, s=13, item_h=24, fills=None):
    """root box + columns of branches with items. branches = [(title, [items]), ...]"""
    g.box(rx - rw / 2, ry, rw, 36, root, s=15, fill=FILL_ACC, c=ACC)
    n = len(branches)
    W = g.w - 40
    bw = bw or (W - gap * (n - 1)) / n
    xs = [20 + i * (bw + gap) for i in range(n)]
    g.line(xs[0] + bw / 2, y1 - 18, xs[-1] + bw / 2, y1 - 18)
    g.line(rx, ry + 36, rx, y1 - 18)
    for i, (t, items) in enumerate(branches):
        x = xs[i]
        g.arrow(x + bw / 2, y1 - 18, x + bw / 2, y1)
        f = fills[i] if fills else FILL_BLUE
        tl = t.split("\n")
        hh = 22 + 16 * (len(tl) - 1) + 12
        g.rect(x, y1, bw, hh, fill=f, rx=4)
        for k, tt in enumerate(tl):
            g.text(x + bw / 2, y1 + 20 + 16 * k, tt, s=s, wt="bold")
        y = y1 + hh + 8
        for it in items:
            g.line(x + 10, y - 8, x + 10, y + item_h / 2 - 8, c=GREY, w=1.2)
            g.line(x + 10, y + item_h / 2 - 8, x + 16, y + item_h / 2 - 8, c=GREY, w=1.2)
            g.text(x + 20, y + item_h / 2 - 4, it, s=s - 1, a="start")
            y += item_h
    return xs, bw


def ifclass():
    g = D(760, 360)
    tree(g, "Интерфейсы ЭВМ", 380, 15, 220, [
        ("Параллельные\nнизкоскоростные", ["IEEE 1284 (LPT,", "  Centronics, EPP, ECP)"]),
        ("Параллельные\nвысокоскоростные", ["ISA, PCI, AGP", "SCSI, P-ATA (IDE)"]),
        ("Последовательные\nнизкоскоростные", ["RS-232C (COM)", "RS-422A, RS-485", "IrDA"]),
        ("Последовательные\nвысокоскоростные", ["USB, IEEE 1394", "PCI Express, S-ATA", "DVI, Fibre Channel"]),
        ("Беспроводные\n(радиоинтерфейсы)", ["Bluetooth (WPAN)", "Wi-Fi (WLAN)", "WiMAX, GSM/3G"]),
    ], y1=90, s=12)
    y = 268
    crit = [("по синхронизации:", "синхронные / асинхронные"), ("по направлению:", "симплекс / полудуплекс / дуплекс"),
            ("по назначению:", "системные и локальные шины, периферийные, сетевые"), ("по топологии:", "общая шина, звезда, кольцо, дерево, точка-точка")]
    for i, (a, b) in enumerate(crit):
        yy = y + 22 * i
        g.text(30, yy, a, s=13, a="start", wt="bold"); g.text(185, yy, b, s=13, a="start")
    g.save("sv_ifclass")


def fields(g, x, y, items, h=34, title=None, scale=1.0):
    if title:
        g.text(x, y - 8, title, s=13, a="start", wt="bold")
    for name, w, sub, fill in items:
        w = w * scale
        g.rect(x, y, w, h, fill=fill)
        g.text(x + w / 2, y + (15 if sub else 22), name, s=12, wt="bold")
        if sub:
            g.text(x + w / 2, y + 29, sub, s=10, c=GREY)
        x += w
    return x


def usbpkt():
    g = D(760, 405)
    W, F, P, Y = "#fff", FILL_GREY, FILL_ACC, FILL_BLUE
    sync = ("SYNC", 70, "8 бит", F)
    pid = ("PID", 70, "8 бит", P)
    eop = ("EOP", 60, "", F)
    fields(g, 30, 40, [sync, pid, ("ADDR", 95, "7 бит", Y), ("ENDP", 75, "4 бита", Y), ("CRC5", 70, "5 бит", W), eop], title="Маркер (Token): OUT, IN, SETUP — кто и с какой конечной точкой обменивается")
    fields(g, 30, 115, [sync, pid, ("номер кадра", 170, "11 бит", Y), ("CRC5", 70, "5 бит", W), eop], title="SOF — начало кадра (каждую 1 мс; микрокадр HS — 125 мкс)")
    fields(g, 30, 190, [sync, pid, ("данные", 260, "0–1023 байт (FS), до 1024 (HS)", Y), ("CRC16", 80, "16 бит", W), eop], title="Данные (Data): DATA0 / DATA1 — чередуются для обнаружения повторов")
    fields(g, 30, 265, [sync, pid, eop], title="Квитирование (Handshake): ACK, NAK, STALL (NYET в HS)")
    x = 300
    g.text(x, 306, "PID: 4 бита типа + те же 4 бита инверсно (самоконтроль)", s=12, a="start", c=GREY)
    for i, t in enumerate(("PID0", "PID1", "PID2", "PID3", "PID̄0", "PID̄1", "PID̄2", "PID̄3")):
        g.rect(x + 50 * i, 265, 50, 26, fill=P if i < 4 else W); g.text(x + 25 + 50 * i, 283, t, s=11)
    g.text(30, 350, "Транзакция:", s=13, a="start", wt="bold")
    bx = [("маркер", "IN / OUT / SETUP"), ("данные", "DATA0 / DATA1"), ("квитирование", "ACK / NAK / STALL")]
    for i, (a, b) in enumerate(bx):
        xx = 140 + 200 * i
        g.box(xx, 325, 150, 40, a, [b], s=12)
        if i < 2:
            g.arrow(xx + 150, 345, xx + 200, 345)
    g.text(380, 390, "кодирование NRZI с битстаффингом; SYNC = 00000001 (KJKJKJKK), EOP — два бита SE0", s=12, c=GREY)
    g.save("sv_usbpkt")


def xor(g, x, y, r=12):
    g.circle(x, y, r, fill="#fff"); g.line(x - r, y, x + r, y, w=1.4); g.line(x, y - r, x, y + r, w=1.4)


def crc():
    g = D(760, 300)
    y = 120
    g.text(20, y - 14, "данные", s=12, a="start"); g.text(20, y + 2, "(мл. бит", s=11, a="start", c=GREY); g.text(20, y + 15, "вперёд)", s=11, a="start", c=GREY)
    g.arrow(70, y, 98, y)
    xor(g, 110, y)
    regs = [(150, "c0"), (240, "c1"), (360, "c2"), (450, "c3"), (540, "c4")]
    g.line(122, y, 150, y); g.dot(135, y)
    for i, (x, t) in enumerate(regs):
        g.rect(x, y - 20, 60, 40, fill=FILL_BLUE); g.text(x + 30, y + 6, t, s=14, wt="bold")
    g.arrow(210, y, 240, y)
    g.line(300, y, 318, y); xor(g, 330, y); g.arrow(342, y, 360, y)
    g.arrow(420, y, 450, y); g.arrow(510, y, 540, y)
    g.line(600, y, 640, y); g.dot(640, y); g.arrow(640, y, 680, y); g.text(688, y + 5, "CRC", s=12, a="start")
    g.path([(640, y), (640, 55), (110, 55), (110, y - 12)], arrow=True)
    g.text(380, 47, "обратная связь f = d ⊕ c4", s=12, c=GREY)
    g.path([(135, y), (135, 180), (330, 180), (330, y + 12)], arrow=True)
    g.text(232, 196, "f → в разряд x²", s=12, c=GREY)
    g.text(380, 235, "USB CRC5: G(x) = x⁵ + x² + 1 (для маркеров);  CRC16: G(x) = x¹⁶ + x¹⁵ + x² + 1 (для данных)", s=13, wt="bold")
    g.text(380, 258, "Передатчик: регистр = 11111, прогоняет поле, CRC = инверсия регистра.", s=12)
    g.text(380, 278, "Приёмник прогоняет поле вместе с CRC: без ошибок остаток постоянен (CRC5 — 01100).", s=12)
    g.save("sv_crc")


def alt():
    g = D(760, 400)
    cols = ["IBM PC (классика)", "PCI / PCIe, многоядерные x86", "микроконтроллеры ARM, SoC"]
    xs = [20, 270, 520]
    for x, t in zip(xs, cols):
        g.text(x + 110, 22, t, s=13, wt="bold")
    g.text(8, 120, "", s=1)
    rows = [
        ("Прерывания", 40, [["ВУ: IRQ0–IRQ15", "2 × 8259 (ведущий + ведомый)", "ЦП: INTR → INTA, № вектора"],
                            ["устройство: MSI — запись сообщения", "в память по шине", "LAPIC ядра → обработчик"],
                            ["периферия: линии запросов", "NVIC в ядре: приоритеты,", "вложенность, таблица векторов"]]),
        ("ПДП", 215, [["ВУ: DRQ → 8237 (КПДП)", "HOLD/HLDA: КПДП захватывает", "шину, ВУ ↔ память"],
                      ["контроллер устройства —", "ведущий шины (bus master)", "REQ#/GNT#, сам пишет в память"],
                      ["многоканальный DMA на", "шине AHB/AXI: дескрипторы,", "периферия ↔ память без ЦП"]]),
    ]
    for name, y0, cells in rows:
        g.raw(f'<text x="14" y="{y0 + 80}" font-size="14" font-weight="bold" fill="{ACC}" text-anchor="middle" transform="rotate(-90 14 {y0 + 80})">{name}</text>')
        for x, cell in zip(xs, cells):
            for k, t in enumerate(cell):
                yy = y0 + k * 52
                g.box(x + 4, yy, 236, 34, None, [t], s=11, fill=FILL_BLUE if k == 1 else "#fff")
                if k < 2:
                    g.arrow(x + 120, yy + 34, x + 120, yy + 52)
    g.text(380, 385, "Итог: вместо отдельных микросхем 8259/8237 — APIC, MSI и bus mastering в ПК, NVIC и DMA-контроллеры в SoC", s=12, c=GREY)
    g.save("sv_alt")


def puclass():
    g = D(760, 360)
    tree(g, "Периферийные устройства ЭВМ", 380, 15, 280, [
        ("Устройства\nввода", ["клавиатура", "мышь, трекбол", "сканеры", "дигитайзеры", "цифровые камеры"]),
        ("Устройства\nвывода", ["мониторы: ЭЛТ, ЖК,", "  плазма, OLED, FED", "принтеры, плоттеры", "видеопроекторы"]),
        ("Ввода-\nвывода", ["модемы", "УСО (АЦП, ЦАП,", "  дискретные входы)", "аудио-, видеоадаптеры"]),
        ("Внешние ЗУ\n(накопители)", ["магнитные диски (HDD)", "оптические CD/DVD", "магнитооптические", "ленточные (стриммеры)", "твердотельные (SSD, flash)"]),
    ], y1=90, s=13)
    g.text(380, 320, "Другие признаки: скорость обмена (низко-/высокоскоростные), способ подключения (внутренние / внешние,", s=12, c=GREY)
    g.text(380, 338, "через какой интерфейс), природа информации (символьная, графическая, аналоговая, звуковая)", s=12, c=GREY)
    g.save("sv_puclass")


def usodesign():
    g = D(760, 400)
    g.box(20, 110, 80, 160, "МП", s=14, fill=FILL_GREY)
    g.box(150, 40, 130, 290, None, [])
    g.text(215, 30, "ППА i8255", s=13, wt="bold")
    g.line(100, 140, 150, 140, w=2.6, arrow=True, arrow2=True); g.bus_label(125, 140, 8)
    g.arrow(100, 180, 150, 180); g.text(125, 172, "RD WR", s=10, c=GREY)
    g.arrow(100, 215, 150, 215); g.text(125, 207, "A0 A1", s=10, c=GREY)
    g.box(40, 300, 90, 40, "ДША", s=12); g.path([(130, 320), (150, 320)], arrow=True); g.otext(165, 312, "CS", s=11)
    g.arrow(60, 270, 60, 300)
    for t, yy in (("PA0–7", 75), ("PC4 (Готов)", 110), ("PC3 Пуск", 150), ("PC2 УВХ", 180), ("PC0–1 адрес", 210), ("PB0–7", 285)):
        g.text(274, yy + 4, t, s=11, a="end")
    g.box(340, 55, 80, 70, "АЦП", s=14, fill=FILL_BLUE)
    g.line(340, 75, 280, 75, w=2.6, arrow=True); g.bus_label(310, 75, 8)
    g.arrow(340, 110, 280, 110)
    g.box(450, 65, 60, 50, "УВХ", s=12)
    g.arrow(450, 90, 420, 90)
    g.box(540, 40, 60, 110, "AMX", s=12)
    g.arrow(540, 90, 510, 90)
    for i in range(4):
        yy = 52 + 28 * i
        g.box(625, yy - 11, 46, 22, f"НУ{i + 1}", s=10, wt=None)
        g.arrow(625, yy, 600, yy)
        g.box(695, yy - 11, 50, 22, f"Д{i + 1}", s=10, wt=None)
        g.arrow(695, yy, 671, yy)
    g.path([(280, 150), (380, 150), (380, 125)], arrow=True)
    g.path([(280, 180), (480, 180), (480, 115)], arrow=True)
    g.path([(280, 210), (570, 210), (570, 150)], arrow=True); g.bus_label(540, 210, 2)
    g.box(340, 263, 80, 44, "ЦАП", s=14, fill=FILL_BLUE)
    g.line(280, 285, 340, 285, w=2.6, arrow=True); g.bus_label(310, 285, 8)
    g.box(450, 263, 100, 44, "усилитель", ["мощности"], s=11, wt=None); g.arrow(420, 285, 450, 285)
    g.box(580, 263, 150, 44, "исполнительное", ["устройство"], s=11, wt=None); g.arrow(550, 285, 580, 285)
    g.text(20, 368, "Ввод: выбрать канал (PC0–1) → УВХ в «хранение» (PC2) → Пуск АЦП (PC3) → ждать Готов (PC4) → IN PA.", s=12, a="start")
    g.text(20, 388, "Вывод: код → PB → ЦАП → усилитель → ИУ.   УС = 98h: PA ввод, PC7–4 ввод, PB вывод, PC3–0 вывод (режим 0).", s=12, a="start", c=GREY)
    g.save("sv_usodesign")


def evmclass():
    g = D(760, 330)
    tree(g, "Классификация ЭВМ", 380, 15, 220, [
        ("По принципу\nдействия", ["аналоговые (АВМ)", "цифровые (ЦВМ)", "гибридные (ГВМ)"]),
        ("По\nназначению", ["универсальные", "проблемно-", "  ориентированные", "специализированные"]),
        ("По мощности\nи размерам", ["суперЭВМ", "мейнфреймы", "мини-ЭВМ, серверы", "микроЭВМ, ПК", "встроенные (МК)"]),
        ("По\nархитектуре", ["фон Неймана", "гарвардская", "по Флинну: SISD,", "  SIMD, MISD, MIMD"]),
        ("По элементной\nбазе", ["лампы", "транзисторы", "ИС", "БИС, СБИС, SoC"]),
    ], y1=90, s=12)
    g.save("sv_evmclass")


def evol():
    g = D(760, 360)
    items = [("1974", "i8080", ["8 бит, 64 КБ"]), ("1978", "i8086", ["16 бит, сегменты,", "1 МБ"]),
             ("1982", "80286", ["защищённый", "режим, 16 МБ"]), ("1985", "80386", ["32 бит, страницы,", "4 ГБ"]),
             ("1989", "80486", ["конвейер,", "кэш L1, FPU"]), ("1993", "Pentium", ["суперскаляр:", "2 конвейера"]),
             ("1995", "P6 (PPro–PIII)", ["микрооперации,", "внеочередное вып."]), ("2000", "Pentium 4", ["NetBurst,", "Hyper-Threading"]),
             ("2006", "Core 2", ["2–4 ядра,", "общий L2"]), ("2008", "Core i, Phenom", ["L3, контроллер", "памяти в ЦП"]),
             ("2020", "Apple M1", ["SoC ARM,", "big.LITTLE 4+4"])]
    y = 180
    g.line(30, y, 735, y, w=3, c="#495057", arrow=True)
    n = len(items)
    for i, (yr, name, lines) in enumerate(items):
        x = 50 + i * 66
        g.circle(x, y, 7, c=ACC, fill=FILL_ACC, sw=2)
        up = i % 2 == 0
        g.line(x, y - 8 if up else y + 8, x, y - 30 if up else y + 30, c=GREY, w=1.2)
        by = y - 34 if up else y + 34
        g.text(x, by - (60 if up else -14), yr, s=12, c=ACC, wt="bold")
        g.text(x, by - (44 if up else -30), name, s=12, wt="bold")
        for k, t in enumerate(lines):
            g.text(x, by - (28 - 14 * k if up else -46 - 14 * k), t, s=10.5)
    g.text(380, 25, "", s=12)
    g.text(380, 330, "Разрядность и адресное пространство → защита памяти → конвейер и кэш → суперскаляр и внеочередное", s=12, c=GREY)
    g.text(380, 348, "выполнение → многоядерность → системы на кристалле с разнотипными ядрами", s=12, c=GREY)
    g.save("sv_evol")


if __name__ == "__main__":
    for f in (ifclass, usbpkt, crc, alt, puclass, usodesign, evmclass, evol):
        f(); print("ok", f.__name__)
