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

  <h1>Step 5: GTM Traction Integration — From Share to CLV</h1>
  <div class="subtitle">The Final Translation</div>

  <p>You have part-worths. You have market share. Now you must answer the question the board actually cares about: <strong>Is this business worth building?</strong></p>

  <p>A product with 15% share is not automatically good. If the margin is thin and the customer leaves after one year, 15% share is a trap. You need to connect share to lifetime value.</p>

  <h2>1. The CLV Formula for Yana</h2>
  <p>We use a simplified but defensible CLV model:</p>

  <div class="formula">
    CLV = (Margin per Unit × Expected Ownership Years × Annual Service Revenue) − Customer Acquisition Cost
  </div>

  <p>Where:</p>
  <ul>
    <li><strong>Margin per Unit</strong> depends on configuration. The 150 km battery pack costs ₹18,000 more than the 75 km pack. Fast charging adds ₹4,000. Basic smart features save ₹6,000 versus Advanced.</li>
    <li><strong>Expected Ownership Years</strong> is higher when warranty is longer and service network is denser.</li>
    <li><strong>Annual Service Revenue</strong> is higher for Advanced smart features (OTA subscriptions, app services).</li>
    <li><strong>Customer Acquisition Cost</strong> is lower when service network is dense (word-of-mouth replaces paid ads).</li>
  </ul>

  <h2>2. Traction Revisited</h2>
  <p>Recall V × A × E from Lec07. We now compute it from conjoint utilities:</p>
  <ul>
    <li><strong>V</strong> = utility from Range + Smart Features</li>
    <li><strong>A</strong> = utility from low Price + wide Service + fast Charging</li>
    <li><strong>E</strong> = utility from Warranty + Brand trust</li>
  </ul>

  <div class="callout">
    <p>Traction by segment tells you who will adopt. CLV by segment tells you who is worth adopting.</p>
    <p>The beachhead is where both are high.</p>
  </div>

  <h2>3. What You Will Do Now</h2>
  <p>The code cell below will:</p>
  <ol>
    <li>Compute margin and CLV for each simulated configuration.</li>
    <li>Plot Traction vs. CLV by segment (the "Beachhead Map").</li>
    <li>Identify the configuration that maximizes expected contribution margin (Share × CLV × Segment Size).</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, mark your prediction on the map. Where do you think each segment sits?</p>

    <table>
      <thead>
        <tr>
          <th>Segment</th>
          <th>My Prediction: High or Low Traction?</th>
          <th>My Prediction: High or Low CLV?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Tech Enthusiasts</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Pragmatists</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Price Hunters</td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>The segment in the top-right quadrant is your beachhead.</p>
    <p>If no segment sits there, you have a product-market fit problem, not a pricing problem.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
