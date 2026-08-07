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

  <h1>Step 2: Map Your Segments to Moore's World</h1>
  <div class="subtitle">From algorithmic clusters to strategic identities</div>

  <p>In the previous step we uncovered four hidden tribes inside Hridayam's survey data.</p>
  <p>The algorithm labelled them Segment 1, Segment 2, and so on.</p>
  <p>As strategists we now need to give each tribe a real identity that links to how technology markets actually buy.</p>

  <h2>1. The Theory in One Minute</h2>
  <p>Geoffrey Moore observed that every technology market contains five kinds of buyers arranged along an adoption curve:</p>

  <table>
    <thead>
      <tr>
        <th>Category</th>
        <th>Nickname</th>
        <th>Mindset</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Innovators</strong></td>
        <td>The Techies</td>
        <td>"I'll try anything new. I don't need proof."</td>
      </tr>
      <tr>
        <td><strong>Early Adopters</strong></td>
        <td>The Visionaries</td>
        <td>"I see the future. I want competitive advantage."</td>
      </tr>
      <tr>
        <td><strong>Early Majority</strong></td>
        <td>The Pragmatists</td>
        <td>"I'll buy only when it's proven, easy, and safe."</td>
      </tr>
      <tr>
        <td><strong>Late Majority</strong></td>
        <td>The Skeptics</td>
        <td>"I'll buy only when everyone else already has."</td>
      </tr>
      <tr>
        <td><strong>Laggards</strong></td>
        <td>The Resisters</td>
        <td>"I don't want this. Go away."</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p><strong>The critical idea:</strong> The biggest gap in the market is not between any two random segments.</p>
    <p>It is the gap between the <strong>Visionaries</strong> and the <strong>Pragmatists</strong>.</p>
    <p>Moore calls this <strong>the chasm</strong>.</p>
    <p>Visionaries will buy an incomplete product. Pragmatists will not.</p>
    <p>Trying to sell a D2C wearable patch straight into a corporate HR department is an attempt to leap that chasm without a bridge. That is precisely the trap Hridayam fell into.</p>
  </div>

  <h2>2. What You Will Do Now</h2>
  <p>In the next cell a simple mapper will open.</p>
  <p>For each of the four segments the algorithm discovered, you will assign it to one of Moore's five categories.</p>

  <p><strong>Before you run the mapper, look back at your segment profiles from Step 1 and ask:</strong></p>
  <ul>
    <li>Which segment scores high on Pioneer Drive and Risk Tolerance but low on Compliance? Those are likely your <strong>Visionaries</strong>.</li>
    <li>Which segment demands Clinical Proof, Integration, and Privacy? Those are your <strong>Pragmatists</strong> - the other side of the chasm.</li>
    <li>Which segment is low across the board? Those are your <strong>Laggards</strong>. They can be set aside for now.</li>
  </ul>

  <div class="pause-box">
    <h3>Pause and Predict (30 seconds)</h3>
    <p>Look at your four segments.</p>
    <p>Write down your provisional mapping for each one <strong>before</strong> you click Auto-Suggest.</p>
    <p>Run the next cell when ready.</p>
  </div>

</div>
"""))
