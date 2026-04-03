#!/usr/bin/env python3
"""Generate an 8-page PDF guide: 3 Frameworks That Make Claude Code Unstoppable."""

import os
from fpdf import FPDF
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "3-frameworks-claude-code.pdf")

# Page dimensions (landscape letter in mm)
W, H = 279.4, 215.9
MARGIN = 12
CONTENT_W = W - 2 * MARGIN


class FrameworksPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="L", unit="mm", format="Letter")
        self.set_auto_page_break(auto=False)

    def add_image_centered(self, path, y, max_w=None, max_h=None):
        """Place image centered horizontally, return bottom y coordinate."""
        if max_w is None:
            max_w = CONTENT_W
        if max_h is None:
            max_h = 80

        img = Image.open(path)
        iw, ih = img.size
        ratio = iw / ih

        w = max_w
        h = w / ratio
        if h > max_h:
            h = max_h
            w = h * ratio

        x = (W - w) / 2
        self.image(path, x=x, y=y, w=w, h=h)
        return y + h

    def section_header(self, text, y):
        """Draw a section header."""
        self.set_xy(MARGIN, y)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(50, 50, 50)
        self.cell(CONTENT_W, 7, text)
        return y + 8

    def bullet(self, text, y, indent=4):
        """Draw a bullet point."""
        self.set_xy(MARGIN + indent, y)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.cell(3, 5, "-")
        self.set_x(MARGIN + indent + 4)
        self.multi_cell(CONTENT_W - indent - 4, 5, text)
        return self.get_y() + 1

    def small_text(self, text, y, size=9, bold=False):
        """Draw smaller text line."""
        self.set_xy(MARGIN, y)
        style = "B" if bold else ""
        self.set_font("Helvetica", style, size)
        self.set_text_color(80, 80, 80)
        self.multi_cell(CONTENT_W, 4.5, text, align="L")
        return self.get_y() + 1


