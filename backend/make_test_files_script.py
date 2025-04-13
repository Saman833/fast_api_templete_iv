"""
By running this script, you can create test files for all the files in a directory you put as input.
It also adds __init__.py in each mirrored test folder and ignores __pycache__ and .pyc files.
"""

import os
dst = "app/tests"  # dst is static for tests folders, so we can hardcode it

def replicate_as_tests(src_path, tests_root):
    if not os.path.exists(src_path):
        print(f"Source path does not exist: {src_path}")
        return

    folder_name = os.path.basename(os.path.normpath(src_path))

    for root, dirs, files in os.walk(src_path):
        # ❌ Skip __pycache__ folders
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        relative = os.path.relpath(root, src_path)
        new_dir = os.path.join(tests_root, folder_name, relative)
        os.makedirs(new_dir, exist_ok=True)

        # ✅ Add __init__.py to the mirrored test directory
        init_path = os.path.join(new_dir, '__init__.py')
        if not os.path.exists(init_path):
            open(init_path, 'w').close()
            print(f"Created __init__.py in: {new_dir}")

        for file in files:
            # ❌ Skip non-.py files and .pyc files
            if not file.endswith(".py") or file.endswith(".pyc") or file.startswith("test_"):
                continue

            test_filename = f"test_{file}"
            test_file_path = os.path.join(new_dir, test_filename)
            if not os.path.exists(test_file_path):
                open(test_file_path, 'w').close()
                print(f"Created empty test file: {test_file_path}")
            else:
                print(f"Test file already exists: {test_file_path}")

if __name__ == "__main__":
    # Be careful to write the correct path.
    src = input("Enter path to the folder you want to mirror (e.g., ./domain): ").strip()
    replicate_as_tests(src, dst)
