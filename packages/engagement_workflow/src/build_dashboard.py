r"""Generate a self-contained Plotly HTML dashboard template.

Inputs:
    --json : path to results JSON (e.g. D:\_batch7_results_v2.json)
    --out  : output HTML path (e.g. D:\GR\02_reports\dashboard_batch7.html)
    --title: dashboard title shown at the top

JSON schema (per row):
    site, slug, source, upload_date,
    users, sessions, eng_users, eng_pct,
    s_p50, s_p90, s_avg,
    page_p50, page_p90, page_avg,
    measurements

Workflow for future batches:
    1. Run _batch_query_v2.py -> produces {batch}_results_v2.json
    2. Run this script with the new JSON -> produces dashboard_{batch}.html
    3. Open HTML in browser
"""
import argparse
import json
import html
from pathlib import Path

METRIC_DEFS = [
    # (key,             display label, fmt,    yaxis prefix, sort)
    ('users',           'Users',         'int',  '',           True),
    ('sessions',        'Sessions',      'int',  '',           True),
    ('eng_pct',         'Eng%',          'pct',  '',           True),
    ('s_p50',           'S_p50 (s)',     'dec',  's',          True),
    ('s_p90',           'S_p90 (s)',     'dec',  's',          True),
    ('s_avg',           'S_avg (s)',     'dec',  's',          True),
    # page-level (kept optional — for future expansion)
    # ('page_p50', 'Page_p50 (s)', 'dec', 's', True),
    # ('page_p90', 'Page_p90 (s)', 'dec', 's', True),
    # ('page_avg', 'Page_avg (s)', 'dec', 's', True),
]

SOURCE_COLORS = {
    'GR':    '#2E7D32',  # green
    'AZ':    '#1565C0',  # blue
    'owner': '#E65100',  # orange
}

SOURCE_ORDER = ['GR', 'AZ', 'owner']

def fmt_value(v, kind):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return ''
    if kind == 'int':
        return f'{int(v):,}'
    if kind == 'pct':
        return f'{v:.2f}%'
    if kind == 'dec':
        return f'{v:.2f}'
    return str(v)

def build_dashboard(rows, title):
    """Return full HTML string with embedded Plotly.js + data + UI."""
    # Detect sites & dates
    sites = sorted({r['site'].replace('.io', '') for r in rows})
    dates = sorted({r['upload_date'] for r in rows})
    n_rows = len(rows)

    # Serialize rows for the JS
    rows_json = json.dumps([
        {
            'site': r['site'].replace('.io', ''),
            'date': r['upload_date'],
            'slug': r['slug'],
            'source': r['source'],
            'values': {key: (float(r[key]) if r[key] not in (None, 'None', '') else 0)
                       for key, *_ in METRIC_DEFS},
        }
        for r in rows
    ], ensure_ascii=False)

    metrics_json = json.dumps([
        {'key': k, 'label': lbl, 'fmt': fmt, 'prefix': pre, 'sortDesc': sd}
        for k, lbl, fmt, pre, sd in METRIC_DEFS
    ])

    sites_json = json.dumps(sites)
    dates_json = json.dumps(dates)
    colors_json = json.dumps(SOURCE_COLORS)
    order_json = json.dumps(SOURCE_ORDER)
    title_json = json.dumps(title)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {{
    --bg: #fafafa;
    --panel: #ffffff;
    --ink: #212121;
    --ink-soft: #616161;
    --line: #e0e0e0;
    --accent: #1565C0;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--ink);
    margin: 0; padding: 24px;
  }}
  h1 {{ font-size: 22px; margin: 0 0 4px; }}
  .sub {{ color: var(--ink-soft); margin: 0 0 16px; font-size: 13px; }}
  .controls {{
    display: flex; gap: 16px; align-items: end;
    background: var(--panel); border: 1px solid var(--line);
    border-radius: 8px; padding: 16px; margin-bottom: 16px;
  }}
  .ctrl {{ display: flex; flex-direction: column; gap: 4px; }}
  .ctrl label {{ font-size: 12px; color: var(--ink-soft); font-weight: 600; }}
  .ctrl select {{
    font-size: 14px; padding: 6px 10px;
    border: 1px solid var(--line); border-radius: 4px;
    background: #fff; min-width: 160px;
  }}
  #chart {{
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 8px; padding: 8px;
    min-height: 520px;
  }}
  .legend-row {{
    display: flex; gap: 16px; padding: 0 16px 12px;
    font-size: 13px; color: var(--ink-soft);
  }}
  .legend-row .swatch {{
    display: inline-block; width: 14px; height: 14px;
    border-radius: 3px; margin-right: 6px; vertical-align: middle;
  }}
  .empty {{
    display: none; padding: 60px; text-align: center;
    color: var(--ink-soft); font-size: 14px;
  }}
  .winners {{
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;
    margin-bottom: 16px;
  }}
  .winners .card {{
    background: var(--panel); border: 1px solid var(--line);
    border-left: 4px solid var(--accent);
    border-radius: 6px; padding: 10px 14px;
  }}
  .winners .card .lbl {{
    font-size: 11px; color: var(--ink-soft);
    text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;
  }}
  .winners .card .name {{
    font-size: 14px; font-weight: 600; margin-top: 4px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }}
  .winners .card .val {{
    font-size: 12px; color: var(--ink-soft); margin-top: 2px;
  }}
  .winners .card[data-source="GR"]    {{ border-left-color: {SOURCE_COLORS['GR']}; }}
  .winners .card[data-source="AZ"]    {{ border-left-color: {SOURCE_COLORS['AZ']}; }}
  .winners .card[data-source="owner"] {{ border-left-color: {SOURCE_COLORS['owner']}; }}
  .footer {{ font-size: 12px; color: var(--ink-soft); margin-top: 16px; }}
