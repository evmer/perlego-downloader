# Perlego PDF Downloader
Download books from Perlego.com in PDF format.

## Installation

Install Python 3 and run:

  >$ pip3 install -r requirements.txt

## Configuration
Edit *BOOK_ID* and *AUTH_TOKEN* constants in downloader.py.

You can find the **BOOK_ID** in the Perlego's book page URL:
![perlego-downloader](https://i.postimg.cc/r8qtcCdd/Screenshot-2022-09-01-at-09-57-38.png)

Grab the **AUTH_TOKEN** (Perlego API Authentication Bearer Token) analyzing the browser traffic (look at the Network tab of Chrome's Inspect Element):

![perlego-downloader](https://i.postimg.cc/QhZwXHbL/Screenshot-2022-09-01-at-09-55-15.png)

## Run!
>$ python3 downloader.py

## Troubleshoot
Windows users may encounter the following error messages running the script:
> The application has failed to start because its side-by-side configuration is incorrect

> pyppeteer.errors.BrowserError: Browser closed unexpectedly

This issue can be solved reinstalling the chrome client with:
>$ pyppeteer-install.exe

If the issue persists, please try to (re)install [chrome](https://www.google.com/chrome/) on your computer or download the [chromedriver](https://sites.google.com/chromium.org/driver/) and add it to the system path.

## Demonstration video
https://www.youtube.com/watch?v=-OidkWsjzJE

[![perlego-downloader](https://img.youtube.com/vi/-OidkWsjzJE/0.jpg)](https://www.youtube.com/watch?v=-OidkWsjzJE)

# DISCLAIMER:
The code is not intended for piracy or unlawful re-sharing purposes. You can only download the books you have purchased for the sole purpose of personal use. I do not take responsibility for illegal use of the software.
