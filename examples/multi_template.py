#!/usr/bin/env python3
"""
debug.py - Render a scene with all templates
This script modifies the template import in your Python file and renders each version.
To apply to beanim, use impor_template_name_package
"""

import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

# All available templates in your package
TEMPLATES = [
    "beamer_blue",
    "beamer_green",
    "blue_ice",
    "dark_energy",
    "default_template",
    "green_mint",
    "quantum_dusk",
    "red_autumn"
]


def modify_template_import(file_content, template_name):
    """Replace the template import line with the specified template."""
    lines = file_content.split('\n')
    modified_lines = []

    for line in lines:
        if 'import_template_beanim' in line:
            # Replace the template argument
            modified_line = f'import_template_beanim("{template_name}")'
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)

    return '\n'.join(modified_lines)


def render_scene(file_path, scene_name, template_name, output_dir):
    """Render the scene with a specific template."""
    print(f"\n🎨 Rendering with template: {template_name}")
    print("=" * 60)

    # Read original file
    with open(file_path, 'r') as f:
        original_content = f.read()

    # Modify template import
    modified_content = modify_template_import(original_content, template_name)

    # Create temporary file
    temp_file = Path(output_dir) / f"temp_{template_name}.py"
    with open(temp_file, 'w') as f:
        f.write(modified_content)

    # Render with manim
    output_name = f"{scene_name}_{template_name}"
    cmd = [
        'manim',
        '-pqm',  # preview, low quality
        # '-s',
        '-o',
        output_name,
        str(temp_file),
        scene_name
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {template_name}: SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {template_name}: FAILED")
        print(f"Error: {e.stderr}")
        return False
    finally:
        # Clean up temp file
        if temp_file.exists():
            temp_file.unlink()


def main():
    if len(sys.argv) != 3:
        print("Usage: python debug.py <file.py> <SceneName>")
        print("Example: python debug.py compactification.py MyScene")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    scene_name = sys.argv[2]

    if not file_path.exists():
        print(f"❌ Error: File '{file_path}' not found")
        sys.exit(1)

    print(f"🚀 Rendering {scene_name} from {file_path}")
    print(f"📋 Templates to render: {len(TEMPLATES)}")
    print("=" * 60)

    # Create temp directory for modified files
    temp_dir = Path(tempfile.mkdtemp())

    try:
        success_count = 0
        fail_count = 0

        for template in TEMPLATES:
            if render_scene(file_path, scene_name, template, temp_dir):
                success_count += 1
            else:
                fail_count += 1

        print("\n" + "=" * 60)
        print(f"🎉 Rendering complete!")
        print(f"✅ Success: {success_count}")
        print(f"❌ Failed: {fail_count}")

    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
