# -*- coding: utf-8 -*-
"""
Lec09 — Step 5a Theory: Market Simulation from Part-Worths
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/05a_theory.py').text)
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

  <h1>Market Simulation: From Part-Worths to Predicted Share</h1>

  <h2>1. What Is a Market Simulator?</h2>
  <p>A market simulator takes the part-worths you estimated from conjoint data and uses them to <strong>project choice probabilities</strong> for any set of competing products.</p>
  <p>It answers the question: <em>"If I launch Product X against Competitors Y and Z, what share will I capture?"</em></p>

  <div class="callout">
    <p><strong>The core insight:</strong> You do not win in a vacuum. You win <em>relative</em> to the alternatives available. A product with high part-worths may still lose if a competitor is priced ₹30,000 lower.</p>
  </div>

  <h2>2. From Utility to Probability: The Logit Rule</h2>
  <p>For each respondent, we compute the <strong>total utility</strong> of each product by summing the part-worths of its attribute levels:</p>

  <div class="formula">
    U(Product) = β_Range + β_Charge + β_Price + β_Service + β_Smart + β_Warranty + β_Brand
  </div>

  <p>Then we convert utilities to <strong>choice probabilities</strong> using the multinomial logit formula:</p>

  <div class="formula">
    P(choose Product i) = exp(U_i) / [exp(U_1) + exp(U_2) + ... + exp(U_n) + exp(U_None)]
  </div>

  <p>The "None" option has utility 0 (or a small negative value). If all products have low utility, the probability mass flows to "None" — respondents walk away.</p>

  <h2>3. Microsimulation: Why Respondent-Level Matters</h2>
  <p>Professional simulators do not use <em>aggregate</em> part-worths. They run the logit formula <strong>once per respondent</strong>, then average the probabilities across all 400 respondents.</p>
  <p>This is called <strong>microsimulation</strong>. It respects heterogeneity: a product that appeals strongly to Tech buyers but not at all to PriceHunters gets the correct blended share, not a distorted average.</p>

  <div class="callout">
    <p><strong>Rule:</strong> Aggregate part-worths → wrong share. Individual part-worths → right share. Always simulate at the respondent level.</p>
  </div>

  <h2>4. What You Will Do Now</h2>
  <p>In the next cell, you will configure a competitive scenario:</p>
  <ol>
    <li><strong>Your product:</strong> Pick a Yana configuration (one level per attribute).</li>
    <li><strong>Competitors:</strong> Configure up to 3 rival products (Honda, Ola, Ather, or another Yana).</li>
    <li><strong>Simulate:</strong> The model computes choice probabilities for each product, by segment and overall.</li>
  </ol>
  <p>The output is a market share projection — the probability that a random respondent from this sample would choose your product over the competitive set.</p>

  <div class="pause-box">
    <h3>Before You Simulate: Sketch Your Strategy</h3>
    <p>Which segment are you targeting? What product configuration do you think will maximize your share against Honda, Ola, and Ather?</p>
    <table class="scribble-table">
      <thead><tr><th>Target Segment</th><th>My Yana Configuration</th><th>Why This Will Win</th></tr></thead>
      <tbody>
        <tr>
          <td><textarea placeholder="e.g., Pragmatist..."></textarea></td>
          <td><textarea placeholder="e.g., 110km, 4hrs, 110K, 300 cities, Basic, 4yr, Yana..."></textarea></td>
          <td><textarea placeholder="Because Pragmatists value service and warranty..."></textarea></td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
"""))
