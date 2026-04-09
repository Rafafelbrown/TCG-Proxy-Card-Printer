"""

card_printer.py — tcg Proxy Card Sheet Generator
Arranges card images in a printable A4/Letter PDF (3x3 or 3x3 grid).
this script is ideal for creating proxy sheets for Magic: The Gathering or similar TCGs.
is not for mass production, but for quick home printing of a few proxies.
and is for personal use only (not for commercial distribution of copyrighted card images).
and is not for piracy or unauthorized reproduction of official cards is for personal use only.


Usage:
    python card_printer.py <image_path> [options]

Options:
    --copies   N     Total number of copies to print (default: 9)
    --cols     N     Cards per row (default: 3)
    --rows     N     Cards per column (default: 3)
    --output   FILE  Output PDF filename (default: proxy_sheet.pdf)
    --paper    SIZE  Paper size: A4 or LETTER (default: A4)
    --margin   MM    Page margin in mm (default: 10)
    --gap      MM    Gap between cards in mm (default: 2)
    --cut-marks      Draw cut guide lines between cards (default: True)

Example:
    python card_printer.py my_card.png --copies 18 --cols 3 --rows
or:
    python card_printer.py my_card.png --copies 18 --cols 2 --rows 3 --output my_proxies.pdf
    
"""

import argparse
import sys
from pathlib import Path
from PIL import Image
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import tempfile
import os

# Standard MTG card size in mm
MTG_CARD_W_MM = 63.0
MTG_CARD_H_MM = 88.0


def mm_to_pt(value_mm: float) -> float:
    return value_mm * mm


def draw_cut_marks(c: canvas.Canvas, x: float, y: float, w: float, h: float, size: float = 3 * mm):
    """Draw corner cut marks around a card position (in points)."""
    c.saveState()
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.setLineWidth(0.3)
    # Top-left
    c.line(x - size, y + h, x, y + h)
    c.line(x, y + h + size, x, y + h)
    # Top-right
    c.line(x + w, y + h, x + w + size, y + h)
    c.line(x + w, y + h + size, x + w, y + h)
    # Bottom-left
    c.line(x - size, y, x, y)
    c.line(x, y - size, x, y)
    # Bottom-right
    c.line(x + w, y, x + w + size, y)
    c.line(x + w, y - size, x + w, y)
    c.restoreState()


