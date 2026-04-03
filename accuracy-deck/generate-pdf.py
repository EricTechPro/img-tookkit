#!/usr/bin/env python3
"""Generate a 5-page PDF guide: 7 Tips to Improve Claude Code Accuracy."""

import os
from fpdf import FPDF
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "7-tips-claude-code-accuracy.pdf")

# Page dimensions (landscape letter in mm)
W, H = 279.4, 215.9
MARGIN = 12
CONTENT_W = W - 2 * MARGIN


class AccuracyPDF(FPDF):
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

        # Fit within max dimensions
        w = max_w
        h = w / ratio
        if h > max_h:
            h = max_h
            w = h * ratio

        x = (W - w) / 2
        self.image(path, x=x, y=y, w=w, h=h)
        return y + h

    def section_header(self, text, y):
        """Draw a colored section header."""
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


def build_pdf():
    pdf = AccuracyPDF()

    # ── Page 1: Cover + Credibility ──
    pdf.add_page()
    # Title
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(30, 30, 30)
    pdf.set_xy(MARGIN, 10)
    pdf.cell(CONTENT_W, 14, "7 Tips to Improve Claude Code Accuracy", align="C")
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(MARGIN, 25)
    pdf.cell(CONTENT_W, 7, "A Visual Guide by EricTech  |  skool.com/erictech", align="C")

    # Cover image
    y = pdf.add_image_centered(os.path.join(BASE, "0-intro", "0-intro.jpg"), 38, max_h=78)

    # Credibility image
    pdf.add_image_centered(os.path.join(BASE, "0-intro", "0.jpg"), y + 4, max_h=78)

    # ── Page 2: Tips 1 & 2 ──
    pdf.add_page()

    # Tip 1
    y = pdf.section_header("Tip 1: Context Management", 8)
    y = pdf.bullet(
        "Claude Code's accuracy drops significantly after ~40% context usage --leading to bugs, hallucinations, and wasted time.",
        y,
    )
    y = pdf.bullet(
        'Solution: Add a status line progress bar to track context usage. When you hit ~50%, run /clear to reset.',
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "1-context", "1.jpg"), y + 2, max_h=72)

    # Tip 2
    y = pdf.section_header("Tip 2: Sub-Agents", y + 4)
    y = pdf.bullet(
        "Instead of one agent doing everything, delegate tasks to sub-agents --each gets a fresh context window.",
        y,
    )
    y = pdf.bullet(
        "Benefits: fresh context per task, parallel execution, fewer bugs and hallucinations.",
        y,
    )
    pdf.add_image_centered(os.path.join(BASE, "2-sub-agents", "1.jpg"), y + 2, max_h=72)

    # ── Page 3: Tips 3 & 4 ──
    pdf.add_page()

    # Tip 3
    y = pdf.section_header("Tip 3: Superpowers Framework", 8)
    y = pdf.bullet(
        "An agentic skill framework that manages sub-agents, follows spec-driven and test-driven development, and uses git worktrees.",
        y,
    )
    y = pdf.bullet(
        "Workflow: Clarify requirements -> Generate execution plan/spec -> Sub-agents build it with TDD (Red -> Green -> Refactor).",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "3-superpowers", "1.jpg"), y + 2, max_h=72)

    # Tip 4
    y = pdf.section_header("Tip 4: Agent Teams", y + 4)
    y = pdf.bullet(
        "Takes sub-agents further by adding cross-communication --frontend, backend, and database agents talk to each other.",
        y,
    )
    y = pdf.bullet(
        "A team leader coordinates and supervises, enabling complex multi-agent collaboration.",
        y,
    )
    pdf.add_image_centered(os.path.join(BASE, "4-agent-team", "1.jpg"), y + 2, max_h=72)

    # ── Page 4: Tips 5 & 6 ──
    pdf.add_page()

    # Tip 5
    y = pdf.section_header("Tip 5: Context7 --Up-to-Date Documentation", 8)
    y = pdf.bullet(
        "Without Context7, Claude relies on outdated training data --hallucinated APIs, old code examples, generic answers.",
        y,
    )
    y = pdf.bullet(
        "Context7 pulls version-specific docs straight from the source. Set up via context7.com/dashboard with CLI + Skills.",
        y,
    )
    y = pdf.bullet(
        "Use it to fact-check your entire codebase against current documentation after building features.",
        y,
    )

    # Tip 6
    y = pdf.section_header("Tip 6: NotebookLM Knowledge Base", y + 3)
    y = pdf.bullet(
        "Stuff research (YouTube videos, Google Drive files, PRDs, web sources) into NotebookLM as a zero-infrastructure RAG.",
        y,
    )
    y = pdf.bullet(
        "Claude queries NotebookLM on-demand instead of loading all docs into context --grounded answers, less context bloat.",
        y,
    )
    y = pdf.add_image_centered(os.path.join(BASE, "5-notebooklm", "1.jpg"), y + 2, max_h=60)
    pdf.add_image_centered(os.path.join(BASE, "5-notebooklm", "3.jpg"), y + 2, max_h=60)

    # ── Page 5: Tip 7 + Closing ──
    pdf.add_page()

    # Tip 7
    y = pdf.section_header("Tip 7: CLI + Skills Over MCP", 8)
    y = pdf.bullet(
        "MCP loads all tool schemas into context at startup, eating into your context window from the start.",
        y,
    )
    y = pdf.bullet(
        "CLI + Skills only loads information when relevant --dramatically reduces token usage and cost.",
        y,
    )
    y = pdf.bullet(
        "Real-world test: Playwright CLI used fewer tokens and produced more accurate results than MCP.",
        y,
    )

    # Closing image
    y = pdf.add_image_centered(os.path.join(BASE, "6-outro", "0-intro-v3.jpg"), y + 4, max_h=90)

    # CTA
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(40, 40, 40)
    pdf.set_xy(MARGIN, y + 5)
    pdf.cell(CONTENT_W, 7, "Ready to level up? Join the community: skool.com/erictech", align="C")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_xy(MARGIN, y + 14)
    pdf.cell(CONTENT_W, 5, "Watch the full video and deep dives on the EricTech YouTube channel", align="C")

    # Save
    pdf.output(OUT)
    print(f"PDF saved to: {OUT}")


if __name__ == "__main__":
    build_pdf()
