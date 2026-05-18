from io import BytesIO
from reportlab.pdfgen import canvas

def html_report(narrative: str, analysis: dict) -> bytes:
    return f"<html><body><h1>Neurocognitive Mirror Report</h1><p>{narrative}</p><pre>{analysis}</pre></body></html>".encode()

def pdf_report(narrative: str, analysis: dict) -> bytes:
    buf = BytesIO(); c = canvas.Canvas(buf); y=780
    c.drawString(72,y,"Neurocognitive Mirror Report"); y-=30
    for token in narrative.split():
        if y < 72: c.showPage(); y=780
        c.drawString(72,y,token[:100]); y-=12
    c.save(); return buf.getvalue()
