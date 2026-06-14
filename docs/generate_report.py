#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a complete technical report (PDF) for the SpeakerDiff project.

SpeakerDiff: Speaker Embedding Generation using Denoising Diffusion
Probabilistic Models.

The report is built programmatically with ReportLab so it can be regenerated
deterministically from the repository:

    python3 docs/generate_report.py

Output:
    docs/SpeakerDiff_Technical_Report.pdf

The text and equations in this document are derived directly from the source
code in ``code/`` (model.py, utils.py, main.py, ema.py, dataNormalize.py),
the README, and the dataset tensors in ``dataset/``.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(HERE, "SpeakerDiff_Technical_Report.pdf")

# --------------------------------------------------------------------------- #
# Fonts (DejaVu has full Greek + math coverage; Liberation provides italics)
# --------------------------------------------------------------------------- #
DJ = "/usr/share/fonts/truetype/dejavu"
LB = "/usr/share/fonts/truetype/liberation"

pdfmetrics.registerFont(TTFont("Body", f"{DJ}/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("Body-Bold", f"{DJ}/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Body-Italic", f"{LB}/LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Body-BoldItalic", f"{LB}/LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFontFamily(
    "Body", normal="Body", bold="Body-Bold",
    italic="Body-Italic", boldItalic="Body-BoldItalic",
)

pdfmetrics.registerFont(TTFont("Head", f"{DJ}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Head-Bold", f"{DJ}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("Head", normal="Head", bold="Head-Bold",
                              italic="Head", boldItalic="Head-Bold")

pdfmetrics.registerFont(TTFont("Mono", f"{DJ}/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", f"{DJ}/DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFontFamily("Mono", normal="Mono", bold="Mono-Bold",
                              italic="Mono", boldItalic="Mono-Bold")

# --------------------------------------------------------------------------- #
# Palette
# --------------------------------------------------------------------------- #
NAVY = colors.HexColor("#1b2a4a")
BLUE = colors.HexColor("#2a5db0")
ACCENT = colors.HexColor("#c0392b")
LIGHT = colors.HexColor("#eef2f8")
GREY = colors.HexColor("#5b6470")
RULE = colors.HexColor("#c7d0de")
CODEBG = colors.HexColor("#f4f6fa")

# --------------------------------------------------------------------------- #
# Page geometry
# --------------------------------------------------------------------------- #
PAGE = A4
LMAR = RMAR = 2.2 * cm
TMAR = 2.3 * cm
BMAR = 2.0 * cm
CONTENT_W = PAGE[0] - LMAR - RMAR

# --------------------------------------------------------------------------- #
# Styles
# --------------------------------------------------------------------------- #
styles = getSampleStyleSheet()


def S(name, **kw):
    st = ParagraphStyle(name, **kw)
    styles.add(st)
    return st


BODY = S("BodyTxt", fontName="Body", fontSize=10.2, leading=15.5,
         alignment=TA_JUSTIFY, spaceAfter=7, textColor=colors.HexColor("#1c1c1c"))

LEAD = S("Lead", parent=BODY, fontSize=11, leading=17, textColor=NAVY,
         spaceAfter=9)

H1 = S("H1", fontName="Head-Bold", fontSize=18, leading=22, textColor=NAVY,
       spaceBefore=18, spaceAfter=10, keepWithNext=True)
H2 = S("H2", fontName="Head-Bold", fontSize=13.5, leading=18, textColor=BLUE,
       spaceBefore=14, spaceAfter=6, keepWithNext=True)
H3 = S("H3", fontName="Head-Bold", fontSize=11.5, leading=15, textColor=NAVY,
       spaceBefore=10, spaceAfter=4, keepWithNext=True)

EQ = S("Eq", fontName="Body", fontSize=11, leading=18, alignment=TA_CENTER,
       textColor=colors.black, spaceBefore=6, spaceAfter=8)

CAP = S("Cap", fontName="Body-Italic", fontSize=9, leading=12.5,
        alignment=TA_CENTER, textColor=GREY, spaceBefore=4, spaceAfter=12)

BULLET = S("Bul", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=4)

CODE = S("CodeBlk", fontName="Mono", fontSize=8.2, leading=11.2,
         textColor=colors.HexColor("#13294b"), backColor=CODEBG,
         borderColor=RULE, borderWidth=0.6, borderPadding=7,
         leftIndent=2, spaceBefore=4, spaceAfter=10)

TH = S("TH", fontName="Head-Bold", fontSize=9.3, leading=12,
       textColor=colors.white, alignment=TA_LEFT)
TD = S("TD", fontName="Body", fontSize=9.3, leading=12.5, textColor=colors.HexColor("#1c1c1c"))
TDB = S("TDB", parent=TD, fontName="Body-Bold")

TOCH = S("TOCHead", fontName="Head-Bold", fontSize=16, textColor=NAVY,
         spaceAfter=10)

# Title-page styles
TITLE = S("Title2", fontName="Head-Bold", fontSize=30, leading=36,
          alignment=TA_CENTER, textColor=NAVY)
SUBTITLE = S("Sub2", fontName="Head", fontSize=14.5, leading=20,
             alignment=TA_CENTER, textColor=BLUE)
TMETA = S("TMeta", fontName="Body", fontSize=11, leading=16,
          alignment=TA_CENTER, textColor=GREY)

# Table-of-contents entry styles
styles.add(ParagraphStyle("TOC1", fontName="Head-Bold", fontSize=10.5,
                          leading=15.5, spaceBefore=3, textColor=NAVY,
                          leftIndent=0))
styles.add(ParagraphStyle("TOC2", fontName="Body", fontSize=10,
                          leading=13, textColor=colors.HexColor("#33414f"),
                          leftIndent=16))


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
_heading_counter = [0]


def heading(text, level, style):
    """Create a heading paragraph tagged for the TOC and PDF outline."""
    _heading_counter[0] += 1
    key = f"h{_heading_counter[0]}"
    p = Paragraph(f'<a name="{key}"/>{text}', style)
    p._bookmarkKey = key
    p._tocLevel = level
    p._tocText = text
    # Top-level sections avoid being orphaned at the foot of a page without
    # forcing a hard break (which would leave under-filled pages).
    if level == 0:
        return [CondPageBreak(6 * cm), p]
    return p


def para(text, style=BODY):
    return Paragraph(text, style)


def bullets(items, style=BULLET):
    return [Paragraph(f"<bullet>&bull;</bullet>{t}", style) for t in items]


def figure(filename, caption, max_w_frac=1.0, max_h=15.0 * cm):
    """Scaled, centered image flowable + caption, preserving aspect ratio."""
    path = os.path.join(FIG, filename)
    iw, ih = ImageReader(path).getSize()
    aspect = ih / float(iw)
    w = CONTENT_W * max_w_frac
    h = w * aspect
    if h > max_h:
        h = max_h
        w = h / aspect
    img = Image(path, width=w, height=h, hAlign="CENTER")
    return [Spacer(1, 4), KeepTogether([img, Paragraph(caption, CAP)])]


def eq(text):
    return Paragraph(text, EQ)


def rule(color=RULE, thickness=0.7, space_before=2, space_after=8):
    t = Table([[""]], colWidths=[CONTENT_W], rowHeights=[0.1])
    t.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, -1), thickness, color),
        ("TOPPADDING", (0, 0), (-1, -1), space_before),
        ("BOTTOMPADDING", (0, 0), (-1, -1), space_after),
    ]))
    return t


