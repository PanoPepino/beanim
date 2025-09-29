import os
import re


def shorten_api_titles_remove_suffix(api_dir):
    """
    Change rst file titles to only leaf module/class name without 'package' or 'module' suffix.
    """
    for fname in os.listdir(api_dir):
        if fname.endswith(".rst"):
            path = os.path.join(api_dir, fname)
            with open(path, "r", encoding="utf8") as f:
                lines = f.readlines()
            # Match the first line for module/package title
            match = re.match(r"([\w\.]+) (package|module)", lines[0])
            if match:
                leaf = match.group(1).split(".")[-1]  # Get only the last part
                # Replace title with just the leaf name, no suffix
                new_title = f"{leaf}\n"
                lines[0] = new_title
                # Underline line length must match new title's length
                lines[1] = "=" * len(new_title.strip()) + "\n"
                with open(path, "w", encoding="utf8") as f:
                    f.writelines(lines)


shorten_api_titles_remove_suffix("api")
