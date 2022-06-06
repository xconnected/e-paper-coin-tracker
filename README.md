# epapercointracker
# cointracker on epaper

My attempt to build a coin tracker 
## System Prerequisites
Open raspi-config and enable SPI
```shell
raspi-config
```

### Required Libraries
```shell
pip install pytz
pip install mplfinance
pip install yfinance
pip install pillow
```

### Required System Updates 
Add the following statements to ``.bashrc`` also make sure is adding this to the path (normally done by default)  ``.profile``

```bash
export PATH=/home/pi/.local/bin:$PATH
```

### Known Issues
If there is an issue with version mismatches on numpy the following needs to be done
```shell
sudo pip install numpy --upgrade
sudo apt-get install libatlas-base-dev
```

## Application 
### Required Application Files 
The following files are being required:

#### [coin symbol].png
Logo for Crypto Coin based on the coin symbol 
e.g. Bitvoin BTC.png

#### DS-DIGI.TTF
Font used for dashboard text

## Python Scripts
### clear.py
Clears the e-paper display

### coin-info.py
Compiles the ticker dashboard and render it into a bitmap file ``display.png``

### display.py 
Clear the epaper display and show the bitmap file named ``display.png``

### do.sh 
Bash script chaining ``coin-info.py`` and ``dispaly.py``, which can be scheduled

## Scheduling
Add a schedule into crontab 
```shell
crontab -e
```

and add the following
```
*/30 * * * * cd /home/pi/App && bash do.sh > run.log 2>&1
```

## References
https://www.waveshare.com/product/raspberry-pi/displays/e-paper/7.5inch-e-paper-hat.htm

https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python

https://github.com/mendhak/waveshare-epaper-display#readme

https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh

https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb

https://crontab.guru/every-30-minutes
