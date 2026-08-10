from IPython.display import HTML, display

display(HTML("""
<h3>Part A — Product Rating Task</h3>
<p>You will see 16 electric scooter profiles, one at a time. Each profile describes a specific scooter available in the market. <strong>Rate your likelihood of buying it</strong> on a scale of 1 to 10.</p>
<p><em>1 = "I would definitely not buy this scooter"</em> &nbsp;|&nbsp; <em>10 = "I would definitely buy this scooter"</em></p>

<div style="border:2px solid #003366; border-radius:8px; padding:20px; max-width:600px; margin:20px 0; background:#f8fafc;">
  <div style="font-weight:bold; color:#003366; font-size:1.1em; margin-bottom:12px;">Profile 1 of 16</div>
  <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Brand</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Yana</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Range</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">75 km per charge</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Charging Time</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">4 hours (standard home outlet)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Price</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">₹85,000 (ex-showroom)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Service Network</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">25 cities</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Smart Features</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Basic (digital display, trip meter)</td></tr>
    <tr><td style="padding:6px 0;"><strong>Warranty</strong></td><td style="text-align:right;">2 years on battery and motor</td></tr>
  </table>
  <div style="margin-top:16px;">
    <label style="font-weight:bold;">Your rating (1–10):</label>
    <div style="margin-top:8px; display:flex; gap:6px; font-size:13px;">
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">1</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">2</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">3</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">4</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">5</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">6</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">7</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">8</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">9</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">10</span>
    </div>
  </div>
</div>

<div style="border:2px solid #E37222; border-radius:8px; padding:20px; max-width:600px; margin:20px 0; background:#fffbeb;">
  <div style="font-weight:bold; color:#003366; font-size:1.1em; margin-bottom:12px;">Profile 2 of 16</div>
  <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Brand</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Honda</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Range</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">110 km per charge</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Charging Time</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">1.5 hours (fast charge)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Price</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">₹1,10,000 (ex-showroom)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Service Network</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">100 cities</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Smart Features</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Advanced (app, GPS, OTA, keyless)</td></tr>
    <tr><td style="padding:6px 0;"><strong>Warranty</strong></td><td style="text-align:right;">4 years on battery and motor</td></tr>
  </table>
  <div style="margin-top:16px;">
    <label style="font-weight:bold;">Your rating (1–10):</label>
    <div style="margin-top:8px; display:flex; gap:6px; font-size:13px;">
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">1</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">2</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">3</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">4</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">5</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">6</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">7</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">8</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">9</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">10</span>
    </div>
  </div>
</div>

<div style="border:2px solid #003366; border-radius:8px; padding:20px; max-width:600px; margin:20px 0; background:#f8fafc;">
  <div style="font-weight:bold; color:#003366; font-size:1.1em; margin-bottom:12px;">Profile 3 of 16</div>
  <table style="width:100%; border-collapse:collapse; font-size:14px;">
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Brand</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Ola</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Range</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">150 km per charge</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Charging Time</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">4 hours (standard home outlet)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Price</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">₹1,40,000 (ex-showroom)</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Service Network</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">300 cities</td></tr>
    <tr><td style="padding:6px 0; border-bottom:1px solid #e2e8f0;"><strong>Smart Features</strong></td><td style="border-bottom:1px solid #e2e8f0; text-align:right;">Basic (digital display, trip meter)</td></tr>
    <tr><td style="padding:6px 0;"><strong>Warranty</strong></td><td style="text-align:right;">6 years on battery and motor</td></tr>
  </table>
  <div style="margin-top:16px;">
    <label style="font-weight:bold;">Your rating (1–10):</label>
    <div style="margin-top:8px; display:flex; gap:6px; font-size:13px;">
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">1</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">2</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">3</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">4</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">5</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">6</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">7</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">8</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">9</span>
      <span style="border:1px solid #cbd5e1; padding:4px 10px; border-radius:4px;">10</span>
    </div>
  </div>
</div>
"""))
