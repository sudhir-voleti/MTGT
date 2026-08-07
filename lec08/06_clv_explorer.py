"""Chunk 6: CLV Proxy Explorer — separate from traction, using WTP + Engagement - Risk."""

if 'df' not in globals():
    raise RuntimeError("Run Chunk 1 first!")

sel_wtp = widgets.SelectMultiple(description='WTP', options=item_cols, rows=4,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['pioneer.drive','data.hunger'])),
    layout=widgets.Layout(width='240px'))
sel_eng = widgets.SelectMultiple(description='Engage', options=item_cols, rows=4,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['social.sharing','support'])),
    layout=widgets.Layout(width='240px'))
sel_risk = widgets.SelectMultiple(description='Risk', options=item_cols, rows=4,
    value=tuple(c for c in item_cols if any(k in c.lower() for k in ['privacy','accuracy','stigma'])),
    layout=widgets.Layout(width='240px'))

btn_clv = widgets.Button(description='▶ Compute CLV', button_style='success')
out = widgets.Output()

def compute_clv(_):
    with out:
        clear_output()
        
        wtp = df[list(sel_wtp.value)].apply(lambda x: normalize(x).mean(), axis=1) if sel_wtp.value else 0.5
        eng = df[list(sel_eng.value)].apply(lambda x: normalize(x).mean(), axis=1) if sel_eng.value else 0.5
        risk = df[list(sel_risk.value)].apply(lambda x: normalize(x).mean(), axis=1) if sel_risk.value else 0.5
        
        # FORMULA: CLV = 0.5*WTP + 0.5*Engagement - 0.3*Risk
        df['CLV_proxy'] = 0.5*wtp + 0.5*eng - 0.3*risk
        df['CLV_proxy'] = df['CLV_proxy'].clip(0.05, 1.0)
        
        # Show formula prominently
        print("=" * 50)
        print("CLV PROXY FORMULA")
        print("=" * 50)
        print("CLV = 0.5 × WTP + 0.5 × Engagement − 0.3 × Risk")
        print("  WTP       = willingness to pay (Pioneer.Drive, Data.Hunger)")
        print("  Engagement = social + support items")
        print("  Risk       = privacy + accuracy + stigma concerns")
        print("=" * 50)
        
        summary = df.groupby(seg_col)['CLV_proxy'].agg(['mean','std','count']).reset_index()
        summary['Moore'] = summary[seg_col].map(moore_map)
        print("\n📊 CLV by Segment:")
        display(summary.round(3))
        
        # Boxplot
        import seaborn as sns
        fig, ax = plt.subplots(figsize=(8,5))
        order = sorted(df[seg_col].dropna().unique(), key=str)
        sns.boxplot(data=df, x=seg_col, y='CLV_proxy', order=order, ax=ax, palette='Set2')
        means = df.groupby(seg_col)['CLV_proxy'].mean().reindex(order)
        ax.scatter(range(len(means)), means, color='black', marker='D', s=60, zorder=5, label='Mean')
        ax.set_title('CLV Proxy Distribution by Segment'); ax.legend()
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')
        plt.tight_layout(); plt.show()

btn_clv.on_click(compute_clv)

display(widgets.VBox([
    widgets.HTML("<h2>Step 6: CLV Proxy Explorer (Standalone)</h2>"),
    widgets.HTML("<p><b>Formula:</b> CLV = 0.5×WTP + 0.5×Engagement − 0.3×Risk</p>"),
    widgets.HBox([sel_wtp, sel_eng, sel_risk]),
    btn_clv,
    out
]))
