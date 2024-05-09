import shutil
import subprocess
from glob import glob
from os import makedirs
from os.path import dirname, exists, isdir, join, relpath, abspath
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--target", action="store", type=str, required=True)
parser.add_argument(
    "--type", action="store", choices=("compile", "conf"), required=True
)
args = parser.parse_args()

if exists(args.target):
    args.target = abspath(args.target)
else:
    parser.error("argument --target: target must exists: %s" % args.target)

BASE_DIR = dirname(dirname(__file__))
PATCHES_DIR = join(BASE_DIR, "patches", args.type)
CHANGES_DIR = join(BASE_DIR, "changes", args.type)
TARGET_DIR = args.target

for filepath in glob(pathname=join(CHANGES_DIR, "**", "*"), recursive=True):
    filepath = relpath(filepath, CHANGES_DIR)
    source_file = join(CHANGES_DIR, filepath)
    target_file = join(TARGET_DIR, filepath)
    if isdir(source_file):
        continue

    if not exists(target_file):
        # Copy file as is
        print("patching file %s" % target_file)
        makedirs(dirname(target_file), exist_ok=True)
        shutil.copyfile(source_file, target_file)
        continue

    patch_file = join(PATCHES_DIR, "%s.patch" % filepath)
    if not exists(patch_file):
        continue

    # Patch file
    with open(patch_file, "r") as changes:
        proc = subprocess.run(
            ["patch", target_file], stdin=changes, cwd=dirname(target_file)
        )
        if proc.returncode != 0:
            raise RuntimeError("Failed to patch %s" % target_file)
