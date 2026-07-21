"""
MTGT Lec03 Quiz — Feature Parity Matrices & Ideal Traction Metrics
Usage in Colab:
    import requests
    exec(requests.get("https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/quiz/lec03_mtgt.py").text)
"""

import gradio as gr
import gspread
from google.oauth2.service_account import Credentials
from google.colab import userdata
from datetime import datetime
import json, os

# ── CONFIG ───────────────────────────────────────────────────────────────────
COURSE_ID = "MTGT"
LEC_ID = "Lec03"
SHEET_NAME = "BANM_Class_Responses"

# ── QUESTIONS ──────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "q_id": "q1",
        "text": "From the Ideal Metrics Suite you (and your team) built in the group exercise: List your top 3 highest-leverage metrics (one from Access, one from Value, one from Evidence). For each metric, state: (a) Whether it is Cardinal or Inferred, (b) Why it belongs under that pillar, (c) Why it is high-leverage for Traction diagnosis."
    },
    {
        "q_id": "q2",
        "text": "Paste one actual prompt you used with an LLM while designing the Ideal Metrics Suite or while analyzing the Feature Parity Matrix / Colab tool. Briefly note: (a) What you were trying to achieve with that prompt, (b) Whether the LLM's response was useful, partially useful, or misleading — and why."
    },
    {
        "q_id": "q3",
        "text": "Using the Feature Parity Matrix in Caselet 1 (or the CSV in the Colab tool): Which competitor currently shows the highest estimated Traction Proxy under a pure PLG/Speed weighting scheme? Which competitor appears most vulnerable to DevSuite? Defend both answers with specific metrics and the role of Switching Friction."
    },
    {
        "q_id": "q4",
        "text": "If DevSuite could improve only one metric in the Feature Parity Matrix next quarter, which single metric would create the largest strategic benefit? Justify using both Traction impact and competitive vulnerability. Finally, rate your overall confidence in the Traction estimates (High / Medium / Low) and explain which data points (Cardinal vs Inferred) most affect that confidence."
    }
]

# ── GOOGLE SHEETS ───────────────────────────────────────────────────────────
def get_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    raw_creds = userdata.get('GOOGLE_CREDS_JSON')
    creds_dict = json.loads(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

def append_rows(rows):
    sheet = get_sheet()
    for row in rows:
        sheet.append_row(row)
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
                COURSE_ID,
                LEC_ID,
                q_id,
                email.strip().lower(),
                "TEXT",
                ans.strip(),
                "SUBMITTED",
                datetime.now().isoformat(),
                student_name.strip(),
                reg_id.strip() if reg_id else ""
            ])
            submitted += 1
        else:
            skipped += 1
    
    if submitted == 0:
        return "ERROR: No answers provided. Please answer at least one question."
    
    try:
        append_rows(rows)
        return f"✓ Submitted {submitted} answer(s) for {LEC_ID}. Skipped {skipped} empty."
    except Exception as e:
        return f"✗ Submit failed: {str(e)}"

# ── GRADIO UI ────────────────────────────────────────────────────────────────
with gr.Blocks(title=f"{COURSE_ID} {LEC_ID} Quiz") as demo:
    gr.Markdown(f"# {COURSE_ID} {LEC_ID}: Feature Parity Matrices & Ideal Traction Metrics")
    gr.Markdown("Answer in clear, concise paragraphs. Support every claim with specific reference to the Feature Parity Matrix, Ideal Metrics Suite, or the Colab tool. Where relevant, paste the exact prompt you used with an LLM.")
    
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
            lines=6
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
