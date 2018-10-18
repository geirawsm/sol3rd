#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import re
from subprocess import check_output
import argparse
import os
import sys
import inspect
from time import sleep
from sol3rd.__version__ import version
from colorama import init, Fore, Style
init(autoreset=True)


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version',
                    action='version',
                    version='%(prog)s {}'.format(version))
parser.add_argument('-V', '--verbose',
                    help='Increase output verbosity',
                    action='store_true', default=False,
                    dest='verbose')
parser.add_argument('-la', '--list-available',
                    help='List available 3rd party apps',
                    action='store_true', default=False,
                    dest='list_available')
parser.add_argument('-li', '--list-installed',
                    help='List installed 3rd party apps',
                    action='store_true', default=False,
                    dest='list_installed')
parser.add_argument('-t', '--test',
                    help='Run the script in test mode',
                    action='store_true', default=False,
                    dest='test')
parser.add_argument('-u', '--upgrade',
                    help='Upgrade installed 3rd party apps',
                    action='store_true', default=False,
                    dest='upgrade')
parser.add_argument('-i', '--install',
                    help='Install a package from 3rd party',
                    action='store', default=False,
                    dest='install')
args = parser.parse_args()


def print_new(output):
    '''
    Instead of normal print, print directly to stdout with a carriage return
    '''
    sys.stdout.flush()
    sys.stdout.write('\r{}'.format(output))


def get_available_apps():
    _start_text = ' [ ] Getting available versions...'
    _stop_text = ' [' + Fore.CYAN + '✔' + Style.RESET_ALL + '] Getting'\
                 ' available versions{}\n'.format(' ' * 20)
    print_new(_start_text)
    if args.test:
        out = {'spotify': {'link': 'testlink', 'version': '2.0',
                           'full_code': ''},
               'teamviewer': {'link': 'testlink', 'version': '2.2',
                              'full_code': 'code to run2'}
               }
        print_new(_stop_text)
    else:
        def get_version_and_summary(link):
            try:
                req = requests.get(link, timeout=5)
            except(requests.exceptions.RequestException) as e:
                print('Couldn\'t connect to getsol.us:\n{}'.format(e))
                sys.exit()
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            version = soup.find('history').find('update').find('version').text
            summary = soup.find('summary').text
            return {'version': version, 'summary': summary}
        out = {}
        try:

            req = requests.get('https://getsol.us/articles/software/'
                               'third-party/en', timeout=5)
        except(requests.exceptions.RequestException) as e:
            print('Couldn\'t connect to solus-project.com:\n{}'.format(e))
            sys.exit()
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        bs_page = soup.find('div', attrs={'data-solbit': 'blog-content'})
        apps = bs_page.find_all('pre')
        i = 0
        for app in apps:
            code_lines = app.text.strip().split('\n')
            full_code = ''
            if len(code_lines) >= 2:
                for line in code_lines:
                    if line == code_lines[len(code_lines) - 1]:
                        full_code += line
                    else:
                        full_code += '{} && '.format(line)
                link = re.search(r'.*(https.*xml)', full_code).group(1)
                app_name = re.search(r'https.*/([a-zA-Z0-9-]+)/.*xml',
                                     full_code).group(1)
                _version_and_summary = get_version_and_summary(link)
                version = _version_and_summary['version']
                summary = _version_and_summary['summary']
                out[app_name] = {'link': link, 'version': version,
                                 'summary': summary, 'full_code': full_code}
            i += 1
            print_new(' [ ] Getting available versions ({}/{}){}'
                      .format(i, len(apps) - 1, ' ' * 10))
    if args.verbose:
        print('{}: Got these available apps:\n{}'
              .format(inspect.stack()[0][3], out))
    print_new(' [' + Fore.CYAN + '✔' + Style.RESET_ALL + '] Getting'
              ' available versions{}\n'.format(' ' * 20))
    return out


