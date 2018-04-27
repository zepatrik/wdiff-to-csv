# wdiff to csv
A simple python cli wrapper for wdiff, allowing to edit differences and safe them in a csv file.

Usage:
```
./script.py path/to/file/1 path/to/file/2 path/to/output.csv
```

Note: wdiff has to be installed before.

You can quit in the middle of your editing, your current position will be printed and appended to the csv. Your progress will be saved in the `output.csv`. To continue just add the current position as two seperate numbers after the ouput path.

Available commands:
```
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
    ```
