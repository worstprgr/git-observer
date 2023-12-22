# Author and E-Mail Check (AM-C)
## Description
This tool compares the Git author and e-mail address of the latest commit, against a custom whitelist.  

If it found a match, it prints a success message to stdout.  
Else, it prints an error message to stderr and terminates with an exit code 1.  

If you don't want to expose E-Mail addresses into a file in your repo, you can also use secret variables from your CI-Tool.  
See the section *Arguments: -s, --secret (optional)*

> [!Warning]  
> This tool isn't meant for OpSec, only for an additional quality gate.

# Usage
## File Format
The file encoding must be **UTF-8**.  

With the `whitelist.amc` file, you can define which authors should be verified. The syntax for an entry is:
```text
<author name> <email>
             ^ white space in between
```
It doesn't matter if the author name (configured in Git) has multiple whitespaces. The script fetches the information via `--pretty=format:%an %ae`.


Multiple entries are possible and have to be delimited by a newline:
```text
somefirstname somelastname foo@domain.com
somenickname nick@domain.com
```

You can invalidate single entries, by prepending a `#` symbol:
```text
name lastname name@domain.com       <- Not ignored
# name lastname name@domain.com     <- Ignored
- name lastname name@domain.com     <- Ignored
```
Basically you can use any symbol, but if you use something like:
`ignore name lastname name@domain.com` and a coworker has this same exact name configured, it would result in false-positives.

## CI-Integration
In GitHub, you can integrate it in your `*.yml` file with:
```yaml
    - name: Author and E-Mail check
      run: |
        python anypath/am-c/amc.py -p whitelist.amc
```

## Arguments
### -p, --path \<Path> (optional)
You can pass a custom path to the `whitelist.amc`. Just invoke the script with:
```commandline
python amc.py -p path/path/whitelist.amc
```

### -s, --secret (optional)
If you don't want to expose your E-Mail addresses to webcrawlers, you can store the data inside a secret variable 
from your CI environment. 
(See ["Using Secrets in GitHub Actions"](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions) 
for more information)  

You have to set up a new secret variable, named `WHITELIST_AMC`. The content of the variable follows the same
formatting rules, like in the section *File Format*.  
After that, modify your entry in the `*.yml` file and expose the variable to the environment:
```yaml
    - name: Author and E-Mail check
      env:
        WHITELIST_AMC: ${{ secrets.WHITELIST_AMC }}
      run: |
        python amc.py -s
```

## Changing File Name / Env Variable Name
Currently, I leave those both names hard coded, because I don't expect, that they have to be altered that much.  
But if the demand rises, I'm going to implement a config file.  

### Change file name: `whitelist.amc`
Head to:
```text
amc.py
    |- class: FilePaths
        |- self.whitelist_file: pathlib.Path = self.conv_path('whitelist.amc')
```
Change the string `whitelist.amc` to your needs.

### Change env variable name: `WHITELIST_AMC`
Head to:
```text
amc.py
    |- class: FetchSecretEnvVariable
        |- self.whitelist_env: str = 'WHITELIST_AMC'
```
Change the string `WHITELIST_AMC` to your needs.



