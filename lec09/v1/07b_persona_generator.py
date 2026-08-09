# -*- coding: utf-8 -*-
"""
Lec09 — Step 7b: Persona Document Generator for NotebookLM
Generates 8-10 rich persona markdown files from respondent data.
Pure code cell. Run AFTER 07a_nlm_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/07b_persona_generator.py').text)
"""

import pandas as pd
import numpy as np
from IPython.display import display, clear_output
import ipywidgets as widgets

_state = {'ib_df': None}

# =============================================================================
# 1. Retrieve ib_df
# =============================================================================

if 'ib_df' in globals():
    _state['ib_df'] = globals()['ib_df']
    print("✓ Using ib_df from Step 3")
    proceed = True
else:
    print("⚠ ib_df not found. Please upload your individual part-worths CSV below:")
    proceed = False

    upload_widget = widgets.FileUpload(accept='.csv', multiple=False, description='Upload Part-Worths CSV')
    def on_upload(change):
        if not upload_widget.value:
            return
        file_info = list(upload_widget.value.values())[0]
        with open('/tmp/ib.csv', 'wb') as f:
            f.write(file_info['content'])
        ib_df = pd.read_csv('/tmp/ib.csv')
        _state['ib_df'] = ib_df
        globals()['ib_df'] = ib_df
        clear_output(wait=True)
        print(f"✓ Loaded {len(ib_df)} respondent part-worth profiles")
        show_generator()
    upload_widget.observe(on_upload, names='value')
    display(upload_widget)

# =============================================================================
# 2. Persona narrative templates
# =============================================================================

PERSONA_TEMPLATES = {
    'Tech': {
        'names': ['Arjun', 'Rohan', 'Kiran', 'Vikram', 'Neel'],
        'cities': ['Bangalore', 'Hyderabad', 'Pune'],
        'jobs': ['software engineer', 'product manager', 'data scientist', 'UX designer'],
        'incomes': ['₹18–25 lakh', '₹20–30 lakh', '₹15–22 lakh'],
        'ages': [28, 32, 26, 30, 29],
        'quotes': [
            "I research everything for three weeks before I buy.",
            "My friends come to me for tech advice.",
            "I don't mind paying more if the product is genuinely better.",
            "I hate it when companies treat me like I don't understand specs.",
            "The app ecosystem matters more than the hardware."
        ],
        'fears': [
            "The company will shut down and my scooter will become unrepairable.",
            "The smart features will be buggy and I'll be the beta tester.",
            "The range will drop 40% in two years like my friend's EV."
        ],
        'pride': [
            "Being the first in my circle to own an EV.",
            "My scooter's app integration with my smart home.",
            "The OTA updates that keep adding features."
        ]
    },
    'Pragmatist': {
        'names': ['Suresh', 'Meera', 'Rajesh', 'Anita', 'Deepak'],
        'cities': ['Jaipur', 'Indore', 'Kochi', 'Chennai', 'Coimbatore'],
        'jobs': ['bank manager', 'school principal', 'small business owner', 'government officer', 'pharmacist'],
        'incomes': ['₹12–18 lakh', '₹10–16 lakh', '₹14–20 lakh'],
        'ages': [42, 38, 45, 35, 40],
        'quotes': [
            "I don't need fancy features. I need it to work every single day.",
            "My Honda Activa has run for 12 years with zero issues. That's my benchmark.",
            "I will pay more for peace of mind. Cheap is expensive if it breaks.",
            "I need to know I can get it serviced in my city, not just Bangalore.",
            "My family uses this scooter. It has to be safe and reliable."
        ],
        'fears': [
            "The service center is 200km away and I can't get spare parts.",
            "The battery dies in year 3 and costs ₹60,000 to replace.",
            "The company is a startup and might not exist in 5 years."
        ],
        'pride': [
            "My family's safety and comfort.",
            "The resale value when I upgrade in 7 years.",
            "My neighbor asking me for advice because I chose wisely."
        ]
    },
    'PriceHunter': {
        'names': ['Ravi', 'Priya', 'Amit', 'Sunita', 'Karthik'],
        'cities': ['Lucknow', 'Patna', 'Bhopal', 'Nagpur', 'Visakhapatnam'],
        'jobs': ['delivery executive', 'call center supervisor', 'retail store manager', 'freelance accountant', 'tutor'],
        'incomes': ['₹6–10 lakh', '₹5–9 lakh', '₹7–11 lakh'],
        'ages': [24, 27, 31, 26, 29],
        'quotes': [
            "₹1,40,000 for a scooter? That's a down payment on a small car.",
            "I compare prices on three apps before I buy groceries. You think I won't for a scooter?",
            "I don't care about apps. I care about EMI.",
            "If the government subsidy doesn't apply, I'm not buying.",
            "My current petrol scooter costs ₹2,500/month. Show me the savings."
        ],
        'fears': [
            "The EMI will strain my monthly budget.",
            "The electricity bill will be higher than petrol costs.",
            "I'll be stuck with a product I can't resell if I need cash."
        ],
        'pride': [
            "Getting the best deal in my entire family.",
            "My spreadsheet that proves the total cost of ownership.",
            "The cashback and discounts I stacked."
        ]
    }
}

