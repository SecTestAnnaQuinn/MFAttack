# MFAttack
An MFA brute forcer to use against inadequately secured mfa solutions.  This is based on labs found in Portswigger Academy's MFA Authentication section.  This will not bypass WAF, so be aware of that before using so you are not IP blocked.  In addition, please be aware of the password lockout policies on accounts, this is a brute force and will lock out accounts.

However, should you find a 2fa solution that requires you to login and input a 2FA code immediately after, this tool should work well for you.  If the site uses CSRF tokens, the tool will automatically detect them and use them in the attack.  This script currently assumes that the CSRF tokens are granted by the pages directly referenced.  However, iterative searching of all requests after the initial redirect is not yet implemented, and as such middleware tokens may not be detected.  This is soon to come in upcoming versions.  If CSRF tokens are not used, threading is activated to speed the attack, however further work remains to be done to allow threading on sites that utilize the tokens.

## Installation

Installation should be simple.  After cloning the repo, run `pip3 install -r requirements.txt`.  After that, the tool can be run with the following options:

```code
usage: MFAttack.py [-h] [-u USERNAME] [-p PASSWORD] [--url URL] [-m MFACHARS]

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
  --url URL             Full Url to login page
  -m MFACHARS, --mfachars MFACHARS
                        Number of characters in the MFA code
```
