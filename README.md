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
I would advise creating a shortcut to ```launch.bat``` and placing it in a convenient location for users to access. One has been provided, but the link location will need to be manually edited.

## Features
- Counting daily customers
- Summing total bar presales

## Roadmap
### Definite
- [ ] Counting daily customers
- [ ] Summing total bar presales
- [ ] Counting same-day bookings
- [ ] Full daily report automation

### Potential
- [ ] Google Sheets integration
- [ ] Resovauto API

## Notes
### Quirks
#### Item Extras
As of ```v1.0.0-alpha.2```, Resovauto calculates bar pre-sales by first counting tickets with pre-sales, and then calculating the total "item extras" added onto each booking. 

Specific item extras aren't exposed to the API in a nice way, so Resovauto just pulls the total item extra value in £GBP, and divides by a constant (£4.00). If any item extras are purchases that aren't divisible by this constant (eg. ABD full exp.) then the output may be inaccurate. 

Since ABD full exp. has been mostly removed now, I don't foresee much issue, but if it poses a problem the fix *is* possible, just difficult.
#### XMAS
When XMAS packages are revoked and renamed, this tool ***will*** break as tickets are identified by a series of hardcoded IDs. When this happens I will update as fast as possible, but expect teething issues.

### Sheffield
This should *theoretically* work for Sheffield and GSAS, but lack of proximity to Sheffield makes it not worthwhile to deploy this there until it's *way* more robust and feature complete. 

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
### Python
- Requests - https://pypi.org/project/requests/
- Rich - https://github.com/Textualize/rich