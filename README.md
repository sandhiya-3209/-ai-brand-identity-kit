# AI Brand Identity Kit

A beginner-friendly Python + Streamlit project that creates a starter identity kit for a fictional brand.

## Features
- User inputs: brand name, category, target audience, style, and values
- Automated tagline, brand description, color palette, font suggestions, and social bio
- Logo concept preview using brand initials
- PDF download
- Responsive web interface

## Important project scope note
This version is a rule-based prototype, not a trained machine-learning model and not a live LLM integration. In a presentation, describe it as an **AI-assisted brand identity generator prototype** and explain that its generation logic uses predefined rules and templates. A future version can integrate a language-model API and an image-generation service.

## Run on Windows
1. Install Python 3.10 or newer from https://www.python.org/downloads/ and select **Add Python to PATH** during installation.
2. Extract this folder to a convenient location.
3. Open Command Prompt in this folder.
4. Run:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
5. Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Suggested demo
Use brand name `LumiLeaf`, category `Skincare`, target audience `Young adults`, and style `Natural & eco-friendly`. Then generate the kit and download the PDF.

## Limitations
- Taglines and descriptions come from templates and rules.
- The logo preview is a simple initials-based concept, not an original logo image.
- Font names are suggestions; fonts are not bundled with the app.
- Trademark and domain availability are not checked.
