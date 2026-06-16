from io import BytesIO
from re import sub
from unicodedata import normalize

from django.utils.text import slugify


def _import_reportlab():
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:
        raise RuntimeError(
            "ReportLab is required to generate PDFs. Install it with: pip install reportlab"
        ) from exc

    return {
        "colors": colors,
        "TA_CENTER": TA_CENTER,
        "letter": letter,
        "getSampleStyleSheet": getSampleStyleSheet,
        "ParagraphStyle": ParagraphStyle,
        "inch": inch,
        "Paragraph": Paragraph,
        "SimpleDocTemplate": SimpleDocTemplate,
        "Spacer": Spacer,
        "Table": Table,
        "TableStyle": TableStyle,
    }


def _plain_text(value):
    return str(value or "").strip()


def _safe_pdf_text(value):
    text = _plain_text(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def profile_pdf_filename(profile):
    normalized_name = (
        normalize("NFKD", _plain_text(profile.name))
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    fallback = f"cv-{profile.pk or 'profile'}"
    slug = slugify(normalized_name) or fallback
    slug = sub(r"[^a-zA-Z0-9_-]+", "-", slug).strip("-") or fallback
    return f"{slug}-cv.pdf"


def build_profile_pdf(profile):
    rl = _import_reportlab()
    colors = rl["colors"]
    styles = rl["getSampleStyleSheet"]()
    buffer = BytesIO()

    doc = rl["SimpleDocTemplate"](
        buffer,
        pagesize=rl["letter"],
        rightMargin=0.65 * rl["inch"],
        leftMargin=0.65 * rl["inch"],
        topMargin=0.55 * rl["inch"],
        bottomMargin=0.55 * rl["inch"],
        title=f"CV - {_plain_text(profile.name)}",
    )

    title_style = rl["ParagraphStyle"](
        "ResumeTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        alignment=rl["TA_CENTER"],
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6,
    )
    subtitle_style = rl["ParagraphStyle"](
        "ResumeSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=rl["TA_CENTER"],
        textColor=colors.HexColor("#475569"),
        spaceAfter=18,
    )
    section_style = rl["ParagraphStyle"](
        "ResumeSection",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#4338ca"),
        spaceBefore=10,
        spaceAfter=7,
    )
    body_style = rl["ParagraphStyle"](
        "ResumeBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8,
    )
    label_style = rl["ParagraphStyle"](
        "ResumeLabel",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
    )

    story = [
        rl["Paragraph"](_safe_pdf_text(profile.name), title_style),
        rl["Paragraph"](
            f"{_safe_pdf_text(profile.email)} | {_safe_pdf_text(profile.phone)} | {_safe_pdf_text(profile.degree)}",
            subtitle_style,
        ),
    ]

    education_rows = [
        [rl["Paragraph"]("Escuela", label_style), rl["Paragraph"](_safe_pdf_text(profile.school), body_style)],
        [rl["Paragraph"]("Universidad", label_style), rl["Paragraph"](_safe_pdf_text(profile.university), body_style)],
        [rl["Paragraph"]("Grado", label_style), rl["Paragraph"](_safe_pdf_text(profile.degree), body_style)],
    ]
    education_table = rl["Table"](
        education_rows,
        colWidths=[1.25 * rl["inch"], 5.4 * rl["inch"]],
    )
    education_table.setStyle(
        rl["TableStyle"](
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#e2e8f0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    sections = [
        ("Perfil profesional", profile.sumary),
        ("Educacion", education_table),
        ("Experiencia previa", profile.previous_work),
        ("Habilidades", profile.skills),
    ]

    for title, content in sections:
        story.append(rl["Paragraph"](title, section_style))
        if isinstance(content, str):
            story.append(rl["Paragraph"](_safe_pdf_text(content).replace("\n", "<br/>"), body_style))
        else:
            story.append(content)
            story.append(rl["Spacer"](1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer
