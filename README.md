# pyfauths.py

This is a python script which emulates a user authenticating to a WatchGuard Fireware OS https portal on port 4100.
It's useful when you cannot use the Watchguard provided authentication or SSO methods, for example when you need to authenticate from a script.

## Usage example
```
./pyfauths.py mywgaddress.mydom.dom login Firebox-DB john
```
Or you can type the password directy on the commandline:

```
./pyfauths.py mywgaddress.mydom.dom login Firebox-DB john itspassword
```
To logout:
```
./pyfauths.py mywgaddress.mydom.dom logout
```

## License
GPLv3

## Security notes
* Putting a cleartext password on the commandline is considered to be not secure.
* This script currently does not verify certificate and is not protected from simple MITM SSL attacks to discover the password

## Compatibility
* Tested on ubuntu 16.04 against Fireware OS 11.11.4
* Does not work on MacOS Sierra, because the installed python 2.7.10 is linked to an old openssl library. You can try to workaround it installing an updated python via [Homebrew](https://brew.sh/)
