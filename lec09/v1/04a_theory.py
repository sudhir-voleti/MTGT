# -*- coding: utf-8 -*-
"""
Lec09 — Step 4a Theory: Choice-Based Conjoint (CBC)
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/04a_theory.py').text)
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
  .caselet-body table { width: 100%; border-collapse: collapse; font-size: 14.5px; margin: 16px 0 20px; }
  .caselet-body th { background-color: #003366; color: white; padding: 11px 14px; text-align: left; border: 1px solid #003366; }
  .caselet-body td { padding: 10px 14px; border: 1px solid #d0d7de; vertical-align: top; }
  .caselet-body tr:nth-child(even) td { background-color: #f8fafc; }
</style>

<div class="caselet-body">

  <h1>Choice-Based Conjoint: From Desire to Decision</h1>

  <h2>1. Why Metric Conjoint Isn't Enough</h2>
  <p>Metric conjoint asks: <em>"How much do you like this product?"</em> Respondents rate each profile in isolation. This measures <strong>desire</strong> — the strength of preference.</p>
  <p>But desire is not decision. In the real market, consumers face competitors, budget constraints, and the option to walk away entirely. CBC asks: <em>"Which of these would you actually buy?"</em> This measures <strong>choice</strong> — the decision under pressure.</p>

  <div class="callout">
    <p><strong>The gap between desire and decision is where marketing strategy lives.</strong> A segment may rate your product 8/10 in metric conjoint, but if a competitor is priced ₹20,000 lower and they choose "None," the 8/10 was an illusion.</p>
  </div>

  <h2>2. The Long Format: One Row Per Alternative</h2>
  <p>CBC data is stored in <strong>long format</strong>. Each choice task produces multiple rows — one for every alternative the respondent saw, plus one for the "None" option.</p>

  <p>Here is what one choice task looks like in the raw data:</p>

  <table>
    <thead>
      <tr><th>RespID</th><th>Task</th><th>AltID</th><th>Range</th><th>Price</th><th>Brand</th><th>Chosen</th></tr>
    </thead>
    <tbody>
      <tr><td>42</td><td>7</td><td>1</td><td>110km</td><td>₹1.1L</td><td>Yana</td><td>0</td></tr>
      <tr><td>42</td><td>7</td><td>2</td><td>150km</td><td>₹1.4L</td><td>Honda</td><td>0</td></tr>
      <tr><td>42</td><td>7</td><td>3</td><td>75km</td><td>₹85K</td><td>Ola</td><td><strong>1</strong></td></tr>
      <tr><td>42</td><td>7</td><td>4</td><td>None</td><td>None</td><td>None</td><td>0</td></tr>
    </tbody>
  </table>

  <p>Respondent 42, in Task 7, saw three Yana product configurations and a "None" option. They chose Alternative 3 — the cheapest Ola-branded scooter with 75km range. The <code>Chosen</code> column is 1 for the selected row and 0 for all others.</p>

  <h2>3. The "None" Option: The Leaky Funnel</h2>
  <p>The "None of these" alternative is not a nuisance — it is the most important row in the dataset. It tells you when the entire competitive set fails.</p>
  <p>If 30% of respondents choose "None" in a task where all three products are priced at ₹1.4L, that is not random noise. That is a <strong>market signal</strong>: the price point is too high for this segment, regardless of features.</p>

  <div class="callout">
    <p><strong>Without "None," you overestimate demand.</strong> Every conjoint study that omits an outside good produces inflated share projections. The "None" rate is your reality check.</p>
  </div>

  <h2>4. What We Will Discover</h2>
  <p>In this step, we estimate a <strong>multinomial logit (MNL)</strong> model from the CBC data. The output is:</p>
  <ol>
    <li><strong>Coefficients</strong> for each attribute level — the log-odds impact on choice probability.</li>
    <li><strong>Willingness-to-pay (WTP)</strong> — how much each feature is worth in rupees, derived from the ratio of attribute and price coefficients.</li>
    <li><strong>Segment-specific choice patterns</strong> — which attributes each segment actually selects when forced to choose.</li>
    <li><strong>"None" rates by segment</strong> — who walks away, and why.</li>
  </ol>

  <p>The critical question: <strong>Do the CBC results agree with the metric conjoint results from Step 3?</strong> Where they diverge, the CBC is usually more trustworthy — it simulates real competitive choice.</p>

  <div class="pause-box">
    <h3>Before You Run: Predict the "None" Rate</h3>
    <p>Which segment do you think will choose "None of these" most often? Write your prediction and reasoning.</p>
    <table class="scribble-table">
      <thead><tr><th>My Prediction</th><th>Why?</th></tr></thead>
      <tbody>
        <tr>
          <td><textarea placeholder="e.g., PriceHunters, because all alternatives are too expensive..."></textarea></td>
          <td><textarea placeholder="Your reasoning..."></textarea></td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
"""))
