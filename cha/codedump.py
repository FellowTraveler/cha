from datetime import datetime
import subprocess
import fnmatch
import time
import sys
import os

from cha import colors, utils, config
import pathspec


def is_probably_binary_by_extension(file_path):
    _, ext = os.path.splitext(file_path.lower())
    return ext in config.BINARY_EXTENSIONS


def is_binary_file_by_sniff(file_path, num_bytes=1024):
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(num_bytes)
            if b"\x00" in chunk:
                return True
    except:
        return True
    return False


def is_text_file(file_path):
    if is_probably_binary_by_extension(file_path):
        return False
    if is_binary_file_by_sniff(file_path):
        return False
    return True


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except:
        return None


def get_git_tracked_and_untracked_files(repo_path):
    try:
        cmd = ["git", "ls-files", "--exclude-standard", "--cached", "--others"]
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.splitlines()
    except:
        return []


def load_gitignore_patterns(dir_path):
    if not pathspec:
        return None
    gitignore_path = os.path.join(dir_path, ".gitignore")
    if not os.path.isfile(gitignore_path):
        return None
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            ignore_lines = f.read().splitlines()
        return pathspec.PathSpec.from_lines("gitwildmatch", ignore_lines)
    except:
        return None


def get_all_files_with_ignore(dir_path):
    spec = load_gitignore_patterns(dir_path)
    all_paths = []
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, dir_path)
            if spec and spec.match_file(rel_path):
                continue
            all_paths.append(rel_path)
    return all_paths


def matches_specific_includes(file_path, root_path, specific_includes):
    if not specific_includes:
        return False

    rel_path = os.path.relpath(file_path, root_path)

    for include_pattern in specific_includes:
        include_pattern = include_pattern.strip()
        if not include_pattern:
            continue

        # handle directory includes (add trailing slash if needed)
        if os.path.isdir(os.path.join(root_path, include_pattern)):
            if not include_pattern.endswith("/"):
                include_pattern += "/"

        # check exact match
        if rel_path == include_pattern or rel_path == include_pattern.rstrip("/"):
            return True

        # check if file is under a directory pattern
        if include_pattern.endswith("/") and rel_path.startswith(include_pattern):
            return True

        # check glob pattern match
        if fnmatch.fnmatch(rel_path, include_pattern):
            return True

        # check if any parent directory matches the pattern
        parent_path = os.path.dirname(rel_path)
        while parent_path:
            if fnmatch.fnmatch(
                parent_path, include_pattern
            ) or parent_path == include_pattern.rstrip("/"):
                return True
            parent_path = os.path.dirname(parent_path)

    return False


