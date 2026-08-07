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
    margin: 16px 0;
    color: #003366;
  }
</style>

<div class="caselet-body">

  <h1>Step 6: CLV Diagnosis</h1>
  <div class="subtitle">Willingness to Pay, Engagement, and Risk</div>

  <p>Traction tells you whether a segment will buy.</p>
  <p>CLV tells you how much that segment is worth once they do.</p>

  <div class="callout">
    <p>Notice the minus sign on Risk.</p>
    <p>A customer who loves your product but fears for their data is worth less than their enthusiasm suggests.</p>
    <p>The formula captures that drag.</p>
    <p>Unlike traction, CLV does not collapse to zero when one block is weak. It simply gets discounted.</p>
  </div>

  <h2>1. What You Will Do Now</h2>
  <p>The code cell below opens the CLV Explorer. You will:</p>
  <ol>
    <li>Confirm or edit which survey items map to WTP, Engagement, and Risk.</li>
    <li>Compute per-respondent CLV and see the distribution by segment.</li>
    <li>Compare CLV against traction from Step 3. Ask yourself: does the segment with the highest traction also have the highest CLV?</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, look back at your segment profiles from Step 1.</p>
    <p>Which segment do you think will have the highest CLV? Which will have the lowest?</p>

    <table>
      <thead>
        <tr>
          <th>Segment</th>
          <th>My Prediction: Highest or Lowest CLV?</th>
          <th>Why?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Visionaries / Early Adopters</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Pragmatists / Early Majority</td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Skeptics / Late Majority</td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>A segment with high WTP and high Engagement but also high Risk is a puzzle.</p>
    <p>They love the idea but fear the consequences.</p>
    <p>That is where product policy -- not product features -- unlocks value.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
