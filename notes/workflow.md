# General Workflow
_-- Suggestions --_  

### Versioning
Because this tool could have the potential to provide a public API, I would suggest _semantic versioning_.  
Starting with `0.1.0`. After the repo goes public, we increase the version to `1.0.0`.  


### Branches
- the `main` branch is our stable release branch. _(And is protected from direct merges)_
- our "working" branch is `dev`
- only `dev` merges into `main`

### Merge 
Only `rebase` merge allowed, if merging a PR.

### Linter
I would include [Flake8](https://flake8.pycqa.org/en/latest) into the CI Pipeline.

Also, I suggest, that merging with a warning from a linter can still be done. 
Because we don't know yet how much we have to configure the linter.
In a later stage, we can disable the possibility to merge with warnings.  

### Unit Tests
If there'll be unit tests, they should belong to `<module>/tests/`.  
The idea is, to keep the unit tests on the same place, like their counterpart.  

For example:  
```text
project-root
    |- foo1
        |- foo1.py
        |- bar1.py
        |- tests
            |- test_foo1.py
            |- test_bar1.py
    |- foo2
        |- foo2.py
        |- tests
            |- test_foo2.py
```

The unit test module should be the [unittest](https://docs.python.org/3/library/unittest.html)- 
it ships with the standard lib.  

### Pull Request
Since the repo is private, I would suggest merging a PR can be done without approval from the other dev.
If there's some CR needed, then we just add the other dev to the PR as reviewer.  

### Discussion
All discussions regarding the code, should be documented inside the tab "Issues". 
If the discussion happened via Mail/Chat/other, it is enough to write a summary of the discussion inside the ticket.

### Documentation
User documentation should be in `/docs/<example>.md`  

### Using `'` for strings
Since the project contains mostly `'` for strings, we can stick to that.
