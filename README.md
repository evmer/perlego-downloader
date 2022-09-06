# Perlego PDF Downloader
Download books from Perlego.com in PDF format.

## Installation
### Install wkhtmltopdf:
  **• Windows:** 
  
  Download intaller [from here](https://wkhtmltopdf.org/downloads.html).

  **• Debian/Ubuntu:**
  
  Get a static version of wkhtmltopdf [from here](https://wkhtmltopdf.org/downloads.html) or download the latest release:
  >$ sudo apt-get install wkhtmltopdf
  
  **• macOS:**
  >$ brew install wkhtmltopdf

### Install python dependencies:
  >$ pip3 install -r requirements.txt

## Configuration
Edit *BOOK_ID* and *AUTH_TOKEN* constants in downloader.py.

You can find the **BOOK_ID** in the Perlego's book page URL:
![perlego-downloader](https://i.postimg.cc/r8qtcCdd/Screenshot-2022-09-01-at-09-57-38.png)

Grab the **AUTH_TOKEN** (Perlego API Authentication Bearer Token) analyzing the browser traffic (look at the Network tab of Chrome's Inspect Element):

![perlego-downloader](https://i.postimg.cc/QhZwXHbL/Screenshot-2022-09-01-at-09-55-15.png)

## Run!
>$ python3 downloader.py

## Demonstration video
https://www.youtube.com/watch?v=-OidkWsjzJE

[![perlego-downloader](https://img.youtube.com/vi/-OidkWsjzJE/0.jpg)](https://www.youtube.com/watch?v=-OidkWsjzJE)

# DISCLAIMER:
The code is not intended for piracy or unlawful re-sharing purposes. You can only download the books you have purchased for the sole purpose of personal use. I do not take responsibility for illegal use of the software.