def get_installed_apps():
    _start_text = ' [ ] Getting installed versions... {}'.format(' ' * 20)
    _stop_text = ' [' + Fore.CYAN + '✔' + Style.RESET_ALL + '] Getting'\
                 ' installed versions{}\n'.format(' ' * 20)
    print_new(_start_text)
    if args.test:
        installed_apps = {'spotify': {'version': '1.0'},
                          'teamviewer': {'version': '1.1'}}
    else:
        installed_apps = {}
    global apps_available
    apps = apps_available.keys()
    i = 0
    for app in apps:
        if args.test:
            sleep(1)
        else:
            status = check_output(['eopkg', 'info', app]).decode('utf-8')
            if 'Installed package' in status:
                _regex = r'.*\nName\s+:\s+(.*), version: (.*), release.*'
                regex = re.search(_regex, str(status))
                name = regex.group(1)
                version = regex.group(2)
                installed_apps[name] = {'version': version}
        i += 1
        print_new(' [ ] Getting installed versions ({}/{}){}'
                  .format(i, len(apps), ' ' * 10))
    if args.verbose:
        '''
        The following outputs like this:
        {'google-chrome-stable': {'version': '66.0.3359.181'},
         'spotify': {'version': '1.0.80.480'},
         'teamviewer': {'version': '12.0.90041'}}

        '''
        print('These are the installed apps:\n{}'.format(installed_apps))
    print_new(_stop_text)
    return installed_apps


def get_upgradeable():
    '''
    Upgrade app, but only if the available version doesn't match with the
    installed version
    '''
    global apps_available, apps_installed
    upgrade = []
    for app_name, value in apps_installed.items():
        installed_ver = apps_installed[app_name]['version']
        available_ver = apps_available[app_name]['version']
        # If versions mismatch, add them to the 'to_be_upgraded' list
        if installed_ver != available_ver:
            print_new('\n' + Fore.GREEN + 'Upgrading {}'.format(app_name) +
                      Style.RESET_ALL + '\nInstalled: {}\nAvailable: {}'
                      .format(installed_ver, available_ver))
            do_upgrade = str(input('\nOK? (yes or no): '))
            if do_upgrade == 'no' or do_upgrade == 'n':
                print('')
                if args.verbose:
                    print('Skipped upgrading \'{}\''.format(app_name))
                continue
            elif do_upgrade == 'yes' or do_upgrade == 'y':
                upgrade.append(app_name)
                if args.verbose:
                    print('Added\'{}\' to \'upgrade\''.format(app_name))
    if args.verbose:
        print('The following is to be updated:\n{}'.format(upgrade))
    # If there are no apps in the upgrade-list return False
    if not upgrade:
        return False
    else:
        return upgrade


def upgrade(code):
    if args.verbose:
        print('I want to upgrade with the following code:'
              '\n{split}\n{}\n{split}'.format(code, split='-' * 20))
    if args.test and args.verbose:
        print('Dry-running the following code: {}'.format(code))
    else:
        os.system(code)


def main():
    # These two are used both for upgrading and installing so no need to call
    # them twice
    # If the script is called with -i/--install, it should search for what you
    # want, then suggest if it finds something close, else say it didn't find
    # anything
    install = []
    if args.install:
        for install_in in args.install.split(' '):
            for app_available in apps_available.keys():
                if re.search('.*{}.*'.format(install_in), app_available):
                    if app_available in apps_installed.keys():
                        print('\'{}\' already installed, skipping...'
                              .format(app_available))
                        continue
                    else:
                        do_install = str(input('I found app \'{}\', is this '
                                               'the one you want? '
                                               .format(app_available)))
                        if do_install == 'no' or do_install == 'n':
                            print('')
                            if args.verbose:
                                print('Skipped installing \'{}\''
                                      .format(app_available))
                            continue
                        elif do_install == 'yes' or do_install == 'y':
                            install.append(app_available)
                            if args.verbose:
                                print('Added\'{}\' to \'install\''
                                      .format(app_available))
        for install_app in install:
            upgrade(apps_available[install_app]['full_code'])
    # ...but standard procedure for the script is updating existing 3rd party
    # apps
    else:
        apps_upgradeable = get_upgradeable()
        if args.verbose:
            print('I want to upgrade the following:\n{}'
                  .format(apps_upgradeable))
        if not apps_upgradeable:
            print('No 3rd party apps to upgrade')
        else:
            print(Fore.GREEN + 'Updating installed 3rd party apps')
            for app in apps_upgradeable:
                if args.test:
                    os.system("whoami && sleep 3")
                else:
                    upgrade(apps_available[app]['full_code'])
        sys.exit()


if not args.install and not args.upgrade and not args.list_available and not args.list_installed:
        parser.print_help(sys.stderr)
        sys.exit()

apps_available = get_available_apps()
# List the available 3rd party apps and exit
if args.list_available:
    for app in apps_available:
        print(app)
    sys.exit()

apps_installed = get_installed_apps()
# List the installed 3rd party apps and exit
if args.list_installed:
    for app in apps_installed:
        print(app)
    sys.exit()


if __name__ == "__main__":
    main()
