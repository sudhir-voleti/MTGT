# -*- coding: utf-8 -*-
"""
Lec09 — Step 3b Theory: Segmentation on Part-Worths
Pure HTML content cell. Run in Colab via:
  exec(requests.get('https://raw.githubusercontent.com/sudhir-voleti/MTGT/main/lec09/v1/03b_theory.py').text)
"""

from IPython.display import HTML, display

display(HTML("""
<style>
  .caselet-body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; 
                  font-size: 15px; line-height: 1.55; color: #1e293b; max-width: 860px; margin: 0 auto; }
  .caselet-body h1 { font-size: 1.55em; color: #003366; margin: 0 0 6px 0; }
  .caselet-body h2 { font-size: 1.2em; color: #003366; border-bottom: 2px solid #E37222; 
                     padding-bottom: 4px; margin-top: 28px; }
  .caselet-body h3 { font-size: 1.05em; color: #003366; margin-top: 20px; }
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

  <h1>Segmentation: Finding Buyer Personas in Part-Worths</h1>

  <h2>1. Why Segment on Part-Worths, Not Demographics?</h2>
  <p>Demographics tell you <em>who</em> the respondent is — age, income, city. Part-worths tell you <em>what they will buy</em>. A 28-year-old software engineer in Bangalore might look identical to a 45-year-old bank manager in Pune on paper, but if one values smart features and the other values service coverage, they are different <em>buyers</em>.</p>

  <div class="callout">
    <p><strong>Behavioral segmentation:</strong> Group respondents by what they value, not who they are. The clustering input is the estimated part-worth vector — typically 10–20 numbers per person that encode their preference DNA.</p>
  </div>

  <h2>2. The Elbow Criterion: How Many Segments?</h2>
  <p>K-Means requires you to specify K (number of clusters) in advance. But how do you choose?</p>
  <p>The <strong>elbow method</strong> runs K-Means for K = 2, 3, 4, 5, 6 and plots the <em>inertia</em> — the total within-cluster sum of squared distances. As K increases, inertia always falls (more clusters = tighter clusters). The "elbow" is the point where adding another cluster stops giving you a meaningful drop. That is your K.</p>

  <h2>3. Part-Worths as Behavioral DNA</h2>
  <p>Each respondent's part-worth vector is a point in high-dimensional space. Two respondents with similar vectors are "preference neighbors" — they want similar products. K-Means partitions this space into regions, each region becoming a segment.</p>
  <p>The output is not just a label. It is a <em>profile</em> — the mean part-worths of everyone in that cluster. That profile tells you what the segment values, what it ignores, and what product configuration would win them over.</p>

  <div class="pause-box">
    <h3>Before You Run: Guess the Elbow</h3>
    <p>How many distinct buyer types do you think exist in this market? Write your guess before seeing the plot.</p>
    <table class="scribble-table">
      <thead><tr><th>My Guess for K</th><th>Why this many segments?</th></tr></thead>
      <tbody>
        <tr>
          <td><textarea placeholder="e.g., 3 — Tech, Pragmatist, PriceHunter..."></textarea></td>
          <td><textarea placeholder="Your reasoning..."></textarea></td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="pause-box">
    <h3>Where Do the "True" Segments Come From?</h3>
    <p>If your data has a <code>Segment</code> column (Tech / Pragmatist / PriceHunter), that is the <strong>ground truth</strong> used to generate this synthetic dataset. In real data, you will not have this column — you will only have the clusters you discover yourself. We show the ground truth here so you can check whether your clustering recovered the true structure.</p>
  </div>

</div>
"""))
