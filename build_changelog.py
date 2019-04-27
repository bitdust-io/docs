head = "# BitDust Change Log"

import os
import sys

full_changelog = open(sys.argv[1]).read()
strip_header = '\n'.join(full_changelog.split('\n')[2:])

fout = open(sys.argv[2], 'w')
fout.write(head)
fout.write(strip_header)
fout.close()
