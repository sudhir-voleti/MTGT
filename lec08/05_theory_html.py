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

  <h1>Step 5: The Board Meeting -- $3M Budget Simulator</h1>
  <div class="subtitle">You Cannot Build Everything. You Must Choose.</div>

  <p>You now know where the chasm is.</p>
  <p>The Pragmatists need L2, L3a, and L3b.</p>
  <p>But Hridayam does not have unlimited money. The board has allocated exactly <strong>$3,000,000</strong> from Series A to close the gap.</p>

  <div class="callout">
    <p>Here is the tension: every feature costs something, and some features cost a lot.</p>
    <p>FDA 510(k) clearance is $2,000,000. That alone eats two-thirds of the budget.</p>
    <p>A peer-reviewed study is $800,000. IT integration is $200,000.</p>
    <p>You cannot check every box.</p>
    <p>The question is not "What would be nice to have?"</p>
    <p>The question is: <strong>What is the minimum set of features that gets Pragmatist traction above the chasm line, without bankrupting the firm?</strong></p>
  </div>

  <h2>1. The Rules of the Simulator</h2>
  <p>The code cell below opens the Configuration Builder. You will:</p>
  <ol>
    <li>Select features to build. Current features are sunk cost ($0). Future features have price tags.</li>
    <li>Watch the budget bar. If you go over $3M, the config is invalid.</li>
    <li>Save multiple configs and compare them side-by-side.</li>
    <li>The tool will plot a Chasm Cliff for each config -- traction across all five Moore categories -- so you can see which configuration flattens the drop between Early Adopters and Early Majority.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, think about the tradeoff.</p>
    <p>FDA clearance is expensive but powerful. An IT API is cheap but narrow.</p>
    <p>Where do you place the bet?</p>

    <table>
      <thead>
        <tr>
          <th>Config Name</th>
          <th>Features I Would Include</th>
          <th>Estimated Cost</th>
          <th>Why This Mix?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Config A</td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td>Config B</td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>Remember: the Pragmatist does not need a better Patch.</p>
    <p>They need trust, proof, and ease.</p>
    <p>Your job is to find the cheapest way to give them that.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
