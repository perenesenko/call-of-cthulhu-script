"""build.py – assemble Call of Cthulhu scenario files into dist/ markdown files."""

import os

SOURCES_DIR = os.path.join(os.path.dirname(__file__), "sources", "scenarios")
DIST_DIR = os.path.join(os.path.dirname(__file__), "dist")


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


def main():
    if not os.path.isdir(SOURCES_DIR):
        print(f"No scenarios found in {SOURCES_DIR}")
        return

    for entry in sorted(os.listdir(SOURCES_DIR)):
        scenario_dir = os.path.join(SOURCES_DIR, entry)
        if os.path.isdir(scenario_dir):
            build_scenario(scenario_dir)


if __name__ == "__main__":
    main()
