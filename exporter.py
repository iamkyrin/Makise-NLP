from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO

def export_summary(summary):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Makise — Summary Export", styles["Heading1"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(summary, styles["BodyText"]))
    doc.build(story)
    return buffer.getvalue()