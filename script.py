import sys
import subprocess
import re
from colored import fg, attr

with open(sys.argv[1], 'r') as f:
    text1 = f.read()

with open(sys.argv[2], 'r') as f:
    text2 = f.read()

diff = ''
try:
    diff = subprocess.check_output(['wdiff', sys.argv[1], sys.argv[2]])
except subprocess.CalledProcessError as grepexc:
    diff = grepexc.output

added = map(lambda s: s[2:-2], re.findall("\{\+[^{}]*\+\}", diff))
added.append('$end$')

removed = map(lambda s: s[2:-2], re.findall("\[-[^\[\]]*-\]", diff))
removed.append('$end$')

output = []
history_a = []
history_r = []

print("""input commands to manipulate found diffs:
    sa      skip added
    sr      skip removed
    s       skip both
    a       add current tuple to output
    da      delete last added tuple
    ca      concat added to next match
    cr      concat removed to next match
    rla     remove left char of added
    rlr     remove left char of removed
    rra     remove right char of added
    rrr     remove right char of removed
    ua      undo on added
    ur      undo on removed
    ba      jump back in added
    br      jump back in removed
    b       jump back in both
    end     stop and write output
    cancel  stop and don't write output
    
    $end$ means the end of the list is reached
          skipping the end terminates the script
""")

j = 0 if len(sys.argv) < 5 else int(sys.argv[4])
i = 0 if len(sys.argv) < 6 else int(sys.argv[5])
last_answer = ''

try:
    while i < len(added) and j < len(removed):
        answer = raw_input('\n%s%s\n%s%s%s\n' % (fg(1), removed[j], fg(2), added[i], attr(0)))

        if answer == '':
            answer = last_answer

        last_answer = answer
        if answer == 'a':
            output.append((removed[j], added[i]))
            i += 1
            j += 1
        elif answer == 's':
            i += 1
            j += 1
        elif answer == 'b':
            i -= 1
            j -= 1
        elif answer == 'sa':
            i += 1
        elif answer == 'sr':
            j += 1
        elif answer == 'ba':
            i -= 1
        elif answer == 'br':
            j -= 1
        elif answer == 'rl':
            added[i] = added[i][1:]
            removed[j] = removed[j][1:]
        elif answer == 'rr':
            added[i] = added[i][:-1]
            removed[j] = removed[j][:-1]
        elif answer == 'rla':
            added[i] = added[i][1:]
        elif answer == 'rlr':
            removed[j] = removed[j][1:]
        elif answer == 'rra':
            added[i] = added[i][:-1]
        elif answer == 'rrr':
            removed[j] = removed[j][:-1]
        elif answer == 'ca' and added[i+1] != '$end$':
            history_a.append((added[j], added[j + 1]))
            added[i] += added[i+1]
            del added[i+1]
        elif answer == 'cr' and removed[j+1] != '$end$':
            history_r.append((removed[j], removed[j + 1]))
            removed[j] += removed[j+1]
            del removed[j+1]
        elif answer == 'ua':
            added.insert(i+1, '')
            added[i], added[i+1] = history_a.pop()
        elif answer == 'ur':
            removed.insert(j+1, '')
            removed[i], removed[i + 1] = history_r.pop()
        elif answer == 'da':
            added.pop()
        elif answer == 'end':
            print 'current position: ', i, j
            break
        elif answer == 'cancel':
            exit(0)
except:
    print 'an error occurred, but your changes until now should have been saved'
    print 'current position: ', i, j
    pass

with open(sys.argv[3], 'w' if len(sys.argv) <= 4 else 'a') as f:
    f.writelines(map(lambda x: '"%s","%s"\n' % x, output))
    f.write('current position: %d %d\n' % (i, j))
