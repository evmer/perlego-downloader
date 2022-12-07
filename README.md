# Perlego PDF Downloader
Download books from Perlego.com in PDF format.

## Installation

Install Python 3 and run:

  >$ pip3 install -r requirements.txt

## Configuration
Please watch the [demonstration video](https://youtu.be/X4msqCulOYk).

You'll need to find the *authToken*, *bookId* and *reCaptchaToken* analyzing the browser/websocket traffic and replace the constants in downloader.py.

## Run!
>$ python3 downloader.py

## Troubleshoot
Windows users may encounter the following error messages running the script:
> The application has failed to start because its side-by-side configuration is incorrect

> pyppeteer.errors.BrowserError: Browser closed unexpectedly

This issue can be solved reinstalling the chrome client with:
>$ pyppeteer-install.exe

If the issue persists, please try:
1) to manually (re)install [chrome](https://www.google.com/chrome/) on your computer or download the correct version of [chromedriver](https://sites.google.com/chromium.org/driver/) and add it to the system path (ie. C:/Windows);
2) modify line 171 adding `executablePath` with the correct path of Chrome executable:

```
			'headless': True,
			'autoClose': False,
			'executablePath': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
```

# DISCLAIMER:
The code is not intended for piracy or unlawful re-sharing purposes. You can only download the books you have purchased for the sole purpose of personal use. I do not take responsibility for illegal use of the software.
