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

  <h1>Step 1: Upload and Profile</h1>
  <div class="subtitle">Meet the Data Before You Model It</div>

  <p>You have two files in front of you: a metric conjoint ratings file and a CBC choice file.</p>
  <p>Before you estimate a single coefficient, you must know what is inside.</p>

  <p>Metric conjoint data has a specific structure. Each row is one respondent evaluating one product profile. The columns are the attributes, and the final column is the rating. If you have 400 respondents and 16 profiles each, you should see 6,400 rows.</p>

  <p>CBC data looks different. Each row is one choice task. The respondent chose one alternative from a set. The data is usually in "long" format: one row per alternative per task, with a binary choice indicator.</p>

  <h2>What You Will Do Now</h2>
  <p>The code cell below will open an upload widget. Load either file, inspect its shape, and confirm that the attribute levels match the caselet table.</p>
  <p>Look for missing values, impossible attribute combinations, or respondents who gave the same rating to every profile.</p>

  <div class="pause-box">
    <h3>Pause and Inspect</h3>
    <p>Before you run any model, answer these three questions by looking at the raw data:</p>

    <table>
      <thead>
        <tr>
          <th>Question</th>
          <th>My Answer</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>How many respondents completed all 16 metric profiles?</td>
          <td></td>
        </tr>
        <tr>
          <td>What is the distribution of the 1–10 ratings? Is it skewed?</td>
          <td></td>
        </tr>
        <tr>
          <td>In the CBC data, how often was "None" chosen versus a Yana product?</td>
          <td></td>
        </tr>
      </tbody>
    </table>

    <p>Garbage in, garbage out. Conjoint models are obedient. They will estimate utilities for whatever you feed them.</p>
    <p>Your job is to make sure what you feed them makes sense.</p>
    <p>Run the next cell when you are ready.</p>
  </div>

</div>
"""))
