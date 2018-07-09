# sol3rd
Install 3rd party apps in Solus or upgrade them.

&nbsp;

## Short description

This script scrapes the apps on the [3rd party list](https://solus-project.com/articles/software/third-party/en/) on solus-project.com and can either check for available upgrades or install an app from that page.

&nbsp;

## Installation

It can't get any more simple than `pip`:

`pip install sol3rd`

&nbsp;

## How to use

```
usage: sol3rd [-h] [-v] [-t] [-u] [-i INSTALL]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -t, --test            Run the script in test mode
  -u, --upgrade         Upgrade installed 3rd party apps
  -i INSTALL, --install INSTALL
                        Install a package from 3rd party
```




## Dependencies:
- colorgram
- Pillow