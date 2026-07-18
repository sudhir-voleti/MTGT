#!/usr/bin/env python3
"""
MTGT Lec02 Quiz Submission - ipywidgets version
Upload to git, pull into Colab via !git clone or raw URL.
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import os, sys, json
from datetime import datetime

# ── CONFIG ───────────────────────────────────────────────────────────────────
# Change this to match your actual Google Sheet name
SHEET_NAME = "BANM_Class_responses"

# Path to service account credentials (in Colab, upload or mount from Drive)
CREDS_PATH = "/content/google_creds.json"  # Colab default
# Fallback for local testing
if not os.path.exists(CREDS_PATH):
    CREDS_PATH = "/Users/sudhirvoleti/teaching_trials/production/MTGT/assets/google_creds.json"

# ── LOAD RUBRICS ───────────────────────────────────────────────────────────
def load_rubrics():
    """Load rubrics from local SQLite or fallback to hardcoded."""
    try:
        sys.path.insert(0, '/Users/sudhirvoleti/teaching_trials/production/shared_core/tools')
        from global_utils import get_db_connection
        config = {
            "_runtime_path": "/Users/sudhirvoleti/teaching_trials/production/MTGT",
            "paths": {"db": "db/course_matrix.db"}
        }
        conn = get_db_connection(config)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT q_id, target_rubric, point_value, max_stars "
            "FROM assessment_rubrics WHERE lec_id = 'Lec02' ORDER BY q_id"
        )
        rubrics = {
            row[0]: {"rubric": row[1], "points": row[2], "stars": row[3]}
            for row in cursor.fetchall()
        }
        conn.close()
        return rubrics
    except Exception as e:
        print(f"DB load failed ({e}), using fallback rubrics")
        # Fallback if DB not accessible in Colab
        return {
            "q1": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant DevSuite variables for Value...", "points": 10.0, "stars": 5},
            "q2": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant DevSuite variables for Access...", "points": 10.0, "stars": 5},
            "q3": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant DevSuite variables for Evidence...", "points": 10.0, "stars": 5},
            "q4": {"rubric": "CHECKLIST: [1] Provides a complete V-A-E mapping...", "points": 5.0, "stars": 5},
            "q5": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant FinScale variables for Value...", "points": 10.0, "stars": 5},
            "q6": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant FinScale variables for Access...", "points": 10.0, "stars": 5},
            "q7": {"rubric": "CHECKLIST: [1] Identifies 2-3 relevant FinScale variables for Evidence...", "points": 10.0, "stars": 5},
            "q8": {"rubric": "CHECKLIST: [1] Provides a complete V-A-E mapping for all FinScale variables...", "points": 5.0, "stars": 5},
        }

# ── GOOGLE SHEETS WRITE ────────────────────────────────────────────────────
def append_to_sheet(row_data):
    """Append a row to the Google Sheet."""
    import gspread
    from google.oauth2.service_account import Credentials
    
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=scope)
    client = gspread.authorize(creds)
    
    spreadsheet = client.open(SHEET_NAME)
    worksheet = spreadsheet.sheet1
    worksheet.append_row(row_data)
    return True

# ── UI BUILDER ───────────────────────────────────────────────────────────────
def build_quiz_ui():
    """Build and display the ipywidgets quiz interface."""
    
    rubrics = load_rubrics()
    
    # ── Student info ──
    display(HTML("<h2>MTGT Lec02 Quiz Submission</h2>"))
    display(HTML("<hr>"))
    
    student_name = widgets.Text(
        description="Name:",
        placeholder="Your full name",
        layout=widgets.Layout(width='400px')
    )
    email = widgets.Text(
        description="Email:",
        placeholder="your.email@isb.edu",
        layout=widgets.Layout(width='400px')
    )
    reg_id = widgets.Text(
        description="Reg ID:",
        placeholder="Optional",
        layout=widgets.Layout(width='400px')
    )
    
    display(HTML("<h3>Student Information</h3>"))
    display(widgets.VBox([student_name, email, reg_id]))
    
    # ── Question selector ──
    q_options = [(f"{q.upper()} ({r['points']} pts)", q) for q, r in rubrics.items()]
    q_dropdown = widgets.Dropdown(
        options=q_options,
        description="Question:",
        style={'description_width': '100px'},
        layout=widgets.Layout(width='400px')
    )
    
    rubric_display = widgets.HTML(
        value="<i>Select a question to see rubric</i>",
        layout=widgets.Layout(width='100%', margin='10px 0')
    )
    
    response_input = widgets.Textarea(
        description="Answer:",
        placeholder="Type your response here...",
        layout=widgets.Layout(width='100%', height='150px'),
        style={'description_width': '100px'}
    )
    
    def on_question_change(change):
        q = change['new']
        if q in rubrics:
            r = rubrics[q]
            rubric_html = r['rubric'].replace('\n', '<br>')
            rubric_display.value = (
                f"<div style='background:#f5f5f5;padding:10px;border-radius:5px;'>"
                f"<b>{q.upper()}</b> — {r['points']} points, {r['stars']} stars max<br>"
                f"<div style='margin-top:8px;font-size:0.95em;'>{rubric_html}</div>"
                f"</div>"
            )
        else:
            rubric_display.value = "<i>Rubric not found</i>"
    
    q_dropdown.observe(on_question_change, names='value')
    on_question_change({'new': q_dropdown.value})  # Initialize
    
    display(HTML("<h3>Question Response</h3>"))
    display(q_dropdown)
    display(rubric_display)
    display(response_input)
    
    # ── Submit ──
    submit_btn = widgets.Button(
        description="Submit Response",
        button_style="success",
        layout=widgets.Layout(width='200px')
    )
    status = widgets.HTML(value="")
    output = widgets.Output()
    
    def on_submit(b):
        with output:
            clear_output()
            
            # Validate
            errors = []
            if not student_name.value.strip():
                errors.append("Name required")
            if not email.value.strip():
                errors.append("Email required")
            if "@" not in email.value:
                errors.append("Valid email required")
            if not response_input.value.strip():
                errors.append("Response required")
            
            if errors:
                status.value = (
                    f"<div style='color:red;padding:10px;background:#ffebee;border-radius:5px;'>"
                    f"✗ {'; '.join(errors)}</div>"
                )
                return
            
            q = q_dropdown.value
            lec_id = "Lec02"
            
            row = [
                datetime.now().isoformat(),
                student_name.value.strip(),
                email.value.strip().lower(),
                reg_id.value.strip(),
                lec_id,
                q,
                response_input.value.strip()
            ]
            
            try:
                append_to_sheet(row)
                status.value = (
                    f"<div style='color:green;padding:10px;background:#e8f5e9;border-radius:5px;'>"
                    f"✓ {lec_id}_{q} submitted successfully!</div>"
                )
                response_input.value = ""  # Clear for next
                
            except Exception as e:
                status.value = (
                    f"<div style='color:red;padding:10px;background:#ffebee;border-radius:5px;'>"
                    f"✗ Submit failed: {str(e)}</div>"
                )
                print(f"Full error: {e}")
    
    submit_btn.on_click(on_submit)
    
    display(HTML("<hr>"))
    display(submit_btn)
    display(status)
    display(output)
    
    display(HTML(
        "<div style='margin-top:20px;padding:10px;background:#e3f2fd;border-radius:5px;'>"
        "<b>Instructions:</b> Fill info → Select question → Read rubric → Type answer → Submit. "
        "Repeat for each question. Responses save to <code>{}</code>."
        "</div>".format(SHEET_NAME)
    ))

# ── ENTRY POINT ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    build_quiz_ui()