def data_table(header, rows, col_widths, header_bg=NAVY, zebra=True,
               align_right_cols=()):
    data = [[Paragraph(h, TH) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), TD) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1, hAlign="CENTER")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, header_bg),
        ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ]
    if zebra:
        for i in range(1, len(data)):
            if i % 2 == 0:
                style.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    for c in align_right_cols:
        style.append(("ALIGN", (c, 1), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t


def callout(title, body_html, bar=BLUE, bg=LIGHT):
    """A boxed note / algorithm block."""
    inner = []
    if title:
        inner.append(Paragraph(title, ParagraphStyle(
            "coT", fontName="Head-Bold", fontSize=10, leading=14,
            textColor=bar, spaceAfter=4)))
    inner.append(Paragraph(body_html, ParagraphStyle(
        "coB", fontName="Body", fontSize=9.6, leading=14.5,
        textColor=colors.HexColor("#1c1c1c"))))
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("BOX", (0, 0), (-1, -1), 0.4, RULE),
    ]))
    return [t, Spacer(1, 10)]


def code_block(text):
    return Preformatted(text.strip("\n"), CODE)


# --------------------------------------------------------------------------- #
# Document template with TOC + outline + header/footer
# --------------------------------------------------------------------------- #
class Report(SimpleDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.title_text = "SpeakerDiff — Technical Report"

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            level = getattr(flowable, "_tocLevel", None)
            if level is not None:
                key = getattr(flowable, "_bookmarkKey")
                text = getattr(flowable, "_tocText")
                self.notify("TOCEntry", (level, text, self.page, key))
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=level,
                                          closed=(level > 0))


def _title_page(canvas, doc):
    canvas.saveState()
    # top + bottom accent bands
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE[1] - 1.0 * cm, PAGE[0], 1.0 * cm, stroke=0, fill=1)
    canvas.setFillColor(BLUE)
    canvas.rect(0, PAGE[1] - 1.18 * cm, PAGE[0], 0.18 * cm, stroke=0, fill=1)
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE[0], 1.0 * cm, stroke=0, fill=1)
    canvas.setFillColor(BLUE)
    canvas.rect(0, 1.0 * cm, PAGE[0], 0.18 * cm, stroke=0, fill=1)
    canvas.restoreState()


