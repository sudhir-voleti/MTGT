"""
MTGT Lec03 Factor Analysis Quiz — Gradio "Submit All" (Revised 5 Questions)
Usage in Colab:
    import requests
    exec(requests.get("https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/quiz/lec03_banm.py").text)
"""

import gradio as gr
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

# ── CONFIG ───────────────────────────────────────────────────────────────────
SHEET_NAME = "BANM_Class_responses"
# With this block:
def get_creds_path():
    """Find google_creds.json from file or Colab secrets."""
    # Check file first
    if os.path.exists("/content/google_creds.json"):
        return "/content/google_creds.json"
    
    # Try Colab secrets
    try:
        from google.colab import userdata
        import tempfile
        creds_json = userdata.get('GOOGLE_CREDS')
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(creds_json)
            return f.name
    except:
        pass
    
    return None

CREDS_PATH = get_creds_path()
if not CREDS_PATH:
    raise FileNotFoundError("google_creds.json not found. Upload to /content/ or set GOOGLE_CREDS in Colab secrets.")

LEC_ID = "Lec03"

# ── QUESTIONS ONLY (no rubrics) ────────────────────────────────────────────
QUESTIONS = [
    {
        "q_id": "q1",
        "text": "In a customer survey for a streaming platform, the following variables load highly on the same factor: binge_watching_hours, content_discovery_time, subscription_upgrade_likelihood, and skip_intro_rate (negative loading). What would you name this factor? Briefly justify your label."
    },
    {
        "q_id": "q2",
        "text": "An insurance company runs Factor Analysis on policyholder data. Three variables load strongly on Factor 1: claim_frequency (positive), premium_sensitivity (positive), and loyalty_tenure (negative). What latent construct is this factor most likely capturing? How might the company use this factor in its marketing or underwriting strategy?"
    },
    {
        "q_id": "q3",
        "text": "In an e-commerce dataset, Factor 2 is defined by high loadings on: cart_abandonment_rate, price_comparison_clicks, coupon_usage_frequency, and return_rate. Give this factor a clear managerial name and explain what kind of customer behavior it represents."
    },
    {
        "q_id": "q4",
        "text": "A bank analyzes customer digital banking data and finds two clean factors: Factor A: high on mobile_app_logins, upi_transactions, instant_loan_uptake; Factor B: high on branch_visits, cheque_usage, fixed_deposit_preference. Interpret both factors. What strategic recommendation would you give the bank based on these two factors?"
    },
    {
        "q_id": "q5",
        "text": "Why is Factor Analysis particularly useful when a firm has 30–50 survey items or operational KPIs? Give one concrete marketing or managerial benefit of reducing them to 4–6 factors."
    }
]

# ── GOOGLE SHEETS ───────────────────────────────────────────────────────────
def append_to_sheet(rows):
    scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(SHEET_NAME)
    worksheet = spreadsheet.sheet1
    for row in rows:
        worksheet.append_row(row)
    return True

# ── SUBMIT HANDLER ──────────────────────────────────────────────────────────
def submit_all(student_name, email, reg_id, *answers):
    if not student_name or not email:
        return "ERROR: Name and Email are required."
    
    if "@" not in email:
        return "ERROR: Valid email required."
    
    rows = []
    submitted = 0
    skipped = 0
    
    for i, ans in enumerate(answers):
        q_id = QUESTIONS[i]["q_id"]
        if ans and ans.strip():
            rows.append([
                datetime.now().isoformat(),
                student_name.strip(),
                email.strip().lower(),
                reg_id.strip() if reg_id else "",
                LEC_ID,
                q_id,
                ans.strip()
            ])
            submitted += 1
        else:
            skipped += 1
    
    if submitted == 0:
        return "ERROR: No answers provided. Please answer at least one question."
    
    try:
        append_to_sheet(rows)
        return f"✓ Submitted {submitted} answer(s) for {LEC_ID}. Skipped {skipped} empty."
    except Exception as e:
        return f"✗ Submit failed: {str(e)}"

# ── GRADIO UI ────────────────────────────────────────────────────────────────
with gr.Blocks(title=f"MTGT {LEC_ID} Quiz") as demo:
    gr.Markdown(f"# MTGT {LEC_ID}: Factor Analysis In-Class Quiz")
    gr.Markdown("Answer in 2–4 short sentences. Be precise. Justify where asked. Submit all at once.")
    
    with gr.Row():
        student_name = gr.Textbox(label="Full Name", placeholder="Your name")
        email = gr.Textbox(label="Email", placeholder="your.email@isb.edu")
        reg_id = gr.Textbox(label="Reg ID (optional)", placeholder="")
    
    gr.Markdown("---")
    
    answer_inputs = []
    for q in QUESTIONS:
        gr.Markdown(f"### {q['q_id'].upper()}")
        gr.Markdown(q['text'])
        
        ans = gr.Textbox(
            label="Your answer",
            placeholder="Type your response here...",
            lines=4
        )
        answer_inputs.append(ans)
        
        gr.Markdown("---")
    
    submit_btn = gr.Button("Submit All Answers", variant="primary", size="lg")
    status = gr.Markdown(value="")
    
    submit_btn.click(
        submit_all,
        inputs=[student_name, email, reg_id] + answer_inputs,
        outputs=status
    )
    
    gr.Markdown("*Only non-empty answers are submitted. Answer any subset of questions.*")

demo.launch(share=True, debug=True)
