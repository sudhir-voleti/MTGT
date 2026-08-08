from IPython.display import HTML, display

display(HTML("""
<style>
  .caselet-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.55;
    color: #1e293b;
    max-width: 900px;
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
    margin-top: 22px;
  }
  .caselet-body p {
    margin: 10px 0;
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
  .caselet-body .green { color: #16a34a; font-weight: 700; }
  .caselet-body .red { color: #dc2626; font-weight: 700; }
  .caselet-body .ref-note {
    font-size: 12px;
    color: #64748b;
    font-style: italic;
  }
</style>

<div class="caselet-body">

  <h1>Reading the Results: What the Numbers Mean</h1>
  <div class="subtitle">From coefficients to strategic action</div>

  <h2>1. How to Read the Coefficient Table</h2>
  <p>Every coefficient is a <strong>log-odds</strong>. Positive means that level <em>increases</em> choice probability relative to the reference level. Negative means it <em>decreases</em> it.</p>
  <p>The reference level for each attribute is the <strong>worst</strong> one: highest price, shortest range, smallest service network, basic smart features, shortest warranty, slowest charging. Every dummy is an <em>upgrade</em> from that baseline.</p>

  <table>
    <thead>
      <tr>
        <th>Level</th>
        <th>Coefficient</th>
        <th>Meaning</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Price = 85K <span class="ref-note">(vs 140K)</span></td>
        <td class="green">+1.251</td>
        <td>Cutting price to 85K strongly increases choice.</td>
      </tr>
      <tr>
        <td>Warranty = 6yr <span class="ref-note">(vs 2yr)</span></td>
        <td class="green">+1.176</td>
        <td>Doubling warranty strongly increases choice.</td>
      </tr>
      <tr>
        <td>Service = 300 cities <span class="ref-note">(vs 25)</span></td>
        <td class="green">+0.688</td>
        <td>Nationwide service network increases choice.</td>
      </tr>
      <tr>
        <td>Range = 150km <span class="ref-note">(vs 75km)</span></td>
        <td class="green">+0.655</td>
        <td>Double the range increases choice.</td>
      </tr>
      <tr>
        <td>Smart = Advanced <span class="ref-note">(vs Basic)</span></td>
        <td class="green">+0.647</td>
        <td>Advanced features increase choice.</td>
      </tr>
      <tr>
        <td>Charge = 1.5hrs <span class="ref-note">(vs 4hrs)</span></td>
        <td class="green">+0.354</td>
        <td>Fast charging increases choice.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>All coefficients are positive.</strong> This is by design. The reference level is always the worst option. Every dummy represents an upgrade.</p>
    <p>If a coefficient were negative, it would mean that "upgrade" actually hurts choice — a signal to check your data.</p>
  </div>

  <h2>2. The WTP Table: What Is Each Upgrade Worth?</h2>
  <p>WTP tells you how much price reduction (or equivalent value) each feature upgrade provides. It is computed as <code>beta_attribute / beta_price</code> (both positive, so WTP is positive).</p>

  <table>
    <thead>
      <tr>
        <th>Upgrade</th>
        <th>WTP</th>
        <th>Interpretation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>85K vs 140K</td>
        <td class="green">1.251</td>
        <td>The biggest driver. Price dominates.</td>
      </tr>
      <tr>
        <td>6yr vs 2yr warranty</td>
        <td class="green">1.176</td>
        <td>Nearly as valuable as a price cut. Trust matters.</td>
      </tr>
      <tr>
        <td>300 cities vs 25 cities</td>
        <td class="green">0.688</td>
        <td>Service reach is worth ~55% of the 85K price advantage.</td>
      </tr>
      <tr>
        <td>150km vs 75km range</td>
        <td class="green">0.655</td>
        <td>Range is worth ~52% of the 85K price advantage.</td>
      </tr>
      <tr>
        <td>Advanced vs Basic smart</td>
        <td class="green">0.647</td>
        <td>Smart features are worth ~52% of the 85K price advantage.</td>
      </tr>
      <tr>
        <td>1.5hrs vs 4hrs charge</td>
        <td class="green">0.354</td>
        <td>Fast charging is worth ~28% of the 85K price advantage.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>The hierarchy is clear:</strong> Price > Warranty > Service ≈ Range ≈ Smart > Charge speed.</p>
    <p>This is the order in which engineering budget should be allocated if the goal is to maximize choice probability.</p>
  </div>

  <h2>3. The Segment-Specific Models: Who Wants What?</h2>
  <p>The same model run separately for each segment reveals heterogeneity. The magnitude of each coefficient tells you how much that segment cares.</p>

  <table>
    <thead>
      <tr>
        <th>Segment</th>
        <th>Top Driver</th>
        <th>Magnitude</th>
        <th>Strategic Reading</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Tech</strong></td>
        <td>Range 150km</td>
        <td class="green">+1.366</td>
        <td>Tech enthusiasts will pay for performance. Range is everything.</td>
      </tr>
      <tr>
        <td><strong>Pragmatist</strong></td>
        <td>Price 85K</td>
        <td class="green">+1.112</td>
        <td>Pragmatists are value hunters. Price sensitivity is high.</td>
      </tr>
      <tr>
        <td><strong>PriceHunter</strong></td>
        <td>Price 85K</td>
        <td class="green">+1.569</td>
        <td>Price dominates completely. Other features are noise.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>The chasm is in the coefficients.</strong></p>
    <p>Tech cares about range (+1.366) more than price (+1.057). Pragmatist cares about price (+1.112) more than range (+0.498). PriceHunter cares about price (+1.569) and nothing else comes close.</p>
    <p>You cannot build one product for all three.</p>
  </div>

  <h2>4. The Choice Summary: Which Complete Products Won?</h2>
  <p>Coefficients predict. Win rates confirm. The most popular complete profile was chosen 86% of the time it appeared. The least popular was chosen 0%.</p>

  <table>
    <thead>
      <tr>
        <th>Profile</th>
        <th>Times Shown</th>
        <th>Times Chosen</th>
        <th>Win Rate</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>150km, 1.5hrs, <strong>85K</strong>, <strong>300 cities</strong>, Advanced, 4yr</td>
        <td>59</td>
        <td class="green">51</td>
        <td class="green">86.4%</td>
      </tr>
      <tr>
        <td>110km, 1.5hrs, <strong>85K</strong>, <strong>300 cities</strong>, Advanced, 6yr</td>
        <td>43</td>
        <td class="green">38</td>
        <td class="green">88.4%</td>
      </tr>
      <tr>
        <td>75km, 4hrs, <strong>140K</strong>, <strong>25 cities</strong>, Basic, 4yr</td>
        <td>—</td>
        <td class="red">0</td>
        <td class="red">0.0%</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>The pattern:</strong> Winners have low price + wide service + good warranty. Losers have high price + poor service. Range and smart features are secondary.</p>
    <p>The Yana S1 (150km, 1.5hrs, <strong>140K</strong>, <strong>25 cities</strong>, Advanced, 4yr) has the right range and smart features but the wrong price and service. That is why the chasm exists.</p>
  </div>

  <h2>5. The Attribute-Level Win Rates: What Wins When Shown?</h2>
  <p>Win rate = P(chosen | this level appears in the task). It is independent of how often the level appears. A level with high win rate but low frequency is a hidden gem — underutilized in your design.</p>

  <table>
    <thead>
      <tr>
        <th>Attribute</th>
        <th>Best Level</th>
        <th>Win Rate</th>
        <th>Worst Level</th>
        <th>Win Rate</th>
        <th>Gap</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Price</td>
        <td>85K</td>
        <td class="green">47.5%</td>
        <td>140K</td>
        <td class="red">14.0%</td>
        <td>33.5 pts</td>
      </tr>
      <tr>
        <td>Service</td>
        <td>300 cities</td>
        <td class="green">39.1%</td>
        <td>25 cities</td>
        <td class="red">18.0%</td>
        <td>21.1 pts</td>
      </tr>
      <tr>
        <td>Warranty</td>
        <td>6yr</td>
        <td class="green">37.1%</td>
        <td>2yr</td>
        <td class="red">21.7%</td>
        <td>15.4 pts</td>
      </tr>
      <tr>
        <td>Smart</td>
        <td>Advanced</td>
        <td class="green">36.1%</td>
        <td>Basic</td>
        <td class="red">22.8%</td>
        <td>13.3 pts</td>
      </tr>
      <tr>
        <td>Range</td>
        <td>150km</td>
        <td class="green">37.1%</td>
        <td>75km</td>
        <td class="red">21.8%</td>
        <td>15.3 pts</td>
      </tr>
      <tr>
        <td>Charge</td>
        <td>1.5hrs</td>
        <td class="green">33.4%</td>
        <td>4hrs</td>
        <td class="red">25.4%</td>
        <td>8.0 pts</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>The gap column is your priority list.</strong> Price has the largest gap (33.5 points). That is where the biggest competitive leverage lives.</p>
    <p>Charge speed has the smallest gap (8.0 points). That is where engineering effort yields the least market return.</p>
  </div>

  <div class="pause-box">
    <h3>Pause and Decide</h3>
    <p>You have ₹3,000,000. The gaps tell you where to spend.</p>
    <p>Price is structural — you set it. Service and warranty are operational — you build them. Range and smart are engineering — you design them. Charge speed is electrochemistry — you wait for it.</p>
    <p><strong>Which gap do you close first? Which do you deliberately leave open?</strong></p>
  </div>

</div>
"""))
