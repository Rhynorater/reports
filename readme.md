## Usage:
```
python report.py templatefile.md [args]
```
The resulting report will be opened in default text editor. 

## Templates
When creating a template for your reports, there are two major functionalities you must know: variables and commands. Variables allow you to provide arguments from the command line and these arguments will be substituted into the template in the prescribed areas. Commands will run various PoC command line tools from the current machine and insert the output directly into your report.

### Variables
When generating a report, the following syntax is used `python report.py templatefile.md arg0 arg1 arg2`. In order to insert `argX` (ie, arg0 or arg1, ect...) into your template, you must use the `$` sign along with the argument index. For example `$0` would result in `arg0` being inserted using the command above.


**Example**

template.md:
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `$0`. Bounty Plz. 
```
generate command:
```
python template.md "https://example.com?injection="><script>alert(1)</script>
```

output: 
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `https://example.com?injection="><script>alert(1)</script>`. Bounty Plz. 
```

### Commands

Often times when writing a report, it is useful to be able to show the output of a command. This is possible using the Commands functionality. In order to insert a command into your template, use the `{$ COMMANDHERE }` syntax. This will result in whatever replaces `COMMANDHERE` being run on the command line and the output being injected into the report. Please see the Usage Notes section for quirks.

**Example**

template.md:
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `$0`. Bounty Plz. 

My IP address is: {$ curl ipinfo.io/ip }
```
generate command:
```
python report.py template.md "https://example.com?injection="><script>alert(1)"></script>
```

output: 
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `https://example.com?injection="><script>alert(1)</script>`. Bounty Plz. 

My IP address is: 13.33.33.37
```

### Variables + Commands
It is imperative to be able to insert variables into your templates. Variable processing is done before Command processing, so this works just as you would think it would.

**Example**

template.md:
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `$0`. Bounty Plz. 
You can see that it is injected on line $1 of the vulnerable page: `{$ curl -s $0 | head -n $1 | tail -n 1 }`
```
generate command:
```
python report.py template.md "https://example.com?injection="><script>alert(1)</script> 10
```

output: 
```
Hello! I've discovered an XSS vulnerability in the following endpoint: `https://example.com?injection="><script>alert(1)</script>`. Bounty Plz. 
You can see that it is injected on line 10 of the vulnerable page: `<input id="injection" value=""><script>alert(1)</script>">`
```

### Usage Notes
The way that this tool parses the Commands and passes them to Python's `subprocess` module is via the `.split(" ")`. This is an insecure method since it removes the safety of specifying which pieces of the string are a single argument. This method should not be re-used in application where arbitrary command execution is not the intent. **However**, this does introduce some quirks with strings. For some reason, python doesn't like something like this: `curl "https://example.com"`. It wants something like `curl https://example.com` without the quotes. This is because the quotes are interpreted by the shell as a single argument so if you have spaces or something like that, it can deal with it. However, since we are injecting the parameter directly, the quotes are passed into the target application which is not helpful. This also affects the way the application deals with arguments with spaces in it. Traditionally, if we did something like this `echo "THIS IS ONE ARGUMENT"` the shell would interpret this like so: `[echo, "THIS IS ONE ARGUMENT"]`, However, since quotes and spaces are not friendly with this setup, the shell will see it like this: `[echo, "This, IS, ONE, ARGUMENT"]`, which passes 4 parameters to echo rather than one. That is why this will not function correctly. Please feel free to fix this by issuing a pull request or sending me a message with a recommendation. For now, it doesn't affect my workflow much, so I won't be changing it. Just something to be aware of.

TLDR: Don't use quotes to signify a single command line argument. Also, spaces are used to delimit command line arguments, so if you command has spaces in it, functionality may vary.  

## Want to help me? You can, in 30 seconds...
If you find this tool useful, please give my wife Mariah a follow on Mixer! Simply navigate to https://mixer.com/mariachan, log into your Microsoft account, and click follow! She is nearly to her 2k goal and we'd appreciate any extra support! 
