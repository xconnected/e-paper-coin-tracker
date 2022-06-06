# !/usr/bin/python
import logging
from waveshare_epd import epd7in5_V2

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Clear display...")
    epd = epd7in5_V2.EPD()

    try:
        epd.init()
        epd.Clear()
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
