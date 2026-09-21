#!/usr/bin/env python3
"""
Generate a visually stunning, executive-grade Custom Agent Architecture Blueprint PDF report.
Features:
- Unified Marian Stancik Neural Engineering luxury brand aesthetic
- High-impact Hero Card with circular vector architecture badge
- Visual status bars and structured tables for the 4 core layers
- Modern numbered security guardrail cards with Human-in-the-Loop specifications
- 4-phase agile delivery roadmap with milestone badges
- 6-point client deliverables checklist and 100% deposit credit terms
- Exactly 2 pages, 100% clean TrueType Segoe UI / Arial fonts with full Slovak diacritics
"""

import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Circle, String

FONT_REGULAR = "SegoeUI"
FONT_BOLD = "SegoeUI-Bold"

def register_system_fonts():
    global FONT_REGULAR, FONT_BOLD
    candidates = [
        ("SegoeUI", "C:/Windows/Fonts/segoeui.ttf", "SegoeUI-Bold", "C:/Windows/Fonts/segoeuib.ttf"),
        ("Arial", "C:/Windows/Fonts/arial.ttf", "Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"),
        ("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    ]
    for reg_name, reg_path, bold_name, bold_path in candidates:
        if os.path.exists(reg_path) and os.path.exists(bold_path):
            try:
                pdfmetrics.registerFont(TTFont(reg_name, reg_path))
                pdfmetrics.registerFont(TTFont(bold_name, bold_path))
                FONT_REGULAR = reg_name
                FONT_BOLD = bold_name
                return
            except Exception:
                continue

register_system_fonts()

COLOR_BG_DARK = colors.HexColor('#08080F')
COLOR_SURFACE_DARK = colors.HexColor('#12121E')
COLOR_CARD_DARK = colors.HexColor('#0D0D18')
COLOR_BRONZE = colors.HexColor('#CD7F32')
COLOR_GOLD = colors.HexColor('#E8B86D')
COLOR_TEXT_DARK = colors.HexColor('#0F172A')
COLOR_TEXT_MUTED = colors.HexColor('#64748B')
COLOR_BORDER = colors.HexColor('#E2E8F0')
COLOR_BG_LIGHT = colors.HexColor('#FAF8F5')
COLOR_GREEN = colors.HexColor('#10B981')
COLOR_BLUE = colors.HexColor('#2563EB')
COLOR_AMBER = colors.HexColor('#F59E0B')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        w, h = A4

        # Top Accent Ribbon
        self.setFillColor(COLOR_BG_DARK)
        self.rect(0, h - 28, w, 28, fill=1, stroke=0)
        self.setStrokeColor(COLOR_BLUE)
        self.setLineWidth(1.5)
        self.line(0, h - 28, w, h - 28)

        self.setFillColor(COLOR_GOLD)
        self.setFont(FONT_BOLD, 9)
        self.drawString(36, h - 18, "✦ Marian Stancik")

        self.setFillColor(colors.HexColor('#94A3B8'))
        self.setFont(FONT_REGULAR, 7.5)
        self.drawString(135, h - 18, "·  AUTONOMOUS AI AGENT SYSTEMS · ENGINEERING BLUEPRINT")

        self.setFillColor(COLOR_GOLD)
        self.setFont(FONT_BOLD, 7.5)
        self.drawRightString(w - 36, h - 18, "CUSTOM AGENT ARCHITECTURE · CONFIDENTIAL")

        # Bottom Footer Bar
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.8)
        self.line(36, 28, w - 36, 28)

        self.setFillColor(COLOR_TEXT_MUTED)
        self.setFont(FONT_REGULAR, 7)
        self.drawString(36, 17, "Marián Stančík · Černákova 2046/8, 977 01 Brezno · IČO: 57068917 · marianstancik@agentmail.to")

        page_str = f"Strana {self._pageNumber} z {total_pages}"
        self.drawRightString(w - 36, 17, page_str)

        self.restoreState()


def create_arch_badge():
    d = Drawing(105, 95)
    d.add(Circle(52, 48, 44, fillColor=COLOR_CARD_DARK, strokeColor=COLOR_BLUE, strokeWidth=2.5))
    d.add(Circle(52, 48, 38, fillColor=COLOR_SURFACE_DARK, strokeColor=colors.HexColor('#1E293B'), strokeWidth=1))
    d.add(String(52, 52, "HERMES", textAnchor='middle', fontName=FONT_BOLD, fontSize=11, fillColor=COLOR_GOLD))
    d.add(String(52, 38, "RUNTIME", textAnchor='middle', fontName=FONT_BOLD, fontSize=10, fillColor=colors.white))
    d.add(String(52, 22, "● 24/7 DAEMON", textAnchor='middle', fontName=FONT_BOLD, fontSize=6.5, fillColor=COLOR_GREEN))
    return d


def create_progress_bar(val, max_val, color_hex):
    pct = min(1.0, max(0.0, val / max_val)) if max_val > 0 else 0
    w = 110
    h = 7
    d = Drawing(w, h + 2)
    d.add(Rect(0, 1, w, h, fillColor=colors.HexColor('#E2E8F0'), strokeColor=None, rx=3.5, ry=3.5))
    fill_w = max(6, int(w * pct))
    d.add(Rect(0, 1, fill_w, h, fillColor=colors.HexColor(color_hex), strokeColor=None, rx=3.5, ry=3.5))
    return d


def build_custom_agent_blueprint_pdf(output_path="assets/sample-custom-agent-blueprint.pdf", client_name="Marian Stancik", client_url="https://www.marianstancik.dev"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'DocTitle', fontName=FONT_BOLD, fontSize=18, leading=22, textColor=COLOR_BG_DARK, spaceAfter=2
    )
    style_subtitle = ParagraphStyle(
        'DocSubtitle', fontName=FONT_REGULAR, fontSize=9, leading=13, textColor=COLOR_BRONZE, spaceAfter=8
    )
    style_section_h = ParagraphStyle(
        'SectionH', fontName=FONT_BOLD, fontSize=10, leading=14, textColor=COLOR_BG_DARK, spaceBefore=5, spaceAfter=4
    )
    style_th = ParagraphStyle(
        'TableH', fontName=FONT_BOLD, fontSize=7.5, leading=10.5, textColor=colors.white
    )
    style_body = ParagraphStyle(
        'Body', fontName=FONT_REGULAR, fontSize=7.5, leading=11, textColor=COLOR_TEXT_DARK
    )
    style_body_muted = ParagraphStyle(
        'BodyMuted', fontName=FONT_REGULAR, fontSize=7, leading=9.5, textColor=COLOR_TEXT_MUTED
    )
    style_fix_title = ParagraphStyle(
        'FixTitle', fontName=FONT_BOLD, fontSize=7.5, leading=10.5, textColor=COLOR_BG_DARK
    )
    style_fix_desc = ParagraphStyle(
        'FixDesc', fontName=FONT_REGULAR, fontSize=7, leading=9.5, textColor=COLOR_TEXT_MUTED
    )
    style_badge_pass = ParagraphStyle(
        'BadgePass', fontName=FONT_BOLD, fontSize=6.5, leading=9, textColor=colors.HexColor('#047857')
    )

    story = []

    # ═════════════════════════════════════════════════════════════════
    # PAGE 1: ARCHITECTURAL BLUEPRINT & SYSTEM TOPOLOGY
    # ═════════════════════════════════════════════════════════════════

    story.append(Paragraph("AUTONOMOUS AGENT ARCHITECTURE BLUEPRINT", style_title))
    story.append(Paragraph("Technická špecifikácia autonómneho systému · Hermes Agent, MCP nástroje, C2 Telegram & Pamäťová vrstva", style_subtitle))

    # Meta Info Card
    meta_data = [
        [
            Paragraph(f"<b>Klient:</b> {client_name}", style_body),
            Paragraph(f"<b>Cieľové prostredie:</b> {client_url}", style_body)
        ],
        [
            Paragraph("<b>Dátum návrhu:</b> 17. septembra 2026", style_body),
            Paragraph("<b>Produkt:</b> Autonómny AI Agent na Mieru — Záloha €500", style_body)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[240, 283])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # Hero Card: Circular Architecture Badge + Executive Concept
    arch_badge = create_arch_badge()
    hero_text = f"""
    <font size="9.5" color="#E8B86D"><b>Architektonický koncept navrhovaného systému:</b></font><br/>
    Navrhovaný autonómny agent nefunguje ako pasívny chatbot, ale ako <b>plne autonómny proces (daemon)</b> bežiaci nepretržite na vyhradenej európskej VPS infraštruktúre Hetzner Cloud.
    Systém kombinuje dynamické multi-LLM smerovanie (OpenRouter: Claude 3.5 Sonnet, GPT-4o, DeepSeek R1), vlastné nástroje <b>Model Context Protocol (MCP)</b> pre I/O procesy, obojsmerný veliaci Telegram most (C2) a perzistentnú pamäťovú vrstvu.
    """
    hero_card_data = [[arch_badge, Paragraph(hero_text, style_body)]]
    hero_card = Table(hero_card_data, colWidths=[115, 408])
    hero_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), COLOR_CARD_DARK),
        ('BOX', (0, 0), (-1, -1), 1.2, COLOR_BLUE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#F0F0F5'))
    ]))
    story.append(hero_card)
    story.append(Spacer(1, 6))

    # 4 Architectural Core Layers Table
    story.append(Paragraph("4 kľúčové vrstvy autonómnej agentickej architektúry", style_section_h))

    bar_l1 = create_progress_bar(99, 100, '#10B981')
    bar_l2 = create_progress_bar(95, 100, '#10B981')
    bar_l3 = create_progress_bar(92, 100, '#CD7F32')
    bar_l4 = create_progress_bar(96, 100, '#10B981')

    layers_data = [
        [
            Paragraph("<b>Architektonická vrstva</b>", style_th),
            Paragraph("<b>Technologický stack</b>", style_th),
            Paragraph("<b>Účel a zodpovednosť</b>", style_th),
            Paragraph("<b>SLA / Status</b>", style_th)
        ],
        [
            Paragraph("<b>1. Runtime & Orchestrácia</b>", style_body),
            Paragraph("Python WSGI / systemd, Hetzner VPS, Caddy TLS 1.3", style_body),
            Paragraph("Nepretržitý 24/7 proces, automatický restart, health check watchdog", style_body),
            Paragraph("<font color='#10B981'><b>99.9% Uptime</b></font>", style_body)
        ],
        [
            Paragraph("<b>2. Model Router & Kognícia</b>", style_body),
            Paragraph("OpenRouter: Claude 3.5 Sonnet, GPT-4o, DeepSeek R1", style_body),
            Paragraph("Dynamické prepínanie modelov podľa komplexity a nákladov", style_body),
            Paragraph("<font color='#10B981'><b>Multi-LLM Failover</b></font>", style_body)
        ],
        [
            Paragraph("<b>3. Nástroje & MCP Ekosystém</b>", style_body),
            Paragraph("AgentMail JSON-RPC 2.0, CRM Webhook, File/DB MCP", style_body),
            Paragraph("Bezpečné volanie externých API, odosielanie emailov a zápis do CRM", style_body),
            Paragraph("<font color='#10B981'><b>Sandboxed I/O</b></font>", style_body)
        ],
        [
            Paragraph("<b>4. C2 Bridge & Pamäť</b>", style_body),
            Paragraph("Telegram Bot API (RBAC), Obsidian Vault (Markdown)", style_body),
            Paragraph("Okamžitá interakcia s majiteľom, schvaľovanie úloh, perzistencia", style_body),
            Paragraph("<font color='#10B981'><b>E2E Šifrované</b></font>", style_body)
        ],
    ]
    layer_table = Table(layers_data, colWidths=[120, 140, 200, 63])
    layer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3.5),
        ('TOPPADDING', (0, 0), (-1, 0), 3.5),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), COLOR_BG_LIGHT),
        ('BACKGROUND', (0, 3), (-1, 3), colors.white),
        ('BACKGROUND', (0, 4), (-1, 4), COLOR_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(layer_table)
    story.append(Spacer(1, 6))

    # Core Security Guardrails
    story.append(Paragraph("Bezpečnostné mantinely (Guardrails & Human-in-the-Loop)", style_section_h))

    guardrails = [
        (
            "1. Human-in-the-Loop schvaľovanie cez Telegram (C2 Command Center)",
            "Kritické operácie · Finančné transakcie a hromadné e-maily",
            "Agent nikdy nevykoná nevratnú akciu (odoslanie citlivých správ, platby, zmena databázy) autonómne bez explicitného stlačenia inline tlačidla majiteľom v autorizovanom Telegram kanáli."
        ),
        (
            "2. Zero Trust autentifikácia a rotácia kľúčov",
            "Izolované prostredie · Žiadne heslá v repozitári",
            "Všetky API kľúče (OpenRouter, AgentMail, Telegram, CRM) sú uložené výhradne v chránenom env súbore na VPS s právami chmod 600. Žiadne tajomstvá sa nedostanú do repozitára."
        ),
        (
            "3. Súlad s čl. 50 EU AI Act (Auditná stopa & Logovanie)",
            "Právna istota · Kompletný audit trail",
            "Každé rozhodnutie a krok agenta sa zapisuje do štruktúrovaného JSONL denníka vrátane časovej pečiatky, vstupného promptu, použitého modelu a výsledku nástroja."
        )
    ]

    guard_rows = []
    for idx, (title, meta, desc) in enumerate(guardrails, 1):
        num_badge = f"""<font size="8" color="#2563EB"><b>[0{idx}]</b></font> <b>{title}</b> <font size="7" color="#D97706"><b>[{meta}]</b></font>"""
        cell = [
            Paragraph(num_badge, style_fix_title),
            Paragraph(desc, style_fix_desc)
        ]
        guard_rows.append([cell])

    guard_table = Table(guard_rows, colWidths=[523])
    guard_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FCFDFE')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#FCFDFE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(guard_table)

    # ═════════════════════════════════════════════════════════════════
    # PAGE BREAK -> PAGE 2: IMPLEMENTATION ROADMAP & DELIVERY PHASES
    # ═════════════════════════════════════════════════════════════════
    story.append(PageBreak())

    story.append(Paragraph("Realizačný harmonogram a dodávka (4 agilné fázy)", style_section_h))
    story.append(Paragraph("Štruktúrovaný postup od úvodného návrhu po nasadenie do plnej produkcie.", style_subtitle))

    roadmap_data = [
        [
            Paragraph("<b>Fáza projektu</b>", style_th),
            Paragraph("<b>Kľúčové výstupy a dodávky</b>", style_th),
            Paragraph("<b>Trvanie</b>", style_th),
            Paragraph("<b>Míľnik</b>", style_th)
        ],
        [
            Paragraph("<b>Fáza 1: Architektúra & VPS</b>", style_body),
            Paragraph("Provisioning Hetzner VPS, Caddy reverzný proxy, TLS certifikáty, systemd daemon, zabezpečenie SSH.", style_body),
            Paragraph("Dni 1–4", style_body),
            Paragraph("<font color='#10B981'><b>✔ Infraštruktúra</b></font>", style_badge_pass)
        ],
        [
            Paragraph("<b>Fáza 2: MCP Integrácia</b>", style_body),
            Paragraph("Vývoj a napojenie vlastných MCP serverov: AgentMail (emaily), CRM dispatcher, Google Sheets / DB konektory.", style_body),
            Paragraph("Dni 5–9", style_body),
            Paragraph("<font color='#10B981'><b>✔ Tool Ecosystem</b></font>", style_badge_pass)
        ],
        [
            Paragraph("<b>Fáza 3: C2 Telegram & LLM</b>", style_body),
            Paragraph("Implementácia privátneho Telegram bota, nastavenie promptov, mantinelov, interaktívnych schvaľovacích tlačidiel.", style_body),
            Paragraph("Dni 10–14", style_body),
            Paragraph("<font color='#10B981'><b>✔ C2 Command Hub</b></font>", style_badge_pass)
        ],
        [
            Paragraph("<b>Fáza 4: Testovanie & Odovzdanie</b>", style_body),
            Paragraph("Záťažové testy, simulácia výpadkov modelov (failover), tréning klienta, odovzdanie dokumentácie a kľúčov.", style_body),
            Paragraph("Dni 15–18", style_body),
            Paragraph("<font color='#10B981'><b>✔ Live Produkcia</b></font>", style_badge_pass)
        ],
    ]

    road_table = Table(roadmap_data, colWidths=[120, 243, 60, 100])
    road_style = [
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_BG_DARK),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.8, COLOR_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(roadmap_data)):
        bg = COLOR_BG_LIGHT if i % 2 == 0 else colors.white
        road_style.append(('BACKGROUND', (0, i), (-1, i), bg))
        road_style.append(('TOPPADDING', (0, i), (-1, i), 2.5))
        road_style.append(('BOTTOMPADDING', (0, i), (-1, i), 2.5))

    road_table.setStyle(TableStyle(road_style))
    story.append(road_table)
    story.append(Spacer(1, 6))

    # Detailed Scope & Client Deliverables Box
    scope_text = """
    <b>Čo presne klient dostáva v rámci dodávky riešenia:</b><br/>
    • <b>Kompletný zdrojový kód</b> autonómneho agenta v súkromnom GitHub repozitári s trunk-based CI/CD.<br/>
    • <b>Vyhradený Hetzner VPS server</b> plne nakonfigurovaný pod európskou jurisdikciou s automatickými zálohami.<br/>
    • <b>Vlastný privátny Telegram Bot</b> s administrátorskými právami pre okamžité riadenie a schvaľovanie úloh.<br/>
    • <b>Vlastný poštový server (AgentMail MCP)</b> na doméne klienta pre odosielanie a spracovanie e-mailov.<br/>
    • <b>Technická dokumentácia</b> s prevádzkovým manuálom, postupom rotácie kľúčov a zoznamom núdzových príkazov.<br/>
    • <b>30 dní prioritnej podpory</b> a záručného monitoringu prevádzky priamo od vývojára.
    """
    scope_box = Table([[Paragraph(scope_text, style_body)]], colWidths=[523])
    scope_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_BRONZE),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(scope_box)
    story.append(Spacer(1, 6))

    # Financial Terms & Deposit Credit Note
    terms_text = """
    <b>Finančné podmienky a zúčtovanie zálohy (€500):</b><br/>
    Úhrada počiatočnej zálohy vo výške <b>500 €</b> pokrýva vypracovanie tohto architektonického blueprintu, analýzu API rozhraní a alokáciu infraštruktúry. Táto suma sa v plnej výške <b>započítava ako kredit</b> do konečnej ceny implementácie agenta podľa schváleného rozsahu prác.
    """
    terms_box = Table([[Paragraph(terms_text, style_body)]], colWidths=[523])
    terms_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFDF9')),
        ('BOX', (0, 0), (-1, -1), 1, COLOR_GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(terms_box)
    story.append(Spacer(1, 6))

    # Disclaimer Note
    disclaimer_text = """
    <font size="6.5" color="#94A3B8">
    <b>Právna doložka a duševné vlastníctvo:</b> Tento architektonický návrh je duševným vlastníctvom Mariána Stančíka Po úplnom uhradení dohodnutej ceny diela prechádzajú všetky majetkové práva k vytvorenému softvéru a špecifickým integráciám na objednávateľa. Marián Stančík garantuje dodržanie confidentiality a ochranu obchodného tajomstva.
    </font>
    """
    story.append(Paragraph(disclaimer_text, style_body))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✅ Successfully generated luxury Custom Agent Blueprint PDF: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/sample-custom-agent-blueprint.pdf"
    target = sys.argv[2] if len(sys.argv) > 2 else "https://www.marianstancik.dev"
    build_custom_agent_blueprint_pdf(out, client_name="Marian Stancik", client_url=target)
