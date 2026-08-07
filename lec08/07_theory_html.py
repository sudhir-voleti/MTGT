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

  <h1>Recap: From Data to Decision</h1>
  <div class="subtitle">What You Have Built</div>

  <p>You started with a raw survey of 200 respondents and a failing B2B pivot.</p>
  <p>Step by step, you turned that data into a strategic diagnosis. Here is what you now hold:</p>

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
        <td>Uploaded and profiled the data</td>
        <td>Four distinct segments hiding inside the averages</td>
      </tr>
      <tr>
        <td><strong>Step 2</strong></td>
        <td>Mapped segments to Moore's categories</td>
        <td>The chasm sits between Visionaries and Pragmatists</td>
      </tr>
      <tr>
        <td><strong>Step 3</strong></td>
        <td>Diagnosed traction with V &times; A &times; E</td>
        <td>Two pillars collapsed for Pragmatists, so traction went to zero</td>
      </tr>
      <tr>
        <td><strong>Step 4</strong></td>
        <td>Mapped survey items to Whole Product layers</td>
        <td>The Generic product is built; the Augmented layer is empty</td>
      </tr>
      <tr>
        <td><strong>Step 5</strong></td>
        <td>Simulated product configurations under $3M</td>
        <td>Some combinations cross the chasm; others burn cash without results</td>
      </tr>
      <tr>
        <td><strong>Step 6</strong></td>
        <td>Estimated CLV independently of traction</td>
        <td>The highest-traction segment is not always the most valuable segment</td>
      </tr>
    </tbody>
  </table>

  <h2>The Three Ideas to Take Away</h2>

  <p><strong>First, segmentation is not the end of the analysis.</strong></p>
  <p>The algorithm gave you four clusters. Strategy begins when you name them, place them on Moore's line, and decide which side of the chasm you can realistically serve today.</p>

  <p><strong>Second, multiplication is cruel.</strong></p>
  <p>Traction = V &times; A &times; E means a buyer who wants your product but cannot get it through procurement and sees no clinical proof does not buy a little. They buy nothing.</p>
  <p>That is why Hridayam's conversion rate did not dip from 24% to 15%. It crashed to under 3%.</p>

  <p><strong>Third, traction and CLV are different lenses.</strong></p>
  <p>A segment can score high on willingness to pay but low on readiness to adopt.</p>
  <p>Your beachhead decision requires both. Traction tells you who will buy now. CLV tells you who is worth serving once they do.</p>

  <h2>The Final Synthesis</h2>
  <p>The VP asked three questions in the memo. You can now answer them with evidence:</p>
  <ol>
    <li><strong>What distinct groups exist?</strong> Four segments, spanning Visionaries to Laggards.</li>
    <li><strong>Why did the same product fail in B2B?</strong> The product did not change. The context did. Pragmatists demand Whole Product completeness that D2C athletes filled in themselves.</li>
    <li><strong>Where should Hridayam place its next bet?</strong> On the Pragmatist beachhead -- but only if the budget is spent on L3a Evidence and L3b Access, not on a better Patch.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Synthesize</h3>
    <p>Before you close the notebook, write your one-sentence recommendation to the board.</p>
    <p>Be specific about budget, features, and the segment you would target.</p>

    <table>
      <thead>
        <tr>
          <th>Element</th>
          <th>My Recommendation</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Target Segment</td>
          <td></td>
        </tr>
        <tr>
          <td>Total Budget</td>
          <td></td>
        </tr>
        <tr>
          <td>Top 2 Features to Build</td>
          <td></td>
        </tr>
        <tr>
          <td>Feature to Deliberately Skip</td>
          <td></td>
        </tr>
        <tr>
          <td>Expected Outcome in 12 Months</td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>A good strategy is not a list of everything you could do.</p>
    <p>It is a list of what you will do, what you will not do, and why the difference matters.</p>
    <p>That is the difference between data analysis and strategic choice.</p>
  </div>

</div>
"""))
