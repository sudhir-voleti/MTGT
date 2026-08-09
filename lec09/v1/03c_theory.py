# -*- coding: utf-8 -*-
"""
Lec09 — Step 3c Theory: Exploring Part-Worth Space with Scatterplots
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03c_theory.py').text)
"""

from IPython.display import HTML, display

display(HTML("""
<style>
  .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                  font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
  .caselet-body h1 { font-size: 1.55em; color: #003366; margin: 0 0 6px 0; }
  .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                     padding-bottom: 4px; margin-top: 28px; }
  .caselet-body p { margin: 10px 0; }
  .caselet-body ul { margin: 8px 0 12px 22px; }
  .caselet-body li { margin: 4px 0; }
  .caselet-body .callout { background: #f0f7ff; border-left: 5px solid #003366; padding: 14px 18px; margin: 18px 0; }
  .caselet-body .pause-box { background: #fffbeb; border: 1px dashed #d97706; padding: 16px 18px; margin: 22px 0; }
  .caselet-body .pause-box h3 { font-size: 1.05em; color: #003366; margin-top: 0; }
  .caselet-body textarea { width: 100%; min-height: 50px; padding: 8px 10px; 
                            border: 1px solid #cbd5e1; border-radius: 6px; 
                            font-family: inherit; font-size: 14px; box-sizing: border-box; resize: vertical; }
  .caselet-body .scribble-table th { background-color: #475569; color: white; 
                                      font-size: 13.5px; padding: 9px 12px; text-align: left; }
  .caselet-body .scribble-table td { padding: 8px 12px; vertical-align: top; border: 1px solid #d0d7de; }
</style>

<div class="caselet-body">

  <h1>Exploring Part-Worth Space: Scatterplots</h1>

  <h2>1. What Is a Part-Worth Scatterplot?</h2>
  <p>Each respondent is a point. The X-axis is their estimated part-worth for one attribute level; the Y-axis is their part-worth for another. Where the point lands tells you what kind of buyer they are.</p>

  <div class="callout">
    <p><strong>Example:</strong> If X = <em>Smart_Advanced</em> and Y = <em>Brand_Ola</em>, a point in the top-right corner is a Tech enthusiast who loves both smart features and the Ola brand. A point in the bottom-left cares about neither.</p>
  </div>

  <h2>2. Why This Matters</h2>
  <p>Clustering (K-Means) gives you segment labels, but scatterplots let you <em>see</em> the segments as clouds in 2D space. You can:</p>
  <ul>
    <li><strong>Verify clusters:</strong> Do the K-Means clusters actually form tight clouds, or are they spread out?</li>
    <li><strong>Find outliers:</strong> Who is the extreme respondent at (2.5, 3.0)? What product would win them?</li>
    <li><strong>Discover trade-offs:</strong> Are Smart and Price negatively correlated? If so, respondents who want smart features accept higher prices — a pricing insight.</li>
  </ul>

  <h2>3. Where Do the Segments Come From?</h2>
  <p>If your data has a <code>Segment</code> column, that is the <strong>ground truth</strong> — the true buyer type used to generate this synthetic dataset. In real data, you will not have this. Instead, you will color by the <strong>Cluster</strong> labels you discovered in Step 3b.</p>
  <p>The scatterplot lets you check: did your clustering recover the true structure? Do the colored clouds overlap or separate cleanly?</p>

  <div class="pause-box">
    <h3>Before You Explore: Pick Your Axes</h3>
    <p>Which two attribute levels do you think will separate the segments most clearly? Write your prediction before building the plot.</p>
    <table class="scribble-table">
      <thead><tr><th>X-axis (attribute level)</th><th>Y-axis (attribute level)</th><th>Why these two?</th></tr></thead>
      <tbody>
        <tr>
          <td><textarea placeholder="e.g., Brand_Ola..."></textarea></td>
          <td><textarea placeholder="e.g., Smart_Advanced..."></textarea></td>
          <td><textarea placeholder="Because Tech buyers love both..."></textarea></td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
"""))
