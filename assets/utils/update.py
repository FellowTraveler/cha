import subprocess
import sys
import os
import re


def safe_input(starting_text):
    try:
        return input(starting_text)
    except (KeyboardInterrupt, EOFError):
        print()
        sys.exit(1)


def update_setup():
    # path to setup file
    PYTHON_SETUP_FILE_PATH = None
    for i in range(4):
        setup_file_path = "/".join(
            os.path.dirname(os.path.abspath(__file__)).split("/")[:-(i)] + ["setup.py"]
        )
        if os.path.isfile(setup_file_path):
            PYTHON_SETUP_FILE_PATH = setup_file_path
            break

    if PYTHON_SETUP_FILE_PATH is None:
        print("Failed to load 'setup.py' file(s) because it does not exist!")
        sys.exit(1)

    # confirm the loaded setup file path is correct
    print(f"Found 'setup.py' at:\n{PYTHON_SETUP_FILE_PATH}")
    confirm_input = safe_input(f"Continue with this path (Y/n)? ")
    if confirm_input.lower() in ["n", "no"]:
        PYTHON_SETUP_FILE_PATH = safe_input(
            "Please manually input the path to 'setup.py': "
        ).strip()
        if not os.path.isfile(PYTHON_SETUP_FILE_PATH):
            print(f"The file path '{PYTHON_SETUP_FILE_PATH}' does not exist!")
            sys.exit(1)

    # read the current setup file
    with open(PYTHON_SETUP_FILE_PATH, "r") as f:
        content = f.read()

    # get and update version
    version_match = re.search(r'version="([^"]*)"', content)
    if version_match:
        current_version = version_match.group(1)
        print(f"Current version: {current_version}")

        try:
            major, minor, patch = map(int, current_version.split("."))

            patch_bump = f"{major}.{minor}.{patch + 1}"
            minor_bump = f"{major}.{minor + 1}.0"
            major_bump = f"{major + 1}.0.0"

            print("Select the new version:")
            print(f"  1. Patch -> {patch_bump}")
            print(f"  2. Minor -> {minor_bump}")
            print(f"  3. Major -> {major_bump}")
            print(f"  4. Keep current version ({current_version})")
            while True:
                choice = safe_input("Enter your choice (1-4): ").strip()
                if choice == "1":
                    new_version = patch_bump
                    break
                elif choice == "2":
                    new_version = minor_bump
                    break
                elif choice == "3":
                    new_version = major_bump
                    break
                elif choice == "4":
                    new_version = current_version
                    break
                else:
                    print("Invalid choice, please try again!")

        except ValueError:
            print("Could not parse current version. Please update manually.")
            new_version = safe_input("Enter new version: ").strip()
            if len(new_version) == 0 or "." not in new_version:
                new_version = current_version

        if new_version != current_version:
            print(f"Updated version to: {new_version}")

        content = content.replace(
            f'version="{current_version}"', f'version="{new_version}"'
        )

    # find all dependencies
    deps = re.findall(r'"([^"]+)==([^"]+)"', content)

    print("Scanning dependencies...")

    # update each dependency
    changed_count = 0
    for package, current_version in deps:
        try:
            # get latest version by running the pip CLI command
            result = subprocess.run(
                ["pip", "index", "versions", package],
                capture_output=True,
                text=True,
                check=True,
            )

            # extract latest version
            for line in result.stdout.split("\n"):
                if "Available versions:" in line:
                    latest_version = line.split(":")[1].strip().split(",")[0].strip()
                    if latest_version != current_version:
                        update_input = safe_input(
                            f"Update {package} from {current_version} to {latest_version} (Y/n)? "
                        )
                        if update_input.lower() in ["y", "yes"]:
                            print(
                                f"Updating {package}: {current_version} -> {latest_version}"
                            )
                            content = content.replace(
                                f'"{package}=={current_version}"',
                                f'"{package}=={latest_version}"',
                            )
                            changed_count += 1
                    break

        except subprocess.CalledProcessError:
            print(f"Failed to get version for {package}, skipping...")
            continue

    # write updated content
    with open(PYTHON_SETUP_FILE_PATH, "w") as f:
        f.write(content)
    print(f"Updated setup file!")

    print(f"A total of {changed_count} package versions got changed!")

    # (optional) reinstall Cha
    user_input = safe_input(f"Do you like to reinstall Cha (Y/n)? ")
    if user_input.lower() in ["y", "yes"]:
        user_input = safe_input('Install with "-e" option (Y/n)? ')
        if user_input.lower() in ["y", "yes"]:
            print('> Installing Cha WITH "-e" Option!')
            os.system("pip3 install -e .")
        else:
            print('> Installing Cha WITHOUT "-e" Option!')
            os.system("pip3 install .")


if __name__ == "__main__":
    update_setup()
