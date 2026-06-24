from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "schematics" / "gamepocket-m5sticks3-schematic.png"


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def centered(draw, xy, text, fill, fnt):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - (box[2] - box[0]) / 2, y - (box[3] - box[1]) / 2), text, fill=fill, font=fnt)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, points, fill, width=5):
    draw.line(points, fill=fill, width=width, joint="curve")
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    dx, dy = x2 - x1, y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    size = 18
    tip = (x2, y2)
    left = (x2 - ux * size + px * size * 0.48, y2 - uy * size + py * size * 0.48)
    right = (x2 - ux * size - px * size * 0.48, y2 - uy * size - py * size * 0.48)
    draw.polygon([tip, left, right], fill=fill)


def label_box(draw, box, title, subtitle, fill, outline, title_size=34):
    rounded(draw, box, 18, fill, outline, 4)
    x1, y1, x2, y2 = box
    centered(draw, ((x1 + x2) / 2, y1 + 42), title, "#111827", font(title_size, True))
    centered(draw, ((x1 + x2) / 2, y1 + 82), subtitle, "#334155", font(24))


def main():
    img = Image.new("RGB", (1600, 1000), "#f7f8fb")
    draw = ImageDraw.Draw(img)

    centered(draw, (800, 68), "GamePocket for M5StickS3", "#0f172a", font(54, True))
    centered(
        draw,
        (800, 118),
        "Schematics and circuit diagrams - standalone device, no external wiring required",
        "#475569",
        font(28),
    )

    rounded(draw, (70, 165, 1530, 885), 22, "#ffffff", "#c9d1d9", 3)

    board = (600, 235, 1000, 795)
    rounded(draw, board, 52, "#263238", "#0f1720", 4)
    rounded(draw, (660, 285, 940, 545), 18, "#0b1830", "#80d8ff", 4)
    centered(draw, (800, 395), "GamePocket", "#ffffff", font(38, True))
    centered(draw, (800, 442), "Launcher + 2 games", "#ffffff", font(25))

    rounded(draw, (690, 595, 910, 687), 10, "#111827", "#6b7280", 3)
    centered(draw, (800, 635), "ESP32-S3", "#ffffff", font(29, True))
    centered(draw, (800, 669), "M5StickS3 main MCU", "#ffffff", font(20))

    draw.ellipse((672, 707, 728, 763), fill="#ecfdf3", outline="#22a06b", width=4)
    centered(draw, (700, 737), "A", "#334155", font(26, True))
    draw.ellipse((872, 707, 928, 763), fill="#ecfdf3", outline="#22a06b", width=4)
    centered(draw, (900, 737), "B", "#334155", font(26, True))
    rounded(draw, (780, 808, 820, 844), 6, "#e5e7eb", "#111827", 2)
    centered(draw, (800, 827), "USB", "#334155", font(16, True))

    label_box(draw, (150, 240, 480, 360), "USB-C", "Power + firmware upload", "#fff7e6", "#f59e0b")
    label_box(draw, (150, 430, 480, 550), "Built-in Battery", "Portable power source", "#fff7e6", "#f59e0b")
    label_box(draw, (150, 620, 480, 740), "Speaker", "Music and sound effects", "#eef6ff", "#2f80ed")
    label_box(draw, (1115, 235, 1445, 355), "LCD Display", "GamePocket UI and gameplay", "#eef6ff", "#2f80ed")
    label_box(draw, (1115, 405, 1445, 525), "Buttons A / B", "Select, play, jump, back", "#ecfdf3", "#22a06b")
    label_box(draw, (1115, 575, 1445, 695), "IMU / Accelerometer", "Tilt controls", "#ecfdf3", "#22a06b", 30)

    orange = "#f97316"
    blue = "#2563eb"
    green = "#16a34a"
    arrow(draw, [(480, 300), (560, 300), (560, 827), (780, 827)], orange, 6)
    arrow(draw, [(480, 490), (555, 490), (585, 642), (690, 642)], orange, 5)
    arrow(draw, [(910, 625), (1030, 625), (1030, 295), (1115, 295)], blue, 5)
    arrow(draw, [(928, 735), (1030, 735), (1030, 465), (1115, 465)], blue, 5)
    arrow(draw, [(910, 662), (1035, 662), (1035, 635), (1115, 635)], green, 5)
    arrow(draw, [(690, 660), (555, 660), (555, 680), (480, 680)], blue, 5)

    draw.text((510, 270), "5V USB / 3.3V board regulation", fill="#475569", font=font(20))
    draw.text((1012, 266), "display bus", fill="#475569", font=font(20))
    draw.text((1015, 437), "GPIO input", fill="#475569", font=font(20))
    draw.text((970, 600), "I2C / internal bus", fill="#475569", font=font(20))
    draw.text((505, 650), "audio output", fill="#475569", font=font(20))

    rounded(draw, (150, 800, 1445, 854), 12, "#f1f5f9", "#94a3b8", 2)
    centered(
        draw,
        (800, 828),
        "Circuit note: GamePocket uses the stock M5StickS3 board only. No breadboard, jumper wires, external sensors, or custom PCB are used.",
        "#334155",
        font(22),
    )
    draw.text((80, 928), "Project repository: https://github.com/joooooyzh/gamepocket-m5stack-sticks3", fill="#64748b", font=font(24))
    draw.text(
        (80, 962),
        "Hardware: M5StickS3 development device with integrated display, buttons, IMU, speaker, battery, USB-C, and ESP32-S3 MCU.",
        fill="#64748b",
        font=font(22),
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