</style>
</head>
<body>

<h1 id="page-title">{html.escape(title)}</h1>
<p class="sub">
  {n_rows} games loaded &middot; {len(sites)} sites &middot; {len(dates)} dates
</p>

<div class="controls">
  <div class="ctrl">
    <label for="sel-site">Site</label>
    <select id="sel-site"></select>
  </div>
  <div class="ctrl">
    <label for="sel-date">Date</label>
    <select id="sel-date"></select>
  </div>
  <div class="ctrl">
    <label for="sel-metric">Metric</label>
    <select id="sel-metric"></select>
  </div>
</div>

<div class="legend-row">
  <span><span class="swatch" style="background:{SOURCE_COLORS['GR']}"></span>GR</span>
  <span><span class="swatch" style="background:{SOURCE_COLORS['AZ']}"></span>AZ</span>
  <span><span class="swatch" style="background:{SOURCE_COLORS['owner']}"></span>owner</span>
</div>

<div class="winners" id="winners"></div>

<div id="chart"></div>
<div id="empty" class="empty">No games match this cohort.</div>

<p class="footer">
  Template: <code>plotly_dashboard_template.html</code> &middot;
  Data source: <code id="data-source">embedded</code>
</p>

<script id="data-rows" type="application/json">{rows_json}</script>
<script id="data-meta" type="application/json">{{
  "sites": {sites_json},
  "dates": {dates_json},
  "metrics": {metrics_json},
  "colors": {colors_json},
  "order": {order_json},
  "title": {title_json}
}}</script>

