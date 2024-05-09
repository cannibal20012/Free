from difflib import unified_diff
from glob import glob
from os import makedirs, remove
from os.path import basename, dirname, exists, isdir, join, relpath

BASE_DIR = dirname(dirname(__file__))
CHANGES_DIR = join(BASE_DIR, "changes")
PATCHES_DIR = join(BASE_DIR, "patches")
REFERENCES_DIR = join(dirname(BASE_DIR), ".modules", "freeswitch")


for filepath in glob(pathname=join(CHANGES_DIR, "**", "*"), recursive=True):
    filepath = relpath(filepath, CHANGES_DIR)
    patch_type = filepath.split("/")[0]
    filepath = "/".join(filepath.split("/")[1:])
    changed_file = join(CHANGES_DIR, patch_type, filepath)
    ref_suffix = "%s" if patch_type == "compile" else "conf/vanilla/%s"
    ref_file = join(REFERENCES_DIR, ref_suffix % filepath)
    if isdir(changed_file) or not exists(ref_file):
        continue

    print("patching file %s" % filepath)
    patch_file = join(PATCHES_DIR, patch_type, "%s.patch" % filepath)
    from_name = basename(filepath)
    to_name = "%s.new" % from_name

    # Read contents of the files
    with open(ref_file, "r") as ref, open(changed_file, "r") as changed:
        ref_lines = ref.readlines()
        changed_lines = changed.readlines()

    # Compute the difference between the files
    diff = unified_diff(
        ref_lines, changed_lines, fromfile=from_name, tofile=to_name
    )

    # Save patch file
    if exists(patch_file):
        remove(patch_file)
    makedirs(dirname(patch_file), exist_ok=True)
    with open(patch_file, "w") as patch:
        patch.writelines(diff)
