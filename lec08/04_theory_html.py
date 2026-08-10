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

  <h1>Step 4: Whole Product Gap Analysis</h1>
  <div class="subtitle">The Product Did Not Change. The Context Did.</div>

  <p>In Step 3 you saw the math: Traction = V &times; A &times; E.</p>
  <p>For Hridayam's D2C athletes, all three pillars held up. For B2B enterprise buyers, two pillars collapsed.</p>
  <p>But here is the deeper question: <strong>Why did they collapse?</strong></p>

  <p>The Patch, the App, and the Portal are the same hardware and software in both markets.</p>
  <p>So the collapse is not a product-feature problem. It is a <strong>Whole Product</strong> problem.</p>

  <h2>1. Moore's Four Layers</h2>
  <p>Geoffrey Moore draws four layers around the core innovation:</p>

  <table>
    <thead>
      <tr>
        <th>Layer</th>
        <th>What It Is</th>
        <th>Hridayam Example</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>L1 Generic</strong></td>
        <td>The core innovation that ships in the box</td>
        <td>ECG Patch + App + Portal</td>
      </tr>
      <tr>
        <td><strong>L2 Expected</strong></td>
        <td>Minimum trust and safety any buyer assumes</td>
        <td>Privacy, accuracy, basic encryption</td>
      </tr>
      <tr>
        <td><strong>L3a Evidence</strong></td>
        <td>Proof that the technology works and meets standards</td>
        <td>Clinical studies, FDA clearance, compliance</td>
      </tr>
      <tr>
        <td><strong>L3b Access</strong></td>
        <td>Infrastructure that makes it usable inside an organization</td>
        <td>IT integration, support desk, procurement portal</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p>The D2C athlete bought the Generic product and filled in the gaps themselves.</p>
    <p>The enterprise buyer cannot.</p>
    <p>Without L3a and L3b, the Pragmatist sees an incomplete product and walks away.</p>
  </div>

  <h2>2. How We Detect the Gap</h2>
  <p>For each segment, we look at the four layer scores in order:</p>
  <ol>
    <li>Find the highest layer where the segment scores at least 0.50. That is the ceiling of their demand.</li>
    <li>Look at the very next layer up. If that next layer scores below 0.40, that is <strong>the gap</strong>.</li>
    <li>If no layer reaches 0.50, the segment has <strong>No Core Demand</strong>.</li>
    <li>If the highest layer is L3b, the segment is <strong>Whole Product Ready</strong>.</li>
  </ol>

  <h2>3. What You Will Do Now</h2>
  <p>The code cell below opens the Whole Product mapper.</p>
  <p>You will drag the 12 survey items into the four layers, lock the mapping, and see which segment has which gap.</p>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, look at your segment means from Step 1.</p>
    <p>Which layer do you think is missing for each segment?</p>

<table style="width:100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; font-size: 14.5px;">
  <thead>
    <tr>
      <th style="background-color: #003366; color: white; padding: 11px 14px; text-align: left; border: 1px solid #003366;">Segment</th>
      <th style="background-color: #003366; color: white; padding: 11px 14px; text-align: left; border: 1px solid #003366;">My Prediction: Highest Layer They Accept</th>
      <th style="background-color: #003366; color: white; padding: 11px 14px; text-align: left; border: 1px solid #003366;">My Prediction: The Gap</th>
      <th style="background-color: #003366; color: white; padding: 11px 14px; text-align: left; border: 1px solid #003366;">Why?</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #d0d7de; background-color: #f8fafc; font-weight: 600;">Visionaries / Early Adopters</td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="e.g. L1 / L2 / L3a / L3b" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="e.g. L3a Evidence" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="Your reasoning…" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #d0d7de; font-weight: 600;">Pragmatists / Early Majority</td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de;">
        <input type="text" placeholder="e.g. L1 / L2 / L3a / L3b" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de;">
        <input type="text" placeholder="e.g. L3b Access" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de;">
        <input type="text" placeholder="Your reasoning…" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
    </tr>
    <tr>
      <td style="padding: 10px 14px; border: 1px solid #d0d7de; background-color: #f8fafc; font-weight: 600;">Skeptics / Late Majority</td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="e.g. L1 / L2 / L3a / L3b" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="e.g. No Core Demand" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
      <td style="padding: 8px 10px; border: 1px solid #d0d7de; background-color: #f8fafc;">
        <input type="text" placeholder="Your reasoning…" style="width:100%; padding:6px 8px; border:1px solid #cbd5e1; border-radius:4px; font-size:14px; box-sizing:border-box;">
      </td>
    </tr>
  </tbody>
</table>


    <p>The chasm is not a competitive gap. It is a column of missing layers.</p>
    <p>Your job is to find exactly which column is empty.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
