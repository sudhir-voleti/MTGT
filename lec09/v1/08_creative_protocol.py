# -*- coding: utf-8 -*-
"""
Marketing Campaign Creatives Protocol — Lec09 Yana Mobility
Render inline HTML for Colab via: exec(requests.get(BASE + "08_creative_protocol.py").text)
"""

from IPython.display import display, HTML

HTML_CONTENT = """
<style>
  .creative-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.55;
    color: #1e293b;
    max-width: 900px;
    margin: 0 auto;
  }
  .creative-body h1 {
    font-size: 1.45em;
    color: #003366;
    margin: 0 0 6px 0;
  }
  .creative-body .subtitle {
    font-size: 1.0em;
    color: #475569;
    margin-bottom: 20px;
  }
  .creative-body h2 {
    font-size: 1.15em;
    color: #003366;
    border-bottom: 2px solid #E37222;
    padding-bottom: 4px;
    margin-top: 24px;
  }
  .creative-body h3 {
    font-size: 1.05em;
    color: #003366;
    margin-top: 18px;
  }
  .creative-body p {
    margin: 10px 0;
  }
  .creative-body ul, .creative-body ol {
    margin: 8px 0 12px 22px;
  }
  .creative-body li {
    margin: 5px 0;
  }
  .creative-body .callout {
    background: #f0f7ff;
    border-left: 5px solid #003366;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .creative-body .note {
    background: #fffbeb;
    border: 1px dashed #d97706;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .creative-body .phase {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 18px 20px;
    margin: 18px 0;
  }
  .creative-body .phase-header {
    font-weight: 700;
    color: #003366;
    font-size: 1.05em;
    margin-bottom: 10px;
  }
  .creative-body code {
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 13.5px;
  }
  .creative-body pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 14px 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 13.5px;
    line-height: 1.5;
  }
  .creative-body table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin: 14px 0 18px;
  }
  .creative-body th {
    background-color: #003366;
    color: white;
    padding: 10px 12px;
    text-align: left;
    border: 1px solid #003366;
  }
  .creative-body td {
    padding: 9px 12px;
    border: 1px solid #d0d7de;
    vertical-align: top;
  }
  .creative-body tr:nth-child(even) td {
    background-color: #f8fafc;
  }
</style>

<div class="creative-body">

  <h1>Campaign Creatives Protocol</h1>
  <div class="subtitle">From Part-Worths to Print Ads — Lec09 Yana Mobility &nbsp;|&nbsp; MTGT @ ISB</div>

  <div class="callout">
    <strong>The logic:</strong> A great ad is not born whole. It is assembled from tested parts. 
     <p>You will use genAI to generate <em>variations</em> of each ad element, test them in isolation with your NLM persona, pick winners, and assemble a full creative. 
     <p>Then, finally, you test the whole. Ready?
  </div>

  <h2>The 7 Atomic Elements</h2>
  <p>Every static / print ad can be decomposed into these elements. You will generate and test each one separately.</p>

  <table>
    <thead>
      <tr><th>#</th><th>Element</th><th>What to generate</th><th>Test prompt to NLM</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td><strong>Target Avatar</strong></td>
        <td>A 2-sentence persona snapshot</td>
        <td>"Read this avatar. Does it describe you? What is missing?"</td>
      </tr>
      <tr>
        <td>2</td>
        <td><strong>Headline / Slogan</strong></td>
        <td>3 alternative hooks (3–8 words each)</td>
        <td>"Rate each headline 1–10 for how much it makes you want to read the rest."</td>
      </tr>
      <tr>
        <td>3</td>
        <td><strong>Visual Scene</strong></td>
        <td>A text description for image gen (subject, setting, mood, colors)</td>
        <td>"Imagine this image. Does it feel like your life? Does it feel aspirational or fake?"</td>
      </tr>
      <tr>
        <td>4</td>
        <td><strong>Body Copy</strong></td>
        <td>2–3 supporting sentences</td>
        <td>"Does this copy address your real concerns, or does it sound like marketing?"</td>
      </tr>
      <tr>
        <td>5</td>
        <td><strong>USP Anchor</strong></td>
        <td>The one non-negotiable claim</td>
        <td>"Which of these claims would you actually repeat to a friend?"</td>
      </tr>
      <tr>
        <td>6</td>
        <td><strong>Call to Action</strong></td>
        <td>What the reader does next</td>
        <td>"Would you actually do this? What would stop you?"</td>
      </tr>
      <tr>
        <td>7</td>
        <td><strong>Tone / Voice</strong></td>
        <td>1-sentence emotional register</td>
        <td>"Does this tone feel like it is talking <em>to</em> you or <em>at</em> you?"</td>
      </tr>
    </tbody>
  </table>

  <h2>The 5-Phase Workflow</h2>

  <div class="phase">
    <div class="phase-header">Phase A — Elemental Generation (genAI)</div>
    <p>Use ChatGPT / Claude / Gemini to generate <strong>3 variations</strong> of each element. Be specific in your prompt.</p>
    <p><strong>Example genAI prompt for Element 2 (Headline):</strong></p>
    <pre>
I am creating a print ad for an electric scooter called Yana.
Target: A 34-year-old IT manager in Indore who trusts Honda, cares about
service reach and warranty, and finds "smart features" irrelevant.
She is price-sensitive but not a bargain hunter — she wants "peace of mind."

Generate 3 headline options (max 8 words each) that would make her stop
and read the ad. Avoid tech jargon. Avoid lifestyle fluff.
    </pre>
    <p><strong>Example genAI prompt for Element 3 (Visual):</strong></p>
    <pre>
Describe a photograph for a print ad. Subject: a working mother picking up
her child from school. The Yana scooter is in frame, but not the hero.
The mood is warm, practical, and trustworthy — not aspirational or glossy.
Setting: a tier-2 Indian city street at 4:30 PM. Describe lighting, colors,
and what the mother is wearing. No text in the image.
    </pre>
  </div>

  <div class="phase">
    <div class="phase-header">Phase B — Elemental Testing (NLM)</div>
    <p>Test <strong>one element at a time</strong> with your NLM persona. Do not show the full ad yet.</p>
    <p><strong>Query template for testing a headline:</strong></p>
    <pre>
You are reading a newspaper. You see a Yana scooter ad with this headline:
"[HEADLINE OPTION A]"

Rate how much this headline makes you want to read the rest of the ad:
1 = "I would skip the page"
10 = "I would definitely read more"

Then explain in one sentence why.
    </pre>
    <p>Run this for all 3 headline variations. Pick the winner. Repeat for each element.</p>
    <div class="note">
      <strong>Why test in isolation?</strong> Because a great headline can rescue bad body copy, and great body copy can survive a weak headline. You need to know which element is actually doing the work.
    </div>
  </div>

  <div class="phase">
    <div class="phase-header">Phase C — Assembly (The Full Ad)</div>
    <p>Combine the winning element from each phase into one coherent creative brief:</p>
    <pre>
CAMPAIGN BRIEF — Yana [SKU Name]

Target Avatar: [Paste winner from Phase B, Element 1]
Headline: [Paste winner from Phase B, Element 2]
Visual Description: [Paste winner from Phase B, Element 3]
Body Copy: [Paste winner from Phase B, Element 4]
USP Anchor: [Paste winner from Phase B, Element 5]
Call to Action: [Paste winner from Phase B, Element 6]
Tone / Voice: [Paste winner from Phase B, Element 7]
    </pre>
    <p>If you have access to an image generator (Midjourney, DALL-E), generate the visual now. Otherwise, keep the text description as your "storyboard."</p>
  </div>

  <div class="phase">
    <div class="phase-header">Phase D — Holistic Testing (NLM)</div>
    <p>Now show the <strong>complete ad</strong> to your persona. Use this query:</p>
    <pre>
You see a full-page newspaper ad for Yana. Here is exactly what it contains:

HEADLINE: "[Your headline]"
IMAGE: [Your visual description]
BODY COPY: "[Your body copy]"
USP: "[Your USP anchor]"
CTA: "[Your call to action]"

You are currently considering buying an electric scooter. You also have the
option to buy Honda, Ola, or Ather, or to stick with your current petrol
scooter (None).

Questions:
1. Rate this ad overall: 1–10.
2. Does this ad make you more likely to consider Yana? Yes / No / Unsure.
3. Which competitor brand does this ad most threaten? Honda / Ola / Ather / None.
4. What is the one thing missing from this ad that would change your mind?
5. If you saw this ad AND the Yana product was [your SKU config], would you
   choose it over your current best alternative? Explain.
    </pre>
  </div>

  <div class="phase">
    <div class="phase-header">Phase E — VAE Diagnosis (Advanced)</div>
    <p>Ask NLM to decompose its reaction into the three Traction pillars:</p>
    <pre>
Now diagnose your own reaction using the V × A × E framework:

V (Value — desire for the product): Did the ad make the scooter itself feel
   desirable? Rate 1–10.

A (Access — reduced friction): Did the ad make buying feel easy, affordable,
   and reachable? Rate 1–10.

E (Evidence — trust and proof): Did the ad make you trust Yana? Rate 1–10.

Which pillar is strongest? Which is weakest? What specific word or image
moved that pillar?
    </pre>
    <div class="callout">
      <strong>Teaching point:</strong> A student whose ad scores 8/10 overall but E = 3/10 has a <em>trust problem</em>, not a product problem. The fix is not a better scooter — it is a warranty claim, a service partnership, or a testimonial.
    </div>
  </div>

  <h2>Deliverable — Creative Portfolio</h2>
  <p>Submit a 2-page PDF with:</p>
  <ol>
    <li><strong>Element Scorecard:</strong> A table showing all 3 variations of each element and the NLM rating for each. Highlight the winner.</li>
    <li><strong>Final Creative Brief:</strong> The assembled ad (text + visual description or generated image).</li>
    <li><strong>Holistic Test Output:</strong> Copy-paste NLM's Phase D response.</li>
    <li><strong>VAE Diagnosis:</strong> NLM's V, A, E scores with your interpretation.</li>
    <li><strong>One-paragraph reflection:</strong> "If I had ₹5 lakh to change one thing about this ad, I would change ______ because NLM told me ______."</li>
  </ol>

  <div class="note">
    <strong>Time budget:</strong> Phase A–B (30 min), Phase C (15 min), Phase D–E (20 min), Assembly (10 min). Total: ~75 minutes in class, or split across two sessions.
  </div>

</div>
"""

display(HTML(HTML_CONTENT))