def _later_pages(canvas, doc):
    canvas.saveState()
    # header
    canvas.setFont("Head", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(LMAR, PAGE[1] - 1.35 * cm,
                      "SpeakerDiff: Speaker Embedding Generation with DDPMs")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(LMAR, PAGE[1] - 1.5 * cm, PAGE[0] - RMAR, PAGE[1] - 1.5 * cm)
    # footer
    canvas.line(LMAR, 1.35 * cm, PAGE[0] - RMAR, 1.35 * cm)
    canvas.setFont("Head", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(LMAR, 1.0 * cm, "Technical Report")
    canvas.drawRightString(PAGE[0] - RMAR, 1.0 * cm, f"Page {doc.page}")
    canvas.restoreState()


# --------------------------------------------------------------------------- #
# Build the story
# --------------------------------------------------------------------------- #
def build_story():
    s = []

    # ----------------------------- Title page ----------------------------- #
    s.append(Spacer(1, 3.6 * cm))
    s.append(Paragraph("SpeakerDiff", TITLE))
    s.append(Spacer(1, 0.35 * cm))
    s.append(Paragraph("Speaker Embedding Generation using<br/>"
                       "Denoising Diffusion Probabilistic Models", SUBTITLE))
    s.append(Spacer(1, 0.7 * cm))
    s.append(rule(color=RULE, thickness=1.0, space_after=2))
    s.append(Paragraph(
        "A privacy-preserving generative framework that synthesizes "
        "LibriSpeech-derived speaker embeddings, preserving the statistical "
        "structure of speech features while anonymizing speaker identity.",
        ParagraphStyle("pitch", parent=TMETA, fontSize=11.5, leading=17)))
    s.append(rule(color=RULE, thickness=1.0, space_before=4))
    s.append(Spacer(1, 1.6 * cm))

    meta_rows = [
        ["Project", "SpeakerDiff (speaker_embedding_generation_diffusion_models)"],
        ["Domain", "Generative modeling · Speech privacy · Diffusion models"],
        ["Core method", "Denoising Diffusion Probabilistic Models (DDPM)"],
        ["Data", "Speaker embeddings (64-, 128- and 704-dimensional)"],
        ["Implementation", "Python 3.8 · PyTorch 1.12 · scikit-learn · Weights & Biases"],
        ["Document type", "Complete technical report"],
    ]
    mt = Table([[Paragraph(k, TDB), Paragraph(v, TD)] for k, v in meta_rows],
               colWidths=[3.6 * cm, CONTENT_W - 3.6 * cm], hAlign="CENTER")
    mt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
    ]))
    s.append(mt)
    s.append(Spacer(1, 1.4 * cm))
    s.append(Paragraph("Generated from the project repository", TMETA))
    s.append(PageBreak())

    # ------------------------------- Abstract ------------------------------ #
    s.append(heading("Abstract", 0, H1))
    s.append(rule())
    s.append(para(
        "<b>SpeakerDiff</b> is a probabilistic generative framework that "
        "produces high-quality, synthetic <i>speaker embeddings</i> using a "
        "Denoising Diffusion Probabilistic Model (DDPM). Speaker embeddings are "
        "compact fixed-length vectors that encode the identity-bearing "
        "characteristics of a voice; they are widely used in speaker "
        "verification, recognition and text-to-speech (TTS) systems. Because "
        "these vectors carry biometric identity, sharing or publishing them "
        "raises significant privacy concerns. SpeakerDiff addresses this by "
        "learning the <i>distribution</i> of real embeddings and sampling new "
        "vectors from it. The generated vectors retain the global statistical "
        "structure of natural speech &mdash; so they remain useful for "
        "downstream synthesis &mdash; while the one-to-one link to any "
        "individual speaker is broken, effectively anonymizing the identity.", LEAD))
    s.append(para(
        "The model adapts the diffusion formulation of Ho et&nbsp;al. (2020) to "
        "operate directly on embedding vectors rather than images. A forward "
        "Markov chain gradually corrupts a data vector into isotropic Gaussian "
        "noise over a fixed number of steps using a <b>sigmoid</b> variance "
        "schedule, and a learned reverse chain denoises Gaussian samples back "
        "into realistic embeddings. Two interchangeable denoiser architectures "
        "are provided: a compact timestep-conditioned multilayer perceptron "
        "(MLP) and a 1-D convolutional U-Net with squeeze-and-excitation "
        "residual blocks. Training minimizes the simplified noise-prediction "
        "objective, stabilized with gradient clipping and an exponential moving "
        "average (EMA) of the weights.", BODY))
    s.append(para(
        "The framework is evaluated on three embedding sets derived from the "
        "LibriSpeech corpus (64-, 128- and 704-dimensional). Quality is "
        "assessed qualitatively with t-SNE projections that overlay real and "
        "generated points, and quantitatively with per-dimension mean and "
        "variance comparisons and cosine similarity. The results show that the "
        "generated embeddings occupy the same region of feature space as the "
        "originals, confirming that the diffusion process preserves feature "
        "information while decoupling it from speaker identity.", BODY))
    s.append(Spacer(1, 6))
    s.append(callout(
        "At a glance",
        "&bull;&nbsp; <b>Goal:</b> generate realistic, identity-anonymized speaker embeddings.<br/>"
        "&bull;&nbsp; <b>Method:</b> DDPM with a sigmoid &beta;-schedule over 100 diffusion steps.<br/>"
        "&bull;&nbsp; <b>Denoisers:</b> conditional MLP and 1-D U-Net (SE residual blocks).<br/>"
        "&bull;&nbsp; <b>Data:</b> LibriSpeech embeddings &mdash; 64-D (&asymp;20k), 128-D, 704-D (5k).<br/>"
        "&bull;&nbsp; <b>Evaluation:</b> t-SNE overlays, mean/variance match, cosine similarity."))
    s.append(PageBreak())

    # --------------------------- Table of contents ------------------------- #
    s.append(Paragraph("Contents", TOCH))
    s.append(rule())
    toc = TableOfContents()
    toc.levelStyles = [styles["TOC1"], styles["TOC2"]]
    toc.dotsMinLevel = 0
    s.append(toc)
    s.append(PageBreak())

    # ---------------------------- 1. Introduction -------------------------- #
    s.append(heading("1.  Introduction", 0, H1))
    s.append(rule())

    s.append(heading("1.1  Background and motivation", 1, H2))
    s.append(para(
        "Modern speech systems rarely operate on raw waveforms. Instead, a "
        "front-end network maps an utterance to a <b>speaker embedding</b> "
        "&mdash; a dense, fixed-length vector (such as an i-vector, x-vector or "
        "d-vector) that summarizes <i>who</i> is speaking, largely independent "
        "of <i>what</i> is said. These embeddings power speaker verification, "
        "diarization, and the speaker-conditioning input of multi-speaker "
        "text-to-speech engines.", BODY))
    s.append(para(
        "Precisely because an embedding captures voice identity, it behaves "
        "like a biometric. A leaked embedding can be used to impersonate a "
        "speaker or to link records across databases. Yet many applications "
        "need <i>realistic</i> embeddings &mdash; for data augmentation, for "
        "stress-testing recognizers, or for driving a TTS voice that sounds "
        "natural but belongs to no real person. This is the gap SpeakerDiff "
        "targets: generating embeddings that are statistically faithful to real "
        "speech yet are not traceable to any enrolled individual.", BODY))

    s.append(heading("1.2  Problem statement", 1, H2))
    s.append(para(
        "Given a collection of real speaker embeddings drawn from an unknown "
        "data distribution <i>q</i>(<b>x</b><sub>0</sub>), learn a generative "
        "model <i>p</i><sub>&theta;</sub>(<b>x</b><sub>0</sub>) from which we can "
        "draw new embeddings that (i)&nbsp;lie on the same manifold as real "
        "embeddings (high utility) and (ii)&nbsp;do not reproduce any individual "
        "training speaker (anonymity). The trade-off between these two goals "
        "&mdash; <i>utility</i> versus <i>privacy</i> &mdash; is the central "
        "tension the project explores.", BODY))

    s.append(heading("1.3  Why diffusion models", 1, H2))
    s.append(para(
        "Generative adversarial networks (GANs) can synthesize sharp samples "
        "but are notoriously unstable to train and prone to mode collapse, in "
        "which the generator covers only part of the data distribution. For an "
        "anonymization task, faithfully covering the full distribution matters: "
        "we want the diversity of real speakers, not a few prototypes. "
        "Diffusion models offer a favorable balance between <i>flexibility</i> "
        "and <i>tractability</i>. They are trained with a simple, stable "
        "regression objective, have no adversarial dynamics, and have been "
        "shown to match or beat GANs on image synthesis. SpeakerDiff transfers "
        "these properties to the embedding domain.", BODY))

    s.append(heading("1.4  Contributions", 1, H2))
    for b in bullets([
        "A DDPM formulation that operates directly on speaker-embedding "
        "vectors rather than images, including a tailored <b>sigmoid</b> noise "
        "schedule for low-dimensional continuous data.",
        "Two interchangeable denoiser backbones &mdash; a timestep-conditioned "
        "MLP and a 1-D U-Net with squeeze-and-excitation residual blocks "
        "&mdash; exposed through a single training entry point.",
        "An evaluation protocol combining t-SNE visualization with "
        "distribution-level statistics (per-dimension mean and variance) and "
        "cosine similarity between real and generated embeddings.",
        "An end-to-end, reproducible pipeline (data normalization, training, "
        "sampling, logging to Weights&nbsp;&amp;&nbsp;Biases) released across "
        "three embedding dimensionalities derived from LibriSpeech.",
    ]):
        s.append(b)

    # ------------------------ 2. DDPM background --------------------------- #
    s.append(heading("2.  Denoising Diffusion Probabilistic Models", 0, H1))
    s.append(rule())
    s.append(para(
        "A diffusion model defines two Markov chains over a sequence of latent "
        "variables <b>x</b><sub>1</sub>, &hellip;, <b>x</b><sub>T</sub> that "
        "share the dimensionality of the data <b>x</b><sub>0</sub>. The "
        "<i>forward</i> (diffusion) chain is fixed and gradually adds Gaussian "
        "noise; the <i>reverse</i> (denoising) chain is learned and removes it. "
        "Generation amounts to sampling pure noise and running the reverse "
        "chain. The notation below follows Ho et&nbsp;al.&nbsp;(2020) and maps "
        "one-to-one onto the code in <font face='Mono'>code/utils.py</font> and "
        "<font face='Mono'>code/main.py</font>.", BODY))

    s.append(heading("2.1  The forward (diffusion) process", 1, H2))
    s.append(para(
        "Starting from a real embedding <b>x</b><sub>0</sub>, the forward "
        "process produces progressively noisier vectors according to a fixed "
        "variance schedule &beta;<sub>1</sub>, &hellip;, &beta;<sub>T</sub> "
        "&isin; (0,&nbsp;1):", BODY))
    s.append(eq("q(<b>x</b><sub>t</sub> | <b>x</b><sub>t&minus;1</sub>) = "
                "N( <b>x</b><sub>t</sub> ; &radic;(1&minus;&beta;<sub>t</sub>)&middot;<b>x</b><sub>t&minus;1</sub> , "
                "&beta;<sub>t</sub><b>I</b> )"))
    s.append(para(
        "A key property is that we can sample <b>x</b><sub>t</sub> at an "
        "arbitrary step in closed form, without iterating. Defining "
        "&alpha;<sub>t</sub> = 1 &minus; &beta;<sub>t</sub> and the cumulative "
        "product &alpha;&#x0304;<sub>t</sub> = &prod;<sub>s=1</sub><super>t</super> &alpha;<sub>s</sub>:", BODY))
    s.append(eq("<b>x</b><sub>t</sub> = &radic;(&alpha;&#x0304;<sub>t</sub>)&middot;<b>x</b><sub>0</sub> "
                "+ &radic;(1&minus;&alpha;&#x0304;<sub>t</sub>)&middot;&epsilon; ,&nbsp;&nbsp;&nbsp; "
                "&epsilon; ~ N(<b>0</b>, <b>I</b>)"))
    s.append(para(
        "In code this is exactly <font face='Mono'>q_sample</font>: "
        "<font face='Mono'>x = x0 &middot; &alpha;&#x0304;<sub>t</sub><super>&frac12;</super> "
        "+ &epsilon; &middot; (1&minus;&alpha;&#x0304;<sub>t</sub>)<super>&frac12;</super></font>, "
        "where the two coefficients are precomputed as "
        "<font face='Mono'>alphas_bar_sqrt</font> and "
        "<font face='Mono'>one_minus_alphas_bar_sqrt</font>. As "
        "<i>t</i>&nbsp;&rarr;&nbsp;T the signal term vanishes and "
        "<b>x</b><sub>T</sub> approaches a standard Gaussian.", BODY))
    s.append(figure(
        "Forward_noise.png",
        "Figure 1.  The forward diffusion process. A structured, well-clustered "
        "embedding distribution (left) is progressively corrupted by Gaussian "
        "noise until it becomes an isotropic blob (right). Each panel is a "
        "2-D projection at an increasing diffusion step t.",
        max_w_frac=1.0))

    s.append(heading("2.2  The reverse (denoising) process", 1, H2))
    s.append(para(
        "The reverse process is parameterized by a neural network and undoes "
        "the corruption one step at a time. Each transition is modeled as a "
        "Gaussian whose mean is predicted by the network:", BODY))
    s.append(eq("p<sub>&theta;</sub>(<b>x</b><sub>t&minus;1</sub> | <b>x</b><sub>t</sub>) = "
                "N( <b>x</b><sub>t&minus;1</sub> ; &mu;<sub>&theta;</sub>(<b>x</b><sub>t</sub>, t) , "
                "&sigma;<sub>t</sub><super>2</super><b>I</b> )"))
    s.append(para(
        "Rather than predicting the mean directly, the network "
        "&epsilon;<sub>&theta;</sub>(<b>x</b><sub>t</sub>, t) predicts the "
        "<i>noise</i> that was added. The sampling mean is then reconstructed "
        "as implemented in <font face='Mono'>p_sample</font>:", BODY))
    s.append(eq("&mu;<sub>&theta;</sub> = (1 / &radic;&alpha;<sub>t</sub>) &middot; "
                "( <b>x</b><sub>t</sub> &minus; "
                "((1&minus;&alpha;<sub>t</sub>) / &radic;(1&minus;&alpha;&#x0304;<sub>t</sub>)) "
                "&middot; &epsilon;<sub>&theta;</sub>(<b>x</b><sub>t</sub>, t) )"))
    s.append(eq("<b>x</b><sub>t&minus;1</sub> = &mu;<sub>&theta;</sub> + "
                "&radic;(&beta;<sub>t</sub>) &middot; <b>z</b> ,&nbsp;&nbsp;&nbsp; "
                "<b>z</b> ~ N(<b>0</b>, <b>I</b>)"))
    s.append(para(
        "The variance is fixed to &sigma;<sub>t</sub><super>2</super> = "
        "&beta;<sub>t</sub> (the simplest choice from the DDPM paper). "
        "Generation, in <font face='Mono'>p_sample_loop</font>, starts from "
        "<b>x</b><sub>T</sub>&nbsp;~&nbsp;N(<b>0</b>,&nbsp;<b>I</b>) and applies "
        "<font face='Mono'>p_sample</font> for t = T&minus;1, &hellip;, 0, "
        "returning the full trajectory of intermediate samples.", BODY))
    s.append(figure(
        "backward_noise.png",
        "Figure 2.  The learned reverse process. Beginning from isotropic "
        "Gaussian noise (left), the trained denoiser progressively recovers "
        "structure until distinct clusters re-emerge (right) &mdash; the model "
        "reconstructing the embedding distribution step by step.",
        max_w_frac=1.0))

    s.append(heading("2.3  The variance (noise) schedule", 1, H2))
    s.append(para(
        "The schedule &beta;<sub>t</sub> controls how quickly signal is "
        "destroyed. SpeakerDiff uses the <b>sigmoid</b> schedule from "
        "<font face='Mono'>make_beta_schedule</font>: a linear ramp on "
        "[&minus;6,&nbsp;6] is passed through a sigmoid and rescaled to "
        "[start,&nbsp;end]. This keeps &beta;<sub>t</sub> small at both ends and "
        "larger in the middle, which empirically suits the smooth, "
        "low-dimensional embedding manifold better than a purely linear "
        "schedule. Linear and quadratic schedules are also implemented and can "
        "be selected by argument.", BODY))
    s.append(code_block(
        "def make_beta_schedule(schedule='linear', n_timesteps=100,\n"
        "                       start=1e-5, end=1e-2):\n"
        "    if schedule == 'linear':\n"
        "        betas = torch.linspace(start, end, n_timesteps)\n"
        "    elif schedule == 'quad':\n"
        "        betas = torch.linspace(start**0.5, end**0.5, n_timesteps) ** 2\n"
        "    elif schedule == 'sigmoid':\n"
        "        betas = torch.linspace(-6, 6, n_timesteps)\n"
        "        betas = torch.sigmoid(betas) * (end - start) + start\n"
        "    return betas"))
    s.append(para(
        "From &beta; the training script derives every quantity needed for both "
        "chains: &alpha;<sub>t</sub>, the cumulative products "
        "&alpha;&#x0304;<sub>t</sub>, their square roots, and the closed-form "
        "posterior coefficients used by the variational objective "
        "(<font face='Mono'>posterior_mean_coef_1/2</font>, "
        "<font face='Mono'>posterior_variance</font>).", BODY))

    s.append(heading("2.4  Training objective", 1, H2))
    s.append(para(
        "Diffusion models can be trained by maximizing a variational lower "
        "bound on the data log-likelihood. Ho et&nbsp;al. showed this reduces "
        "to a remarkably simple <i>noise-prediction</i> regression: sample a "
        "random step t, corrupt <b>x</b><sub>0</sub> to <b>x</b><sub>t</sub>, "
        "and train the network to predict the noise &epsilon; that was added. "
        "SpeakerDiff's primary loss, "
        "<font face='Mono'>noise_estimation_loss</font>, is exactly the "
        "mean-squared error between true and predicted noise:", BODY))
    s.append(eq("L<sub>simple</sub> = E<sub>t, <b>x</b><sub>0</sub>, &epsilon;</sub> "
                "[ &#8214; &epsilon; &minus; &epsilon;<sub>&theta;</sub>("
                "&radic;(&alpha;&#x0304;<sub>t</sub>)&middot;<b>x</b><sub>0</sub> + "
                "&radic;(1&minus;&alpha;&#x0304;<sub>t</sub>)&middot;&epsilon; , t) &#8214;<super>2</super> ]"))
    s.append(para(
        "A neat implementation detail: timesteps are sampled "
        "<i>antithetically</i>. The code draws half the batch's timesteps at "
        "random and sets the other half to their mirror "
        "(<font face='Mono'>n_steps&nbsp;&minus;&nbsp;t&nbsp;&minus;&nbsp;1</font>), "
        "which reduces the variance of the loss estimate across the diffusion "
        "horizon. A full variational bound "
        "(<font face='Mono'>loss_variational</font>) is also provided, combining "
        "the analytic KL between the true and predicted posteriors with a "
        "discretized-Gaussian decoder likelihood at t&nbsp;=&nbsp;0; the "
        "simplified MSE objective is used by default for its stability and "
        "speed.", BODY))

    # ----------------------------- 3. Dataset ------------------------------ #
    s.append(heading("3.  Dataset", 0, H1))
    s.append(rule())
    s.append(para(
        "All embeddings are derived from the <b>LibriSpeech</b> corpus, a "
        "large, freely available collection of read English audiobook speech. "
        "An upstream speaker-encoder maps utterances to fixed-length vectors; "
        "SpeakerDiff consumes these vectors as its training data. The "
        "repository ships three embedding sets at different dimensionalities, "
        "stored as serialized PyTorch tensors under "
        "<font face='Mono'>dataset/</font>:", BODY))
    s.append(Spacer(1, 2))
    s.append(data_table(
        ["Embedding set", "Dimensionality", "Samples", "File"],
        [
            ["Low-dimensional", "64", "&asymp; 20,000", "embedding_vectors_as_list64.pt"],
            ["Mid-dimensional", "128", "tens of thousands", "embedding_vectors_as_list128.pt"],
            ["High-dimensional", "704", "5,000", "704dim_embeds.pt"],
        ],
        col_widths=[3.8 * cm, 3.1 * cm, 2.6 * cm, CONTENT_W - 9.5 * cm]))
    s.append(Paragraph(
        "Table 1.  Embedding sets shipped with the project. Each file is a "
        "Python list of equal-length vectors loaded with <font face='Mono'>"
        "torch.load</font>.", CAP))
    s.append(para(
        "The three dimensionalities probe how diffusion behaves as the embedding "
        "space grows: 64-D is compact and densely sampled; 704-D is "
        "high-dimensional but sparsely sampled (only 5,000 vectors), a harder "
        "regime for any generative model. The default configuration in "
        "<font face='Mono'>main.py</font> uses a 128-dimensional input with the "
        "first 5,000 vectors, 100 diffusion steps and a batch size of 64.", BODY))

    s.append(heading("3.1  Preprocessing", 1, H2))
    s.append(para(
        "Before training, vectors are stacked into a single matrix and "
        "standardized with scikit-learn's "
        "<font face='Mono'>StandardScaler</font> "
        "(<font face='Mono'>code/dataNormalize.py</font>), giving every "
        "dimension zero mean and unit variance. This is important for "
        "diffusion: the forward process drives the data toward a "
        "<i>standard</i> normal, so matching the data's scale to that target at "
        "the outset makes the noise schedule well-behaved and keeps the "
        "noise-prediction targets on a consistent scale across dimensions.", BODY))
    s.append(code_block(
        "from sklearn.preprocessing import StandardScaler\n\n"
        "def dataNormalize(ndarray):\n"
        "    scaler = StandardScaler()\n"
        "    data_scaled = scaler.fit_transform(ndarray)\n"
        "    return data_scaled"))

    # --------------------------- 4. Methodology ---------------------------- #
    s.append(heading("4.  Model Architecture", 0, H1))
    s.append(rule())
    s.append(para(
        "The reverse process needs a network that, given a noisy embedding "
        "<b>x</b><sub>t</sub> and its timestep t, predicts the noise "
        "&epsilon;<sub>&theta;</sub>. SpeakerDiff provides two such denoisers in "
        "<font face='Mono'>code/model.py</font>. Both consume the timestep as a "
        "conditioning signal so that a single network can denoise across all "
        "noise levels.", BODY))

    s.append(heading("4.1  Conditional MLP denoiser (default)", 1, H2))
    s.append(para(
        "<font face='Mono'>ConditionalModel</font> is a five-layer MLP. The "
        "novel ingredient is <font face='Mono'>ConditionalLinear</font>: a "
        "linear layer whose output is modulated by a learned, per-timestep "
        "embedding. The timestep index t is mapped through an "
        "<font face='Mono'>nn.Embedding</font> table to a vector &gamma;(t), "
        "which scales the linear output element-wise &mdash; a multiplicative "
        "(FiLM-style) gating that lets the same weights behave differently at "
        "each noise level:", BODY))
    s.append(eq("ConditionalLinear(<b>x</b>, t) = &gamma;(t) &#8857; (<b>W</b><b>x</b> + <b>b</b>)"))
    s.append(para(
        "Layers are interleaved with the smooth <font face='Mono'>softplus</font> "
        "nonlinearity, and the final projection is an unconditioned linear layer "
        "back to the input dimension. The default widths are listed below "
        "(shown for the 128-dimensional configuration).", BODY))
    s.append(Spacer(1, 2))
    s.append(data_table(
        ["Layer", "Type", "In &rarr; Out", "Conditioning", "Activation"],
        [
            ["lin1", "ConditionalLinear", "128 &rarr; 128", "&gamma;(t) gate", "softplus"],
            ["lin2", "ConditionalLinear", "128 &rarr; 264", "&gamma;(t) gate", "softplus"],
            ["lin3", "ConditionalLinear", "264 &rarr; 128", "&gamma;(t) gate", "softplus"],
            ["lin4", "ConditionalLinear", "128 &rarr; 100", "&gamma;(t) gate", "softplus"],
            ["lin5", "Linear", "100 &rarr; 128", "&mdash;", "(none)"],
        ],
        col_widths=[1.8 * cm, 3.7 * cm, 2.6 * cm, 3.0 * cm, CONTENT_W - 11.1 * cm]))
    s.append(Paragraph("Table 2.  Layer stack of the conditional MLP denoiser "
                       "(<font face='Mono'>ConditionalModel</font>).", CAP))
    s.append(code_block(
        "class ConditionalLinear(nn.Module):\n"
        "    def __init__(self, num_in, num_out, n_steps):\n"
        "        super().__init__()\n"
        "        self.num_out = num_out\n"
        "        self.lin   = nn.Linear(num_in, num_out)\n"
        "        self.embed = nn.Embedding(n_steps, num_out)\n"
        "        self.embed.weight.data.uniform_()\n\n"
        "    def forward(self, x, y):\n"
        "        out   = self.lin(x)\n"
        "        gamma = self.embed(y)                 # per-timestep scale\n"
        "        return gamma.view(-1, self.num_out) * out"))

    s.append(heading("4.2  1-D U-Net denoiser", 1, H2))
    s.append(para(
        "For higher-dimensional or harder settings, "
        "<font face='Mono'>UNET_1D</font> offers a more expressive alternative. "
        "It treats the embedding as a 1-D signal and applies a convolutional "
        "encoder&ndash;decoder with skip connections. Three building blocks "
        "compose it:", BODY))
    for b in bullets([
        "<b>conbr_block</b> &mdash; Conv1D &rarr; BatchNorm &rarr; ReLU, the "
        "basic convolutional unit.",
        "<b>se_block</b> &mdash; a squeeze-and-excitation block that recalibrates "
        "channels by global-average-pooling, passing through a bottleneck, and "
        "gating with a sigmoid, letting the network emphasize informative "
        "channels.",
        "<b>re_block</b> &mdash; a residual block stacking two "
        "<font face='Mono'>conbr_block</font>s and an "
        "<font face='Mono'>se_block</font> with a skip connection for stable "
        "gradient flow.",
    ]):
        s.append(b)
    s.append(para(
        "The encoder progressively downsamples while multi-scale average-pooled "
        "copies of the input are concatenated back in; the decoder upsamples and "
        "fuses encoder features through skip connections &mdash; the "
        "characteristic U-Net shape. The conceptual layer plan is shown below.", BODY))
    s.append(figure(
        "Unet.drawio.png",
        "Figure 3.  Conceptual 1-D U-Net for embedding denoising. The encoder "
        "(left) contracts the representation through successive Conv1D / pooling "
        "stages; the decoder (right) expands it back to the input dimension, "
        "with skip connections (horizontal arrows) carrying high-resolution "
        "detail across the bottleneck.",
        max_w_frac=1.0, max_h=8.5 * cm))

    s.append(heading("4.3  Weight averaging (EMA)", 1, H2))
    s.append(para(
        "Training maintains an <b>exponential moving average</b> of the model "
        "weights (<font face='Mono'>code/ema.py</font>). After every optimizer "
        "step the shadow weights are updated as "
        "shadow&nbsp;&larr;&nbsp;&mu;&middot;shadow&nbsp;+&nbsp;(1&minus;&mu;)&middot;&theta;, "
        "with decay &mu;&nbsp;=&nbsp;0.9 in the default configuration. EMA "
        "weights are smoother and typically yield better, less noisy samples "
        "than the raw training weights &mdash; a standard and effective trick "
        "for diffusion models.", BODY))

    s.append(heading("4.4  Default hyperparameters", 1, H2))
    s.append(data_table(
        ["Hyperparameter", "Value", "Source / notes"],
        [
            ["Diffusion steps (T)", "100", "settings['num_steps']"],
            ["&beta; schedule", "sigmoid", "start 1e-5, end 5e-3"],
            ["Input dimension", "128", "settings['input_dimension']"],
            ["Batch size", "64", "settings['batch_size']"],
            ["Optimizer", "Adam", "learning rate 1e-4"],
            ["Gradient clipping", "max-norm 1.0", "clip_grad_norm_"],
            ["EMA decay (&mu;)", "0.9", "EMA(0.9)"],
            ["Training epochs", "1000", "outer training loop"],
            ["Variance &sigma;<sub>t</sub><super>2</super>", "&beta;<sub>t</sub>", "fixed (DDPM simple)"],
        ],
        col_widths=[4.6 * cm, 3.2 * cm, CONTENT_W - 7.8 * cm]))
    s.append(Paragraph("Table 3.  Default training and diffusion settings from "
                       "<font face='Mono'>code/main.py</font>.", CAP))

    # ------------------------ 5. Training & sampling ----------------------- #
    s.append(heading("5.  Training and Sampling", 0, H1))
    s.append(rule())
    s.append(heading("5.1  Training loop", 1, H2))
    s.append(para(
        "Training is a straightforward supervised regression. For each "
        "mini-batch the script draws random (antithetic) timesteps, forms the "
        "noisy inputs via the closed-form forward process, asks the denoiser to "
        "predict the injected noise, and minimizes the MSE. Gradients are "
        "clipped to a max-norm of 1.0 for stability, and the EMA shadow weights "
        "are refreshed after each step. Loss and intermediate t-SNE snapshots "
        "are logged to Weights&nbsp;&amp;&nbsp;Biases every 100 epochs.", BODY))
    s.append(callout(
        "Algorithm 1 &mdash; Training (noise prediction)",
        "1.&nbsp; <b>repeat</b> for each epoch and mini-batch <b>x</b><sub>0</sub>:<br/>"
        "2.&nbsp;&nbsp;&nbsp; sample t (antithetic) and &epsilon; ~ N(<b>0</b>, <b>I</b>)<br/>"
        "3.&nbsp;&nbsp;&nbsp; <b>x</b><sub>t</sub> = &radic;(&alpha;&#x0304;<sub>t</sub>)&middot;<b>x</b><sub>0</sub> "
        "+ &radic;(1&minus;&alpha;&#x0304;<sub>t</sub>)&middot;&epsilon;<br/>"
        "4.&nbsp;&nbsp;&nbsp; take a gradient step on "
        "&#8214;&epsilon; &minus; &epsilon;<sub>&theta;</sub>(<b>x</b><sub>t</sub>, t)&#8214;<super>2</super><br/>"
        "5.&nbsp;&nbsp;&nbsp; clip gradients (max-norm 1.0); optimizer step; update EMA<br/>"
        "6.&nbsp; <b>until</b> converged"))
    s.append(code_block(
        "for t in range(1000):\n"
        "    permutation = torch.randperm(dataset.size()[0])\n"
        "    for i in range(0, dataset.size()[0], batch_size):\n"
        "        indices = permutation[i:i + batch_size]\n"
        "        batch_x = dataset[indices]\n"
        "        loss = noise_estimation_loss(model, batch_x,\n"
        "                  alphas_bar_sqrt, one_minus_alphas_bar_sqrt, num_steps)\n"
        "        optimizer.zero_grad()\n"
        "        loss.backward()\n"
        "        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)\n"
        "        optimizer.step()\n"
        "        ema.update(model)"))

    s.append(heading("5.2  Sampling / generation", 1, H2))
    s.append(para(
        "To synthesize new embeddings, the model starts from pure Gaussian "
        "noise and iteratively applies the learned reverse step from "
        "t&nbsp;=&nbsp;T&minus;1 down to 0. "
        "<font face='Mono'>p_sample_loop</font> returns the entire trajectory, "
        "so intermediate states can be inspected (as in Figure&nbsp;2). The "
        "final state <b>x</b><sub>0</sub> is the generated embedding, ready to "
        "be denormalized and passed to a downstream TTS engine.", BODY))
    s.append(callout(
        "Algorithm 2 &mdash; Sampling",
        "1.&nbsp; <b>x</b><sub>T</sub> ~ N(<b>0</b>, <b>I</b>)<br/>"
        "2.&nbsp; <b>for</b> t = T&minus;1, &hellip;, 0 <b>do</b><br/>"
        "3.&nbsp;&nbsp;&nbsp; &epsilon;<sub>&theta;</sub> = model(<b>x</b><sub>t</sub>, t)<br/>"
        "4.&nbsp;&nbsp;&nbsp; &mu; = (1/&radic;&alpha;<sub>t</sub>)("
        "<b>x</b><sub>t</sub> &minus; ((1&minus;&alpha;<sub>t</sub>)/&radic;(1&minus;&alpha;&#x0304;<sub>t</sub>))&middot;&epsilon;<sub>&theta;</sub>)<br/>"
        "5.&nbsp;&nbsp;&nbsp; <b>x</b><sub>t&minus;1</sub> = &mu; + &radic;(&beta;<sub>t</sub>)&middot;<b>z</b>,&nbsp;&nbsp; <b>z</b> ~ N(<b>0</b>, <b>I</b>)<br/>"
        "6.&nbsp; <b>return</b> <b>x</b><sub>0</sub>",
        bar=ACCENT))

    # ----------------------------- 6. Results ------------------------------ #
    s.append(heading("6.  Experiments and Results", 0, H1))
    s.append(rule())
    s.append(heading("6.1  Evaluation methodology", 1, H2))
    s.append(para(
        "Because there is no single ground-truth target for a <i>generated</i> "
        "embedding, evaluation focuses on whether the generated set matches the "
        "real set as a <i>distribution</i>. Three complementary measures are "
        "used:", BODY))
    for b in bullets([
        "<b>t-SNE projection.</b> Real (red) and generated (blue) embeddings "
        "are projected to 2-D with t-SNE and overlaid. Strong overlap indicates "
        "the generated points share the real manifold.",
        "<b>Per-dimension statistics.</b> The mean and variance along each "
        "embedding dimension are computed for both sets and compared; small "
        "differences indicate the global structure is preserved.",
        "<b>Cosine similarity.</b> Cosine similarity between real and generated "
        "vectors summarizes directional agreement in the high-dimensional space.",
    ]):
        s.append(b)
    s.append(para(
        "Mean/variance differences and cosine statistics are computed in "
        "<font face='Mono'>main.py</font> and logged to "
        "Weights&nbsp;&amp;&nbsp;Biases alongside the plots.", BODY))

    s.append(heading("6.2  Distribution match across dimensionalities", 1, H2))
    s.append(para(
        "Figure 4 overlays real and generated embeddings for all three "
        "dimensionalities. Across 64-, 128- and 704-D the generated (blue) "
        "points populate the same region as the real (red) points, with the "
        "densest agreement in the core of the distribution &mdash; evidence that "
        "the diffusion model has captured the bulk of the embedding manifold.", BODY))
    s.append(figure(
        "TSNE-Based 2D Plot of 64 dimensional Embeddings.png",
        "Figure 4.  t-SNE overlays of real (red) and generated (blue) "
        "embeddings for the 64-, 128- and 704-dimensional sets. Generated "
        "points share the support of the real distribution; the high-density "
        "core overlaps most strongly.",
        max_w_frac=1.0, max_h=6.5 * cm))

    s.append(heading("6.3  Per-set results", 1, H2))
    s.append(para(
        "Figures 5&ndash;7 show individual overlays. For the 64-D set the two "
        "clouds are thoroughly interleaved, indicating an excellent match. For "
        "the 704-D set the generated points form a coherent central cluster "
        "within the broader real spread; with only 5,000 high-dimensional "
        "training vectors this is the hardest regime, and the model "
        "concentrates mass on the dominant mode.", BODY))
    s.append(figure(
        "After DDM Both 64_dimension_embedding.png",
        "Figure 5.  64-dimensional embeddings: real (red) vs. generated (blue) "
        "after diffusion. The clouds are strongly interleaved.",
        max_w_frac=0.62, max_h=8.0 * cm))
    s.append(figure(
        "After DDM Both 128_dimension_embedding_datapoints.png",
        "Figure 6.  128-dimensional embeddings: generated points concentrate in "
        "the high-density core of the real distribution.",
        max_w_frac=0.62, max_h=8.0 * cm))
    s.append(figure(
        "After DDM Both 704_dimension_embedding.png",
        "Figure 7.  704-dimensional embeddings: with only 5,000 sparse "
        "high-dimensional samples, the model captures the dominant central mode "
        "of the real spread.",
        max_w_frac=0.62, max_h=8.0 * cm))
    s.append(para(
        "The U-Net denoiser was also evaluated on the 64-D set (Figure&nbsp;8), "
        "producing a comparably broad, well-mixed overlay and confirming that "
        "the framework is backbone-agnostic.", BODY))
    s.append(figure(
        "After DDM Both 64UNET_dimension_embedding_datapoints.png",
        "Figure 8.  64-dimensional embeddings generated with the 1-D U-Net "
        "denoiser: real (red) vs. generated (blue).",
        max_w_frac=0.62, max_h=8.0 * cm))

    s.append(heading("6.4  Downstream audio", 1, H2))
    s.append(para(
        "Because the generated vectors live in the speaker-embedding space, "
        "they can be fed to a multi-speaker TTS engine to render audio in the "
        "voice of a synthetic, non-existent speaker. The project notes both "
        "male- and female-sounding outputs produced this way &mdash; a concrete "
        "demonstration that the embeddings carry usable, speech-relevant "
        "information while no longer identifying a real individual.", BODY))

    # --------------------- 7. Discussion / limitations --------------------- #
    s.append(heading("7.  Discussion", 0, H1))
    s.append(rule())
    s.append(para(
        "The central finding is that a diffusion model can learn the "
        "distribution of speaker embeddings and sample new members of it. This "
        "directly serves the privacy goal: a sampled embedding is drawn from "
        "the learned density rather than copied from a training speaker, so it "
        "preserves the <i>statistics</i> of real voices (utility) without "
        "reproducing any one identity (anonymity). The t-SNE overlays make this "
        "visible &mdash; generated points are diffused throughout the real "
        "support rather than collapsing onto a few prototypes, the failure mode "
        "that plagues GANs.", BODY))
    s.append(para(
        "The dimensionality sweep is instructive. Low-dimensional, densely "
        "sampled spaces (64-D, &asymp;20k vectors) are matched almost perfectly. "
        "The high-dimensional, sparsely sampled 704-D set is harder: the model "
        "reliably captures the dominant mode but does not fully expand to the "
        "outer real spread, the expected behavior when data is scarce relative "
        "to dimensionality.", BODY))

    s.append(heading("7.1  Limitations", 1, H2))
    for b in bullets([
        "<b>Distribution-level, not identity-level, evaluation.</b> The metrics "
        "confirm the generated set matches the real set in aggregate, but do "
        "not formally quantify anonymity (e.g. via a speaker-verification "
        "attack) or downstream ASR/TTS utility.",
        "<b>Data scarcity at high dimension.</b> The 704-D set's 5,000 samples "
        "limit coverage of the tails of the distribution.",
        "<b>Sampling cost.</b> Generation runs the full T-step reverse chain; "
        "faster samplers (e.g. DDIM) are referenced but not yet integrated.",
        "<b>Fixed reverse variance.</b> &sigma;<sub>t</sub><super>2</super> is "
        "fixed to &beta;<sub>t</sub>; learning the variance could improve "
        "sample quality.",
    ]):
        s.append(b)

    s.append(heading("7.2  Future work", 1, H2))
    for b in bullets([
        "Quantify anonymity with an equal-error-rate study against a speaker "
        "verifier, and utility with ASR word-error-rate on TTS output.",
        "Integrate accelerated sampling (DDIM) to cut generation time.",
        "Scale and rebalance the high-dimensional dataset; explore conditional "
        "generation (e.g. by gender or accent attributes).",
        "Adopt learned reverse variances and richer time embeddings "
        "(sinusoidal positional encodings).",
    ]):
        s.append(b)

    # --------------------------- 8. Reproducibility ------------------------ #
    s.append(heading("8.  Reproducibility and Usage", 0, H1))
    s.append(rule())
    s.append(para(
        "Experiments were run on a 3.3&nbsp;GHz AMD EPYC 7002-series CPU with "
        "Python&nbsp;3.8; the code also runs on GPU when available "
        "(<font face='Mono'>torch.device('cuda' if &hellip;)</font>). All "
        "dependencies are pinned in <font face='Mono'>requirements.txt</font> "
        "(PyTorch&nbsp;1.12, scikit-learn, matplotlib, NumPy, "
        "Weights&nbsp;&amp;&nbsp;Biases).", BODY))
    s.append(heading("8.1  Setup and run", 1, H2))
    s.append(code_block(
        "# 1. Install dependencies\n"
        "pip3 install -r requirements.txt\n\n"
        "# 2. Train (and generate + evaluate) from the code/ directory\n"
        "cd code\n"
        "python3 main.py\n\n"
        "# Outputs:\n"
        "#   figures/   t-SNE plots (before / after / overlay)\n"
        "#   GeneratedEmbeddings/   saved sampled embeddings\n"
        "#   Weights & Biases run:  loss curves + scatter plots"))
    s.append(para(
        "The denoiser backbone is selected in <font face='Mono'>main.py</font> "
        "by instantiating either <font face='Mono'>ConditionalModel</font> or "
        "<font face='Mono'>UNET_1D</font>; the embedding set is chosen via "
        "<font face='Mono'>DATA_PATH</font> and the input dimension in the "
        "<font face='Mono'>settings</font> dictionary.", BODY))

    s.append(heading("8.2  Repository structure", 1, H2))
    s.append(data_table(
        ["Path", "Contents"],
        [
            ["code/main.py", "End-to-end training, sampling, evaluation, logging"],
            ["code/model.py", "ConditionalModel (MLP) and UNET_1D denoisers"],
            ["code/utils.py", "Schedules, forward/reverse steps, loss functions"],
            ["code/ema.py", "Exponential moving average of weights"],
            ["code/dataNormalize.py", "StandardScaler normalization"],
            ["dataset/", "64-, 128- and 704-D embedding tensors (.pt)"],
            ["figures/", "Forward/reverse plots, U-Net diagram, t-SNE overlays"],
            ["references/", "Background paper (GANSpace, NeurIPS 2020)"],
            ["requirements.txt", "Pinned Python dependencies"],
        ],
        col_widths=[5.0 * cm, CONTENT_W - 5.0 * cm]))
    s.append(Paragraph("Table 4.  Project layout.", CAP))

    s.append(heading("8.3  Note on credentials", 1, H2))
    s.append(callout(
        "Security note",
        "The training script contains a hard-coded Weights&nbsp;&amp;&nbsp;Biases "
        "API key. Committed secrets should be revoked and rotated, then supplied "
        "at runtime via an environment variable "
        "(<font face='Mono'>WANDB_API_KEY</font>) or a local, git-ignored "
        "configuration file rather than stored in source control.",
        bar=ACCENT, bg=colors.HexColor("#fbeeec")))

    # --------------------------- 9. Conclusion ----------------------------- #
    s.append(heading("9.  Conclusion", 0, H1))
    s.append(rule())
    s.append(para(
        "SpeakerDiff demonstrates that Denoising Diffusion Probabilistic Models "
        "are an effective, stable tool for generating speaker embeddings. By "
        "adapting the DDPM forward/reverse formulation to operate on embedding "
        "vectors &mdash; with a tailored sigmoid noise schedule, a simple "
        "noise-prediction objective, EMA weight averaging, and a choice of MLP "
        "or 1-D U-Net denoisers &mdash; the project produces synthetic "
        "embeddings whose distribution closely matches real LibriSpeech "
        "embeddings. The generated vectors retain the speech-relevant feature "
        "structure needed for downstream TTS while breaking the link to any "
        "individual speaker, advancing the goal of privacy-preserving speech "
        "generation. The clearest next steps are formal anonymity/utility "
        "benchmarks and faster sampling.", LEAD))

    s.append(heading("References", 0, H1))
    s.append(rule())
    refs = [
        "J. Ho, A. Jain, and P. Abbeel. <i>Denoising Diffusion Probabilistic "
        "Models.</i> Advances in Neural Information Processing Systems "
        "(NeurIPS), 2020. arXiv:2006.11239.",
        "J. Song, C. Meng, and S. Ermon. <i>Denoising Diffusion Implicit "
        "Models.</i> International Conference on Learning Representations "
        "(ICLR), 2021. arXiv:2010.02502.",
        "P. Dhariwal and A. Nichol. <i>Diffusion Models Beat GANs on Image "
        "Synthesis.</i> Advances in Neural Information Processing Systems "
        "(NeurIPS), 2021. arXiv:2105.05233.",
        "E. H&auml;rk&ouml;nen, A. Hertzmann, J. Lehtinen, and S. Paris. "
        "<i>GANSpace: Discovering Interpretable GAN Controls.</i> NeurIPS, 2020. "
        "(Included under <font face='Mono'>references/</font>.)",
        "V. Panayotov, G. Chen, D. Povey, and S. Khudanpur. <i>LibriSpeech: An "
        "ASR corpus based on public domain audio books.</i> IEEE ICASSP, 2015.",
    ]
    ref_style = ParagraphStyle("ref", parent=BODY, leftIndent=18,
                               firstLineIndent=-18, spaceAfter=7)
    for i, r in enumerate(refs, 1):
        s.append(Paragraph(f"[{i}]&nbsp;&nbsp;{r}", ref_style))

    return s


def _flatten(items):
    out = []
    for it in items:
        if isinstance(it, (list, tuple)):
            out.extend(_flatten(it))
        else:
            out.append(it)
    return out


def main():
    doc = Report(
        OUT, pagesize=PAGE,
        leftMargin=LMAR, rightMargin=RMAR, topMargin=TMAR, bottomMargin=BMAR,
        title="SpeakerDiff — Technical Report",
        author="SpeakerDiff project",
        subject="Speaker Embedding Generation using Denoising Diffusion Probabilistic Models",
    )
    story = _flatten(build_story())

    def first(canvas, d):
        _title_page(canvas, d)

    def later(canvas, d):
        # Title page is page 1: skip header/footer there.
        if d.page == 1:
            _title_page(canvas, d)
        else:
            _later_pages(canvas, d)

    doc.multiBuild(story, onFirstPage=first, onLaterPages=later)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
