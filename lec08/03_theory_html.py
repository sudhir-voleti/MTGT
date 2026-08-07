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
    font-size: 1.25em;
    font-weight: 700;
    text-align: center;
    margin: 18px 0;
    color: #003366;
  }
</style>

<div class="caselet-body">

  <h1>Step 3: Traction Diagnosis</h1>
  <div class="subtitle">From Moore Mapping to the Multiplication Trap</div>

  <p>You have named your segments and placed them on Moore's line.</p>
  <p>Now comes the harder question: <strong>Why did Hridayam's traction collapse when they moved from D2C athletes to B2B enterprise buyers?</strong></p>

  <p>The product did not change. The Patch, the App, and the Portal were identical.</p>
  <p>Yet conversion dropped from 24% to under 3%. Something else broke.</p>

  <h2>1. The Formula That Explains the Collapse</h2>
  <p>We diagnose this using three pillars:</p>

  <table>
    <thead>
      <tr>
        <th>Pillar</th>
        <th>What It Measures</th>
        <th>In Hridayam's World</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>V - Value</strong></td>
        <td>Does the buyer want what you built?</td>
        <td>Athletes want granular HRV data. HR departments do not.</td>
      </tr>
      <tr>
        <td><strong>A - Access</strong></td>
        <td>Can the buyer actually get and use it?</td>
        <td>D2C: one-click purchase. B2B: procurement, legal, IT review.</td>
      </tr>
      <tr>
        <td><strong>E - Evidence</strong></td>
        <td>Does the buyer trust that it works?</td>
        <td>Athletes trust influencer reviews. HR needs clinical proof and compliance.</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>Here is the crucial part.</strong></p>
    <p>Traction is not the sum of these pillars.</p>
    <p>It is the <strong>product</strong>:</p>
    <p class="formula">Traction = Value &times; Access &times; Evidence</p>
    <p>A near-zero score on any single pillar collapses overall traction, no matter how strong the other two pillars are.</p>
  </div>

  <h2>2. What You Will Diagnose Next</h2>
  <p>In the cells that follow you will score each of your Moore-mapped segments on Value, Access, and Evidence.</p>
  <p>Watch especially for segments that look attractive on size or CLV but carry a near-zero on one of the three pillars.</p>
  <p>Those are the multiplication traps.</p>

  <div class="pause-box">
    <h3>Pause and Predict (30 seconds)</h3>
    <p>Before you run the next cell, ask yourself:</p>
    <p>Which of your segments is most likely to have a near-zero on Access or Evidence when sold into enterprise HR?</p>
    <p>Write the name down. Then proceed.</p>
  </div>

</div>
"""))
