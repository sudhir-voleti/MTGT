# -*- coding: utf-8 -*-
"""
Lec09 — Step 6a Theory: Traction = V × A × E
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/06a_vae_theory.py').text)
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
  .caselet-body .formula { background: #f8fafc; border: 1px solid #d0d7de; padding: 14px 18px; 
                           margin: 14px 0; font-family: 'Courier New', monospace; font-size: 14px; }
</style>

<div class="caselet-body">

  <h1>Traction: V × A × E</h1>
  <div class="subtitle">From Part-Worths to Go-To-Market Strategy</div>

  <h2>1. The Three Pillars</h2>
  <p>Every purchase decision rests on three forces. If any one of them collapses to near zero, the product fails — no matter how strong the other two are.</p>

  <div class="formula">
    Traction = V(Value) × A(Access) × E(Evidence)
  </div>

  <p><strong>V — Value:</strong> Does the product do something the buyer genuinely wants? This is the <em>performance</em> dimension — range, smart features, power, speed. It answers: <em>"Do I want this?"</em></p>

  <p><strong>A — Access:</strong> Can the buyer actually get it? This is the <em>friction</em> dimension — price, service coverage, charging time, availability. It answers: <em>"Can I afford this? Can I maintain it?"</em></p>

  <p><strong>E — Evidence:</strong> Does the buyer trust that the product will deliver? This is the <em>trust</em> dimension — warranty, brand reputation, reviews, social proof. It answers: <em>"Will this thing still work in three years?"</em></p>

  <div class="callout">
    <p><strong>The chasm appears when V is high but A or E is near zero.</strong> Tech enthusiasts will buy an incomplete product (high V, low A/E) because they are early adopters. Pragmatists will not. They need all three pillars to be solid before they cross.</p>
  </div>

  <h2>2. Mapping Conjoint Attributes to V, A, E</h2>
  <p>The part-worths you estimated in Steps 3 and 4 are the raw material. Your job now is to <strong>classify each attribute</strong> into one of the three pillars. This is not a mechanical exercise — it is a strategic judgment.</p>

  <p>Consider the Yana Mobility attributes:</p>
  <ul>
    <li><strong>Range</strong> and <strong>Smart Features</strong> → <strong>V (Value)</strong>. They make the scooter <em>better</em>.</li>
    <li><strong>Price</strong>, <strong>Service Network</strong>, and <strong>Charging Time</strong> → <strong>A (Access)</strong>. They make the scooter <em>easier to own</em>.</li>
    <li><strong>Warranty</strong> and <strong>Brand</strong> → <strong>E (Evidence)</strong>. They make the scooter <em>trustworthy</em>.</li>
  </ul>

  <p>But this is <em>your</em> mapping. A different strategist might argue that Brand is actually Access (Honda's service network is the real asset) or that Smart Features are Evidence (the app proves the company is tech-forward). The mapping reveals your strategic assumptions.</p>

  <h2>3. From Individual Part-Worths to Traction Scores</h2>
  <p>Once you map the attributes, you can compute a <strong>V score</strong>, <strong>A score</strong>, and <strong>E score</strong> for every respondent by summing their part-worths for the attributes in each pillar.</p>

  <div class="formula">
    V_i = Σ part-worths of V-mapped attributes for respondent i<br>
    A_i = Σ part-worths of A-mapped attributes for respondent i<br>
    E_i = Σ part-worths of E-mapped attributes for respondent i
  </div>

  <p>Plotting V vs. A (with E as color or bubble size) reveals the <strong>traction landscape</strong>. Respondents in the top-right corner have high V and high A — they are easy wins. Respondents in the bottom-left have low everything — they are the "None" choosers. The diagonal frontier is where trade-offs live.</p>

  <h2>4. What You Will Do Now</h2>
  <p>In the next cell, you will:</p>
  <ol>
    <li><strong>Map each attribute</strong> to V, A, E, or Exclude (your strategic choice).</li>
    <li><strong>Compute V/A/E scores</strong> for all 400 respondents.</li>
    <li><strong>Plot the traction landscape</strong> — V vs. A, colored by segment.</li>
    <li><strong>Identify the chasm</strong> — which segment has high V but low A or E?</li>
  </ol>

  <p>Later, in the simulator, you will see how each product configuration scores on V, A, and E — and why some configurations win share even when their total utility is lower.</p>

  <div class="pause-box">
    <h3>Before You Map: Make Your Prediction</h3>
    <p>Before you see the scatterplot, predict which segment will have the highest V score and which will have the highest A score.</p>
    <table class="scribble-table">
      <thead><tr><th>Pillar</th><th>Highest Score Segment</th><th>Why?</th></tr></thead>
      <tbody>
        <tr>
          <td>V (Value)</td>
          <td><textarea placeholder="e.g., Tech — they love range and smart features..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
        </tr>
        <tr>
          <td>A (Access)</td>
          <td><textarea placeholder="e.g., PriceHunter — they care about price and service..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
        </tr>
        <tr>
          <td>E (Evidence)</td>
          <td><textarea placeholder="e.g., Pragmatist — they value warranty and Honda brand..."></textarea></td>
          <td><textarea placeholder="..."></textarea></td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
"""))
