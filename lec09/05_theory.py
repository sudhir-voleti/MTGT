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
</style>

<div class="caselet-body">

  <h1>Step 5: Market Simulator — Who Wins When Everyone Is in the Room?</h1>
  <div class="subtitle">From Utilities to Market Shares</div>

  <p>You now know what individuals value. The next question is what happens when everyone shows up at the same time.</p>

  <p>A market simulator takes the MNL model from Step 4 and drops it into a competitive scenario. You define the attributes of every competitor. The model predicts the probability that each customer type chooses each product. Sum those probabilities across segments, weighted by segment size, and you have a market share forecast.</p>

  <h2>1. The Simulation Logic</h2>
  <p>For any product configuration, compute its utility U. Then compute choice probability against the competitive set. Repeat for every segment. Weight by segment prevalence.</p>
  <p>The formula is the same logit ratio, but now you are running it retrospectively for products that do not yet exist. That is the power of conjoint: it lets you test configurations before you tool the factory.</p>

  <h2>2. What You Will Do Now</h2>
  <p>The code cell below opens the Market Simulator. You will:</p>
  <ol>
    <li>Set the competitive baseline (Honda, Ola, Ather).</li>
    <li>Adjust Yana's configuration and watch predicted share change.</li>
    <li>Test price sensitivity: what happens at ₹85,000? At ₹1,40,000?</li>
    <li>Identify the "kink" — the price point where share drops nonlinearly.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, predict Yana's share for two configurations against the competitive set.</p>

    <table>
      <thead>
        <tr>
          <th>Yana Configuration</th>
          <th>My Predicted Share</th>
          <th>My Reasoning</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Pragmatist SKU (₹1.1L, 110km, Basic, 300+ cities)</td>
          <td>____%</td>
          <td></td>
        </tr>
        <tr>
          <td>Premium SKU (₹1.4L, 150km, Advanced, 25 cities)</td>
          <td>____%</td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>The gap between these two shares is the strategic tension Yana faces.</p>
    <p>A higher share usually means a lower margin. A higher margin usually means a lower share.</p>
    <p>Your job is to find the configuration that maximizes something more important than either: <strong>contribution margin × share</strong>.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
