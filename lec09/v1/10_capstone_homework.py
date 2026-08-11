# -*- coding: utf-8 -*-
"""
Lec10 Capstone Homework — Agent Infrastructure GTM
Render inline HTML for Colab via: exec(requests.get(BASE + "10_capstone_homework.py").text)
"""

from IPython.display import display, HTML

HTML_BLOCK = """
<style>
  .hw-body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 15px;
    line-height: 1.55;
    color: #1e293b;
    max-width: 900px;
    margin: 0 auto;
  }
  .hw-body h1 {
    font-size: 1.45em;
    color: #003366;
    margin: 0 0 6px 0;
  }
  .hw-body .subtitle {
    font-size: 1.0em;
    color: #475569;
    margin-bottom: 20px;
  }
  .hw-body h2 {
    font-size: 1.15em;
    color: #003366;
    border-bottom: 2px solid #E37222;
    padding-bottom: 4px;
    margin-top: 24px;
  }
  .hw-body h3 {
    font-size: 1.05em;
    color: #003366;
    margin-top: 18px;
  }
  .hw-body p {
    margin: 10px 0;
  }
  .hw-body ul, .hw-body ol {
    margin: 8px 0 12px 22px;
  }
  .hw-body li {
    margin: 5px 0;
  }
  .hw-body .callout {
    background: #f0f7ff;
    border-left: 5px solid #003366;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .hw-body .note {
    background: #fffbeb;
    border: 1px dashed #d97706;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .hw-body .danger {
    background: #fef2f2;
    border-left: 5px solid #dc2626;
    padding: 14px 18px;
    margin: 18px 0;
  }
  .hw-body code {
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 13.5px;
  }
  .hw-body pre {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 14px 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 13.5px;
    line-height: 1.5;
  }
  .hw-body table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin: 14px 0 18px;
  }
  .hw-body th {
    background-color: #003366;
    color: white;
    padding: 10px 12px;
    text-align: left;
    border: 1px solid #003366;
  }
  .hw-body td {
    padding: 9px 12px;
    border: 1px solid #d0d7de;
    vertical-align: top;
  }
  .hw-body tr:nth-child(even) td {
    background-color: #f8fafc;
  }
  .hw-body textarea {
    width: 100%;
    min-height: 60px;
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-family: inherit;
    font-size: 14px;
    margin-top: 6px;
    box-sizing: border-box;
  }
  .hw-body .isenberg-list {
    font-size: 13.5px;
    line-height: 1.6;
    column-count: 2;
    column-gap: 30px;
    margin: 14px 0;
  }
  .hw-body .isenberg-list li {
    margin: 3px 0;
    break-inside: avoid;
  }
  @media (max-width: 700px) {
    .hw-body .isenberg-list {
      column-count: 1;
    }
  }
</style>

<div class="hw-body">

  <h1>Lec10 Capstone: GTM for Agent Infrastructure</h1>
  <div class="subtitle">Group Homework &nbsp;|&nbsp; MTGT @ ISB &nbsp;|&nbsp; PGPYL</div>

  <div class="callout">
    <strong>The brief:</strong> You have spent four sessions learning to size markets, segment customers, diagnose traction, and optimize product bundles using conjoint analysis. In this capstone, you apply the <em>entire arc</em> to a product that does <strong>not exist yet</strong>.
  </div>

  <h2>0. The Raw Material — 21 Agent-Startup Ideas</h2>
  <p>Pick <strong>one</strong> idea from the list below. Each is an infrastructure need for the emerging agent economy.</p>
  <ol class="isenberg-list">
    <li>Default tool inside agent harnesses (the new default app)</li>
    <li>Spend controls for agents (Ramp for machines)</li>
    <li>Shared memory / brain that agents read and write to</li>
    <li>Sandbox environments for agents (safe Stripe, safe APIs)</li>
    <li>Docs-as-product (agents onboard by reading your docs)</li>
    <li>Agent reputation / track record before trust</li>
    <li>Permission layer: prove the agent acts for a real person</li>
    <li>Escrow for machines (pay on verified job completion)</li>
    <li>Agent replay / "why did my agent do that" debugger</li>
    <li>Agent court for refunds and disputes between machines</li>
    <li>Throwaway virtual cards per agent task</li>
    <li>High-throughput API access sold to agents</li>
    <li>Negotiation protocol for agent-to-agent deals</li>
    <li>Legal and insurance layer for agent actions</li>
    <li>Always-on compute box that hosts the agent</li>
    <li>Physical-world robots with wallets (warehouse, home)</li>
    <li>Marketplace for machine labor (agent hires robot)</li>
    <li>Verification of real-world work (photos, sensors)</li>
    <li>Version control for agent prompts and skills</li>
    <li>Agent-to-agent subscription (specialist agents)</li>
    <li>Job board where only agents apply (Fiverr for machines)</li>
  </ol>

  <h2>1. The Problem & The Idea (Slide 1)</h2>
  <ul>
    <li>State the idea in <strong>one sentence</strong>.</li>
    <li>Name the <strong>agent buyer</strong> (the machine or the human procuring for it).</li>
    <li>Why is this a chasm problem? What blocks adoption between innovator agents and enterprise agents?</li>
  </ul>
  <textarea placeholder="Write your answer here..."></textarea>

  <h2>2. The Attribute Space (Slides 2–3)</h2>
  <p>List <strong>4 attributes</strong> an agent buyer would trade off. Give <strong>2–3 levels per attribute</strong>. Compute the full factorial.</p>
  <table>
    <thead>
      <tr><th>Attribute</th><th>Level 1</th><th>Level 2</th><th>Level 3</th></tr>
    </thead>
    <tbody>
      <tr><td>1. _____________</td><td></td><td></td><td></td></tr>
      <tr><td>2. _____________</td><td></td><td></td><td></td></tr>
      <tr><td>3. _____________</td><td></td><td></td><td></td></tr>
      <tr><td>4. _____________</td><td></td><td></td><td></td></tr>
    </tbody>
  </table>
  <p><strong>Full factorial count:</strong> ___ × ___ × ___ × ___ = <strong>___ configurations</strong></p>
  <p><strong>Defense:</strong> Why these 4 attributes and not others?</p>
  <textarea placeholder="Write your defense here..."></textarea>

  <h2>3. Whole Product Stack (Slide 4)</h2>
  <table>
    <thead>
      <tr><th>Level</th><th>Name</th><th>What it is for your idea</th></tr>
    </thead>
    <tbody>
      <tr><td>L1</td><td>Generic Product</td><td></td></tr>
      <tr><td>L2</td><td>Expected Product</td><td></td></tr>
      <tr><td>L3</td><td>Augmented Product</td><td></td></tr>
      <tr><td>L4</td><td>Potential Product</td><td></td></tr>
    </tbody>
  </table>
  <p><strong>The chasm:</strong> Which layer is missing from the market today, and why does its absence kill adoption for your Pragmatist-equivalent persona?</p>
  <textarea placeholder="Write your answer here..."></textarea>

  <h2>4. Agent Personas & Traction (Slides 5–6)</h2>
  <p>Define <strong>3 agent personas</strong> (archetypes, not humans).</p>
  <table>
    <thead>
      <tr><th>Persona</th><th>Type</th><th>Dominant Pillar</th><th>Heuristic Override</th><th>Reservation Utility</th></tr>
    </thead>
    <tbody>
      <tr><td>1</td><td></td><td></td><td></td><td></td></tr>
      <tr><td>2</td><td></td><td></td><td></td><td></td></tr>
      <tr><td>3</td><td></td><td></td><td></td><td></td></tr>
    </tbody>
  </table>
  <p><strong>Beachhead:</strong> Which persona is your target? Compute their pseudo-Traction score under your proposed L1+L2+L3 configuration.</p>
  <pre>
Traction = V × A × E
V = ___ (justify)
A = ___ (justify)
E = ___ (justify)
Traction = ___ × ___ × ___ = ___
  </pre>
  <textarea placeholder="Write your justification here..."></textarea>

  <h2>5. The $300K Budget & CBC Task (Slides 7–8)</h2>
  <div class="danger">
    <strong>Budget constraint:</strong> You have $300K. Engineering quotes: L1 = $150K, L2 = $50K, L3 = $200K. You <strong>cannot</strong> afford all three. You must skip or under-invest in one layer.
  </div>
  <p><strong>Your allocation:</strong></p>
  <table>
    <thead>
      <tr><th>Layer</th><th>Amount</th><th>Justification (one sentence)</th></tr>
    </thead>
    <tbody>
      <tr><td>L1 Generic</td><td>$___</td><td></td></tr>
      <tr><td>L2 Expected</td><td>$___</td><td></td></tr>
      <tr><td>L3 Augmented</td><td>$___</td><td></td></tr>
      <tr><td><strong>Total</strong></td><td><strong>$300K</strong></td><td></td></tr>
    </tbody>
  </table>
  <p><strong>What happens to Traction if you skip your chosen layer?</strong></p>
  <textarea placeholder="Write your answer here..."></textarea>

  <p><strong>Design one CBC choice task:</strong></p>
  <pre>
Product A (Your solution):
  Attribute 1: ___
  Attribute 2: ___
  Attribute 3: ___
  Attribute 4: ___

Product B (Competitor 1):
  Attribute 1: ___
  Attribute 2: ___
  Attribute 3: ___
  Attribute 4: ___

Product C (Competitor 2):
  Attribute 1: ___
  Attribute 2: ___
  Attribute 3: ___
  Attribute 4: ___

Product D (None):
  What "None" means for an agent buyer: ___________________________
  </pre>
  <p><strong>Expected choice:</strong> Which product does your beachhead persona choose, and why?</p>
  <textarea placeholder="Write your answer here..."></textarea>

  <h2>6. Validation Before Building (Final Slide)</h2>
  <ul>
    <li><strong>Qualitative method (Lec04–06):</strong> Which one would you run first to discover if your attributes are even relevant?</li>
    <li><strong>Quantitative method (Lec09):</strong> Which one would you run second to validate that your L3 layer actually moves the E pillar?</li>
    <li><strong>Why not conjoint first?</strong> In one sentence, why would running conjoint before FGDs be a mistake here?</li>
  </ul>
  <textarea placeholder="Write your answers here..."></textarea>

  <h2>Deliverable Specs</h2>
  <div class="note">
    <strong>Format:</strong> 5–6 minute group presentation. Max <strong>8 slides</strong>. No code, no live demo. Strategy, numbers, and narrative only.<br><br>
    <strong>Due:</strong> Start of Lec10. No extensions.<br><br>
    <strong>Q&A:</strong> 2 minutes from instructor per group.
  </div>

  <h2>Grading Criteria</h2>
  <table>
    <thead>
      <tr><th>Criterion</th><th>Weight</th><th>What "Excellent" Looks Like</th></tr>
    </thead>
    <tbody>
      <tr>
        <td>Attribute decomposition</td>
        <td>20%</td>
        <td>4 attributes are non-obvious, agent-specific, and justified. Levels are realistic. Full factorial stated.</td>
      </tr>
      <tr>
        <td>Whole Product clarity</td>
        <td>20%</td>
        <td>L1–L4 are distinct and correctly mapped. The chasm is a specific missing layer, not generic "trust."</td>
      </tr>
      <tr>
        <td>Persona + Traction rigor</td>
        <td>20%</td>
        <td>3 personas differentiated by pillar. Traction score is multiplicative. Reservation utility is specific.</td>
      </tr>
      <tr>
        <td>Budget + CBC design</td>
        <td>20%</td>
        <td>Budget defended with trade-off logic. CBC uses valid levels. "None" is defined for agents.</td>
      </tr>
      <tr>
        <td>Validation sequencing</td>
        <td>20%</td>
        <td>Qualitative method fits discovery. Quantitative method fits validation. "Why not conjoint first" shows understanding of exploratory vs. confirmatory research.</td>
      </tr>
    </tbody>
  </table>

</div>
"""

display(HTML(HTML_BLOCK))
