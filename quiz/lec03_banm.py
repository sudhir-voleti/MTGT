"""
MTGT Lec03 Factor Analysis Quiz — Gradio "Submit All"
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
CREDS_PATH = "/content/google_creds.json"

LEC_ID = "Lec03"

# ── QUESTIONS ONLY (no rubrics) ────────────────────────────────────────────
QUESTIONS = [
    {
        "q_id": "q1",
        "text": "In the image reconstruction example (the smiling face), what happens to the quality of the reconstructed image as we increase the number of factors from 1 → 5 → 10 → 25? What does this illustrate about the relationship between number of factors and information retained?"
    },
    {
        "q_id": "q2",
        "text": "A factor is created by re-weighting a group of correlated variables. In the toothpaste example, three variables loaded highly on Factor 1 and three on Factor 2. What descriptive names would you give Factor 1 and Factor 2? Briefly justify your labels using the loading variables."
    },
    {
        "q_id": "q3",
        "text": "In the toothpaste factor solution, Factor Scores are scaled as standard normal (mean ≈ 0, SD ≈ 1). If a particular respondent has a high positive score on the 'Health Benefits' factor and a high negative score on the 'Cosmetic Benefits' factor, how would you describe this person's toothpaste preference? What kind of product positioning might appeal to them?"
    },
    {
        "q_id": "q4",
        "text": "In the mtcars example, the factor solution typically produces two clear factors (one related to power/performance and one related to economy/efficiency). Looking at the factor plot of cars, what does it mean if a car sits in the 'High Power + Low Economy' quadrant? Give one real-world managerial implication of this positioning."
    },
    {
        "q_id": "q5",
        "text": "Suppose you run Factor Analysis on a new dataset and the main variables loading highly on Factor 1 are: crypto_investment_ratio, trading_freq, risk_aversion (negative loading). What would you name Factor 1? Briefly justify and suggest one way a wealth management firm could use this factor."
    },
    {
        "q_id": "q6",
        "text": "In the manufacturing plant data, Factor 1 loads heavily on energy_consumption, material_waste, and carbon_emission_level. What would you name this factor? A plant scores very high on this factor but also high on 'Production & Quality'. What does this combination tell you about their current strategy, and what is your top recommendation?"
    },
    {
        "q_id": "q7",
        "text": "Factor Analysis reduces many variables into a smaller set of latent factors. Why is this useful for marketing managers? Give two concrete examples of how the resulting factors (or factor scores) can be used downstream (e.g., for segmentation, targeting, product design, or communication)."
    }
]

# ── GOOGLE SHEETS ───────────────────────────────────────────────────────────
def append_to_sheet(rows):
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
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
