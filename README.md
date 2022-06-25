# cointracker on epaper

## Introduction
My attempt to build a coin tracker with an waveshare e-paper display (https://www.waveshare.com/product/displays/e-paper/7.5inch-e-paper-g.htm) and an Raspberry Pi Zero W. Display and raspi are hold together with some aluminium profile - Thats it.

The underlying code is also quite simple and runs along the following steps:

1. Collect coin data from the yahoo finance >> coin-info.py
2. Render a picture out of it, complement it with some additional information and save it as a file called display.png >> coin-info.py
3. display the picture >> display.py

The code is not commented but kept simple so it can be easily understood anyway

![cointracker](https://github.com/xconnected/epapercointracker/blob/main/cointracker.jpg?raw=true "Coin Tracker")

If there are any special whishes or ideas to improve the display let me know, or fork the repo into your enhanced version.


## Installation

### Setup hardware configuration 
Setup the raspi with a lite image e.g. 32bit without GUI) using the raspi-imager.

Make sure you enable SSH, credentials and set the WiFi configuration correctly.

Once installed connect to the raspi and perform the usual update

```shell
sudo apt update
sudo apt upgrade
```

To install all the code get ``git``

```shell
sudo apt install git
```

Finally open ``raspi-config`` and enable SPI under interfaces.

As outlined below there are some known issues with the libraries to mitigate them perform the following installs

```shell
sudo pip install numpy --upgrade
sudo apt-get install libatlas-base-dev
sudo apt-get install libopenjp2-tools
```

### Install required Python Libraries
After the system is ready let's prepare the python environment

```shell
pip install pytz
pip install mplfinance
pip install yfinance
pip install pillow
```

### Update Path Environment Variable
Add the following statements to ``.bashrc`` also make sure is adding this to the path (normally done by default)  ``.profile``

```shell
export PATH=/home/pi/.local/bin:$PATH
```

### Application folder
Create the folder to hold the code. In the example below I have chosen ``ct`` as the folder name.
This name will be assumed for the remainder of this readme:

```shell
cd ~
mkdir ct
```

### Install Application Code

Get the application code and copy the contant into the application folder created before

```shell
cd ~
git clone https://github.com/xconnected/e-paper-coin-tracker.git

cp -R e-paper-coin-tracker/* ./ct
```

Grab the font you like e.g. https://www.wfonts.com/font/ds-digital 

```shell
wget <respective url>
cp <original font name.ttf> ./ct/font.ttf
```

If not yet existing make the directory for the display libraries:

```shell
mkdir ./ct/waveshare_epd
```

Get the display libraries and copy the relevant part into the application folder:

```shell
git clone https://github.com/waveshare/e-Paper.git
cp -R e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd/* ./ct/waveshare_epd/*
```

## Use Application Code

### clear.py
Clears the e-paper display e.g. as preparation for a shutdown or break to protect the display
Usage:
```shell
python clear.py
```

### coin-info.py
Compiles the ticker dashboard and render it into a bitmap file ``display.png``
Usage:
```shell
python coin-info.py
```

### display.py 
Clear the epaper display and show the bitmap file named ``display.png``
Usage:
```shell
python display.py
```

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
Mitigation also suggested in the beginning of the installation

**Error Message:**
```shell
...
We have compiled some common reasons and troubleshooting tips at:

    https://numpy.org/devdocs/user/troubleshooting-importerror.html

Please note and check the following:

  * The Python version is: Python3.9 from "/usr/bin/python3"
  * The NumPy version is: "1.22.4"

and make sure that they are the versions you expect.
...
```

**Solution:**
```shell
sudo pip install numpy --upgrade
sudo apt-get install libatlas-base-dev
```

**Error Message:**
```shell
from PIL import Image
../lib/python3.7/site-packages/PIL/Image.py:56: in <module>
    from . import _imaging as core
ImportError: libopenjp2.so.7: cannot open shared object file: No such file or directory
```

**Solution:**
```shell
apt-get install libopenjp2-tools
```


## References
The information I used to compile this can be found below (thanks to all)

- https://www.waveshare.com/product/raspberry-pi/displays/e-paper/7.5inch-e-paper-hat.htm
- https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python
- https://github.com/mendhak/waveshare-epaper-display#readme
- https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
- https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
- https://crontab.guru/every-30-minutes