# =============================================================================
# 3. Generator UI
# =============================================================================

def show_generator():
    ib_df = _state['ib_df']

    clear_output(wait=True)
    print("="*60)
    print("PERSONA DOCUMENT GENERATOR")
    print("="*60)
    print("\nThis will generate 8–10 rich persona markdown documents")
    print("from your respondent data, ready to upload to NotebookLM.")
    print()

    n_personas = widgets.IntSlider(
        value=8, min=3, max=15, step=1,
        description='Personas:', layout=widgets.Layout(width='300px')
    )
    display(n_personas)

    print("\n📋 What will happen when you click 'Generate Personas':")
    print("   • Sample respondents from each segment")
    print("   • Wrap their part-worths in a narrative (demographics, quotes, fears)")
    print("   • Export as markdown files you can download and upload to NotebookLM")
    print("   • Estimated runtime: ~2 seconds")
    print()

    gen_btn = widgets.Button(
        description="▶ Generate Personas",
        button_style='primary',
        layout=widgets.Layout(width='200px', height='40px')
    )
    gen_btn.on_click(lambda b: generate_personas(n_personas.value))
    display(gen_btn)

# =============================================================================
# 4. Generate personas
# =============================================================================

def generate_personas(n):
    ib_df = _state['ib_df']

    clear_output(wait=True)
    print("="*60)
    print("GENERATED PERSONAS")
    print("="*60)

    personas = []

    if 'Segment' in ib_df.columns:
        segments = sorted(ib_df['Segment'].unique())
    else:
        segments = ['All']

    # Distribute personas across segments
    seg_counts = {}
    for i in range(n):
        seg = segments[i % len(segments)]
        seg_counts[seg] = seg_counts.get(seg, 0) + 1

    persona_idx = 0
    for seg in segments:
        seg_data = ib_df[ib_df['Segment'] == seg] if seg != 'All' else ib_df
        if len(seg_data) == 0:
            continue

        # Sample respondents for this segment
        n_seg = seg_counts.get(seg, 1)
        sampled = seg_data.sample(n=min(n_seg, len(seg_data)), random_state=42 + persona_idx)

        template = PERSONA_TEMPLATES.get(seg, PERSONA_TEMPLATES['Pragmatist'])

        for _, resp in sampled.iterrows():
            name = template['names'][persona_idx % len(template['names'])]
            city = template['cities'][persona_idx % len(template['cities'])]
            job = template['jobs'][persona_idx % len(template['jobs'])]
            income = template['incomes'][persona_idx % len(template['incomes'])]
            age = template['ages'][persona_idx % len(template['ages'])]
            quote = template['quotes'][persona_idx % len(template['quotes'])]
            fear = template['fears'][persona_idx % len(template['fears'])]
            pride = template['pride'][persona_idx % len(template['pride'])]

            # Extract part-worths as narrative
            pw_narrative = []
            for col in ib_df.columns:
                if col.startswith('d_') and pd.notna(resp.get(col)):
                    val = resp[col]
                    parts = col.split('_', 2)
                    if len(parts) >= 3:
                        attr = parts[1]
                        level = parts[2]
                        if val > 0.5:
                            pw_narrative.append(f"strongly prefers {level} {attr}")
                        elif val > 0:
                            pw_narrative.append(f"likes {level} {attr}")
                        elif val < -0.5:
                            pw_narrative.append(f"strongly dislikes {level} {attr}")
                        elif val < 0:
                            pw_narrative.append(f"dislikes {level} {attr}")

            # Build markdown
            md = f"""# Persona: {name} ({seg})

## Who I Am
- **Name:** {name}
- **Age:** {age}
- **City:** {city}
- **Occupation:** {job}
- **Household Income:** {income} per year
- **Family:** Married with one child, parents visit frequently
- **Current Vehicle:** Honda Activa (8 years old), considering replacement

## What Drives Me
> "{quote}"

## My Preferences (from conjoint data)
"""
            if pw_narrative:
                md += "\n".join([f"- {item}" for item in pw_narrative[:8]])
            else:
                md += "- Balanced preferences across attributes"

            md += f"""

## What I Fear
> "{fear}"

## What I'm Proud Of
> "{pride}"

## My Decision Process
1. I hear about a product from a friend or YouTube review.
2. I check the price first. If it's too high, I stop.
3. I look for service centers in my city.
4. I ask my spouse. If they say no, I don't buy.
5. I test-ride if possible. The feel of the scooter matters.

## How to Convince Me
- **Do:** Show me total cost of ownership over 5 years.
- **Do:** Give me a test-ride near my home.
- **Do:** Show me real customer reviews from my city.
- **Don't:** Use jargon I don't understand.
- **Don't:** Assume I care about features I didn't ask for.

## My Part-Worth Profile (Raw)
"""
            for col in ib_df.columns:
                if col.startswith('d_') and pd.notna(resp.get(col)):
                    md += f"- {col}: {resp[col]:.2f}\n"

            personas.append({
                'name': name,
                'segment': seg,
                'markdown': md,
                'resp_id': resp.get('RespID', 'unknown')
            })

            persona_idx += 1

    # Display preview
    print(f"✓ Generated {len(personas)} persona documents")
    print("\n--- Preview of first persona ---")
    print(personas[0]['markdown'][:1500])
    print("\n... [truncated] ...")

    # Store for download
    _state['personas'] = personas
    globals()['personas'] = personas

    # Download buttons
    print("\n" + "="*60)
    print("DOWNLOAD PERSONAS")
    print("="*60)

    for i, p in enumerate(personas):
        filename = f"persona_{i+1:02d}_{p['name'].lower()}_{p['segment'].lower()}.md"
        # Save to output for download
        with open(f'/tmp/{filename}', 'w', encoding='utf-8') as f:
            f.write(p['markdown'])
        print(f"   {filename}  ({len(p['markdown'])} chars)")

    print("\n📥 All files saved to /tmp/. Use the file browser to download them,")
    print("   or upload directly to NotebookLM.")

    # Scribble pause
    html_content = """
    <style>
      .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                      font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
      .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                         padding-bottom: 4px; margin-top: 28px; }
      .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; 
                                 padding: 16px 18px; margin: 22px 0; }
      .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
      .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                                border: 1px solid #cbd5e1; border-radius: 6px; 
                                font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
      .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                          font-size: 13.5px; padding: 9px 12px; text-align: left; }
      .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
    </style>
    <div class="caselet-body">
      <div class="pause-box">
        <h3>Pause and Reflect: Choose Your Persona</h3>
        <p>Your instructor will assign you one persona. Before you receive it, write which segment you HOPE to get and why.</p>
        <table class="scribble-table">
          <thead><tr><th>My Preferred Segment</th><th>Why This Segment?</th><th>One Question I Will Ask</th></tr></thead>
          <tbody>
            <tr>
              <td><textarea placeholder="e.g., Pragmatist..."></textarea></td>
              <td><textarea placeholder="Because I think they are the biggest market..."></textarea></td>
              <td><textarea placeholder="e.g., 'What would make you leave Honda?'..."></textarea></td>
            </tr>
          </tbody>
        </table>
        <p style="margin-top:12px;"><strong>Next:</strong> Upload your assigned persona to NotebookLM and begin the interview.</p>
      </div>
    </div>
    """
    display(HTML(html_content))

if proceed:
    show_generator()
