"""cogent_help: USER_GUIDE.md rendered for the Help page (small Markdown subset, HTML escaped)."""
import sys

from support import ROOT

sys.path.insert(0, str(ROOT))


def render(text):
    from cogent_help import render_markdown
    return render_markdown(text)


def test_headings_get_anchors_and_a_table_of_contents():
    html, toc = render("# Title\n\n## First part\n\ntext\n\n## Second part\n")
    assert '<h1 id="title">Title</h1>' in html and '<h2 id="first-part">First part</h2>' in html
    assert toc == [("first-part", "First part"), ("second-part", "Second part")]


def test_paragraph_lines_are_joined_and_inline_markup_is_rendered():
    html, _ = render("Press **Apply**, then\nrun `code` <now> & [the guide](https://example.com).")
    assert html == ('<p>Press <strong>Apply</strong>, then run <code>code</code> &lt;now&gt; &amp; '
                    'the guide (https://example.com).</p>')


def test_lists():
    html, _ = render("- one\n- two `x`\n\n1. first\n2. second\n")
    assert html == "<ul><li>one</li><li>two <code>x</code></li></ul>\n<ol><li>first</li><li>second</li></ol>"


def test_table():
    html, _ = render("| A | B |\n|---|---|\n| 1 | `x` |\n")
    assert html == "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td><code>x</code></td></tr></table>"


def test_fenced_code_is_escaped_and_kept_verbatim():
    html, _ = render("```\na < b\n  **not bold**\n```\n")
    assert html == "<pre><code>a &lt; b\n  **not bold**</code></pre>"


def test_the_user_guide_renders_without_markdown_leftovers():
    from cogent_help import render_guide
    html, toc = render_guide(str(ROOT / "USER_GUIDE.md"))
    text = html.replace("<pre><code>", "\x00").split("\x00")
    outside_code = "".join(part.split("</code></pre>", 1)[-1] for part in text)
    for marker in ("**", "```", "|---", "](http"):
        assert marker not in outside_code, marker
    titles = [t for _, t in toc]
    for section in ("Receive FIFO", "Re-apply edits", "Generate code", "Error messages"):
        assert any(section in t for t in titles), section
