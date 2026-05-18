from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
from jinja2 import Template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DEFAULT_PATH = Path(os.getenv("NCM_DATA_PATH", Path.home() / ".neurocognitive_mirror_mvp.json"))


def load_records(path: Path = DEFAULT_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_records(records: list[dict[str, Any]], path: Path = DEFAULT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(records, indent=2, default=str))


def html_report(df: pd.DataFrame, narrative: str) -> str:
    template = Template("""
    <html><head><title>Neurocognitive Mirror Report</title></head><body>
    <h1>Neurocognitive Mirror Report</h1>
    <h2>Narrative</h2><p>{{ narrative }}</p>
    <h2>Recent Sessions</h2>{{ table }}
    </body></html>
    """)
    return template.render(narrative=narrative, table=df.tail(12).to_html(index=False))


def pdf_report_bytes(df: pd.DataFrame, narrative: str) -> bytes:
    from io import BytesIO
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    y = 750
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "Neurocognitive Mirror Report")
    c.setFont("Helvetica", 10)
    y -= 30
    for line in narrative.replace("\n", " ").split(" "):
        if y < 72:
            c.showPage(); y = 750; c.setFont("Helvetica", 10)
        c.drawString(72, y, line[:95])
        y -= 12
    c.showPage()
    c.setFont("Helvetica-Bold", 12); c.drawString(72, 750, "Recent Sessions")
    c.setFont("Helvetica", 8); y = 730
    for _, row in df.tail(20).iterrows():
        c.drawString(72, y, f"{row['date']} CEI={row.get('cei','')} span={row.get('digit_span','')} rt={row.get('reaction_time_ms','')}")
        y -= 12
    c.save()
    return buf.getvalue()


def download_link(data: bytes | str, filename: str, mime: str) -> str:
    raw = data.encode() if isinstance(data, str) else data
    b64 = base64.b64encode(raw).decode()
    return f'<a href="data:{mime};base64,{b64}" download="{filename}">Download {filename}</a>'
