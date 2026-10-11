"""Help page: USER_GUIDE.md rendered to HTML (the subset the guide uses: headings, paragraphs, bullet and
numbered lists, tables, fenced code, inline code, bold, links). Everything is HTML-escaped."""
import html
import re


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _inline(text):
    parts = re.split(r"(`[^`]*`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append("<code>%s</code>" % html.escape(part[1:-1], quote=False))
            continue
        part = html.escape(part, quote=False)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", part)      # the GUI cannot open links
        out.append(part)
    return "".join(out)


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def render_markdown(text):
    """(HTML, table of contents [(anchor, title)] of the level-2 headings)."""
    lines = text.replace("\r\n", "\n").split("\n")
    out, toc, i = [], [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(lines[i + 1:j]), quote=False))
            i = j + 1
            continue
        m = re.match(r"(#{1,4})\s+(.*)", line)
        if m:
            level, title = len(m.group(1)), m.group(2).strip()
            anchor = _slug(title)
            if level == 2:
                toc.append((anchor, title))
            out.append('<h%d id="%s">%s</h%d>' % (level, anchor, _inline(title), level))
            i += 1
            continue
        if line.lstrip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                if not re.fullmatch(r"\s*\|[\s:|-]+\|?\s*", lines[i]):
                    rows.append(_cells(lines[i]))
                i += 1
            body = ["<tr>%s</tr>" % "".join("<th>%s</th>" % _inline(c) for c in rows[0])]
            body += ["<tr>%s</tr>" % "".join("<td>%s</td>" % _inline(c) for c in r) for r in rows[1:]]
            out.append("<table>%s</table>" % "".join(body))
            continue
        bullet = re.match(r"\s*([-*]|\d+\.)\s+", line)
        if bullet:
            ordered = bullet.group(1)[0].isdigit()
            items = []
            while i < len(lines) and lines[i].strip():
                b = re.match(r"\s*([-*]|\d+\.)\s+(.*)", lines[i])
                if b:
                    items.append(b.group(2))
                elif items:
                    items[-1] += " " + lines[i].strip()            # continuation line of an item
                i += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % _inline(t) for t in items), tag))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"(#{1,4}\s|```|\s*\||\s*([-*]|\d+\.)\s)", lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para)))
    return "\n".join(out), toc


def render_guide(path):
    with open(path, encoding="utf-8") as fh:
        return render_markdown(fh.read())
