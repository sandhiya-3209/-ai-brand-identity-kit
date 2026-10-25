import io
import re
import html
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

st.set_page_config(page_title="AI Brand Identity Kit", page_icon="🎨", layout="wide")

PALETTES = {
    "Natural & eco-friendly": [("Sage Green", "#8BA888"), ("Forest Green", "#365743"), ("Warm Cream", "#F4F0E6"), ("Sand", "#C7A88A")],
    "Bold & energetic": [("Coral", "#FF6B5E"), ("Deep Navy", "#172A46"), ("Sunshine", "#FFD166"), ("Off White", "#FFF8F0")],
    "Minimal & premium": [("Charcoal", "#292929"), ("Ivory", "#F5F0E8"), ("Muted Gold", "#B79A63"), ("Stone", "#B7B1A7")],
    "Playful & youthful": [("Lavender", "#B9A7E8"), ("Peach", "#FFBFA3"), ("Berry", "#754668"), ("Cloud", "#FFF8FC")],
    "Tech & futuristic": [("Electric Blue", "#2563EB"), ("Midnight", "#101827"), ("Cyan", "#22D3EE"), ("Ice", "#EAF7FA")],
}
TAGLINES = {
    "skincare": ["Feel good in your own skin.", "Simple care. Everyday confidence.", "Your routine, naturally better."],
    "food": ["Good food, good mood.", "A little joy in every bite.", "Made to bring people together."],
    "fashion": ["Wear your own story.", "Everyday style, your way.", "Confidence in every detail."],
    "technology": ["Ideas into impact.", "Smarter tools for everyday life.", "Technology that moves with you."],
    "education": ["Learn today. Lead tomorrow.", "Small steps. Big possibilities.", "Make curiosity your superpower."],
    "fitness": ["Move at your pace.", "Stronger habits, brighter days.", "Progress looks different on everyone."],
    "default": ["Made for your kind of everyday.", "A fresh idea, made real.", "Thoughtfully made for you."],
}
DESCRIPTIONS = {
    "Natural & eco-friendly": "A thoughtful, calm identity inspired by nature, simplicity, and responsible choices.",
    "Bold & energetic": "A high-energy identity designed to feel confident, expressive, and memorable.",
    "Minimal & premium": "A refined identity built around clarity, restraint, and carefully chosen details.",
    "Playful & youthful": "A friendly, colorful identity that feels approachable, creative, and optimistic.",
    "Tech & futuristic": "A clean, modern identity that communicates innovation, precision, and forward thinking.",
}
FONT_PAIRS = {
    "Natural & eco-friendly": ("Poppins", "Lora"),
    "Bold & energetic": ("Montserrat ExtraBold", "Inter"),
    "Minimal & premium": ("Playfair Display", "Inter"),
    "Playful & youthful": ("Nunito", "Poppins"),
    "Tech & futuristic": ("Space Grotesk", "Inter"),
}
CATEGORY_INFO = {
    "Skincare": ("✿", "BEAUTY • CARE"),
    "Food & Beverage": ("✦", "FOOD • JOY"),
    "Fashion": ("◇", "STYLE • EXPRESSION"),
    "Technology / AI": ("✧", "IDEAS • INNOVATION"),
    "Education": ("✎", "LEARN • GROW"),
    "Fitness": ("⚡", "MOVE • PROGRESS"),
    "Other": ("✦", "MADE FOR YOU"),
}

def make_tagline(category, name):
    key = category.lower()
    if any(x in key for x in ["skin", "beauty", "cosmetic"]):
        key = "skincare"
    elif any(x in key for x in ["food", "beverage", "cafe", "bakery", "restaurant"]):
        key = "food"
    elif any(x in key for x in ["fashion", "clothing", "apparel"]):
        key = "fashion"
    elif any(x in key for x in ["tech", "software", "app", "ai"]):
        key = "technology"
    elif any(x in key for x in ["school", "education", "learning", "course"]):
        key = "education"
    elif any(x in key for x in ["fitness", "gym", "sport"]):
        key = "fitness"
    else:
        key = "default"
    options = TAGLINES[key]
    return options[sum(ord(ch) for ch in name) % len(options)]

