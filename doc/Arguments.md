# Usage
Arguments of application provided by caller  
_or stored as application configuration file conf.ini (NOT YET IMPLEMENTED)_  

|                      |                                                                                                     |
|----------------------|-----------------------------------------------------------------------------------------------------|
|-h<br>--help         |Opens the help that shows argument list                                                              |
|-ui<br/>--use-viewer |Opens the graphical [user interface](./Viewer.md)                                                    |
|-o<br>--origin       |Prefix to build external reference links from                                                        |
|-fp<br>--filepath    |Git repository root directory, the application relies its observations on                            |
|-lf<br>--logfolders  |Relative location of folders inside _filepath_, that should be observed by application               |
|-ig<br>--ignore      |Author name that should be ignored in observations,<br>e.g. your own name since you know what you did|
|-desc<br>--descending|Flag to call _git log_ with reverse parameter<br>_Default TRUE when used with viewer_                |
|-cnf<br>--config-file|_NOT YET IMPLEMENTED<br>Absolute path of *.ini file containing the application configuration_        |

