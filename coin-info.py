# !/usr/bin/python
import logging
import pytz
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import mplfinance as mpf
import yfinance as yf

g_font = 'font.ttf'
font56 = ImageFont.truetype(g_font, 56)
font22 = ImageFont.truetype(g_font, 22)
font20 = ImageFont.truetype(g_font, 20)
font18 = ImageFont.truetype(g_font, 18)

logging.basicConfig(level=logging.INFO)


def subtract_pos(pos1, pos2):

    return tuple(map(lambda i, j: i - j, pos1, pos2))


def make_image_transparent(image):

    image = image.convert("RGBA")
    data = image.getdata()

    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)

    return image


def get_coin_info(yf_symbol):

    coin = yf.Ticker(yf_symbol)
    data = yf.Ticker(yf_symbol).history("60d")
    data['Volume'] = data['Volume'] / 1000000
    return coin, data


def build_ticker_plot(ticker_data, ticker_plot_size_in, dpi, ticker_plot):

    mc = mpf.make_marketcolors(
        up='white',
        down='black',
        ohlc='inherit',
        edge='black',
        wick={'up': 'black', 'down': 'black'},
        volume='black',
    )
    s = mpf.make_mpf_style(
        base_mpf_style='yahoo',
        rc={'font.size': 10},
        gridcolor='black',
        gridstyle='--',
        gridaxis='horizontal',
        marketcolors=mc
    )

    mpf.plot(
        ticker_data,
        type='candle',
        style=s,
        title='  ',
        ylabel='',
        ylabel_lower='',
        datetime_format='%b %d',
        xrotation=20,
        figsize=ticker_plot_size_in,
        savefig=dict(fname=ticker_plot, dpi=dpi)
    )


def show_param(draw, pos, label, value):

    pos_x = pos[0]
    pos_y = pos[1]
    draw.text(pos, label, font=font20, fill=0)
    draw.text((pos_x, pos_y + 20), value, font=font22, fill=0)

    return pos_x, pos_y + 60


def compile_visual(coin, display_size_px, visual_input, visual_output):

    print(coin.info)
    im1 = Image.open(visual_input)
    im1 = make_image_transparent(im1)
    image_box = im1.getbbox()
    im1 = im1.crop(image_box)
    im1 = im1.convert('1', dither=False)
    text = coin.info['fromCurrency']+'.png'
    im2 = Image.open(text.lower())
    im2 = im2.convert('1', dither=False)

    im = Image.new('1', display_size_px, 255)

    # Paste ticker plot bottom-right
    img_small = subtract_pos(im.size, (10, 10))
    offset = subtract_pos(img_small, im1.size)
    im.paste(im1, offset)

    # Paste logo top-left
    im.paste(im2)

    draw = ImageDraw.Draw(im)
    pos_x = 90
    pos_y = 5
    text = coin.info['name']
    draw.text((pos_x, pos_y), text, font=font56, fill=0)

    pos_x = 90
    pos_y = 60
    tz = pytz.timezone('Europe/Zurich')
    text = datetime.now(tz).strftime("%d-%m-%Y %H:%M:%S")
    draw.text((pos_x, pos_y), text, font=font22, fill=0)

    pos = (10, 120)
    value = f"{coin.info['regularMarketPrice']:,.0f}"
    pos = show_param(draw, pos, 'Price', value)

    value = f"{coin.info['dayHigh']:,.0f}"
    pos = show_param(draw, pos, 'High', value)

    value = f"{coin.info['dayLow']:,.0f}"
    pos = show_param(draw, pos, 'Low', value)

    value = f"{coin.info['previousClose']:,.0f}"
    pos = show_param(draw, pos, 'Last Close', value)

    value = f"{coin.info['twoHundredDayAverage']:,.0f}"
    show_param(draw, pos, 'Average 200', value)

    value = f"{coin.info['volume24Hr']:,.0f}"
    show_param(draw, (400, 10), 'Volume 24h', value)

    value = f"{coin.info['marketCap']:,.0f}"
    show_param(draw, (600, 10), 'Marketcap', value)

    im.save(visual_output)

    return im


def build_ticker_display(symbol, plot_size_in, plot_dpi, display_size_px):

    logging.info("Get coin info...")
    coin, data = get_coin_info(symbol)
    logging.info("Build candle chart...")
    build_ticker_plot(data, plot_size_in, plot_dpi, 'ticker.png')
    logging.info("Build dashboard...")
    im = compile_visual(coin, display_size_px, 'ticker.png', 'display.png')
    logging.info("Done.")

    return im


if __name__ == '__main__':
    logging.info("Build crypto tracker...")
    build_ticker_display('BTC-USD', (6.46, 3.8), 125, (800, 480))
