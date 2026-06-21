import re
from lxml import html as lh

NUM_RE = re.compile(r"-?\d[\d,]*\.?\d*")

def _find_data_table(doc):
    best = None; best_digits = 0
    for t in doc.xpath("//table"):
        if any(a.tag in ("script", "style", "head") for a in t.iterancestors()):
            continue
        rows = t.xpath("./tr") or t.xpath("./tbody/tr") or t.xpath(".//tr")
        if len(rows) < 4:
            continue
        digits = len(NUM_RE.findall(t.text_content()))
        if digits > best_digits:
            best, best_digits = t, digits
    return best

def _expand(cells):
    """Expand a header row honoring colspan -> flat list of labels per column."""
    out = []
    for c in cells:
        try:
            span = int(c.get("colspan") or 1)
        except ValueError:
            span = 1
        out.extend([c.text_content().strip()] * span)
    return out

def parse_value(text):
    t = (text or "").strip()
    if not t:
        return None
    m = NUM_RE.search(t)
    if not m:
        return None
    raw = m.group(0).replace(",", "")
    try:
        return float(raw)
    except ValueError:
        return None

def parse_indicator(html_text):
    doc = lh.fromstring(html_text)
    t = _find_data_table(doc)
    if t is None:
        return []
    rows = t.xpath("./tr") or t.xpath("./tbody/tr") or t.xpath(".//tr")
    header_rows, data_rows = [], []
    for r in rows:
        cells = r.xpath("./td|./th")
        if cells and all(c.tag == "th" for c in cells):
            header_rows.append(cells)
        elif r.xpath("./td"):
            data_rows.append(r.xpath("./td"))
    if not header_rows or not data_rows:
        return []
    ncol = max(len(d) for d in data_rows)
    value_cols = ncol - 1
    if value_cols < 1:
        return []
    # leaf labels: header row whose width == value_cols, else last header minus period col
    leaf = None
    for h in header_rows:
        exp = _expand(h)
        if len(exp) == value_cols:
            leaf = exp; break
    period_name = "period"
    if leaf is None:
        exp = _expand(header_rows[-1])
        if len(exp) >= value_cols + 1:
            period_name = exp[0]
            leaf = exp[1:value_cols + 1]
        else:
            leaf = (exp + [""] * value_cols)[:value_cols]
    else:
        # period axis name from the top header row's first cell
        period_name = header_rows[0][0].text_content().strip() or "period"
    # group labels from the top header row (expanded), offset by the period column
    group = [None] * value_cols
    if len(header_rows) >= 2:
        top = _expand(header_rows[0])
        # the top row includes the period column as its first expanded slot
        grp = top[1:value_cols + 1] if len(top) >= value_cols + 1 else top[:value_cols]
        for i in range(min(value_cols, len(grp))):
            g = grp[i].strip()
            group[i] = g or None
    recs = []
    for d in data_rows:
        period = d[0].text_content().strip()
        for j in range(min(value_cols, len(d) - 1)):
            txt = d[j + 1].text_content().strip()
            recs.append({
                "period": period,
                "period_name": period_name,
                "series": leaf[j] if j < len(leaf) else "",
                "series_group": group[j],
                "value_text": txt,
                "value": parse_value(txt),
            })
    return recs
