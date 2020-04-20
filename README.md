A Python program using Selenium webdriver API to automate searching for Namaste Plaza's namastecart 
delivery or pick-up availability.  
If you are tired of constantly searching for open slots in [Namastecart](https://www.namastecart.com/), 
use this program to do that for you.

---

#### Developed and Tested on:
- macOS Mojave **(10.14.6)**
- Python **3.7.2**

---

## Setup

### Clone repo
```
$ git clone https://github.com/rambattu/namaste-checkgit
```

### Install Chrome webdriver
- Based on the version of your Chrome, please pick up the relevant chrome webdriver
zip file from here:  
https://sites.google.com/a/chromium.org/chromedriver/downloads

- Unzip and place the binary `chromedriver` in the same directory as the repo

### Install python modules

```
$ virtualenv env
$ source env/bin/activate
$ pip install selenium
$ pip install PyYAML
```

```
$ pip list
Package    Version
---------- -------
pip        20.0.2
PyYAML     5.3.1
selenium   3.141.0
setuptools 46.1.3
urllib3    1.25.8
wheel      0.34.2
```

---


## Settings
If you are using this program, I assume you already have an Namastecart account,
if not please create one before using this.  

#### Namastecart deails
Please update your Namastecart account details in [settings.yaml](settings.yaml) file in your local copy
- Replace FANCY_CART_ACCT@EMAIL.COM with your Namaste email id
- Replace SUPER_CRYPTO_PWD with your Namastecart password  

#### Email details 
If you would like to get notified via email when there is an availability, please fill
all 3 sections SENDER_GMAIL_ID, SENDER_GMAIL_PWD, RECEIVER_GMAIL_ID.
SENDER_GMAIL_ID & RECEIVER_GMAIL_ID can be same.  
You will not receive email if any of these 3 fields are missing.  

**For this service to work, you have to relax the security setting for your Gmail account
to allow "Less secure app access", it can be found here https://myaccount.google.com/u/0/lesssecureapps?hl=en. **  

I've only tried with Gmail, not sure if other email services work at this point.

#### Location

Currently there are 4 locations that are available, choose the number for needed one.
- 1 for Lawrence - 1202 APOLLO WAY, SUNNYVALE, CA, 94085
- 2 for Hollenbeck - 1637 HOLLENBECK AVE, SUNNYVALE, CA, 94087
- 3 for Milpitas - 10 S ABBOTT AVE, MILPITAS, CA, 95035
- 4 for San Jose - 1763 CAPITOL EXPY, SAN JOSE, CA, 95121

#### Open Browser
If this setting has value `1`, running will spin up a new instance of Chrome browser
and launches the search activity in that, when it is `0`, no new browser intance gets
kicked off, things will run in the background(in headless mode).

---

**You need to have cart already filled up for this to work and ready for this to work**

## Run the program
```
$ python find_me_slot.py
```

This program keeps running upto 8 hours if it can't find any of the shops listed
in the settings with Delivery or Pickup options.  
If there is a slot open in any of the shops, 
it will print it out to the terminal, and **optionally** sends email
with the details and exits after that.

---

## NOTES
- To be reasonable without overwhelming too much of resources at this time of need, 
I chose 3 minutes interval to keep looking for availability in all listed shops.
This goes on for roughly eight hours and the program quits if it can't find any
after that. You can start again after that.

- I've tested only limited number of times during this exercise, I am not sure if
there are any norms in support or against this approach of browsing.

- Use at your own discretion and please be kind.

---

#### Miscellaneous notes and references used during development of this project
- Started with this https://realpython.com/modern-web-automation-with-python-and-selenium/
    - But had problem with firefox on my machine with headless option
- Switched to this document https://linuxhint.com/browser_automation_selenium_python/
    - Tried with Chrome
    - I had Chrome 80.0 so downloaded the same version from here https://sites.google.com/a/chromium.org/chromedriver/downloads
- For email, We have relax Gmail security settings
    - https://gist.github.com/alexle/1294495#gistcomment-3001681
    - https://myaccount.google.com/u/0/lesssecureapps?hl=en
        [Less secure app access]
- Selenium Python API reference https://selenium-python.readthedocs.io/getting-started.html
- Exception handling http://allselenium.info/how-to-handle-exceptions-in-selenium-python-webdriver/
- http://xpather.com/  Really useful for quick XPath check.
- In Chrome in the developer window, we can get the XPath quickly by right clicking on an element and 
    selection Copy and Copy XPath.