<script>
(function () {{
  const rows    = JSON.parse(document.getElementById('data-rows').textContent);
  const meta    = JSON.parse(document.getElementById('data-meta').textContent);
  const {{ sites, dates, metrics, colors, order, title }} = meta;

  // populate dropdowns
  const $site   = document.getElementById('sel-site');
  const $date   = document.getElementById('sel-date');
  const $metric = document.getElementById('sel-metric');

  sites.forEach(s   => $site  .appendChild(new Option(s,   s)));
  dates.forEach(d   => $date  .appendChild(new Option(d,   d)));
  metrics.forEach(m => $metric.appendChild(new Option(m.label, m.key)));

  // default = first site, first date, first metric
  $site.value   = sites[0];
  $date.value   = dates[0];
  $metric.value = metrics[0].key;

  function fmt(v, kind) {{
    if (v === null || v === undefined || Number.isNaN(v)) return '';
    if (kind === 'int') return Number(v).toLocaleString();
    if (kind === 'pct') return Number(v).toFixed(2) + '%';
    if (kind === 'dec') return Number(v).toFixed(2);
    return String(v);
  }}

  function renderWinners(subset) {{
    const $w = document.getElementById('winners');
    $w.innerHTML = '';
    // 4 winner cards: Users / Eng% / S_p50 / S_avg
    const cards = [
      {{ key: 'users',   lbl: 'Traffic (Users)' }},
      {{ key: 'eng_pct', lbl: 'Engagement (Eng%)' }},
      {{ key: 's_p50',   lbl: 'Duration (S_p50)' }},
      {{ key: 's_avg',   lbl: 'Duration (S_avg)' }},
    ];
    cards.forEach(c => {{
      if (subset.length === 0) return;
      const m = metrics.find(x => x.key === c.key);
      const best = subset.slice().sort(
        (a, b) => b.values[c.key] - a.values[c.key])[0];
      const div = document.createElement('div');
      div.className = 'card';
      div.dataset.source = best.source;
      div.innerHTML =
        '<div class="lbl">' + c.lbl + '</div>' +
        '<div class="name">' + best.slug + '</div>' +
        '<div class="val">' + best.source + ' &middot; ' +
            fmt(best.values[c.key], m.fmt) + '</div>';
      $w.appendChild(div);
    }});
  }}

  function render() {{
    const site   = $site.value;
    const date   = $date.value;
    const metric = $metric.value;
    const m      = metrics.find(x => x.key === metric);
    const subset = rows
      .filter(r => r.site === site && r.date === date)
      .sort((a, b) => m.sortDesc
        ? b.values[metric] - a.values[metric]
        : a.values[metric] - b.values[metric]);

    renderWinners(subset);

    const $chart = document.getElementById('chart');
    const $empty = document.getElementById('empty');
    if (subset.length === 0) {{
      Plotly.purge($chart);
      $chart.style.display = 'none';
      $empty.style.display = 'block';
      return;
    }}
    $chart.style.display = 'block';
    $empty.style.display = 'none';

    // one trace per source (keeps consistent legend + color)
    const traces = order.map(src => {{
      const games = subset.filter(g => g.source === src);
      return {{
        type: 'bar',
        name: src,
        x: games.map(g => g.slug),
        y: games.map(g => g.values[metric]),
        text: games.map(g => fmt(g.values[metric], m.fmt)),
        textposition: 'outside',
        textfont: {{ size: 11 }},
        cliponaxis: false,
        marker: {{ color: colors[src] }},
        hovertemplate: '<b>%{{x}}</b><br>' + src + '<br>' +
                      m.label + ': %{{y}}<extra></extra>',
      }};
    }}).filter(t => t.x.length > 0);

    const winner = subset[0];
    const layout = {{
      title: {{
        text: '<b>' + site + '</b> &middot; ' + date +
              ' &middot; ' + m.label +
              ' &nbsp; <span style="font-size:12px;color:#666">' +
              '(winner: ' + winner.slug + ' \u2014 ' + winner.source + ')</span>',
        font: {{ size: 16 }},
        x: 0.01, xanchor: 'left',
      }},
      barmode: 'group',
      bargap: 0.25,
      bargroupgap: 0.05,
      xaxis: {{
        title: 'Game',
        tickangle: subset.length > 4 ? -30 : 0,
        automargin: true,
      }},
      yaxis: {{
        title: m.label + (m.prefix ? ' (' + m.prefix + ')' : ''),
        rangemode: 'tozero',
        gridcolor: '#eee',
      }},
      legend: {{
        orientation: 'h',
        y: -0.18, x: 0.5, xanchor: 'center',
      }},
      margin: {{ t: 70, l: 60, r: 20, b: 80 }},
      paper_bgcolor: 'white',
      plot_bgcolor: 'white',
      font: {{ family: '-apple-system, "Segoe UI", Roboto, sans-serif' }},
    }};

    const config = {{
      responsive: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d', 'autoScale2d'],
    }};

    Plotly.react($chart, traces, layout, config);
  }}

  $site  .addEventListener('change', render);
  $date  .addEventListener('change', render);
  $metric.addEventListener('change', render);
  window.addEventListener('resize', () => Plotly.Plots.resize('chart'));
  render();
}})();
</script>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True, help='Path to batch results JSON')
    ap.add_argument('--out',  required=True, help='Output HTML path')
    ap.add_argument('--title', default='Game Metrics Dashboard')
    args = ap.parse_args()

    with open(args.json, 'r', encoding='utf-8') as f:
        rows = json.load(f)
    rows = [r for r in rows if 'error' not in r]
    print(f'Loaded {len(rows)} rows from {args.json}')

    html_str = build_dashboard(rows, args.title)
    Path(args.out).write_text(html_str, encoding='utf-8')
    print(f'Wrote {args.out} ({len(html_str):,} bytes)')


if __name__ == '__main__':
    main()