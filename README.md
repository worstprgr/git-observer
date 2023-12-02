[![Linter](https://github.com/worstprgr/git-observer/actions/workflows/flake8.yml/badge.svg)](https://github.com/worstprgr/git-observer/actions/workflows/flake8.yml) 
[![Static CA](https://github.com/worstprgr/git-observer/actions/workflows/pyflake.yml/badge.svg?branch=main)](https://github.com/worstprgr/git-observer/actions/workflows/pyflake.yml) 
[![Unit Tests](https://github.com/worstprgr/git-observer/actions/workflows/unittest.yml/badge.svg)](https://github.com/worstprgr/git-observer/actions/workflows/unittest.yml) 

# Git Alert
Python script to observe a directory in a checked-out repository.
The execution location is indepent from repository, so a automated call is possible.
Ouput will contain a link to local Bitbucket instance as well
## Usage
**-f**:  
_--filepath_ Repository root (location of .git folder)  
**-lf**:  
_--logpath_ Path inside repository to observe  
**-ig**:  
_--ignore_ Author name to be ignored (e.g. your own name)  