def interactive_selection(root_path, files_dict, include_mode=False):
    from cha import utils

    selected = set()

    if include_mode:
        # in include mode, combine directories and files in a single selection
        all_dirs = set()
        for f in files_dict:
            d = os.path.dirname(f)
            while d and os.path.abspath(d) != os.path.abspath(root_path):
                all_dirs.add(d)
                parent = os.path.dirname(d)
                if parent == d:
                    break
                d = parent

        directories = sorted(all_dirs)
        directories = [
            d for d in directories if os.path.abspath(d) != os.path.abspath(root_path)
        ]

        # create a combined list of directories and files for selection
        items_to_select = [config.NOTHING_SELECTED_TAG]
        item_map = {}

        # prepare paths for formatting
        paths_to_format = []

        # add directories
        for d in directories:
            paths_to_format.append(d)
            item_map[d] = ("dir", d)

        # add files
        for f in files_dict.keys():
            paths_to_format.append(f)
            item_map[f] = ("file", f)

        # format paths for better fzf display
        formatted_paths, path_mapping = utils.format_paths_for_fzf(paths_to_format)
        items_to_select.extend(formatted_paths)

        if items_to_select:
            items_to_select.sort()
            fzf_input = "\n".join(items_to_select)

            selected_output = utils.run_fzf_ssh_safe(
                [
                    "fzf",
                    "-m",
                    "--header",
                    "Use TAB to select multiple files/directories to include, ENTER to confirm.",
                ],
                fzf_input,
            )
            if selected_output is None:
                sys.exit(0)
            selected_display_items = (
                selected_output.split("\n") if selected_output else []
            )
            if (
                selected_display_items
                and selected_display_items[0]
                and config.NOTHING_SELECTED_TAG not in selected_display_items
            ):
                # convert back to actual paths
                actual_paths = utils.extract_paths_from_fzf_selection(
                    selected_display_items, path_mapping
                )

                for item_path in actual_paths:
                    if item_path in item_map:
                        item_type, actual_item_path = item_map[item_path]
                        if item_type == "dir":
                            # add all files in this directory
                            for f in files_dict.keys():
                                if f.startswith(actual_item_path):
                                    selected.add(f)
                        else:
                            # add the specific file
                            selected.add(actual_item_path)
    else:
        # original exclude mode logic with the two-phase selection
        all_dirs = set()
        for f in files_dict:
            d = os.path.dirname(f)
            while d and os.path.abspath(d) != os.path.abspath(root_path):
                all_dirs.add(d)
                parent = os.path.dirname(d)
                if parent == d:
                    break
                d = parent

        directories = sorted(all_dirs)
        directories = [
            d for d in directories if os.path.abspath(d) != os.path.abspath(root_path)
        ]

        # handle directory selection with fzf
        if directories:
            # format paths for better fzf display
            formatted_dirs, dir_mapping = utils.format_paths_for_fzf(directories)
            dir_display_list = [config.NOTHING_SELECTED_TAG] + formatted_dirs
            fzf_input = "\n".join(dir_display_list)

            selected_output = utils.run_fzf_ssh_safe(
                [
                    "fzf",
                    "-m",
                    "--header",
                    "Use TAB to select multiple directories to exclude, ENTER to confirm.",
                ],
                fzf_input,
            )
            if selected_output is None:
                sys.exit(0)
            selected_display_dirs = (
                selected_output.split("\n") if selected_output else []
            )
            if (
                selected_display_dirs
                and selected_display_dirs[0]
                and config.NOTHING_SELECTED_TAG not in selected_display_dirs
            ):
                # convert back to actual paths
                actual_dirs = utils.extract_paths_from_fzf_selection(
                    selected_display_dirs, dir_mapping
                )
                selected_dirs = set(actual_dirs)

                for f in list(files_dict.keys()):
                    if any(f.startswith(d) for d in selected_dirs):
                        selected.add(f)

        # handle file selection with fzf
        remaining_files = [f for f in files_dict.keys() if f not in selected]

        if remaining_files:
            remaining_files_sorted = sorted(remaining_files)

            # format paths for better fzf display
            formatted_files, file_mapping = utils.format_paths_for_fzf(
                remaining_files_sorted
            )
            file_display_list = [config.NOTHING_SELECTED_TAG] + formatted_files
            fzf_input = "\n".join(file_display_list)

            selected_output = utils.run_fzf_ssh_safe(
                [
                    "fzf",
                    "-m",
                    "--header",
                    "Use TAB to select multiple files to exclude, ENTER to confirm.",
                ],
                fzf_input,
            )
            if selected_output is None:
                sys.exit(0)
            selected_display_files = (
                selected_output.split("\n") if selected_output else []
            )
            if (
                selected_display_files
                and selected_display_files[0]
                and config.NOTHING_SELECTED_TAG not in selected_display_files
            ):
                # convert back to actual paths
                actual_files = utils.extract_paths_from_fzf_selection(
                    selected_display_files, file_mapping
                )
                for full_path in actual_files:
                    if full_path:
                        selected.add(full_path)

    return selected


def get_tree_output(dir_path):
    try:
        cmd = ["tree", "--gitignore", "--prune", dir_path]
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        return result.stdout
    except:
        return "Failed to generate tree output"


