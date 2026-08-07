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

  <h1>Recap: From Preference to Prescription</h1>
  <div class="subtitle">What You Have Built</div>

  <p>You began with 400 respondents staring at product profiles on a screen. You end with a recommended SKU, a target segment, a projected market share, and a CLV forecast. Here is the chain of logic you built:</p>

  <table>
    <thead>
      <tr>
        <th>Step</th>
        <th>What You Did</th>
        <th>What It Revealed</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Step 1</strong></td>
        <td>Uploaded and profiled metric + CBC data</td>
        <td>Structure, cleanliness, and the "None" option rate</td>
      </tr>
      <tr>
        <td><strong>Step 2</strong></td>
        <td>Estimated metric conjoint part-worths</td>
        <td>Attribute importance and individual utility landscapes</td>
      </tr>
      <tr>
        <td><strong>Step 3</strong></td>
        <td>Estimated CBC logit models</td>
        <td>Choice validation, WTP, and competitive context</td>
      </tr>
      <tr>
        <td><strong>Step 4</strong></td>
        <td>Ran market simulations</td>
        <td>Predicted share for any Yana configuration against rivals</td>
      </tr>
      <tr>
        <td><strong>Step 5</strong></td>
        <td>Integrated Traction and CLV</td>
        <td>The beachhead segment and the expected value of serving it</td>
      </tr>
    </tbody>
  </table>

  <h2>The Three Ideas to Take Away</h2>

  <p><strong>First, preference is not choice.</strong></p>
  <p>Metric conjoint tells you what people like in isolation. CBC tells you what they do when forced to trade. If you launch based on ratings alone, you will overestimate demand for premium features and underestimate price sensitivity.</p>

  <p><strong>Second, the optimal product is not the product with the highest utility.</strong></p>
  <p>It is the product with the highest utility <em>relative to competitors</em> at a cost structure that leaves margin. A feature with high part-worth is not worth building if it costs more than the WTP it generates.</p>

  <p><strong>Third, share without CLV is vanity.</strong></p>
  <p>A configuration that wins 25% share among Price Hunters is a bankruptcy machine if the margin is negative. The beachhead is where Traction and CLV intersect, not where either one is maximized alone.</p>

  <h2>The Final Synthesis</h2>
  <p>The CCO asked four questions in the memo. You can now answer them with numbers:</p>
  <ol>
    <li><strong>Which attributes drive purchase intent?</strong> Your importance scores.</li>
    <li><strong>Do early adopters and pragmatists want different things?</strong> Your segment-level part-worths.</li>
    <li><strong>What is the optimal configuration for the pragmatist beachhead?</strong> Your simulated share-maximizing SKU.</li>
    <li><strong>What is the projected market share and CLV?</strong> Your simulator output.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Synthesize</h3>
    <p>Before you close the notebook, write your one-slide board recommendation.</p>
    <p>One sentence for the product. One sentence for the segment. One number for the share. One number for the CLV.</p>

    <table>
      <thead>
        <tr>
          <th>Element</th>
          <th>My Recommendation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>SKU Configuration</td>
          <td></td>
        </tr>
        <tr>
          <td>Target Segment</td>
          <td></td>
        </tr>
        <tr>
          <td>Projected Year-1 Share</td>
          <td></td>
        </tr>
        <tr>
          <td>Projected CLV per Customer</td>
          <td></td>
        </tr>
        <tr>
          <td>The Competitor We Hurt Most</td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>A good GTM strategy is not a compromise between engineering and finance.</p>
    <p>It is a specific bet on a specific customer, backed by the arithmetic of their revealed preferences.</p>
    <p>That is the difference between a launch and a market entry.</p>
  </div>

</div>
"""))
