# -*- coding: utf-8 -*-
"""
Lec09 — Conjoint Analysis Theory
Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/01_theory.py').text)
"""

from IPython.display import HTML, display

display(HTML("""
<style>
  .caselet-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.55;
    color: #1e293b;
    max-width: 860px;
    margin: 0 auto;
  }
  .caselet-body h1 {
    font-size: 1.55em;
    color: #003366;
    margin: 0 0 6px 0;
  }
  .caselet-body .subtitle {
    font-size: 1.05em;
    color: #475569;
    margin-bottom: 22px;
  }
  .caselet-body h2 {
    font-size: 1.2em;
    color: #003366;
    border-bottom: 2px solid #E37222;
    padding-bottom: 4px;
    margin-top: 28px;
  }
  .caselet-body h3 {
    font-size: 1.05em;
    color: #003366;
    margin-top: 20px;
  }
  .caselet-body p {
    margin: 10px 0;
  }
  .caselet-body ul, .caselet-body ol {
    margin: 8px 0 12px 22px;
  }
  .caselet-body li {
    margin: 4px 0;
  }
  .caselet-body .callout {
    background: #f0f7ff;
    border-left: 5px solid #003366;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .caselet-body .pause-box {
    background: #fffbeb;
    border: 1px dashed #d97706;
    padding: 16px 18px;
    margin: 22px 0;
  }
  .caselet-body table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14.5px;
    margin: 16px 0 20px;
  }
  .caselet-body th {
    background-color: #003366;
    color: white;
    padding: 11px 14px;
    text-align: left;
    border: 1px solid #003366;
  }
  .caselet-body td {
    padding: 10px 14px;
    border: 1px solid #d0d7de;
    vertical-align: top;
  }
  .caselet-body tr:nth-child(even) td {
    background-color: #f8fafc;
  }
  .caselet-body .profile-table td {
    font-size: 13.5px;
    padding: 8px 10px;
  }
  .caselet-body .profile-table th {
    font-size: 13.5px;
    padding: 9px 10px;
  }
  .caselet-body .small-note {
    font-size: 13px;
    color: #64748b;
    margin-top: 6px;
  }
</style>

<div class="caselet-body">

  <h1>Conjoint Analysis: Understanding Trade-offs</h1>
  <div class="subtitle">Lec09 — Yana Mobility Go-To-Market Strategy</div>

  <!-- ============================================================ -->
  <h2>1. What is Conjoint Analysis?</h2>

  <p>Consumers do not buy products in isolation. They buy <strong>bundles of attributes</strong> and implicitly trade one off for another.</p>

  <p>Conjoint analysis is the statistical technique that recovers these hidden trade-offs. It asks respondents to evaluate or choose among product profiles that vary on multiple attributes. By observing patterns in their responses, we can estimate how much each attribute level contributes to overall preference — the <strong>part-worth utility</strong>.</p>

  <div class="callout">
    <p><strong>Core idea:</strong> If a respondent rates a 150km-range scooter higher than a 75km-range scooter — holding price, charging time, and everything else constant — the difference in their ratings reveals the utility they attach to extra range.</p>
  </div>

  <p>There are two common formats:</p>
  <ul>
    <li><strong>Metric (rating-based) conjoint:</strong> Respondents rate each profile on a 1–10 scale. Good for understanding the <em>strength</em> of preference.</li>
    <li><strong>Choice-based conjoint (CBC):</strong> Respondents pick one option from a competitive set, including "None." Good for understanding <em>market choice</em> under realistic trade-offs.</li>
  </ul>

  <p>This caselet uses both. We begin with metric conjoint to discover what drives desire. We validate with CBC to see what drives actual choice when competitors and a "no-buy" option are present.</p>

  <!-- ============================================================ -->
  <h2>2. The Product Attributes</h2>

  <p>Yana Mobility's engineering team has confirmed that the S1 platform can be reconfigured across seven attributes without a full redesign. Each attribute has two or three possible levels.</p>

  <table>
    <thead>
      <tr>
        <th>Attribute</th>
        <th>Level 1 (Reference)</th>
        <th>Level 2</th>
        <th>Level 3</th>
        <th>What it means</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Range</strong></td>
        <td>75 km</td>
        <td>110 km</td>
        <td>150 km</td>
        <td>Single-charge battery range</td>
      </tr>
      <tr>
        <td><strong>Charge</strong></td>
        <td>4 hours (standard)</td>
        <td>1.5 hours (fast)</td>
        <td>—</td>
        <td>Home outlet charging time</td>
      </tr>
      <tr>
        <td><strong>Price</strong></td>
        <td>₹1,40,000</td>
        <td>₹1,10,000</td>
        <td>₹85,000</td>
        <td>Ex-showroom sticker price</td>
      </tr>
      <tr>
        <td><strong>Service</strong></td>
        <td>25 cities</td>
        <td>100 cities</td>
        <td>300+ cities</td>
        <td>Service network coverage</td>
      </tr>
      <tr>
        <td><strong>Smart</strong></td>
        <td>Basic (display only)</td>
        <td>Advanced (app, GPS, OTA)</td>
        <td>—</td>
        <td>Connected features</td>
      </tr>
      <tr>
        <td><strong>Warranty</strong></td>
        <td>2 years</td>
        <td>4 years</td>
        <td>6 years</td>
        <td>Battery + motor coverage</td>
      </tr>
      <tr>
        <td><strong>Brand</strong></td>
        <td>Yana (new entrant)</td>
        <td>Honda (legacy)</td>
        <td>Ola / Ather</td>
        <td>Brand badge on the scooter</td>
      </tr>
    </tbody>
  </table>

  <p class="small-note">Reference levels (in <strong>bold</strong>) are omitted in regression output. All part-worths are measured relative to these baselines.</p>

  <!-- ============================================================ -->
  <h2>3. The Full Factorial Problem</h2>

  <p>If we showed respondents every possible combination of these seven attributes, we would need:</p>

  <p style="text-align:center; font-size:1.15em; margin:18px 0;">
    3 × 2 × 3 × 3 × 2 × 3 × 4 = <strong>1,296 product profiles</strong>
  </p>

  <p>No respondent can rate 1,296 scooters. Even 100 would induce fatigue and random clicking. We need a <strong>fractional factorial design</strong>: a small subset of profiles that preserves our ability to estimate the main effects of each attribute.</p>

  <div class="callout">
    <p><strong>Fractional factorial design:</strong> A statistically optimized subset of profiles chosen so that each attribute level appears with roughly equal frequency, and the effects of different attributes can be estimated independently. Think of it as a "compressed" experiment that retains the signal without the noise of respondent exhaustion.</p>
  </div>

  <!-- ============================================================ -->
  <h2>4. The 16 Profiles</h2>

  <p>The study uses a 16-run fractional factorial design. Each respondent sees all 16 profiles and rates each on a 1–10 purchase-likelihood scale. Below is the full design. Notice how no single profile dominates on every attribute — each forces a trade-off.</p>

  <table class="profile-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Range</th>
        <th>Charge</th>
        <th>Price</th>
        <th>Service</th>
        <th>Smart</th>
        <th>Warranty</th>
        <th>Brand</th>
        <th>What stands out</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td><td>75km</td><td>4hrs</td><td>₹85K</td><td>25 cities</td><td>Basic</td><td>2yr</td><td>Yana</td>
        <td>Budget starter — low everything, but cheap</td>
      </tr>
      <tr>
        <td>2</td><td>110km</td><td>1.5hrs</td><td>₹1.1L</td><td>100 cities</td><td>Advanced</td><td>4yr</td><td>Honda</td>
        <td>Balanced mid-ranger from a trusted name</td>
      </tr>
      <tr>
        <td>3</td><td>150km</td><td>4hrs</td><td>₹1.4L</td><td>300 cities</td><td>Basic</td><td>6yr</td><td>Ola</td>
        <td>Range king with warranty, but slow charge and basic smart</td>
      </tr>
      <tr>
        <td>4</td><td>75km</td><td>1.5hrs</td><td>₹85K</td><td>25 cities</td><td>Advanced</td><td>2yr</td><td>Ather</td>
        <td>Cheap and fast, but range and service are weak</td>
      </tr>
      <tr>
        <td>5</td><td>110km</td><td>4hrs</td><td>₹1.1L</td><td>100 cities</td><td>Basic</td><td>4yr</td><td>Yana</td>
        <td>Mid-range workhorse — no standout, no weakness</td>
      </tr>
      <tr>
        <td>6</td><td>150km</td><td>1.5hrs</td><td>₹1.4L</td><td>300 cities</td><td>Advanced</td><td>6yr</td><td>Honda</td>
        <td>Premium everything — the "whole product" from a legacy brand</td>
      </tr>
      <tr>
        <td>7</td><td>75km</td><td>4hrs</td><td>₹85K</td><td>25 cities</td><td>Basic</td><td>2yr</td><td>Ola</td>
        <td>Entry-level Ola — minimal spec, tech brand</td>
      </tr>
      <tr>
        <td>8</td><td>110km</td><td>1.5hrs</td><td>₹1.1L</td><td>100 cities</td><td>Advanced</td><td>4yr</td><td>Ather</td>
        <td>Mid-range niche premium with fast charging</td>
      </tr>
      <tr>
        <td>9</td><td>150km</td><td>4hrs</td><td>₹1.4L</td><td>300 cities</td><td>Basic</td><td>6yr</td><td>Yana</td>
        <td>Yana's range flagship — long warranty, no smart</td>
      </tr>
      <tr>
        <td>10</td><td>75km</td><td>1.5hrs</td><td>₹85K</td><td>25 cities</td><td>Advanced</td><td>2yr</td><td>Honda</td>
        <td>Cheap Honda with smart features — odd combo</td>
      </tr>
      <tr>
        <td>11</td><td>110km</td><td>4hrs</td><td>₹1.1L</td><td>100 cities</td><td>Basic</td><td>4yr</td><td>Ola</td>
        <td>Mid-range Ola — balanced but basic smart</td>
      </tr>
      <tr>
        <td>12</td><td>150km</td><td>1.5hrs</td><td>₹1.4L</td><td>300 cities</td><td>Advanced</td><td>6yr</td><td>Ather</td>
        <td>Ather's halo product — premium across the board</td>
      </tr>
      <tr>
        <td>13</td><td>75km</td><td>4hrs</td><td>₹85K</td><td>25 cities</td><td>Basic</td><td>2yr</td><td>Honda</td>
        <td>Honda's budget play — minimal but trusted</td>
      </tr>
      <tr>
        <td>14</td><td>110km</td><td>1.5hrs</td><td>₹1.1L</td><td>100 cities</td><td>Advanced</td><td>4yr</td><td>Yana</td>
        <td>Yana's sweet spot — mid-range with fast charge and smart</td>
      </tr>
      <tr>
        <td>15</td><td>150km</td><td>4hrs</td><td>₹1.4L</td><td>300 cities</td><td>Basic</td><td>6yr</td><td>Ather</td>
        <td>Range + service + warranty, but slow charge and basic</td>
      </tr>
      <tr>
        <td>16</td><td>75km</td><td>1.5hrs</td><td>₹85K</td><td>25 cities</td><td>Advanced</td><td>2yr</td><td>Ola</td>
        <td>Cheap, fast, smart — but range and service are thin</td>
      </tr>
    </tbody>
  </table>

  <p class="small-note">Each attribute level appears with roughly equal frequency across the 16 profiles. This balance is what makes the design statistically efficient — no single level dominates the sample and confounds the estimates.</p>

  <!-- ============================================================ -->
  <h2>5. What Happens Next</h2>

  <p>With these 16 profiles, 400 respondents provided 6,400 ratings. Your task is to reverse-engineer the part-worth utilities: how much does each attribute level add to (or subtract from) the purchase-likelihood score?</p>

  <p>The workflow has three phases:</p>
  <ol>
    <li><strong>Discover:</strong> Estimate individual-level part-worths from metric ratings, then cluster respondents into segments.</li>
    <li><strong>Validate:</strong> Run choice models on the CBC data to confirm that segment preferences hold under competitive pressure.</li>
    <li><strong>Simulate:</strong> Build a market simulator to project share for candidate Yana configurations against Honda, Ola, and Ather.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Reflect</h3>
    <p>Before you run any code, look at the 16 profiles above and answer:</p>
    <ul>
      <li>Which profile would <em>you</em> rate highest? Why?</li>
      <li>Which profile is the "worst deal" — high price with low specs?</li>
      <li>Do any profiles feel unrealistic? (That is intentional — unrealistic profiles test whether respondents are paying attention.)</li>
    </ul>
    <p>Your intuition is the benchmark. If the model disagrees with your gut, question the model before you question your gut.</p>
  </div>

</div>
"""))
