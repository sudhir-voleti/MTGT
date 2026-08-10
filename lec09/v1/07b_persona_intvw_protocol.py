# -*- coding: utf-8 -*-
"""
NLM Customer Interview Protocol — Lec09 Yana Mobility
Render inline HTML for Colab via: exec(requests.get(BASE + "nlm_protocol.py").text)
"""

from IPython.display import display, HTML

HTML_CONTENT = """
<style>
  .protocol-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.55;
    color: #1e293b;
    max-width: 900px;
    margin: 0 auto;
  }
  .protocol-body h1 {
    font-size: 1.45em;
    color: #003366;
    margin: 0 0 6px 0;
  }
  .protocol-body .subtitle {
    font-size: 1.0em;
    color: #475569;
    margin-bottom: 20px;
  }
  .protocol-body h2 {
    font-size: 1.15em;
    color: #003366;
    border-bottom: 2px solid #E37222;
    padding-bottom: 4px;
    margin-top: 24px;
  }
  .protocol-body h3 {
    font-size: 1.05em;
    color: #003366;
    margin-top: 18px;
  }
  .protocol-body p {
    margin: 10px 0;
  }
  .protocol-body ul, .protocol-body ol {
    margin: 8px 0 12px 22px;
  }
  .protocol-body li {
    margin: 5px 0;
  }
  .protocol-body .callout {
    background: #f0f7ff;
    border-left: 5px solid #003366;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .protocol-body .note {
    background: #fffbeb;
    border: 1px dashed #d97706;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .protocol-body .danger {
    background: #fef2f2;
    border-left: 5px solid #dc2626;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .protocol-body code {
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 13.5px;
  }
  .protocol-body pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 14px 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 13.5px;
    line-height: 1.5;
  }
  .protocol-body table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin: 14px 0 18px;
  }
  .protocol-body th {
    background-color: #003366;
    color: white;
    padding: 10px 12px;
    text-align: left;
    border: 1px solid #003366;
  }
  .protocol-body td {
    padding: 9px 12px;
    border: 1px solid #d0d7de;
    vertical-align: top;
  }
  .protocol-body tr:nth-child(even) td {
    background-color: #f8fafc;
  }
</style>

<div class="protocol-body">

  <h1>NLM Customer Interview Protocol</h1>
  <div class="subtitle">Lec09 — Yana Mobility Go-To-Market Simulation &nbsp;|&nbsp; MTGT @ ISB</div>

  <div class="callout">
    <strong>Your mission:</strong> You have been assigned one synthetic customer persona (uploaded to your group's NotebookLM source). This persona has <em>exact part-worth utilities</em> encoded in their profile. Your job is to interview them, iterate, and land on a winning Yana SKU + marketing message.
  </div>

  <h2>1. What You Must Prepare Before Querying NLM</h2>
  <ol>
    <li><strong>Yana product configuration</strong> — choose one level for each attribute:</li>
    <li><strong>Competitive choice set</strong> — pick 2 competitor profiles (from Honda, Ola, Ather) that your persona would realistically see in the market.</li>
    <li><strong>Marketing message</strong> — a slogan, ad copy, or 2-sentence creative brief for your Yana SKU.</li>
  </ol>

  <table>
    <thead>
      <tr>
        <th>Attribute</th>
        <th>Valid Levels (choose one)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>Range</strong></td><td>75km, 110km, 150km</td></tr>
      <tr><td><strong>Charge</strong></td><td>4hrs, 1.5hrs</td></tr>
      <tr><td><strong>Price</strong></td><td>₹85,000, ₹1,10,000, ₹1,40,000</td></tr>
      <tr><td><strong>Service</strong></td><td>25cities, 100cities, 300cities</td></tr>
      <tr><td><strong>Smart</strong></td><td>Basic, Advanced</td></tr>
      <tr><td><strong>Warranty</strong></td><td>2yr, 4yr, 6yr</td></tr>
      <tr><td><strong>Brand</strong></td><td>Yana, Honda, Ola, Ather</td></tr>
    </tbody>
  </table>

  <div class="danger">
    <strong>Hard rule:</strong> Do not invent levels. No "₹95,000", no "3-year warranty", no "120km range." If you use an invalid level, NLM will reject the query or compute garbage.
  </div>

  <h2>2. How to Query NLM — Exact Format</h2>
  <p>Paste this template into your NotebookLM chat. Fill in the brackets.</p>

  <pre>
SCENARIO:
Product A (Yana): [Range], [Charge], [Price], [Service], [Smart], [Warranty]
Product B ([Competitor 1 Brand]): [Range], [Charge], [Price], [Service], [Smart], [Warranty]
Product C ([Competitor 2 Brand]): [Range], [Charge], [Price], [Service], [Smart], [Warranty]
Product D: None

MARKETING MESSAGE: [Your slogan / ad copy / brief here]

QUESTION: You are shopping for an electric scooter. You see the products above.
Which do you choose? Rate each product 1–10. React to the marketing message.
  </pre>

  <div class="note">
    <strong>Why 4 alternatives?</strong> The persona computes utility for <em>each</em> product, adds noise, and picks the best. If you only show Yana, you get a false-positive rating. The "None" option captures category exit — critical for PriceHunters.
  </div>

  <h2>3. What NLM Will Return</h2>
  <p>NLM responds <em>in character</em> (first person, persona voice) and appends a structured block:</p>

  <pre>
[STRUCTURED]
Chosen: &lt;Brand or None&gt;
Yana Rating: &lt;1–10&gt;
Competitor 1 Rating: &lt;1–10&gt;
Competitor 2 Rating: &lt;1–10&gt;
None Rating: &lt;1–10 or N/A&gt;
Reason: &lt;one sentence&gt;
[/STRUCTURED]
  </pre>

  <p><strong>Read both parts.</strong> The in-character response tells you <em>why</em>. The structured block gives you the numbers to iterate on.</p>

  <h2>4. Iteration Protocol — 5 Queries Total</h2>
  <p>You get <strong>5 queries</strong>. After each response, you may change:</p>
  <ul>
    <li>Yana's configuration (one or more attributes)</li>
    <li>The competitors you show (different brands, different specs)</li>
    <li>Your marketing message</li>
  </ul>

  <div class="callout">
    <strong>Before your 5th (final) query, answer these three questions internally:</strong>
    <ol>
      <li>What did you learn about your persona's <strong>reservation utility</strong>? At what point do they choose None?</li>
      <li>Which <strong>competitor brand</strong> is your biggest threat — Honda, Ola, or Ather?</li>
      <li>Which <strong>attribute trade-off</strong> moved the rating most (e.g., dropping price vs. adding warranty)?</li>
    </ol>
  </div>

  <h2>5. Deliverable — 1-Page Memo</h2>
  <p>Submit a single-page memo with the following sections:</p>
  <table>
    <thead>
      <tr>
        <th>Section</th>
        <th>What to include</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Final Yana SKU</strong></td>
        <td>Exact configuration (all 6 attributes)</td>
      </tr>
      <tr>
        <td><strong>Final Competitive Set</strong></td>
        <td>The 2 competitor profiles you showed in your last query</td>
      </tr>
      <tr>
        <td><strong>NLM Final Output</strong></td>
        <td>Copy-paste the [STRUCTURED] block from Query 5</td>
      </tr>
      <tr>
        <td><strong>Model vs. NLM</strong></td>
        <td>Your CBC logit predicted share for this SKU vs. what NLM chose. Why did they agree or disagree?</td>
      </tr>
      <tr>
        <td><strong>Marketing Message</strong></td>
        <td>Your final slogan / brief and why it fits this persona</td>
      </tr>
    </tbody>
  </table>

  <div class="note">
    <strong>Pro tip:</strong> If NLM and your logit model disagree, the most likely culprit is <strong>brand bias</strong> (the persona loves Honda regardless of specs) or a <strong>heuristic override</strong> (e.g., "I never buy Basic Smart"). Use the persona card to diagnose.
  </div>

</div>
"""

display(HTML(HTML_CONTENT))
