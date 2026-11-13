# news-image-01 entry: writes the front-page image to the output directory.
# The program copies entry.png (which sits next to this file) to
# <output-dir>/entry.png. The directory comes from MAKEFUN_OUTPUT_DIR,
# falling back to /output when the variable is unset or empty. The copy is
# byte-exact, so repeated runs produce identical bytes.

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

# The competition caps the entry image at 1 MiB. Refuse an oversized
# source here instead of shipping a file the gate would reject.
MAX_BYTES = 1048576


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dest = os.path.join(output_dir, "entry.png")
    if os.path.getsize(SOURCE) > MAX_BYTES:
        print(f"error: entry.png is over the {MAX_BYTES} byte cap", file=sys.stderr)
        sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)

    # Post-write self-check: the run only succeeds if the file on disk is
    # a byte-exact copy of the source image. A truncated or corrupted
    # write must fail loudly (exit 1) instead of passing silently, since
    # the grader runs this program twice and requires both runs to write
    # the same bytes.
    with open(SOURCE, "rb") as f:
        expected = f.read()
    with open(dest, "rb") as f:
        written = f.read()
    if written != expected:
        print("error: entry.png does not match the source byte for byte", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {dest} ({len(written)} bytes)")


if __name__ == "__main__":
    main()
