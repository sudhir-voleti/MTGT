# -*- coding: utf-8 -*-
"""
Lec09 — Step 7a Theory: Persona-Based Marketing with NotebookLM
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/07a_nlm_theory.py').text)
"""

from IPython.display import HTML, display

display(HTML("""
<style>
  .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                  font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
  .caselet-body h1 { font-size: 1.55em; color: #003366; margin: 0 0 6px 0; }
  .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                     padding-bottom: 4px; margin-top: 28px; }
  .caselet-body h3 { font-size: 1.05em; color: #003366; margin-top: 20px; }
  .caselet-body p { margin: 10px 0; }
  .caselet-body ul, .caselet-body ol { margin: 8px 0 12px 22px; }
  .caselet-body li { margin: 4px 0; }
  .caselet-body .callout { background: #f0f7ff; border-left: 5px solid #003366; padding: 14px 18px; margin: 18px 0; }
  .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; padding: 16px 18px; margin: 22px 0; }
  .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
  .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                            border: 1px solid #cbd5e1; border-radius: 6px; 
                            font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
  .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                      font-size: 13.5px; padding: 9px 12px; text-align: left; }
  .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
  .caselet-body .step { background: #f8fafc; border: 1px solid #d0d7de; padding: 12px 16px; margin: 10px 0; border-radius: 6px; }
  .caselet-body .step strong { color: #003366; }
</style>

<div class="caselet-body">

  <h1>Persona-Based Marketing: Talking to a Real Buyer</h1>

  <h2>1. Why Personas Matter</h2>
  <p>You have estimated part-worths, run cluster analyses, and simulated market shares. But numbers do not buy scooters. <strong>People</strong> buy scooters. And people have jobs, anxieties, families, and pride.</p>

  <p>A <strong>persona</strong> is a fictional but data-grounded representation of a buyer type. It is not a demographic label. It is a living profile: what they value, what they fear, what language they use, what they tell their friends about their purchase.</p>

  <div class="callout">
    <p><strong>The test of a good persona:</strong> If you read it aloud and someone says "I know exactly who that is," you have succeeded. If they say "That sounds like a market segment," you have failed.</p>
  </div>

  <h2>2. How NotebookLM Enables Persona Play</h2>
  <p>NotebookLM is an AI research assistant that can adopt the voice and perspective of a source document. When you upload a persona document — a rich narrative of who this buyer is, what they value, and how they speak — NotebookLM becomes that person.</p>

  <p>You can then <strong>interview</strong> the persona:</p>
  <ul>
    <li>"Would you buy a Yana scooter with 110km range and a ₹1.1L price tag?"</li>
    <li>"What would make you switch from Honda to Yana?"</li>
    <li>"What is the one thing an ad would have to say to convince you?"</li>
    <li>"Rate this slogan: 'Yana — The Smart Move.' Why that score?"</li>
  </ul>

  <p>The persona responds not with abstract preferences, but with <em>embodied reasoning</em>: "I don't trust new brands because my uncle's EV battery died in 18 months and the company vanished." This is the kind of insight no conjoint coefficient can give you.</p>

  <h2>3. The Assignment</h2>

  <div class="step">
    <strong>Step 1: Receive Your Persona</strong>
    <p>Your instructor will assign you one of 8–10 pre-built personas. Each persona is a detailed narrative built from a real respondent's part-worth profile plus assumed demographics. Read it carefully. Do not just skim the numbers — absorb the story.</p>
  </div>

  <div class="step">
    <strong>Step 2: Upload to NotebookLM</strong>
    <p>Create a new NotebookLM notebook. Upload your persona document as the sole source. In the "Customize" settings, add this system prompt: <em>"You are the person described in this document. Respond to all questions from that person's perspective, using their values, vocabulary, and concerns. Be specific and concrete."</em></p>
  </div>

  <div class="step">
    <strong>Step 3: Interview the Persona</strong>
    <p>Ask at least 5 questions. Mix product questions ("Would you buy X?") with marketing questions ("What ad would convince you?"). Record the answers. Look for surprises — where did the persona disagree with the cluster average?</p>
  </div>

  <div class="step">
    <strong>Step 4: Design a Marketing Campaign</strong>
    <p>Based on the interview, design a one-page campaign brief: target persona, single message, channel, creative concept, and call-to-action. Keep it tight — one sentence per element.</p>
  </div>

  <div class="step">
    <strong>Step 5: Test with the Persona</strong>
    <p>Upload your campaign brief to the same NotebookLM notebook. Ask the persona to rate each element (slogan, visual description, offer) on a 1–5 scale and explain why. Revise based on feedback. Iterate until you get at least one 5/5.</p>
  </div>

  <h2>4. What You Will Submit</h2>
  <p>A single document containing:</p>
  <ol>
    <li>The persona summary (name, demographics, key values).</li>
    <li>Your 5+ interview questions and the persona's answers.</li>
    <li>The final campaign brief (one page).</li>
    <li>The persona's ratings of your campaign elements + your revisions.</li>
    <li>One insight that surprised you — something the persona said that the conjoint data did not predict.</li>
  </ol>

  <div class="pause-box">
    <h3>Before You Begin: Plan Your Interview</h3>
    <p>Write 3 questions you will ask your persona before you even open NotebookLM. Good questions are specific and personal, not generic.</p>
    <table class="scribble-table">
      <thead><tr><th>#</th><th>My Question</th><th>What I hope to learn</th></tr></thead>
      <tbody>
        <tr><td>1</td><td><textarea placeholder="e.g., 'You rated smart features very high. What exactly do you use them for?'..."></textarea></td><td><textarea placeholder="..."></textarea></td></tr>
        <tr><td>2</td><td><textarea placeholder="..."></textarea></td><td><textarea placeholder="..."></textarea></td></tr>
        <tr><td>3</td><td><textarea placeholder="..."></textarea></td><td><textarea placeholder="..."></textarea></td></tr>
      </tbody>
    </table>
  </div>

</div>
"""))
