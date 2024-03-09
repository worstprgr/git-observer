[![Code Check](https://github.com/worstprgr/git-observer/actions/workflows/codecheck.yml/badge.svg)](https://github.com/worstprgr/git-observer/actions/workflows/codecheck.yml)
[![Unit Tests](https://github.com/worstprgr/git-observer/actions/workflows/unittest.yml/badge.svg)](https://github.com/worstprgr/git-observer/actions/workflows/unittest.yml) 

# Observer for Git 

A Python script to observe a directory in a checked-out repository.
The execution location is independent of the repository, so an automated call is possible.
Output will contain commits from past 7 days, each with a link to pre-defined origin (e.g. BitBucket, GitHub) as well

## Graphical User Interface
The Viewer can be called either by passing argument -ui/--use-viewer or by configuring so in configuration file.  
_See [Viewer](./doc/Viewer.md)_

## Dependencies
For consumers, you'll need only Python 3.11+ (might work with 3.8, but it's not tested).  

For contributors, you'll need:  
- pytest
- pyflakes
- flake8

## Command Line Usage

|                       |                                                                                                       |
|-----------------------|-------------------------------------------------------------------------------------------------------|
| -h<br>--help          | Opens the help that shows argument list                                                               |
| -ui<br/>--use-viewer  | Opens the graphical [user interface](./doc/Viewer.md)                                                 |
| -o<br>--origin        | Prefix to build external reference links from                                                         |
| -fp<br>--filepath     | Git repository root directory, the application relies its observations on                             |
| -lf<br>--logfolders   | Relative location of folders inside _filepath_, that should be observed by application                |
| -ig<br>--ignore       | Author name that should be ignored in observations,<br>e.g. your own name since you know what you did |
| -desc<br>--descending | Flag to call _git log_ with reverse parameter<br>_Default TRUE when used with viewer_                 |
| -cnf<br>--config-file | _Absolute path of *.ini file containing the application configuration_                                |

## Running Tests
Inside the projects root directory, you can just invoke `python -m pytest`  

If you want to run tests, linting and static code analysis, you can use that snippet:  
```commandline
cd path-to-root\git-observer
rem ================================= Starting All Tests =================================
flake8 . --count --ignore=W293,E501,W503,W504 --max-complexity=10 --max-line-length=120 --statistics --show-source
pyflakes .
python -m pytest
```
