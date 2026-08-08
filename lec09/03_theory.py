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

  <h1>Step 3: Segmentation — Finding Tribes in Preferences</h1>
  <div class="subtitle">From Part-Worths to People</div>

  <p>In Step 2, you estimated 400 individual regression models. Each model is a preference fingerprint — a unique combination of part-worths that describes what one person values.</p>
  <p>But you cannot build 400 products. You need tribes.</p>
  <p>The question is not "What does each person want?" The question is "Do people cluster into groups who want similar things?"</p>

  <h2>1. Two Philosophies of Segmentation</h2>

  <table>
    <thead>
      <tr>
        <th>Approach</th>
        <th>When You Use It</th>
        <th>What You Need</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>A priori</strong></td>
        <td>You believe you know the segments already</td>
        <td>Psychographic screener (Part C of survey)</td>
      </tr>
      <tr>
        <td><strong>Post-hoc</strong></td>
        <td>You let the data find the segments</td>
        <td>Part-worth vectors from Step 2</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <p>The a priori approach says: "I think Tech Enthusiasm drives EV adoption. Let me test that belief."</p>
    <p>The post-hoc approach says: "I have no idea. Let the utilities cluster themselves."</p>
    <p>Both are valid. The post-hoc approach is more common in conjoint because it uses the same data twice — once to estimate preferences, once to find segments.</p>
    <p>But the a priori approach is more defensible to a skeptical audience because it was hypothesized before the data was collected.</p>
  </div>

  <h2>2. What You Will Do Now</h2>
  <p>The code cell below opens the Segmentation Tool. You will:</p>
  <ol>
    <li>Confirm or upload the part-worths from Step 2.</li>
    <li>Select which part-worth columns to use for clustering.</li>
    <li>Choose K (number of clusters). Start with 3.</li>
    <li>Run K-means. Name each cluster by its profile.</li>
    <li>Validate: If you have true segment labels or psychographic data, check whether the behavioral clusters match the attitudinal clusters.</li>
  </ol>

  <div class="pause-box">
    <h3>Pause and Predict</h3>
    <p>Before you run the cell, predict what K-means will find. Will there be 3 clean clusters? Will they align with the psychographic items?</p>

    <table>
      <thead>
        <tr>
          <th>My Prediction</th>
          <th>K = ?</th>
          <th>Cluster 1 Name</th>
          <th>Cluster 2 Name</th>
          <th>Cluster 3 Name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>If your post-hoc clusters match your a priori expectations, you have both discovery and validation in one step.</p>
    <p>If they do not match, you have learned something your hypotheses missed.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
