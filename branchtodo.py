import unidiff
import StringIO
import subprocess
from collections import defaultdict
from clint.textui import colored

def do():
    raw_diffs = subprocess.check_output(["git", "diff", "origin/master", "--no-color", "-G", "TODO",  "-i"])
    patch_set = unidiff.PatchSet(StringIO.StringIO(raw_diffs), encoding="utf8")
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
        print path
        for line in path_info[path]:
            if line.is_added:
                num_added += 1
            else:
                num_removed +=1
            val = "%s\t%s" % ((line.target_line_no if line.is_added else line.source_line_no), line.value.strip())
            print colored.green("+:"+val ,bold=True) if line.is_added else colored.red("-:"+val, bold=True)
        print
    print "Total:", colored.green(str(num_added), bold=True), "additions and", colored.red(str(num_removed), bold=True), "removals"

if __name__ == "__main__":
    do()
