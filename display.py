# !/usr/bin/python

import logging
from PIL import Image
from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.INFO)


def main():

    epd = epd7in5_V2.EPD()

    try:
        logging.info("Init and clear epd7in5_V2...")
        epd.init()

        logging.info("Load and display image file...")
        im = Image.open('display.png')
        epd.display(epd.getbuffer(im))

        logging.info("Bring display into sleep...")
        epd.sleep()

        logging.info("Done.")

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd.init()
        epd.Clear()
        epd7in5_V2.epdconfig.module_exit()
        exit()


if __name__ == '__main__':
    main()

