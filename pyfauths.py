#!/usr/bin/env python3

# PYFAUTHS A WatchGuard Fireware portal https authentication script
# Copyright (c) 2017, Giovanni Panozzo https://github.com/giox069

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import ssl
import urllib.request
import argparse
import sys
from getpass import getpass


# -----------------
WGURL='https://%s:4100/wgcgi.cgi'

# -----------------
PARAMSLOGIN = {
	'fw_username': '',
	'fw_password': '',
	'fw_domain': '',
	'submit': 'Login',
	'action': 'fw_logon',
	'fw_logon_type': 'logon',
	'redirect': '',
	'lang': 'en-US'
}

PARAMSLOGOUT = {
	'Logout': 'Logout',
	'action': 'fw_logon',
	'fw_logon_type': 'logout'
}

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		infourl = urllib.request.addinfourl(fp, headers, req.get_full_url())
		# infourl.status = code
		# infourl.code = code
		return infourl
	http_error_300 = http_error_302
	http_error_301 = http_error_302
	http_error_303 = http_error_302
	http_error_307 = http_error_302

def FirewarePost(fwaddr, postparams):
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	h = urllib.request.HTTPSHandler(context=ctx)
	opener = urllib.request.build_opener(h, NoRedirectHandler())
	data = urllib.parse.urlencode(postparams)
	data = data.encode('utf-8')

	url = WGURL % (fwaddr)
	request = urllib.request.Request(url, data=data)
	request.add_header('Content-type', 'application/x-www-form-urlencoded')
	request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	request.get_method = lambda: "POST"
	con = opener.open(request)

	if "success.shtml" in con.headers['location']:
		print("Successfully logged in")
		rc = True
	elif "=501" in con.headers['location']:
		print("Authentication failed: invalid credentials")
		rc = False
	elif "=502" in con.headers['location']:
		print("Successfully logged out")
		rc = True
	elif "=503" in con.headers['location']:
		print("Seession expired")
		rc = False
	elif "=504" in con.headers['location']:
		print("Timeout")
		rc = False
	elif "=505" in con.headers['location']:
		print("Authentication failed: User is already logged in from another host.")
		rc = False
	elif "=506" in con.headers['location']:
		print("Invalid logon type")
		rc = False
	else:
		print("Unable to understand response from https server")
		rc = False

	return rc

def FirewareLogin(args):
	if len(args.password) == 0:
	    password = getpass()
	else:
	    password = args.password[0]
	postparams = PARAMSLOGIN
	postparams['fw_domain'] = args.domain
	postparams['fw_username'] = args.username
	postparams['fw_password'] = password
	return FirewarePost(args.fwaddress, postparams)

def FirewareLogout(args):
	postparams = PARAMSLOGOUT
	return FirewarePost(args.fwaddress, postparams)


parser = argparse.ArgumentParser(description='Fireware Authentication Script')
parser.add_argument('fwaddress', help='IP address of Fireware box')
subparsers = parser.add_subparsers(help='sub-command help')

logon_parser = subparsers.add_parser('login', help='Login to firebox')
logon_parser.add_argument('domain', help="Domain. Use 'Firebox-DB' to logon as Firebox user")
logon_parser.add_argument('username', help='Username')
logon_parser.add_argument('password', nargs='*', help='password')
logon_parser.set_defaults(func=FirewareLogin)

logoff_parser = subparsers.add_parser('logout', help='Logout from firebox')
logoff_parser.set_defaults(func=FirewareLogout)

args = parser.parse_args()

if not 'func' in args:
    print("Nothing to do")
    sys.exit(1)

if args.func(args):
	sys.exit(0)
else:
	sys.exit(1)