def build_pdf():
    pdf = FrameworksPDF()

    # ── Page 1: Cover ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(30, 30, 30)
    pdf.set_xy(MARGIN, 10)
    pdf.cell(CONTENT_W, 14, "3 Frameworks That Make Claude Code Unstoppable", align="C")
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(MARGIN, 25)
    pdf.cell(CONTENT_W, 7, "A Visual Guide by EricTech  |  skool.com/erictech", align="C")

    y = pdf.add_image_centered(os.path.join(BASE, "1-intro", "0.jpg"), 38, max_h=72)
    pdf.add_image_centered(os.path.join(BASE, "2-solution", "1.jpg"), y + 4, max_h=82)

    # ── Page 2: The Problem ──
    pdf.add_page()
    y = pdf.section_header("The Problem: Can We Trust AI-Generated Code?", 8)
    y = pdf.bullet(
        "Claude Code can generate entire apps from ideas -- but do we trust the output? Testing, security, consistency, and framework quality are often missing.",
        y,
    )
    y = pdf.bullet(
        "Without guardrails, fixing AI-written bugs can take longer than writing the code yourself.",
        y,
    )
    y = pdf.bullet(
        "The community built three frameworks to solve this -- each targeting a different part of the problem.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "1-intro", "2.jpg"), y + 2, max_h=68)
    pdf.add_image_centered(os.path.join(BASE, "1-intro", "3.jpg"), y + 4, max_h=72)

    # ── Page 3: Superpowers ──
    pdf.add_page()
    y = pdf.section_header("Framework 1: Superpowers -- Constrain the Process", 8)
    y = pdf.bullet(
        "Forces Claude Code to follow a strict software development methodology instead of coding randomly.",
        y,
    )
    y = pdf.bullet(
        "Workflow: Clarify intent -> Confirm spec -> Plan implementation -> Write tests first (TDD) -> Build code -> Refactor until stable.",
        y,
    )
    y = pdf.bullet(
        "Test-Driven Development: sets the rules on how software should behave BEFORE writing code -- guarantees automation testing is in place.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "3-Superpowers", "variation-1.jpg"), y + 2, max_h=68)
    pdf.add_image_centered(os.path.join(BASE, "2-solution", "Superpowers.png"), y + 4, max_h=62)

    # ── Page 4: GSD ──
    pdf.add_page()
    y = pdf.section_header("Framework 2: GSD -- Constrain the Environment", 8)
    y = pdf.bullet(
        "Solves 'context rot': accuracy drops dramatically as conversation length grows. At 70%+ context, expect hallucinations and broken output.",
        y,
    )
    y = pdf.bullet(
        "GSD keeps every session under 50% context window for maximum accuracy from the LLM.",
        y,
    )
    y = pdf.bullet(
        "Breaks projects into phases, saves state to local .md files, and spins up fresh orchestrators for each phase -- clean slate every time.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "4-GSD", "0.jpg"), y + 2, max_h=62)
    pdf.add_image_centered(os.path.join(BASE, "4-GSD", "1-branded-var2.jpg"), y + 4, max_h=62)

    # ── Page 5: GSD vs Superpowers ──
    pdf.add_page()
    y = pdf.section_header("Key Difference: Orchestrator Switching", 8)
    y = pdf.bullet(
        "Superpowers: one mega-orchestrator handles everything (brainstorm, plan, execute) -- context grows throughout the entire conversation.",
        y,
    )
    y = pdf.bullet(
        "GSD: switches to a fresh orchestrator for each phase. After each phase completes, state is saved to disk and a new orchestrator picks up.",
        y,
    )
    y = pdf.bullet(
        "Both use sub-agents -- but GSD also keeps the orchestrator itself under 50% context, not just the workers.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "4-GSD", "compare-var2.jpg"), y + 2, max_h=62)
    pdf.add_image_centered(os.path.join(BASE, "4-GSD", "3.jpg"), y + 4, max_h=62)

    # ── Page 6: gstack ──
    pdf.add_page()
    y = pdf.section_header("Framework 3: gstack -- Constrain the Perspective", 8)
    y = pdf.bullet(
        "Built by Garry Tan (CEO of Y Combinator). Breaks the single agent into specialist roles: CEO, Engineer, Designer, QA, Security Officer, Release Engineer.",
        y,
    )
    y = pdf.bullet(
        "Each stage of development triggers the right specialist -- planning uses the CEO lens, building uses engineering, QA uses browser-based testing.",
        y,
    )
    y = pdf.bullet(
        "Not just role prompts -- gstack uses a 5-layer mechanism to ensure each role stays in character and does its job without overstepping.",
        y,
    )

    # Two images side by side would be ideal but let's stack them
    y = pdf.add_image_centered(os.path.join(BASE, "5-gstack", "0.jpg"), y + 2, max_h=50)
    y = pdf.add_image_centered(os.path.join(BASE, "5-gstack", "1.0.jpg"), y + 3, max_h=50)
    pdf.add_image_centered(os.path.join(BASE, "5-gstack", "1.6.jpg"), y + 3, max_h=38)

    # ── Page 7: gstack 5 Layers ──
    pdf.add_page()
    y = pdf.section_header("gstack's 5-Layer Mechanism", 8)
    y = pdf.add_image_centered(os.path.join(BASE, "5-gstack", "2.jpg"), y + 1, max_h=72)

    y = pdf.small_text("Layer 1: Role Focus -- Put on blinders. Each specialist only sees what matters for their job. QA sees testing, not architecture.", y + 3, bold=True)
    y = pdf.small_text("Layer 2: Data Flow -- Your homework is someone else's finished homework. Work builds on previous stages naturally.", y, bold=True)
    y = pdf.small_text("Layer 3: Quality Control -- A checklist dashboard everyone can see. Nobody ships until every box is green.", y, bold=True)
    y = pdf.small_text("Layer 4: Boil the Lake -- Finish what you can do perfectly. Don't start what you can't. Small lake = doable. Ocean = skip it.", y, bold=True)
    y = pdf.small_text("Layer 5: ELI16 Mode -- If too many things are juggled (3+ sessions), gstack slows down and re-explains: what I found, why it matters, what to do next.", y, bold=True)

    # ── Page 8: Power Stack + CTA ──
    pdf.add_page()
    y = pdf.section_header("Combining Into a Power Stack", 8)
    y = pdf.bullet(
        "gstack for planning and QA -- diverse specialist perspectives (CEO, designer, security) refine your project idea and polish the final product.",
        y,
    )
    y = pdf.bullet(
        "GSD for project management -- breaks the refined plan into milestones, each under 50% context. Protects accuracy across the entire project lifecycle.",
        y,
    )
    y = pdf.bullet(
        "Superpowers for execution -- each milestone is built with TDD, parallel sub-agents, and strict spec-driven development.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "5-compare.jpg"), y + 2, max_h=78)

    # CTA
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(40, 40, 40)
    pdf.set_xy(MARGIN, y + 6)
    pdf.cell(CONTENT_W, 7, "Ready to level up? Join the community: skool.com/erictech", align="C")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(MARGIN, y + 15)
    pdf.cell(CONTENT_W, 5, "github.com/obra/superpowers  |  github.com/gsd-build/gsd  |  github.com/garrytan/gstack", align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(MARGIN, y + 22)
    pdf.cell(CONTENT_W, 5, "Watch the full video on the EricTech YouTube channel", align="C")

    # Save
    pdf.output(OUT)
    print(f"PDF saved to: {OUT}")


if __name__ == "__main__":
    build_pdf()