def generate_text_output(root_path, files_dict, selected_files, include_mode=False):
    if include_mode:
        included = [f for f in files_dict if f in selected_files]
        # check for empty selection in include mode
        if not included:
            print(colors.red("No files selected in include mode!"))
            return None
    else:
        included = [f for f in files_dict if f not in selected_files]

    utc_now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    tree_output = get_tree_output(root_path)
    epoch_time = time.time()
    header = (
        "GENERAL INFORMATION/DATA:\n"
        "`````\n"
        f"CURRENT EPOCH TIME: {epoch_time} seconds\n"
        f"CURRENT UTC TIME: {utc_now}\n"
        f"ROOT DIR: {root_path}\n"
    )
    if included:
        header += "FILES:\n"
        for f in included:
            short_path = os.path.relpath(f, root_path)
            header += f"- {short_path}\n"
    header += "`````\n"
    header += "\nDIRECTORY STRUCTURE (TREE OUTPUT):\n`````\n"
    header += tree_output
    header += "`````\n"

    body = []
    for f in included:
        content = files_dict[f]
        short_path = os.path.relpath(f, root_path)
        section = (
            f"\nFILE PATH: {short_path}\n"
            "CONTENT:\n"
            "`````\n"
            f"{content}\n"
            "`````\n"
        )
        body.append(section)
    return header + "".join(body)


def extract_code(
    dir_path, include_mode=False, auto_include_all=False, specific_includes=None
):
    root_path = os.path.abspath(dir_path)
    if os.path.isdir(os.path.join(root_path, ".git")):
        rel_paths = get_git_tracked_and_untracked_files(root_path)
    else:
        rel_paths = get_all_files_with_ignore(root_path)
    if not rel_paths:
        print(colors.red("No files found!"))
        return None, 0
    files_dict = {}
    for rel in rel_paths:
        abs_path = os.path.join(root_path, rel)
        if is_text_file(abs_path):
            content = read_file(abs_path)
            if content is not None:
                files_dict[abs_path] = content
    if not files_dict:
        print(colors.red("No text files found!"))
        return None, 0

    if specific_includes:
        # use specific includes mode
        selected_files = set()
        for file_path in files_dict.keys():
            if matches_specific_includes(file_path, root_path, specific_includes):
                selected_files.add(file_path)

        if not selected_files:
            print(colors.red("No files matched the specified include patterns!"))
            return None, 0
    elif auto_include_all:
        selected_files = set(files_dict.keys())
    else:
        selected_files = interactive_selection(root_path, files_dict, include_mode)
        if selected_files is None:
            return None, 0

    output_text = generate_text_output(
        root_path, files_dict, selected_files, include_mode
    )
    if output_text is None:
        return None, 0

    token_count = utils.count_tokens(
        output_text, config.DEFAULT_SEARCH_BIG_MODEL, False
    )

    return output_text, token_count


def code_dump(
    save_file_to_current_dir=False,
    dir_full_path=None,
    auto_include_all=False,
    output_to_stdout=False,
    specific_includes=None,
    quiet=False,
):
    try:
        dir_path = os.getcwd()
        if dir_full_path != None:
            if not os.path.isdir(dir_full_path):
                print(colors.red(f"Directory {dir_full_path} does not exist!"))
                return None, 0
            dir_path = dir_full_path

        if specific_includes:
            include_mode = True  # specific includes implies include mode
        elif auto_include_all:
            include_mode = True
        else:
            mode_options = ["Exclude", "Include"]
            fzf_input = "\n".join(mode_options)

            selected_mode = utils.run_fzf_ssh_safe(
                [
                    "fzf",
                    "--no-clear",
                    "--header",
                    "Select mode:",
                ],
                fzf_input,
            )
            if selected_mode is None:
                sys.exit(0)
            include_mode = selected_mode == "Include"

        content, token_count = extract_code(
            dir_path, include_mode, auto_include_all, specific_includes
        )

        if content is None:
            return None, 0

        if not quiet:
            print(colors.yellow(f"{dir_path}"))
            print(colors.magenta(f"{token_count} Total Tokens"))

        if output_to_stdout:
            return content, token_count

        if save_file_to_current_dir:
            file_name = f"code_dump_{int(time.time())}.txt"
            with open(file_name, "w") as file:
                file.write(content)
            print(colors.green(f"Exported to {file_name}"))
            return None, token_count

        return (
            utils.rls(
                text=f"""
            =====[CODE-DUMP STARTS]=====
            {content}
            ======[CODE-DUMP ENDS]======
            """,
                fast_mode=True,
            ),
            token_count,
        )
    except Exception as e:
        print(colors.red(f"{e}"))
        return None, 0
