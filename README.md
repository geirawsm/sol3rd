# sol3rd
Install 3rd party apps in Solus or upgrade them.

&nbsp;

## Short description

This script scrapes the apps on the [3rd party list](https://getsol.us/articles/software/third-party/en) on getsol.us and can either check for available upgrades or install an app from that page.

&nbsp;

## Installation

Before performing installation, it is recommended that you install dependencies through `eopkg` before installing sol3rd:

`sudo eopkg it python-beautifulsoup4 python-html5lib python-colorama python-webencodings python-requests python-idna python-certifi python-six python-urllib3`

Then install sol3rd with `pip`:

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
- Python 3
- Beautiful Soup 4