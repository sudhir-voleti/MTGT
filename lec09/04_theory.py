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

  <h1>Step 4: Choice-Based Conjoint — Do They Actually Choose You?</h1>
  <div class="subtitle">From Ratings to Decisions</div>

  <p>In Step 2, you learned what people like in isolation. In Step 3, you found tribes of similar preference.</p>
  <p>Now comes the harder question: <strong>When forced to choose among real alternatives, what do they actually do?</strong></p>

  <p>Metric conjoint asks: "Rate this product 1 to 10." CBC asks: "Pick one."</p>
  <p>These are different cognitive tasks. A product rated 8/10 in isolation may never be chosen when a competitor is rated 9/10.</p>
  <p>The market is not a rating contest. It is a choice tournament.</p>

  <h2>1. The Logit Model</h2>
  <p>The multinomial logit (MNL) model converts utilities into choice probabilities:</p>

  <div class="formula">
    P(choose j) = exp(Uⱼ) / Σ exp(Uₖ)
  </div>

  <p>Where Uⱼ is the systematic utility of alternative j. The coefficients tell you how much each attribute changes the log-odds of being chosen.</p>

  <h2>2. Willingness to Pay</h2>
  <p>Because price is an attribute in the model, you can compute WTP:</p>

  <div class="formula">
    WTP = −β_attribute / β_price
  </div>

  <p>This is the rupee amount that makes a customer indifferent to the tradeoff.</p>
  <p>If WTP for fast charging is ₹12,000 but engineering cost is ₹4,000, you have a profitable feature.</p>

  <h2>3. What You Will Do Now</h2>
  <p>The code cell below opens the CBC Analysis Tool. You will:</p>
  <ol>
    <li>Upload or inherit CBC data from the caselet files.</li>
    <li>Map columns: respondent ID, task ID, alternative ID, choice indicator, and attributes.</li>
    <li>Estimate aggregate and segment-specific MNL models.</li>
    <li>Compute WTP for every attribute level.</li>
    <li>Compare attribute ranking from CBC against your metric conjoint ranking.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, predict which will be larger: WTP for "150 km range" or WTP for "300+ cities service network". Then predict which will have a larger coefficient in the MNL model.</p>

    <table>
      <thead>
        <tr>
          <th>Attribute Level</th>
          <th>My WTP Prediction</th>
          <th>Why?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>150 km range vs 75 km</td>
          <td>₹_____</td>
          <td></td>
        </tr>
        <tr>
          <td>300+ cities vs 25 cities</td>
          <td>₹_____</td>
          <td></td>
        </tr>
        <tr>
          <td>Advanced vs Basic smart features</td>
          <td>₹_____</td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>If your WTP predictions do not match the MNL output, ask yourself: did I overestimate what people say they value, or underestimate what they choose when forced to trade?</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
