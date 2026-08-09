# -*- coding: utf-8 -*-
"""
Lec09 — Step 7c: Campaign Builder + NLM Feedback Capture
Interactive template for marketing campaign brief + persona rating form.
Pure code cell. Run AFTER 07a_nlm_theory.py in a separate Colab cell.
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/07c_campaign_builder.py').text)
"""

from IPython.display import HTML, display
import ipywidgets as widgets

# =============================================================================
# 1. Campaign Brief Template
# =============================================================================

display(HTML("""
<style>
  .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                  font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
  .caselet-body h1 { font-size: 1.55em; color: #003366; margin: 0 0 6px 0; }
  .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                     padding-bottom: 4px; margin-top: 28px; }
  .caselet-body h3 { font-size: 1.05em; color: #003366; margin-top: 20px; }
  .caselet-body p { margin: 10px 0; }
  .caselet-body .callout { background: #f0f7ff; border-left: 5px solid #003366; padding: 14px 18px; margin: 18px 0; }
  .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; padding: 16px 18px; margin: 22px 0; }
  .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
  .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                            border: 1px solid #cbd5e1; border-radius: 6px; 
                            font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
  .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                      font-size: 13.5px; padding: 9px 12px; text-align: left; }
  .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
  .caselet-body .section { background: #f8fafc; border: 1px solid #d0d7de; padding: 14px 18px; margin: 14px 0; border-radius: 6px; }
  .caselet-body .section h4 { margin: 0 0 8px 0; color: #003366; font-size: 1.05em; }
</style>

<div class="caselet-body">

  <h1>Campaign Builder: From Persona Insight to Marketing Action</h1>

  <h2>1. The Campaign Brief Template</h2>
  <p>Fill in each section below. Be specific. One sentence per field. If you need more than one sentence, you do not have clarity.</p>

  <div class="section">
    <h4>Target Persona</h4>
    <p>Name, segment, and the ONE thing they care about most:</p>
    <textarea placeholder="e.g., Suresh (Pragmatist, 42, Jaipur). He cares about service network above all else because his family depends on the scooter." style="min-height: 60px;"></textarea>
  </div>

  <div class="section">
    <h4>Key Insight from Interview</h4>
    <p>The ONE surprising thing the persona said that changed your strategy:</p>
    <textarea placeholder="e.g., Suresh said he doesn't trust any EV brand except Honda because his uncle's battery died. This means we need Honda-level warranty, not Honda-level features." style="min-height: 60px;"></textarea>
  </div>

  <div class="section">
    <h4>Single Message (25 words max)</h4>
    <p>If the persona remembers only one thing from your ad, what should it be?</p>
    <textarea placeholder="e.g., 'Yana — 300+ service cities, 6-year warranty, or we fix it free.'" style="min-height: 40px;"></textarea>
  </div>

  <div class="section">
    <h4>Slogan / Headline</h4>
    <p>The 3–7 words that appear on the billboard or Instagram ad:</p>
    <textarea placeholder="e.g., 'Peace of Mind, Every Kilometer.'" style="min-height: 40px;"></textarea>
  </div>

  <div class="section">
    <h4>Channel</h4>
    <p>Where does this persona actually see ads? Be specific:</p>
    <textarea placeholder="e.g., WhatsApp forwards from family groups, local newspaper, YouTube pre-roll in Hindi, dealership walk-ins." style="min-height: 40px;"></textarea>
  </div>

  <div class="section">
    <h4>Creative Concept</h4>
    <p>Describe the visual or video in one sentence:</p>
    <textarea placeholder="e.g., A father dropping his daughter at school on a Yana, voiceover: 'Six years, zero worry.'" style="min-height: 60px;"></textarea>
  </div>

  <div class="section">
    <h4>Call to Action (CTA)</h4>
    <p>What do you want them to do immediately after seeing the ad?</p>
    <textarea placeholder="e.g., 'Book a test ride at your nearest Yana center — free helmet included.'" style="min-height: 40px;"></textarea>
  </div>

  <div class="section">
    <h4>Offer / Incentive</h4>
    <p>What sweetener removes the final friction?</p>
    <textarea placeholder="e.g., 'Zero down payment EMI + 1-year free service + 30-day money-back guarantee.'" style="min-height: 40px;"></textarea>
  </div>

  <h2>2. NLM Query Guide</h2>
  <p>When you upload this brief to NotebookLM, ask the persona these questions. Record their answers verbatim.</p>

  <div class="callout">
    <p><strong>Suggested questions to ask your persona in NotebookLM:</strong></p>
    <ol>
      <li>"I am showing you an ad for Yana. Based on what you know about me, would this ad convince me to book a test ride? Why or why not?"</li>
      <li>"Rate this slogan 1–5: [your slogan]. Explain your rating."</li>
      <li>"What is the weakest part of this campaign? What would make it stronger?"</li>
      <li>"If you were my marketing consultant, what ONE change would you make?"</li>
      <li>"Rate the offer 1–5. Would you actually use it, or is it just marketing fluff?"</li>
      <li>"Which competitor's ad would beat this one, and why?"</li>
    </ol>
  </div>

  <h2>3. Persona Rating Capture</h2>
  <p>After your NLM interview, paste the persona's ratings and explanations below. This is your evidence for revision.</p>

  <table class="scribble-table">
    <thead>
      <tr><th>Campaign Element</th><th>Persona Rating (1–5)</th><th>Persona's Explanation</th><th>My Revision</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Slogan / Headline</td>
        <td><textarea placeholder="3" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="'Too generic. Every brand says peace of mind.'" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="Change to: '300 Cities. 6 Years. Zero Worry.'" style="min-height: 30px;"></textarea></td>
      </tr>
      <tr>
        <td>Single Message</td>
        <td><textarea placeholder="4" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
      </tr>
      <tr>
        <td>Creative Concept</td>
        <td><textarea placeholder="2" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
      </tr>
      <tr>
        <td>Offer / Incentive</td>
        <td><textarea placeholder="5" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
      </tr>
      <tr>
        <td>Overall Campaign</td>
        <td><textarea placeholder="3" style="min-height: 30px;"></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
        <td><textarea placeholder="..."></textarea></td>
      </tr>
    </tbody>
  </table>

  <div class="pause-box">
    <h3>Final Reflection: The Surprise</h3>
    <p>What is the ONE thing your persona said that the conjoint data did NOT predict? This is your real learning.</p>
    <textarea placeholder="e.g., Suresh said he doesn't care about warranty length — he cares about whether the service center is within 5km of his home. The conjoint said warranty was important, but proximity was the real driver." style="min-height: 80px;"></textarea>
  </div>

</div>
"""))