def slug_initials(name):
    words = re.findall(r"[A-Za-z0-9]+", name)
    return "".join(word[0].upper() for word in words[:2]) or "B"

def create_pdf(data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="BrandTitle", parent=styles["Title"], fontSize=26, leading=30, textColor=colors.HexColor(data["palette"][1][1])))
    story = [
        Paragraph("BRAND IDENTITY KIT", styles["Heading2"]), Spacer(1, 10),
        Paragraph(html.escape(data["name"]), styles["BrandTitle"]),
        Paragraph(html.escape(data["tagline"]), styles["Heading2"]), Spacer(1, 12),
        Paragraph("Brand overview", styles["Heading2"]),
        Paragraph(html.escape(data["description"]), styles["BodyText"]), Spacer(1, 8),
        Paragraph("Brand details", styles["Heading2"]),
        Paragraph(f"Business category: {html.escape(data['category'])}<br/>Target audience: {html.escape(data['audience'])}<br/>Brand style: {html.escape(data['style'])}", styles["BodyText"]), Spacer(1, 12),
        Paragraph("Color palette", styles["Heading2"]),
    ]
    rows = [["Color", "Hex code", "Meaning"]]
    meanings = ["Primary brand color", "Supporting color", "Background / neutral", "Accent color"]
    for i, (label, hexcode) in enumerate(data["palette"]):
        rows.append([label, hexcode, meanings[i]])
    table = Table(rows, colWidths=[1.6 * inch, 1.2 * inch, 2.3 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9ECEF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#202124")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D0D0")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [
        table, Spacer(1, 12), Paragraph("Typography", styles["Heading2"]),
        Paragraph(f"Suggested heading font: {html.escape(data['fonts'][0])}<br/>Suggested body font: {html.escape(data['fonts'][1])}", styles["BodyText"]),
        Spacer(1, 12), Paragraph("Social media bio", styles["Heading2"]),
        Paragraph(html.escape(data["bio"]), styles["BodyText"]), Spacer(1, 14),
        Paragraph("Prototype note: This project uses rule-based templates to create a starter brand kit. It does not train a machine-learning model or verify trademarks.", styles["Italic"]),
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

st.title("🎨 AI Brand Identity Kit")
st.write("Create a polished starter brand identity for a fictional business.")
st.info("Student project prototype: this version uses rule-based templates. It does not train an AI model or verify trademarks.")

with st.sidebar:
    st.header("Create your brand")
    brand_name = st.text_input("Brand name", "LumiLeaf", max_chars=50)
    category = st.selectbox("Business category", ["Skincare", "Food & Beverage", "Fashion", "Technology / AI", "Education", "Fitness", "Other"])
    audience = st.text_input("Target audience", "Young adults who like simple, thoughtful products", max_chars=120)
    style = st.selectbox("Brand style", list(PALETTES.keys()))
    values = st.text_area("Brand values (optional)", "simple, thoughtful, trustworthy", max_chars=160)
    generate = st.button("✨ Generate Brand Kit", type="primary", use_container_width=True)

if "brand_data" not in st.session_state:
    st.session_state.brand_data = None

if generate:
    clean_name = brand_name.strip() or "New Brand"
    clean_audience = audience.strip() or "General audience"
    tagline = make_tagline(category, clean_name)
    symbol, descriptor = CATEGORY_INFO.get(category, ("✦", "MADE FOR YOU"))
    bio = f"{clean_name} | {category}. {tagline} Discover a brand made for {clean_audience.lower().rstrip('.')}."
    st.session_state.brand_data = {
        "name": clean_name, "category": category, "audience": clean_audience,
        "style": style, "values": values.strip() or "quality, creativity, trust",
        "palette": PALETTES[style], "tagline": tagline,
        "description": DESCRIPTIONS[style], "fonts": FONT_PAIRS[style],
        "initials": slug_initials(clean_name), "symbol": symbol,
        "descriptor": descriptor, "bio": bio,
    }

data = st.session_state.brand_data
if data is None:
    data = {
        "name": "LumiLeaf", "category": "Skincare", "audience": "Young adults",
        "style": "Natural & eco-friendly", "values": "simple, thoughtful, trustworthy",
        "palette": PALETTES["Natural & eco-friendly"], "tagline": "Feel good in your own skin.",
        "description": DESCRIPTIONS["Natural & eco-friendly"],
        "fonts": FONT_PAIRS["Natural & eco-friendly"], "initials": "LL",
        "symbol": CATEGORY_INFO["Skincare"][0], "descriptor": CATEGORY_INFO["Skincare"][1],
        "bio": "LumiLeaf | Skincare. Feel good in your own skin.",
    }

left, right = st.columns([1, 1.5], gap="large")
with left:
    st.markdown("### Brand logo concept")
    main = data["palette"][1][1]
    bg = data["palette"][2][1]
    initials = html.escape(data["initials"])
    safe_name = html.escape(data["name"])
    safe_category = html.escape(data["category"])
    safe_tagline = html.escape(data["tagline"])
    safe_symbol = html.escape(data["symbol"])
    safe_descriptor = html.escape(data["descriptor"])

    logo_html = f"""
    <div style="background:linear-gradient(145deg,{bg},#FFFFFF);
        border:1px solid #E3E5E8;border-radius:24px;padding:34px 18px;
        text-align:center;box-shadow:0 8px 24px rgba(0,0,0,.07);
        color:{main};">
      <div style="width:92px;height:92px;margin:0 auto 18px;
          border-radius:28px;background:{main};color:{bg};
          display:flex;align-items:center;justify-content:center;
          font-family:Georgia,serif;font-size:34px;font-weight:800;
          letter-spacing:2px;box-shadow:0 6px 16px rgba(0,0,0,.12);">
        {initials}
      </div>
      <div style="font-family:Georgia,serif;font-size:32px;font-weight:bold;
          letter-spacing:.4px;overflow-wrap:anywhere;">{safe_name}</div>
      <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:2.5px;
          text-transform:uppercase;margin-top:10px;">{safe_descriptor}</div>
      <div style="width:50px;height:2px;background:{main};margin:18px auto;border-radius:2px;"></div>
      <div style="font-size:26px;margin-bottom:8px;">{safe_symbol}</div>
      <div style="font-size:12px;letter-spacing:1.5px;text-transform:uppercase;">{safe_category}</div>
      <div style="font-family:Georgia,serif;font-style:italic;font-size:14px;
          line-height:1.6;max-width:320px;margin:12px auto 0;">{safe_tagline}</div>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
    st.caption("Logo concept preview. This is a template-based design, not a final vector logo or trademark check.")
    st.markdown("### Brand overview")
    st.write(data["description"])
    st.write("**Target audience:**", data["audience"])
    st.write("**Brand values:**", data["values"])

with right:
    st.markdown("### Color palette")
    cols = st.columns(4)
    for col, (label, hexcode) in zip(cols, data["palette"]):
        with col:
            st.markdown(f'<div style="height:72px;background:{hexcode};border-radius:10px;border:1px solid #ddd;"></div>', unsafe_allow_html=True)
            st.caption(label)
            st.code(hexcode, language=None)
    st.markdown("### Typography suggestions")
    st.write("**Heading:**", data["fonts"][0])
    st.write("**Body text:**", data["fonts"][1])
    st.markdown("### Brand tagline")
    st.success(data["tagline"])
    st.markdown("### Social media bio")
    st.write(data["bio"])

if st.session_state.brand_data:
    pdf = create_pdf(st.session_state.brand_data)
    safe_filename = re.sub(r"[^a-zA-Z0-9_-]+", "_", data["name"]).strip("_") or "brand"
    st.download_button("📄 Download Brand Kit as PDF", data=pdf, file_name=f"{safe_filename}_brand_kit.pdf", mime="application/pdf")

with st.expander("Project details for your presentation"):
    st.markdown("**Problem statement:** New businesses often need a consistent brand identity but may not have design experience or a large budget.\n\n**Objective:** Build an application that creates a starter brand identity kit from user-provided brand details.\n\n**Method:** Input collection → category/style matching → tagline selection → color palette and font suggestion → logo preview and PDF export.\n\n**Future enhancement:** Connect an AI API for more varied text and original logo image generation, then add trademark/domain checks.")