def generate_proxy_sheet(
    image_path: str,
    copies: int = 9,
    cols: int = 3,
    rows: int = 3,
    output: str = "proxy_sheet.pdf",
    paper: str = "A4",
    margin_mm: float = 10.0,
    gap_mm: float = 2.0,
    cut_marks: bool = True,
):
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"❌  File not found: {image_path}")
        sys.exit(1)

    # --- Page setup ---
    pagesize = A4 if paper.upper() == "A4" else LETTER
    page_w, page_h = pagesize
    margin = mm_to_pt(margin_mm)
    gap = mm_to_pt(gap_mm)

    # --- Compute card slot size that fits the grid ---
    avail_w = page_w - 2 * margin - (cols - 1) * gap
    avail_h = page_h - 2 * margin - (rows - 1) * gap
    slot_w = avail_w / cols
    slot_h = avail_h / rows

    # Preserve aspect ratio of the original image inside the slot
    with Image.open(img_path) as pil_img:
        orig_w, orig_h = pil_img.size
        img_aspect = orig_w / orig_h
        

    slot_aspect = slot_w / slot_h
    if img_aspect > slot_aspect:
        card_w = slot_w
        card_h = slot_w / img_aspect
        
    else:
        card_h = slot_h
        card_w = slot_h * img_aspect

    # Center within slot
    offset_x = (slot_w - card_w) / 2
    offset_y = (slot_h - card_h) / 2

    # --- Pre-process image: save as JPEG for smaller PDF ---
    with Image.open(img_path) as pil_img:
        pil_img = pil_img.convert("RGB")
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        pil_img.save(tmp.name, "JPEG", quality=95)
        tmp_path = tmp.name
        tmp.close()

    output_path = Path(output)
    temp_output = tempfile.NamedTemporaryFile(
        suffix=".pdf",
        prefix=output_path.stem + "_",
        delete=False,
        dir=str(output_path.parent),
    )
    temp_output_path = Path(temp_output.name)
    temp_output.close()

    # --- Build PDF ---
    c = canvas.Canvas(str(temp_output_path), pagesize=pagesize)
    c.setTitle(f"Proxy Sheet — {img_path.stem}")
    c.setAuthor("card_printer.py")

    placed = 0
    page_num = 0

    while placed < copies:
        if page_num > 0:
            c.showPage()

        # Light background marker so printer knows full bleed area
        c.saveState()
        c.setFillColorRGB(1, 1, 1)
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
        c.restoreState()

        for row in range(rows):
            for col in range(cols):
                if placed >= copies:
                    break

                # ReportLab origin is bottom-left; rows go top→bottom
                x = margin + col * (slot_w + gap) + offset_x
                y = page_h - margin - (row + 1) * slot_h - row * gap + offset_y

                c.drawImage(tmp_path, x, y, width=card_w, height=card_h, preserveAspectRatio=True)

                if cut_marks:
                    draw_cut_marks(c, x, y, card_w, card_h)

                placed += 1

        page_num += 1

    rename_succeeded = False
    final_output_path = output_path
    
    try:
        # Finalize PDF to temp file
        c.save()
        
        # Try to save to the target path
        try:
            os.replace(str(temp_output_path), str(output_path))
            rename_succeeded = True
            final_output_path = output_path
        except PermissionError:
            # Target file is locked; try incrementing filename
            counter = 1
            while counter <= 100:
                alt_name = output_path.stem + f"_{counter}" + output_path.suffix
                alt_path = output_path.parent / alt_name
                try:
                    os.replace(str(temp_output_path), str(alt_path))
                    rename_succeeded = True
                    final_output_path = alt_path
                    break
                except PermissionError:
                    counter += 1
            
            if not rename_succeeded:
                raise PermissionError(
                    f"Não foi possível gravar o PDF. {output_path} está bloqueado, "
                    f"e também não foi possível salvar variações numeradas."
                )
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        if rename_succeeded and os.path.exists(temp_output_path):
            try:
                os.unlink(temp_output_path)
            except OSError:
                pass

    pages = page_num
    print(f"✅  PDF criado: {final_output_path.name}")

    print(f"   {copies} cópias · {cols}×{rows} por página · {pages} página(s)")
    print(f"   Papel: {paper.upper()} · Margem: {margin_mm}mm · Gap: {gap_mm}mm")
    if cut_marks:
        print("   ✂  Marcas de corte incluídas")


def main():
    parser = argparse.ArgumentParser(
        description="Gera folha de proxies MTG em PDF para impressão."
    )
    parser.add_argument("image", help="Caminho para a imagem da carta")
    parser.add_argument("--copies", type=int, default=9, help="Total de cópias (default: 9)")
    parser.add_argument("--cols", type=int, default=3, help="Colunas por página (default: 3)")
    parser.add_argument("--rows", type=int, default=3, help="Linhas por página (default: 3)")
    parser.add_argument("--output", default="proxy_sheet.pdf", help="Nome do PDF de saída")
    parser.add_argument("--paper", default="A4", choices=["A4", "LETTER"], help="Tamanho do papel")
    parser.add_argument("--margin", type=float, default=10.0, help="Margem em mm (default: 10)")
    parser.add_argument("--gap", type=float, default=2.0, help="Espaço entre cartas em mm (default: 2)")
    parser.add_argument("--no-cut-marks", action="store_true", help="Desativar marcas de corte")

    args = parser.parse_args()

    generate_proxy_sheet(
        image_path=args.image,
        copies=args.copies,
        cols=args.cols,
        rows=args.rows,
        output=args.output,
        paper=args.paper,
        margin_mm=args.margin,
        gap_mm=args.gap,
        cut_marks=not args.no_cut_marks,
    )


if __name__ == "__main__":
    main()

