"""build.py – assemble Call of Cthulhu scenario files into dist/ markdown files."""

import os
import re

SOURCES_DIR = os.path.join(os.path.dirname(__file__), "sources", "scenarios")
DIST_DIR = os.path.join(os.path.dirname(__file__), "dist")


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Call of Cthulhu Scenario</title>
  <style>
    body {{ font-family: Georgia, serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; }}
    h1, h2, h3 {{ margin-top: 1.5em; }}
    hr {{ margin: 2em 0; border: none; border-top: 1px solid #ccc; }}
    blockquote {{ border-left: 3px solid #999; margin-left: 0; padding-left: 1em; color: #555; font-style: italic; }}
  </style>
</head>
<body>
{content}
</body>
</html>
"""


def inline_md(text):
    """Convert inline markdown (bold, italic) to HTML."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def _is_special_line(line):
    """Return True if the line starts a heading, list, blockquote, or hr."""
    return (
        line.startswith("#")
        or line.startswith("> ")
        or line.strip() == "---"
        or bool(re.match(r"^[-*] ", line))
        or bool(re.match(r"^\d+\. ", line))
    )


def markdown_to_html(text):
    """Convert a simple markdown string to HTML."""
    lines = text.split("\n")
    html_parts = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.startswith("### "):
            html_parts.append(f"<h3>{inline_md(line[4:])}</h3>")
            i += 1
        elif line.startswith("## "):
            html_parts.append(f"<h2>{inline_md(line[3:])}</h2>")
            i += 1
        elif line.startswith("# "):
            html_parts.append(f"<h1>{inline_md(line[2:])}</h1>")
            i += 1
        elif line.strip() == "---":
            html_parts.append("<hr>")
            i += 1
        elif line.startswith("> "):
            html_parts.append(f"<blockquote>{inline_md(line[2:])}</blockquote>")
            i += 1
        elif re.match(r"^[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^[-*] ", lines[i]):
                items.append(f"<li>{inline_md(lines[i][2:])}</li>")
                i += 1
            html_parts.append("<ul>\n" + "\n".join(items) + "\n</ul>")
        elif re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(f"<li>{inline_md(re.sub(r'^\d+\.\s+', '', lines[i]))}</li>")
                i += 1
            html_parts.append("<ol>\n" + "\n".join(items) + "\n</ol>")
        elif line.strip() == "":
            i += 1
        else:
            para_lines = []
            while i < len(lines) and lines[i].strip() != "" and not _is_special_line(lines[i]):
                para_lines.append(inline_md(lines[i].rstrip()))
                i += 1
            if para_lines:
                html_parts.append(f"<p>{'<br>'.join(para_lines)}</p>")

    return "\n".join(html_parts)


def read_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read().strip()


def build_scenario(scenario_dir):
    name = os.path.basename(scenario_dir)

    sections = []

    # Outline
    outline_path = os.path.join(scenario_dir, "outline.md")
    if os.path.isfile(outline_path):
        sections.append(read_file(outline_path))

    # Characters
    characters_dir = os.path.join(scenario_dir, "characters")
    if os.path.isdir(characters_dir):
        character_files = sorted(
            f for f in os.listdir(characters_dir) if f.endswith(".md")
        )
        if character_files:
            sections.append("---\n\n## Characters")
            for filename in character_files:
                sections.append(read_file(os.path.join(characters_dir, filename)))

    # Scenes
    scenes_dir = os.path.join(scenario_dir, "scenes")
    if os.path.isdir(scenes_dir):
        scene_files = sorted(
            f for f in os.listdir(scenes_dir) if f.endswith(".md")
        )
        if scene_files:
            sections.append("---\n\n## Scenes")
            for filename in scene_files:
                sections.append(read_file(os.path.join(scenes_dir, filename)))

    output = "\n\n".join(sections) + "\n"

    os.makedirs(DIST_DIR, exist_ok=True)
    out_path = os.path.join(DIST_DIR, f"{name}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Built: {out_path}")
    return output


def build_index_html(all_markdown):
    """Generate dist/index.html from combined markdown content."""
    combined = "\n\n".join(all_markdown)
    content = markdown_to_html(combined)
    html = HTML_TEMPLATE.format(content=content)
    os.makedirs(DIST_DIR, exist_ok=True)
    out_path = os.path.join(DIST_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Built: {out_path}")


def main():
    if not os.path.isdir(SOURCES_DIR):
        print(f"No scenarios found in {SOURCES_DIR}")
        return

    all_markdown = []
    for entry in sorted(os.listdir(SOURCES_DIR)):
        scenario_dir = os.path.join(SOURCES_DIR, entry)
        if os.path.isdir(scenario_dir):
            md = build_scenario(scenario_dir)
            all_markdown.append(md)

    build_index_html(all_markdown)


if __name__ == "__main__":
    main()
