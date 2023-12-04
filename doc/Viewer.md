# Graphical User Interface "Viewer"
<img src="../static/favicon.png" alt="GitObserver Logo" style="max-width: 100%; float: left;" width="48px" ></img>  
The more folders are in observation, the less structured can results be presented in comand line.  
This experience was gained fast at our tests, we just took two folders and got annoyed to need scrolling back and forward all the time.  

## Motivation
If we had all information structured in a grid, we could have a great overview what was found in which iteration.
So, the list of observed folders can be _n_ and still would be readable. Having scroll bars would provide the capability to focus on single folders but having other folder information on hand as well in the area out of view.

## Usage
The _Vewer_ can be called either by passing [argument](./Arguments.md) _-ui/--use-viewer_ or by configuring so in configutation file. <br>Please note that it will force use of argument "_descanding_" in order to have descending sorted blocks per result time stamp as seen in our example:  
<img src="./img/LinuxMint_ViewerMain.png" alt="Main view on Linux Mint" style="display: block;" width="850px" />  
_Main view on Linux Mint_  

The first column is used to visualize time stamp of observation. Technically, this is the time when the result is print to UI.  
Each folder has a column for message information "[Author][Title][Author date]" and a column representing the SHA1 of corrisponding commit.  

### Origin
By [argument](./Arguments.md) you can pass a origin which then is used to build a web link with pattern [origin]/[SHA1].  
This link will be opened in system default web browser by double clicking a SHA1 value  
This brings the opputunity to check for Pull Requests or further information inside your local Git management system.  

### Commit message
By double clicking one specific message, a new window pop ups holding the equivalent of  
`git log --pretty='medium'`  
<img src="./img/LinuxMint_ViewerDetails.png" alt="Main view on Linux Mint" style="display: block;" width="850px" />  
_Detail view on Linux Mint_  

## Supported platforms
The UI is based on Python TKinter /\*\* TODO: we cannot do that, can we? \*\*/ meaning that the _Vewer_ can be run anywhere, where a commonly used desktop with Python capability runs.  
Our journey started using **Windows** and continued on **Linux** Mint as well.  
We quite didn't try, if MacOS is supported running _Viewer_ yet.  

## Known Issues  
### Multi-Mon  
Currently we know that the details spawn in primary screen. We actually don't see a problem there but this might change in the future  

### Commit message line breaks
The commit message is presented like we receive it from command line.  
This of course means that text might get strange line breaks. We plan to implement a enhancement on this.

### Sorting might irritates when used first  
Our approach is, that the most important information always has to be top message.  
By this, each blocks content is sorted descending but blocks are sorted ascending. This can be confusing and might change in future releases.  