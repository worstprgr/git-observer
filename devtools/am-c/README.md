# Author and E-Mail Check (AM-C)
## Description
This tool compares the Git author and e-mail address of the latest commit, against a custom white list.  

If it found a match, it prints a success message to stdout.  
Else, it prints an error message to stderr and terminates with an exit code 1.

This tool isn't meant for OpSec, only for an additional quality gate.

## Usage
### Basic
With the `whitelist.amc` file, you can define which authors should be verified. The syntax for an entry is:
```text
<author name> <email>
             ^ white space in between
```

You can also ignore single entries, by prepending '#':
```text
name lastname name@domain.com      <- Not ignored
# name lastname name@domain.com    <- Ignored
```

### Arguments
You can pass a custom path to the `whitelist.amc`. Just invoke the script with:
```commandline
python amc.py -p path/path/whitelist.amc
```


## CI-Integration
In GitHub, you can integrate it in your `*.yml` file with:
```yaml
    - name: Author and E-Mail check
      run: |
        python anypath/am-c/amc.py -p whitelist.amc
```

