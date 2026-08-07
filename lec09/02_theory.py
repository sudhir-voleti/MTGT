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
  .caselet-body .formula {
    font-size: 1.05em;
    font-weight: 600;
    text-align: center;
    margin: 16px 0;
    color: #003366;
    background: #f8fafc;
    padding: 12px 14px;
    border-radius: 6px;
    line-height: 1.5;
  }
</style>

<div class="caselet-body">

  <h1>Step 2: Metric Conjoint — What Do They Value?</h1>
  <div class="subtitle">From Ratings to Part-Worths</div>

  <p>In the last step, you confirmed that your data is clean. Now we extract meaning from it.</p>

  <p>Every respondent saw 16 product profiles and rated each one. Those ratings are not random. They are a weighted sum of how much the respondent likes each attribute level. Our job is to recover those weights — the <strong>part-worth utilities</strong>.</p>

  <p>For each respondent, we run one linear regression:</p>

  <div class="formula">
    Rating = β₀ + β₁(Range_110) + β₂(Range_150) + β₃(Charge_Fast) + β₄(Price_110K) + ... + ε
  </div>

  <p>The coefficients are the part-worths. A large positive coefficient means that level strongly increases purchase intent. A negative coefficient means it repels.</p>

  <h2>1. Why This Matters for GTM</h2>
  <p>Part-worths are not academic curiosities. They are the monetary language of customer preference.</p>
  <p>When you know that the part-worth for "150 km range" is +1.8 and the part-worth for "₹1,10,000" is +2.1, you know that the customer would trade some range for a lower price — but only up to a point.</p>

  <h2>2. Attribute Importance</h2>
  <p>Once you have part-worths, compute importance for each attribute:</p>

  <div class="formula">
    Importance(Attribute) = max(part-worth) − min(part-worth)
  </div>

  <p>Normalize these to sum to 100%. This tells you where the battle is won or lost.</p>
  <p>If Price has 45% importance and Smart Features has 8%, you know that your engineering budget should go to cost reduction, not a bigger touchscreen.</p>

  <h2>3. What You Will Do Now</h2>
  <p>The code cell below will:</p>
  <ol>
    <li>Estimate part-worths via dummy regression for every respondent.</li>
    <li>Compute attribute importance.</li>
    <li>Cluster respondents into segments based on their part-worth vectors.</li>
    <li>Profile each segment by psychographics.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, rank the six attributes by how important you think they are to the average Indian two-wheeler buyer. Then rank them by how important you think they are to a tech enthusiast.</p>

    <table>
      <thead>
        <tr>
          <th>Attribute</th>
          <th>My Guess: Mass-Market Rank</th>
          <th>My Guess: Tech-Enthusiast Rank</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Range</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Charging Time</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Price</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Service Network</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Smart Features</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Warranty</td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>If your two rankings are identical, you have not found a chasm.</p>
    <p>The chasm appears when the rankings diverge.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
