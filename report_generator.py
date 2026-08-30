import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(machine_id, status_decision, risk_score, temp, vib, recommendations):
    os.makedirs("output", exist_ok=True)
    pdf_filename = f"output/Incident_Report_{machine_id.replace(' ', '_')}.pdf"
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY_BLUE = colors.HexColor("#1A365D")
    LIGHT_BLUE_BG = colors.HexColor("#F1F5F9")
    HEADER_BLUE = colors.HexColor("#2563EB")
    TEXT_DARK = colors.HexColor("#0F172A")
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    ALERT_RED = colors.HexColor("#DC2626")
    GREEN_ACCENT = colors.HexColor("#16A34A")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY_BLUE,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=NAVY_BLUE,
        spaceBefore=14,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=14,
        textColor=TEXT_DARK
    )

    body_text = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=TEXT_DARK
    )

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Title Header
    story.append(Paragraph("AI FACTORY 2.0 - COMMAND CENTER INCIDENT REPORT", title_style))
    story.append(Paragraph(f"<b>Generated:</b> {now_str} | <b>Facility ID:</b> FAC-NORTH-01", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY_BLUE, spaceBefore=0, spaceAfter=12))

    # 2. Executive Metadata Grid
    grid_data = [
        [
            Paragraph("<b>Target Machine ID:</b>", body_text),
            Paragraph(f"<b>{machine_id}</b>", body_text)
        ],
        [
            Paragraph("<b>Failure Risk Confidence:</b>", body_text),
            Paragraph(f"<font color='{ALERT_RED.hexval()}'><b>{risk_score:.1f}%</b></font>", body_text)
        ],
        [
            Paragraph("<b>Defect Severity (Vision):</b>", body_text),
            Paragraph("Critical" if risk_score > 70 else "Moderate", body_text)
        ],
        [
            Paragraph("<b>Primary Recommendation:</b>", body_text),
            Paragraph("<b>REDUCE_LOAD_AND_INSPECT</b>" if risk_score > 50 else "<b>CONTINUE_MONITORING</b>", body_text)
        ]
    ]

    meta_table = Table(grid_data, colWidths=[180, 360])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE_BG),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 3. Multi-Agent Consensus Findings
    story.append(Paragraph("1. Multi-Agent Consensus Findings", section_heading))
    
    agent_findings = [
        ("Vision Agent:", "Defect Detected - <i>Crack</i> (Confidence: 94.0%)"),
        ("Predictive Maintenance Agent:", f"Sensor Telemetry Warning - Temperature {temp:.1f}°C, Vibration {vib:.1f} mm/s."),
        ("Knowledge Agent:", f"Retrieved Grounded SOP Evidence from <i>{machine_id.split()[1] if len(machine_id.split()) > 1 else 'System'}_SOP.txt</i>."),
        ("Planning Agent Decision:", f"{recommendations}")
    ]

    for label, desc in agent_findings:
        p_content = f"<b>{label}</b> {desc}"
        story.append(Paragraph(p_content, body_text))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))

    # 4. Digital Twin What-If Simulation
    story.append(Paragraph("2. Digital Twin What-If Operational Simulation", section_heading))
    
    sim_data = [
        ["Scenario", "Units Lost", "Failure Risk", "Est. Financial Loss ($)"],
        ["Continue Operation", "480", f"{min(100.0, risk_score * 1.1):.1f}%", f"${(risk_score * 415.0):,.2f}"],
        ["Immediate Maintenance", "300", "5.0%", "$14,875.00"],
        ["Reduce Load (-30%)", "288", f"{max(5.0, risk_score * 0.35):.1f}%", f"${(risk_score * 207.0):,.2f}"],
        ["Reroute to Line 02", "246", "2.0%", "$11,670.00"]
    ]

    sim_table = Table(sim_data, colWidths=[180, 100, 110, 150])
    sim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HEADER_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BLUE_BG]),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(sim_table)
    story.append(Spacer(1, 10))

    # 5. Human Supervisor Sign-Off & Audit Trail
    story.append(Paragraph("3. Human Supervisor Sign-Off & Audit Trail", section_heading))
    
    action_color = GREEN_ACCENT.hexval() if "Approve" in status_decision or "APPROVED" in status_decision else ALERT_RED.hexval()
    
    story.append(Paragraph(f"<b>Supervisor Action:</b> <font color='{action_color}'><b>{status_decision.upper()}</b></font>", body_text))
    story.append(Paragraph("<b>Supervisor ID:</b> SUP-8821", body_text))
    story.append(Paragraph(f"<b>Audit Timestamp:</b> {now_str}", body_text))
    story.append(Paragraph("<b>Supervisor Notes:</b> Action approved per digital twin scenario analysis.", body_text))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=0, spaceAfter=20))

    # Signature Footer Line
    sig_data = [
        [
            Paragraph("<b>Supervisor Signature:</b> ___________________________", body_text),
            Paragraph("<b>Date:</b> _____________", body_text)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[350, 190])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)

    doc.build(story)
    return pdf_filename