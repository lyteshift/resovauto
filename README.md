# resovauto
## Overview
Resovauto *currently* a terminal utility for interacting with The Great Escape Game's Resova booking system. 
## Installation
Before running, you **must** create a file titled ```key.txt``` in the directory containing ```main.py``` and paste in your Resova API key to that file.

```launch.bat``` helpfully installs Python to the system if not already installed, and will create a venv and acquire all the packages it needs automagically. To reinstall, delete both the folder ```.venv``` and ```praise_the_omnissiah.md```

To get a Resova API key, you must login to https://enterprise.resova.co.uk using an enterprise account with admin priveliges, navigate to your site, and go to https://app.resova.co.uk/settings/general/developer/apikey, generate a new key and copy it to ```key.txt```.

You must also add your site's IP address to Resova on the following page: https://app.resova.co.uk/settings/general/developer/whitelisting

I don't know if both Leeds and Sheffield have static IPs configured, so if the tool stops working, check this first.
### API Key Security
Do ***NOT*** upload this key to Github. Do ***NOT*** share this key. If you believe your key to be compromised, go to https://app.resova.co.uk/settings/general/developer/apikey and click the "refresh" button.
### Other installation considerations
I would advise creating a shortcut to ```launch.bat``` and placing it in a convenient location for users to access.
## Features
- Counting daily customers
- Summing total bar presales
## Roadmap
- Counting same-day bookings
## Troubleshooting
1. Check your current IP is the same as the one listed on https://app.resova.co.uk/settings/general/developer/whitelisting
2. Try a new API key.
3. Check the status of Resova's booking site.
4. Conduct the holy rite of troubleshooting, details in ```praise_the_omnissiah.md``` 
5. Just count manually, man.
6. Contact me through WhatsApp, if you don't have my details ask someone in the Supes group.
7. Raise an issue on GitHub if you know how https://github.com/lyteshift/resovauto

## Contributing
If you wish to contribute to the main repo, you'll need a private SSH key. Contact George for information.

## Developers
George Cash-Blackmore / georgecb05@gmail.com
## Required Packages
- requests
- rich