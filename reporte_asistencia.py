import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard — Lista de asistencia",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [class*="css"] { font-family: Arial, sans-serif; }
.block-container { padding: 2rem 3rem 3rem; max-width: 1400px; }
.metric-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.metric-val { font-size: 2rem; font-weight: 600; margin: 0; }
.metric-lbl { font-size: 0.8rem; color: #6b7280; margin: 4px 0 0; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-sub { font-size: 0.75rem; color: #9ca3af; margin: 4px 0 0; }
.section-title { font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem; }
.chart-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.tag-red { background:#fee2e2; color:#991b1b; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.tag-amber { background:#fef3c7; color:#92400e; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.tag-green { background:#d1fae5; color:#065f46; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }
.pending-banner {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
}
hr { border: none; border-top: 1px solid #f3f4f6; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    "red":    "#e24b4a",
    "amber":  "#ba7517",
    "green":  "#1d9e75",
    "blue":   "#2563eb",
    "gray":   "#6b7280",
    "red_l":  "#fee2e2",
    "amber_l":"#fef3c7",
    "green_l":"#d1fae5",
    "blue_l": "#eff6ff",
    "grid":   "#f3f4f6",
    "text":   "#374151",
    "muted":  "#9ca3af",
}

CHART_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial, sans-serif", color=COLORS["text"]),
    margin=dict(t=20, b=40, l=50, r=20),
    height=340,
)

def axis_style(title=""):
    return dict(
        title=title, title_font=dict(size=11, color=COLORS["muted"]),
        tickfont=dict(size=11, color=COLORS["text"]),
        gridcolor=COLORS["grid"], showgrid=True,
        zeroline=False, linecolor="#e5e7eb", showline=True
    )

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem">
  <p style="font-size:0.8rem;color:#9ca3af;margin:0;text-transform:uppercase;letter-spacing:0.08em">Base de datos: abrhil · Tenant analizado: aamx09 · 2026-06-09</p>
  <h1 style="font-size:1.75rem;font-weight:600;color:#111827;margin:4px 0 0">Análisis de rendimiento — módulo lista de asistencia</h1>
  <p style="color:#6b7280;margin:6px 0 0;font-size:0.9rem">Evidencia recopilada en DBeaver mediante consultas directas a PostgreSQL</p>
</div>
""", unsafe_allow_html=True)

# ─── MÉTRICAS ─────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5 = st.columns(5)
metrics = [
    (c1, "1,761",   "workers en aamx09",      "confirmado con COUNT(*)",  "#111827"),
    (c2, "17",      "días en el rango",        "23 mayo — 8 junio 2026",  "#111827"),
    (c3, "× 2",     "repeticiones por fecha",  "SELECT + WHERE/CASE",     "#111827"),
    (c4, "59,874",  "subqueries por carga",    "1,761 × 17 × 2",          COLORS["red"]),
    (c5, "~22 seg", "tiempo estimado en BD",   "0.375ms × 59,874 subq",   COLORS["red"]),
]
for col, val, lbl, sub, color in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <p class="metric-val" style="color:{color}">{val}</p>
          <p class="metric-lbl">{lbl}</p>
          <p class="metric-sub">{sub}</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILA 1: crecimiento + comparativa SELECT vs WHERE ────────────────────────
st.markdown('<p class="section-title">Impacto del error según cantidad de workers</p>', unsafe_allow_html=True)
col_a, col_b = st.columns(2)

workers_pts = [50, 100, 200, 312, 500, 800, 1000, 1761]
subq_total  = [w * 34 for w in workers_pts]
subq_colors = [COLORS["green"] if s < 10000 else COLORS["amber"] if s < 30000 else COLORS["red"] for s in subq_total]

with col_a:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(w) for w in workers_pts],
        y=subq_total,
        marker_color=subq_colors,
        marker_line_width=0,
        text=[f"{s:,}" for s in subq_total],
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>%{x} workers</b><br>%{y:,} subqueries<extra></extra>"
    ))
    fig.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Subqueries generadas por carga del módulo", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style("Workers en el tenant"),
        yaxis=dict(**axis_style("Subqueries"), tickformat=","),
        showlegend=False, bargap=0.35
    )
    fig.add_hline(y=29937, line_dash="dot", line_color=COLORS["amber"], line_width=1.5,
                  annotation_text="aamx09 actual (Error 1 solo)", annotation_font_size=10,
                  annotation_font_color=COLORS["amber"])
    fig.add_annotation(x="1761", y=59874*1.18, text="<b>aamx09<br>59,874</b>",
                       showarrow=False, font=dict(color=COLORS["red"], size=10))
    st.plotly_chart(fig, width="stretch")

with col_b:
    cats = ["Solo Error 1<br>(SELECT)", "Error 1 + Error 2<br>(SELECT + WHERE)"]
    vals = [29937, 59874]
    fig2 = go.Figure(go.Bar(
        x=cats, y=vals,
        marker_color=[COLORS["amber"], COLORS["red"]],
        marker_line_width=0,
        text=[f"{v:,}" for v in vals],
        textposition="outside", textfont=dict(size=12, color=COLORS["text"]),
        width=0.4,
        hovertemplate="<b>%{x}</b><br>%{y:,} subqueries<extra></extra>"
    ))
    fig2.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Impacto de cada error por separado — aamx09", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style(),
        yaxis=dict(**axis_style("Subqueries"), tickformat=","),
        showlegend=False, bargap=0.4
    )
    fig2.add_annotation(x=1, y=59874*0.5,
        text="<b>+29,937 extra</b><br>por duplicación<br>en WHERE/CASE",
        showarrow=False, font=dict(color="white", size=11),
        bgcolor=COLORS["red"], borderpad=6, bordercolor=COLORS["red"])
    st.plotly_chart(fig2, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILA 2: tiempo estimado + EXPLAIN ANALYZE ────────────────────────────────
st.markdown('<p class="section-title">Tiempo de respuesta y evidencia de EXPLAIN ANALYZE</p>', unsafe_allow_html=True)
col_c, col_d = st.columns(2)

tiempos = [round(w * 34 * 0.000375, 2) for w in workers_pts]
time_colors = [COLORS["green"] if t < 5 else COLORS["amber"] if t < 15 else COLORS["red"] for t in tiempos]

with col_c:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=[str(w) for w in workers_pts],
        y=tiempos,
        mode="lines+markers",
        line=dict(color=COLORS["red"], width=2.5),
        marker=dict(color=time_colors, size=9, line=dict(color="white", width=2)),
        fill="tozeroy", fillcolor="rgba(226,75,74,0.07)",
        hovertemplate="<b>%{x} workers</b><br>%{y:.1f} segundos estimados<extra></extra>"
    ))
    fig3.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Tiempo estimado en BD por cantidad de workers (seg)", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style("Workers en el tenant"),
        yaxis=axis_style("Segundos"),
        showlegend=False
    )
    fig3.add_annotation(x="1761", y=22.4,
        text="<b>aamx09: ~22 seg</b>", showarrow=True, arrowhead=2,
        arrowcolor=COLORS["red"], font=dict(color=COLORS["red"], size=10),
        ax=-60, ay=-30)
    fig3.add_hrect(y0=0, y1=5, fillcolor=COLORS["green_l"], opacity=0.4, line_width=0)
    fig3.add_hrect(y0=5, y1=15, fillcolor=COLORS["amber_l"], opacity=0.4, line_width=0)
    fig3.add_hrect(y0=15, y1=max(tiempos)*1.2, fillcolor=COLORS["red_l"], opacity=0.3, line_width=0)
    fig3.add_annotation(x="50", y=2.5, text="Leve", showarrow=False, font=dict(color=COLORS["green"], size=10))
    fig3.add_annotation(x="50", y=10, text="Medio", showarrow=False, font=dict(color=COLORS["amber"], size=10))
    fig3.add_annotation(x="50", y=19, text="Crítico", showarrow=False, font=dict(color=COLORS["red"], size=10))
    st.plotly_chart(fig3, width="stretch")

with col_d:
    explain_labels = ["Sin índice<br>(Seq Scan)", "Con índice<br>(Bitmap Scan)"]
    explain_vals   = [0.926, 0.375]
    fig4 = go.Figure(go.Bar(
        x=explain_labels, y=explain_vals,
        marker_color=[COLORS["red"], COLORS["green"]],
        marker_line_width=0,
        text=[f"{v} ms" for v in explain_vals],
        textposition="outside", textfont=dict(size=13, color=COLORS["text"]),
        width=0.35,
        hovertemplate="<b>%{x}</b><br>%{y} ms por subquery<extra></extra>"
    ))
    fig4.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Tiempo por subquery individual — EXPLAIN ANALYZE aamx09", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style(),
        yaxis=axis_style("Milisegundos"),
        showlegend=False, bargap=0.4
    )
    fig4.add_annotation(x=0, y=0.926/2,
        text="<b>Rows removed: 4,706</b><br>lee toda la tabla",
        showarrow=False, font=dict(color="white", size=10),
        bgcolor=COLORS["red"], borderpad=5)
    fig4.add_annotation(x=1, y=0.375/2,
        text="<b>shared hit: 5</b><br>solo lee 5 bloques",
        showarrow=False, font=dict(color="white", size=10),
        bgcolor=COLORS["green"], borderpad=5)
    st.plotly_chart(fig4, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILA 3: tenants ──────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Comparativa entre tenants</p>', unsafe_allow_html=True)

st.markdown("""
<div class="pending-banner">
<strong>Datos parciales:</strong> Los registros de SalaryMovementRecord se usan como aproximación de workers para aamx01, aamx02, aamx03 y aamx04. 
El conteo real de workers y la verificación de índices en esos tenants está pendiente de confirmar.
</div>
""", unsafe_allow_html=True)

tenants   = ["aamx02", "aamx04", "aamx09", "aamx03", "aamx01"]
registros = [141,       974,      4709,     6445,     13831]
t_colors  = [COLORS["green"] if r < 1000 else COLORS["amber"] if r < 5000 else COLORS["red"] for r in registros]

col_e, col_f = st.columns(2)

with col_e:
    fig5 = go.Figure(go.Bar(
        x=tenants, y=registros,
        marker_color=t_colors, marker_line_width=0,
        text=[f"{r:,}" for r in registros],
        textposition="outside", textfont=dict(size=11),
        hovertemplate="<b>%{x}</b><br>%{y:,} registros<extra></extra>"
    ))
    fig5.update_layout(
        **CHART_LAYOUT,
        title=dict(text="Registros en SalaryMovementRecord por tenant", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style("Tenant"),
        yaxis=dict(**axis_style("Registros"), tickformat=","),
        showlegend=False, bargap=0.4
    )
    st.plotly_chart(fig5, width="stretch")

with col_f:
    t_idx_tiempo  = [round(r * 34 * 0.000375, 1) for r in registros]
    t_noidx_tiempo = [round(r * 34 * 0.0022,  1) for r in registros]

    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        name="Con índice (0.375ms/subq)",
        x=tenants, y=t_idx_tiempo,
        marker_color=COLORS["green"], marker_line_width=0,
        text=[f"{v}s" for v in t_idx_tiempo],
        textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>%{x}</b> con índice<br>%{y}s estimados<extra></extra>"
    ))
    fig6.add_trace(go.Bar(
        name="Sin índice (2.2ms/subq)",
        x=tenants, y=t_noidx_tiempo,
        marker_color=COLORS["red"], marker_line_width=0,
        text=[f"{v}s" for v in t_noidx_tiempo],
        textposition="outside", textfont=dict(size=10),
        hovertemplate="<b>%{x}</b> sin índice<br>%{y}s estimados<extra></extra>"
    ))
    fig6.update_layout(
        **dict(CHART_LAYOUT, height=360),
        title=dict(text="Tiempo estimado en BD: con índice vs sin índice por tenant", font=dict(size=13, color=COLORS["text"]), x=0),
        xaxis=axis_style("Tenant"),
        yaxis=axis_style("Segundos"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
        barmode="group", bargap=0.3, bargroupgap=0.05
    )
    st.plotly_chart(fig6, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ─── FILA 4: niveles de impacto ───────────────────────────────────────────────
st.markdown('<p class="section-title">Escala de impacto según workers del tenant</p>', unsafe_allow_html=True)

workers_full = list(range(50, 2000, 50))
subq_full    = [w * 34 for w in workers_full]
tiempo_full  = [round(w * 34 * 0.000375, 2) for w in workers_full]

fig7 = go.Figure()
fig7.add_trace(go.Scatter(
    x=workers_full, y=tiempo_full,
    mode="lines", line=dict(color=COLORS["red"], width=2.5),
    fill="tozeroy", fillcolor="rgba(226,75,74,0.05)",
    hovertemplate="<b>%{x} workers</b><br>~%{y:.1f} seg estimados<extra></extra>"
))
fig7.add_vrect(x0=0,   x1=300,  fillcolor=COLORS["green_l"], opacity=0.5, line_width=0, annotation_text="Leve", annotation_position="top left", annotation_font_color=COLORS["green"], annotation_font_size=11)
fig7.add_vrect(x0=300, x1=800,  fillcolor=COLORS["amber_l"], opacity=0.5, line_width=0, annotation_text="Medio", annotation_position="top left", annotation_font_color=COLORS["amber"], annotation_font_size=11)
fig7.add_vrect(x0=800, x1=2000, fillcolor=COLORS["red_l"],   opacity=0.4, line_width=0, annotation_text="Crítico", annotation_position="top left", annotation_font_color=COLORS["red"], annotation_font_size=11)
fig7.add_vline(x=1761, line_dash="dash", line_color=COLORS["red"], line_width=1.5,
               annotation_text="aamx09 (1,761 workers)", annotation_font_color=COLORS["red"], annotation_font_size=10)
fig7.update_layout(
    **dict(CHART_LAYOUT, height=300),
    title=dict(text="Tiempo estimado de respuesta en BD según workers del tenant", font=dict(size=13, color=COLORS["text"]), x=0),
    xaxis=dict(**axis_style("Workers en el tenant"), range=[0, 2000]),
    yaxis=axis_style("Segundos estimados"),
    showlegend=False
)
st.plotly_chart(fig7, width="stretch")

col_g, col_h, col_i = st.columns(3)
for col, color, bg, title, workers_range, subq_range, tiempo_range in [
    (col_g, COLORS["green"], COLORS["green_l"], "Leve", "1 — 300", "hasta 10,200", "< 4 seg"),
    (col_h, COLORS["amber"], COLORS["amber_l"], "Medio", "300 — 800", "10,200 — 27,200", "4 — 10 seg"),
    (col_i, COLORS["red"],   COLORS["red_l"],   "Crítico", "800+", "más de 27,200", "+10 seg"),
]:
    with col:
        st.markdown(f"""
        <div style="background:{bg};border-radius:10px;padding:1.25rem;border:1px solid {color}22;text-align:center">
          <p style="font-size:1rem;font-weight:600;color:{color};margin:0">{title}</p>
          <p style="font-size:1.5rem;font-weight:600;color:{color};margin:8px 0 0">{workers_range}</p>
          <p style="font-size:0.75rem;color:{color};margin:2px 0 0">workers</p>
          <hr style="border-color:{color}33;margin:10px 0">
          <p style="font-size:0.8rem;color:{color};margin:0">{subq_range} subqueries</p>
          <p style="font-size:0.8rem;color:{color};margin:4px 0 0">{tiempo_range} estimados en BD</p>
        </div>""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<p style="font-size:0.75rem;color:#9ca3af;text-align:center">
Tiempos estimados basados en 0.375ms/subquery medido en EXPLAIN ANALYZE sobre aamx09 con índices activos · 
Tenants sin índices verificados pueden superar significativamente estos valores ·
Evidencia recopilada en DBeaver conectado a base de datos abrhil
</p>
""", unsafe_allow_html=True)