# pyfauths.py

This is a python script which emulates a user authenticating to a WatchGuard Fireware OS https portal on port 4100.
It's useful when you cannot use the Watchguard provided authentication or SSO methods, for example when you need to authenticate from a script.

## Usage example
```
./pyfauths.py mywgaddress.mydom.dom login Firebox-DB john itspassword
./pyfauths.py mywgaddress.mydom.dom logout
```

## License
GPLv3

## Security notes
* Putting a cleartext password on the commandline is considered to be not secure.
* This script currently does not verify certificate and is not protected from simple MITM SSL attacks to discover the password

