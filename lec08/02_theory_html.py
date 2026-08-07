from IPython.display import HTML, display

display(HTML("""
<style>
  .mtgt-card {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border-radius: 16px;
    padding: 36px 40px;
    max-width: 900px;
    margin: 20px auto;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    border: 1px solid #cbd5e1;
    color: #1e293b;
  }
  .mtgt-card h1 {
    font-size: 32px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
  }
  .mtgt-card .subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 28px;
    font-weight: 500;
  }
  .mtgt-card h2 {
    font-size: 22px;
    font-weight: 700;
    color: #1e40af;
    margin-top: 28px;
    margin-bottom: 14px;
    border-left: 5px solid #3b82f6;
    padding-left: 14px;
  }
  .mtgt-card p, .mtgt-card li {
    font-size: 17px;
    line-height: 1.7;
    color: #334155;
  }
  .mtgt-card .callout {
    background: #eff6ff;
    border-left: 5px solid #3b82f6;
    padding: 18px 22px;
    border-radius: 0 10px 10px 0;
    margin: 22px 0;
    font-size: 17px;
  }
  .mtgt-card .callout strong {
    color: #1e40af;
  }
  .mtgt-card table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 16px;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .mtgt-card th {
    background: #1e40af;
    color: white;
    padding: 14px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 15px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
  .mtgt-card td {
    padding: 12px 16px;
    border-bottom: 1px solid #e2e8f0;
    color: #334155;
    font-weight: 500;
    vertical-align: top;
  }
  .mtgt-card tr:last-child td {
    border-bottom: none;
  }
  .mtgt-card tr:nth-child(even) {
    background: #f8fafc;
  }
  .mtgt-card .pause-box {
    background: #fffbeb;
    border: 2px dashed #f59e0b;
    border-radius: 12px;
    padding: 24px 28px;
    margin: 28px 0;
  }
  .mtgt-card .pause-box h3 {
    margin: 0 0 10px 0;
    color: #b45309;
    font-size: 20px;
    font-weight: 700;
  }
  .mtgt-card .pause-box p {
    margin: 0;
    color: #78350f;
    font-size: 16px;
  }
  .mtgt-card textarea {
    width: 100%;
    min-height: 28px;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 15px;
    color: #334155;
    background: #fff;
    resize: vertical;
    box-sizing: border-box;
  }
  .mtgt-card textarea:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
  }
  .mtgt-card .cta {
    text-align: center;
    margin-top: 32px;
    font-size: 16px;
    font-weight: 600;
    color: #1e40af;
  }
</style>

<div class="mtgt-card">
  <h1>Step 2: Map Your Segments to Moore's World</h1>
  <div class="subtitle">From algorithmic clusters to strategic identities</div>

  <p><strong>Class,</strong></p>
  <p>
    In the last step, you discovered four hidden tribes inside Hridayam's survey data.
    The algorithm gave them boring names -- <code>segment_1</code>, <code>segment_2</code>, and so on.
    But <strong>you</strong> are the strategist now. Your job is to look at what each tribe
    actually cares about and give them real identities.
  </p>

  <h2>The Theory in One Minute</h2>
  <p>
    Geoffrey Moore says every technology market has five kinds of buyers, arranged in a line:
  </p>

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
    <strong>Here is the crucial idea:</strong> The biggest gap in the entire market is not between any two random segments.
    It is the gap between the <strong>Visionaries</strong> and the <strong>Pragmatists</strong>.
    Moore calls this <strong>the chasm</strong>.
    <br><br>
    Why? Because Visionaries will buy an incomplete product. Pragmatists will not.
    If you try to sell your D2C patch directly to a corporate HR department,
    you are leaping across that chasm without a bridge. That is exactly what happened to Hridayam.
  </div>

  <h2>What You Will Do Now</h2>
  <p>
    The code cell below will open a simple mapper. For each segment the algorithm found,
    you will assign it to one of Moore's five categories.
  </p>
  <p>
    <strong>Before you run it, look at your segment profiles from Step 1.</strong> Ask yourself:
  </p>
  <ul>
    <li>Which segment scores sky-high on <code>Pioneer.Drive</code> and <code>Risk.Tolerance</code> but low on <code>Compliance</code>? Those are your <strong>Visionaries</strong>.</li>
    <li>Which segment demands <code>Clinical.Proof</code>, <code>Integration</code>, and <code>Privacy</code>? Those are your <strong>Pragmatists</strong> -- and they are the other side of the chasm.</li>
    <li>Which segment is low on everything? Those are your <strong>Laggards</strong>. Ignore them.</li>
  </ul>

  <div class="pause-box">
    <h3>Pause and Predict (30 seconds)</h3>
    <p>
      Look at your four segments. Write down your guess for each one <strong>before</strong> you click Auto-Suggest.
    </p>
  </div>

  <table>
    <thead>
      <tr>
        <th style="width:22%">Segment</th>
        <th style="width:35%">My Guess (Moore Category)</th>
        <th style="width:43%">Why?</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>segment_?</code></td>
        <td><textarea rows="1" placeholder="e.g., Early Adopters"></textarea></td>
        <td><textarea rows="1" placeholder="High Pioneer.Drive, low Compliance..."></textarea></td>
      </tr>
      <tr>
        <td><code>segment_?</code></td>
        <td><textarea rows="1" placeholder="e.g., Early Majority"></textarea></td>
        <td><textarea rows="1" placeholder="Demands Clinical.Proof, Integration..."></textarea></td>
      </tr>
      <tr>
        <td><code>segment_?</code></td>
        <td><textarea rows="1" placeholder="e.g., Late Majority"></textarea></td>
        <td><textarea rows="1" placeholder="Very high Risk Aversion..."></textarea></td>
      </tr>
      <tr>
        <td><code>segment_?</code></td>
        <td><textarea rows="1" placeholder="e.g., Laggards"></textarea></td>
        <td><textarea rows="1" placeholder="Low on everything..."></textarea></td>
      </tr>
    </tbody>
  </table>

  <p>
    The algorithm found the clusters. <strong>You</strong> are assigning the strategic meaning.
    This is the moment where data science becomes marketing strategy.
  </p>

  <div class="cta">
    Run the next cell when you are ready.
  </div>
</div>
"""))
