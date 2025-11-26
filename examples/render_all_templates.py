
import subprocess
import sys
import re
from pathlib import Path

# Configuration
PYTHON_FILE = "example_generic.py"  # Your Manim Python file
SCENE_CLASS = "Generic_Slide_Test"  # Scene class to render
BACKUP_FILE = "example_generic.py.backup"  # Backup of original file
OUTPUT_NAME_PATTERN = "{scene}_{template}"

# Define ALL templates from import_template_beanim
TEMPLATES = ["green_mint",
             "blue_ice",
             "red_autumn",
             "beamer_blue",
             "beamer_green",
             "quantum_dusk",
             "dark_energy",
             "default_template"]


# Manim render settings
QUALITY = "-qh"  # Change to -qm, -qh, -qk as needed
FORMAT = "--format=png"  # Change to mp4, gif, etc.


def read_file(filepath):
    """Read the content of a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    """Write content to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def backup_file(filepath):
    """Create a backup of the original file."""
    content = read_file(filepath)
    write_file(BACKUP_FILE, content)
    print(f"✓ Backup created: {BACKUP_FILE}")


def restore_backup():
    """Restore the original file from backup."""
    if Path(BACKUP_FILE).exists():
        content = read_file(BACKUP_FILE)
        write_file(PYTHON_FILE, content)
        print(f"✓ Restored original file from backup")


def modify_template(content, template_name):
    """
    Modify the import_template_beanim() call to use the specified template.

    Handles multiple patterns:
    - import_template_beanim("template_name")
    - import_template_beanim('template_name')
    - import_template_beanim(  "template_name"  )
    """
    pattern = r'import_template_beanim\s*\(\s*["\']([^"\']+)["\']?\s*\)'

    replacement = f'import_template_beanim("{template_name}")'

    if not re.search(pattern, content):
        print(f"⚠️  Warning: Could not find import_template_beanim() call in {PYTHON_FILE}")
        print("    Make sure your file contains: import_template_beanim(\"template_name\")")
        return None

    modified_content = re.sub(pattern, replacement, content)
    return modified_content


def render_scene(template_name):
    """Render the Manim scene with the current template."""
    print(f"\n{'='*60}")
    print(f"Rendering with template: {template_name}")
    print(f"{'='*60}")

    output_name = OUTPUT_NAME_PATTERN.format(
        scene=SCENE_CLASS,
        template=template_name
    )

    cmd = [
        "manim",
        PYTHON_FILE,
        SCENE_CLASS,
        QUALITY,
        FORMAT,
        "-o", f"{output_name}",
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=False,
            text=True,
            check=True
        )
        print(f"✓ Successfully rendered: {output_name}.png")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error rendering {template_name}")
        print(f"   Return code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("✗ Error: 'manim' command not found. Is Manim installed?")
        return False


def main():
    """Main execution function."""
    print("="*60)
    print("Manim Template Batch Renderer")
    print("="*60)
    print(f"File: {PYTHON_FILE}")
    print(f"Scene: {SCENE_CLASS}")
    print(f"Templates: {len(TEMPLATES)}")
    print("="*60)

    if not Path(PYTHON_FILE).exists():
        print(f"✗ Error: {PYTHON_FILE} not found!")
        sys.exit(1)

    backup_file(PYTHON_FILE)

    original_content = read_file(PYTHON_FILE)

    successful = []
    failed = []

    try:
        for i, template in enumerate(TEMPLATES, 1):
            print(f"\n[{i}/{len(TEMPLATES)}] Processing: {template}")

            modified_content = modify_template(original_content, template)

            if modified_content is None:
                print(f"✗ Skipping {template} - could not modify file")
                failed.append(template)
                continue

            write_file(PYTHON_FILE, modified_content)
            print(f"✓ Updated {PYTHON_FILE} with template: {template}")

            if render_scene(template):
                successful.append(template)
            else:
                failed.append(template)

    finally:
        print(f"\n{'='*60}")
        print("Cleaning up...")
        restore_backup()

    print(f"\n{'='*60}")
    print("Batch Rendering Summary")
    print(f"{'='*60}")
    print(f"Total templates: {len(TEMPLATES)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print(f"\n✓ Successfully rendered:")
        for template in successful:
            output_name = OUTPUT_NAME_PATTERN.format(
                scene=SCENE_CLASS,
                template=template
            )
            print(f"  - {output_name}.png")

    if failed:
        print(f"\n✗ Failed to render:")
        for template in failed:
            print(f"  - {template}")

    print(f"\n{'='*60}")
    print("Batch rendering complete!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
    # Pattern to match
