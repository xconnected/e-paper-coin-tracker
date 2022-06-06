# cointracker on epaper

My attempt to build a coin tracker with an waveshare e-paper display (https://www.waveshare.com/product/displays/e-paper/7.5inch-e-paper-g.htm) and an Raspberry Pi Zero W. Display and raspi are hold together with some aluminium profile - Thats it.

The underlying code is also quite simple and runs along the following steps:

1. Collect coin data from the yahoo finance >> coin-info.py
2. Render a picture out of it, complement it with some additional information and save it as a file called display.png >> coin-info.py
3. display the picture >> display.py

The code is not commented but kept simple so it can be easily understood anyway

![cointracker](https://github.com/xconnected/epapercointracker/blob/main/cointracker.jpg?raw=true "Coin Tracker")


## Installation

### Setup hardware configuration 
Setup the raspi with a lite image e.g. 32bit without GUI) using the raspi-imager.
Make sure you enable SSH, credentialsand set the WiFi configuration correctly.
Once installed open ``raspi-config`` and enable SPI under interfaces.
As usual update the raspi ``sudo apt update`` and ``sudo apt upgrade``
When done start installing the libraries as outlined below.


### Install required Python Libraries
```shell
pip install pytz
pip install mplfinance
pip install yfinance
pip install pillow
```

### Install Display Libraries (Python)
Create a folder where you want to place the code and name it ``waveshare_epd`` and then place the content of ``lib\waveshare_epd`` found here ``https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python`` into this folder

### Update Path Environment Variable
Add the following statements to ``.bashrc`` also make sure is adding this to the path (normally done by default)  ``.profile``

```bash
export PATH=/home/pi/.local/bin:$PATH
```

## Application 
### Required Files 
The following files are being required:

#### [coin symbol].png
PNG graphic file with Logo for Crypto Coin named after the coin symbol size 80x80
e.g. Bitcoin BTC.png

#### font.ttf
Font to be used for dashboard text
e.g. I used DS-DIGI.TTF and renamed to font.ttf
Fonts can be collected from various sites e.g. https://www.wfonts.com/font/ds-digital

## Python Code
### clear.py
Clears the e-paper display
Usage: ``python clear.py``

### coin-info.py
Compiles the ticker dashboard and render it into a bitmap file ``display.png``
Usage: ``python coin-info.py``

### display.py 
Clear the epaper display and show the bitmap file named ``display.png``
Usage: ``python display.py``

### do.sh 
Bash script chaining ``coin-info.py`` and ``display.py``.
This file can be scheduled with crontab

## Scheduling
Add a schedule into crontab 
```shell
crontab -e
```

and add the following line for 30min update intervall
```
*/30 * * * * cd /home/pi/App && bash do.sh > run.log 2>&1
```

Hint: the part ``2>&1``redirects any stderr (error messages) to the standard output

## Known Issues
If there is an issue with version mismatches on numpy the following needs to be done
```shell
sudo pip install numpy --upgrade
sudo apt-get install libatlas-base-dev
```

## References
The information I used to compile this can be found below (thanks to all)

- https://www.waveshare.com/product/raspberry-pi/displays/e-paper/7.5inch-e-paper-hat.htm
- https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python
- https://github.com/mendhak/waveshare-epaper-display#readme
- https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
- https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
- https://crontab.guru/every-30-minutes
