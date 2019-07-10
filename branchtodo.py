import unidiff
from io import BytesIO
import subprocess
from collections import defaultdict
from clint.textui import colored
import argparse


def do(base_branch, include_dir, exclude_dir):
    maybe_exclude_arg = [] if exclude_dir is None else\
        [':(exclude){}'.format(exclude_dir)]
    args = ["git", "diff", base_branch, "--no-color", "-G", "TODO", "-i",
            '--', include_dir] + maybe_exclude_arg
    raw_diffs = subprocess.check_output(args)
    patch_set = unidiff.PatchSet(BytesIO(raw_diffs), encoding="utf8")
    path_info = defaultdict(list)
    for patch in patch_set:
        for hunk in patch:
            for line in hunk:
                if 'todo' in line.value.lower():
                    if line.is_added or line.is_removed:
                        path_info[patch.path].append(line)
    num_added = 0
    num_removed = 0
    for path in sorted(path_info.keys()):
        print(path)
        for line in path_info[path]:
            if line.is_added:
                num_added += 1
            else:
                num_removed += 1
            val = "{}\t{}".format(
                (line.target_line_no if line.is_added else line.source_line_no),
                line.value.strip())
            print(
                colored.green("+:" + val, bold=True)
                if line.is_added else
                colored.red("-:" + val, bold=True))
        print()
    print("Total: {} additions and {} removals".format(
        colored.green(str(num_added), bold=True),
        colored.red(str(num_removed), bold=True)))


def main():
    parser = argparse.ArgumentParser(description='Review TODOs in current git branch.')
    parser.add_argument('dir', type=str, nargs='?', help='Directory to include', default='.')
    parser.add_argument('--exclude-dir',
                        '-x',
                        type=str,
                        default=None,
                        help='Directory to exclude')
    parser.add_argument('--base-branch',
                        '-b',
                        type=str,
                        dest='base',
                        default='origin/master',
                        help='base branch to search TODOs against (default: origin/master)')

    args = parser.parse_args()
    do(base_branch=args.base, include_dir=args.dir, exclude_dir=args.exclude_dir)


if __name__ == "__main__":
    main()
