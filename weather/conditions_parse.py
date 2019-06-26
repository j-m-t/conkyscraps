#!/usr/bin/env python
# coding: utf-8
"""Scrape and parse Accuweather and Moongiant websites"""

import json
import os
import requests
import sys
import argparse as ap
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Parse output path argument for script
parser = ap.ArgumentParser(prog=__file__,
                           description=__doc__,
                           formatter_class=(ap.RawDescriptionHelpFormatter))
out_help = 'Directory where output from script will be saved'
parser.add_argument('outputpath', help=out_help)
loc_default = 'en/us/washington-dc/20006/weather-forecast/327659'
loc_help = 'Info for Accuweather localization'
parser.add_argument('loc', nargs='?', type=str,
                    const=loc_default,
                    default=loc_default,
                    help=loc_help)
scale_help = 'Desired temperature scale; either \'C\' or \'F\''
parser.add_argument('scale', nargs='?', type=str, const='C',
                    default='C', help=scale_help)
args = parser.parse_args()

localaddress = args.loc
out_scale = args.scale
outputpath = args.outputpath

# The address for the local weather
BASEADDRESS = 'http://www.accuweather.com/'
MOON_ADDRESS = 'http://www.moongiant.com/phase/today'
address = BASEADDRESS + localaddress

# A list of different user-agent headers, for redundancy
REQUEST_HEADERS = {'user-agent': 'my-app/0.0.1'}
WGET_HEADERS = {'user-agent': 'wget/1.18'}

# Dictionary for matching the Accuweather image label with the
# Conkyweather font letters
image_conkyweather = {'01': 'a', '02': 'b', '03': 'b', '04': 'c', '05': 'c',
                      '06': 'd', '07': 'e', '08': 'f', '11': '0', '12': 'h',
                      '13': 'g', '14': 'g', '15': 'm', '16': 'k', '17': 'k',
                      '18': 'i', '19': 'q', '20': 'o', '21': 'o', '23': 'o',
                      '22': 'r', '24': 'E', '31': 'E', '25': 'v', '26': 'x',
                      '29': 'y', '30': '5', '32': '6', '33': 'A', '34': 'B',
                      '35': 'B', '36': 'C', '37': 'C', '38': 'D', '39': 'G',
                      '40': 'G', '41': 'K', '42': 'K', '43': 'O', '44': 'O',
                      '*': '-'}

# Dictionary for matching the wind direction with the
# ConkyWindNESW font letters
image_conkywindnesw = {'CLM': '-', 'S': '1', 'SSW': '2', 'SW': '3', 'WSW': '4',
                       'W': '5', 'WNW': '6', 'NW': '7', 'NNW': '8', 'N': '9',
                       'NNE': ':', 'NE': ';', 'ENE': '<', 'E': '=', 'ESE': '>',
                       'SE': '?', 'SSE': '@'}

# Dictionary for matching the Moongiant image labels with the
# Conkyweather font letters
image_moongiant = {'first': 'T', 'WaxG_50': 'U', 'WaxG_55': 'U',
                   'WaxG_60': 'V', 'WaxG_65': 'W', 'WaxG_70': 'W',
                   'WaxG_75': 'X', 'WaxG_80': 'X', 'WaxG_85': 'Y',
                   'WaxG_90': 'Z', 'WaxG_95': 'Z', 'full': '0',
                   'WanG_95': 'A', 'WanG_90': 'A', 'WanG_85': 'B',
                   'WanG_80': 'C', 'WanG_75': 'C', 'WanG_70': 'D',
                   'WanG_65': 'D', 'WanG_60': 'E', 'WanG_55': 'F',
                   'WanG_50': 'F', 'last': 'G', 'WanC_45': 'H',
                   'WanC_40': 'H', 'WanC_35': 'I', 'WanC_30': 'J',
                   'WanC_25': 'J', 'WanC_20': 'K', 'WanC_15': 'K',
                   'WanC_10': 'L', 'WanC_5': 'M', 'WanC_0': 'M',
                   'new': '1', 'WaxC_0': 'N', 'WaxC_5': 'N',
                   'WaxC_10': 'O', 'WaxC_15': 'P', 'WaxC_20': 'P',
                   'WaxC_25': 'Q', 'WaxC_30': 'Q', 'WaxC_35': 'R',
                   'WaxC_40': 'S', 'WaxC_45': 'S'}


def C2F(temp):
    return str(round(1.8*int(temp)+32))


def F2C(temp):
    return str(int(round((int(temp)-32)/1.8)))


def km2mile(dist):
    return str(int(round(0.6213712*float(dist))))


def mile2km(dist):
    return str(int(round(1.609344*float(dist))))


def mm2inch(measure):
    return str(int(round(0.03937008*float(measure))))


def inch2mm(measure):
    return str(int(round(25.4*float(measure))))


def mbar2hg(pressure):
    return '{:.2f}'.format(0.0295301*float(pressure))


def hg2mbar(pressure):
    # This conversion is a little imprecise
    return '{:.2f}'.format(33.8637526*float(pressure))


# The key relies on the actual scale
conversion = {'Ctemp': C2F, 'Ftemp': F2C,
              'Cdist': km2mile, 'Fdist': mile2km,
              'Cmeasure': mm2inch, 'Fmeasure': inch2mm,
              'Cpressure': mbar2hg, 'Fpressure': hg2mbar}


# The key relies on the desired scale
units_conversion = {'Cspeed': ' km/h', 'Fspeed': ' mph',
                    'Cdist': ' km', 'Fdist': ' mi',
                    'Cmeasure': ' mm', 'Fmeasure': ' in',
                    'Cpressure': ' mb', 'Fpressure': ' in'}


def convert_item(val, item, current_scale, desired_scale):
    """
    Converts the between metric and imperial.

    Args
        val (str): The current value of the item being measured.
        item (str): The item with metric and imperial measures.
        current_scale (str): The temperature being displayed on
            Accuweather. Used as a proxy for metric or imperial measures.
        desired_scale (str): The temperature scale that is desired.
            Like before, this is a proxy for metric or imperial measures.

    Returns:
        str: The converted value.

    """
    if current_scale == desired_scale:
        pass
    else:
        val = conversion[current_scale + item](val)
    return val


def convert_time(time):
    """
    Converts 12-hour time to 24-hour time.

    Args:
        time (str): Time, as reported by Accuweather, in twelve-
            hour AM/PM format.

    Returns:
        str: Time in twenty-four-hour format.

    """
    if time[-2:] == 'AM':
        if time[:2] == '12':
            time = "00" + time[2:-3]
        elif len(time[:-3]) == 4:
            time = "0" + time[:-3]
        else:
            time = time[:-3]
    if time[-2:] == 'PM':
        if time[:2] == '12':
            time = time[:-3]
        else:
            time = str(int(time[:-6])+12)+time[-6:-3]
    return time


def skytime(skyobject, skyrise, skyset):
    """
    Calculates solar or lunar duration if the information is not provided.

    Args:
        skyobject (bs4.element.Tag): BeautifulSoup object containing time
            information.
        skyrise (str): Time when celestial object rises, in twenty-four hour
            format.
        skyset (str): Time when celestial object sets, in twenty-four hour
            format.

    Returns:
        (str) Duration that celestial object is in sky, in hours and minutes.

    """
    duration = skyobject("time", "elapsed")[0].text.split()[0]
    if duration == 'N/A':
        if int(skyset[:2]) > int(skyrise[:2]):
            durhour = int(skyset[:2])-int(skyrise[:2])
        else:
            durhour = 24+int(skyset[:2])-int(skyrise[:2])
        durmin = int(skyset[-2:])-int(skyrise[-2:])
        if durmin < 0:
            durhour -= 1
            durmin += 60
            duration = str(durhour) + ':' + str(durmin)
            return duration
        else:
            duration = str(durhour) + ':' + str(durmin)
            return duration
    else:
        return duration


def wordwrap(text):
    """
    Automates wordwrapping for weather description. If the text is less than
    or equal to 13 characters, keep it at one line. If it is more than 13
    characters, try to split the words into two lines as evenly as possible
    using a crude minimization algorithm.

    Args:
        text (str): Weather description to be wrapped to two lines.

    Returns:
        [str, str]: List of two lines which are as equal in length as possible,
            not allowing for words to be split.

    """
    if len(text) <= 13:
        line1 = text
        line2 = ''
        output = [line1, line2]
    if len(text) > 13:
        words = text.split(' ')
        for x in range(0, len(words)):
            if x == 0:
                line1 = ''
                sum1 = len(words[0])
            else:
                line1 = text[:sum1]
                sum1 = sum(len(s) for s in words[0:x+1])+x
            sum2 = len(text[sum1+1:])
            check = abs(sum1-sum2)
            if x == 0:
                diff = check
            if x > 0:
                if check >= diff:
                    line2 = text[len(line1)+1:]
                    break
                diff = check
        output = [line1, line2]
    return output


def strain_forecast(soup, in_scale='C', out_scale='C'):
    """
    'Strains' the daily forecasts from the data in Accuweather websites.

    Args:
        soup (bs4.element.ResultSet): BeautifulSoup object created with
            '.find_all' command.
        in_scale (str): Temperature scale found on website.
        out_scale (str): Temperature scale desired in output.

    Returns:
        dict: Dictionary of daily weather forecast with the following keys:
            day: Day of the forecast
            high: High temperature of the day
            icon: Character for the Conkyweather font
            line1: First line of the wordwrapped weather description
            line2: Second line of the wordwrapped weather description
            low: Low temperature of the day

    """
    daily_forecast = {}
    day = soup("h3")
    icon = soup("div", "icon")
    daily_highs = soup("span", "hi")
    daily_lows = soup("span", "lo")
    details = soup("div", "details")
    for x in range(0, 5):
        dailyinfo = OrderedDict()
        dailyinfo['day'] = day[x].text
        dailyinfo['icon'] = image_conkyweather[icon[x].contents[1]['src']
                                               .split('/')[-1].split('.')[0]]
        # NOTE: We use 'split' because sometimes we have Fahrenheit unit ('F')
        #       after the degree symbol (°), which causes 'strip' to fail.
        dailyinfo['high'] = convert_item(daily_highs[x].text.split('°')[0],
                                         'temp', in_scale, out_scale)
        if 'Lo' in daily_lows[x].text:
            dailyinfo['low'] = daily_lows[x].text
        else:
            dailyinfo['low'] = '/' + convert_item(daily_lows[x].text
                                                  .split('°')[0].split('/')[1],
                                                  'temp', in_scale, out_scale)
        description = wordwrap(details[x].text)
        dailyinfo['line1'] = description[0]
        dailyinfo['line2'] = description[1]
        daily_forecast[x] = dailyinfo
    return daily_forecast


def main():
    # Set up Selenium options to enable headless access
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options,
                               executable_path='/usr/local/bin/geckodriver')

    # Get identifier from address
    loc_id = address.split('/')[-1]
    # Parse the Accuweather websites: Most data is collected from this page
    curr_address = (address.split('weather-forecast')[0]
                    + 'current-weather/' + loc_id)
    driver.get(curr_address)
    curr_cond = BeautifulSoup(driver.page_source, 'lxml')
    # Precipitation data is collected from this page
    daily_address = (address.split('weather-forecast')[0]
                     + 'daily-weather-forecast/' + loc_id)
    driver.get(daily_address)
    daily_cond = BeautifulSoup(driver.page_source,
                               'lxml')("div", "column detail")[0]
    # Extended forecasts are collected from this page
    final_address = daily_address + '?day=6'
    driver.get(final_address)
    final_cond = BeautifulSoup(driver.page_source, 'lxml')
    driver.quit()

    # Strain 'curr_cond' soup
    # NOTE: Accuweather redesigned their website sometime late 2018, so the
    #       code will need to be strained differently:
    try:
        forecast = curr_cond("div", "conditions-wrapper day")[0]
    except IndexError:
        forecast = curr_cond("div", "conditions-wrapper night")[0]
    sun = curr_cond("div", "block rise-set sun")[0]
    moon = curr_cond("div", "block rise-set moon")[0]
    highs = (curr_cond("table", "temp-history text--size14")[0]
             .contents[3].contents[0].text.split('\n'))
    lows = (curr_cond("table", "temp-history text--size14")[0]
            .contents[3].contents[2].text.split('\n'))

    # Strain soup for daily forecasts
    panel_list = curr_cond("div", "five-day")[0]
    extended_list = final_cond("div", "five-day")[0]

    # Get moon phase info
    # Check that we have interent connection (using EAFP principle)
    # Admittedly, this isn't as clean as I would like.
    try:
        HEADERS = REQUEST_HEADERS
        requests.get(MOON_ADDRESS, headers=REQUEST_HEADERS, timeout=3.05)
    except Exception as e:
        HEADERS = WGET_HEADERS
        pass
    try:
        requests.get(MOON_ADDRESS, headers=WGET_HEADERS, timeout=3.05)
    except Exception as e:
        sys.exit()

    moon_info = BeautifulSoup(requests.get(MOON_ADDRESS,
                                           headers=HEADERS).text, 'lxml')

    # Get geolocation info for forecast
    city = curr_cond.find(class_="locality").find().get("title")
    region = curr_cond.find("abbr").get("title")
    country = curr_cond.find(class_="country-name").get("title")

    # Parse JSON data in moon_info
    moon_dict = json.loads(moon_info("script")[3].string.split("jArray")[1]
                           .rsplit(";")[0].lstrip("="))['2']
    moon_minus = (moon_info('img', class_='moonNotToday')[1].attrs['src']
                  .split('moon_day_')[1].split('.')[0])
    moon_icon = (moon_info.find(id='todayMoonContainer').find().get('alt')
                 .split('moon_phase_')[1])
    moon_plus = (moon_info('img', class_='moonNotToday')[2].attrs['src']
                 .split('moon_day_')[-1].split('.')[0])

    # Determine temperature scale used in HTML
    scale = (curr_cond("div", "subnav-dropdown-container location-crumbs")[0]
             .contents[5].contents[3].text[-1])
    # [2018-11-15 Thu] Accuweather changed their setup, and now there is no
    # explicit declaration of the scale used on the page, so I scrape it from
    # its appearance on the top of the page.
    # I don't see Accuweather using Kelvin or other scales anytime soon.

    # Collect the weather information
    # NOTE: I strip the degree symbol to be able to do conditional comparisons
    #       of the temperatures in Conky.  I later append the degree symbols in
    #       the Lua script.
    # NOTE: '\xc2' is part of the UTF8 representation of the degree symbol
    weather = OrderedDict()
    weather['current_icon'] = image_conkyweather[forecast("div", "icon")[0]
                                                 .contents[1]['src']
                                                 .split('/')[-1]
                                                 .split('.')[0]]
    weather['current_cond'] = forecast("div", "phrase")[0].text
    weather['current_temp'] = convert_item(forecast("div", "hi")[0]
                                           .text.strip('°'),
                                           'temp', scale, out_scale)
    weather['current_feel'] = convert_item(forecast("div", "realfeel")[0]
                                           .text.split()[1]
                                           .strip('°'),
                                           'temp', scale, out_scale)
    weather['windicon'] = image_conkywindnesw[forecast("div", "wind-point")
                                              [0]['class'][1]]
    weather['wind_spd'] = (convert_item(forecast("div", "speed")[0]
                                        .text.split()[0],
                                        'dist', scale, out_scale)
                           + units_conversion[out_scale + 'speed'])
    weather['humidity'] = (forecast("div", "details")[0]
                           .contents[1].text.split()[1])
    weather['pressure'] = (convert_item(forecast("div", "details")[0]
                                        .contents[3].text.split()[1],
                                        'pressure', scale, out_scale)
                           + units_conversion[out_scale + 'pressure'])
    weather['uv_index'] = (forecast("div", "details")[0]
                           .contents[5].text.split()[-1])
    weather['cloudcov'] = (forecast("div", "details")[0]
                           .contents[7].text.split()[-1])
    weather['dewpoint'] = convert_item(forecast("div", "details")[0]
                                       .contents[11].text
                                       .split()[2].strip('°'),
                                       'temp', scale, out_scale)
    weather['visiblty'] = (convert_item(forecast("div", "details")[0]
                                        .contents[13].text.split()[1],
                                        'dist', scale, out_scale)
                           + units_conversion[out_scale + 'dist'])
    weather['sunrise'] = convert_time(sun("time", "rise")[0].text)
    weather['sunset'] = convert_time(sun("time", "set")[0].text)
    weather['suntime'] = skytime(sun, weather['sunrise'],
                                 weather['sunset'])
    weather['moonrise'] = convert_time(moon("time", "rise")[0].text)
    weather['moonset'] = convert_time(moon("time", "set")[0].text)
    weather['moontime'] = skytime(moon, weather['moonrise'],
                                  weather['moonset'])
    weather['moon_phase'] = moon_dict[7]
    weather['moonshine'] = ''.join(d for d in moon_dict[1] if d.isdigit())+'%'
    weather['moon_minus'] = image_moongiant[moon_minus]
    weather['moon_icon'] = image_moongiant[moon_icon]
    weather['moon_plus'] = image_moongiant[moon_plus]

    # Make separate dictionary for temperature history
    history = OrderedDict()
    history['high_today'] = convert_item(highs[2].strip('°'),
                                         'temp', scale, out_scale)
    history['high_mean'] = convert_item(highs[3].strip('°'),
                                        'temp', scale, out_scale)
    if highs[5] == 'N/A':
        history['high_record'] = 'No record'
        history['high_record_year'] = ''
    else:
        history['high_record'] = convert_item(highs[5].split('°')[0],
                                              'temp', scale, out_scale)
        history['high_record_year'] = highs[5].split()[1]
    history['high_last_year'] = convert_item(highs[7].strip('°'),
                                             'temp', scale, out_scale)

    history['low_today'] = convert_item(lows[2].strip('°'),
                                        'temp', scale, out_scale)
    history['low_mean'] = convert_item(lows[3].strip('°'),
                                       'temp', scale, out_scale)
    if lows[5] == 'N/A':
        history['low_record'] = 'No record'
        history['low_record_year'] = ''
    else:
        history['low_record'] = convert_item(lows[5].split('°')[0],
                                             'temp', scale, out_scale)
        history['low_record_year'] = lows[5].split()[1]
    history['low_last_year'] = convert_item(lows[7].strip('°'),
                                            'temp', scale, out_scale)

    # Make a dictionary for the precipitation info
    precipitation = OrderedDict()
    precipitation['percent'] = daily_cond.text.split('\n')[2].split()[1]
    precipitation['amount'] = (convert_item(daily_cond.text
                                            .split('\n')[3].split()[1],
                                            'measure', scale, out_scale)
                               + units_conversion[out_scale + 'measure'])
    precipitation['hours'] = daily_cond.text.split('\n')[7].split()[3] + " hrs"

    # Collect forecast information and store in nested dictionaries)
    daily_forecasts = strain_forecast(panel_list, scale, out_scale)
    extended_forecasts = strain_forecast(extended_list, scale, out_scale)

    # Create a timestamp
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Change directory
    os.chdir(outputpath)

    # Write output
    text = open("conditions", "w")
    for key in weather.keys():
        text.write("%s\n" % weather[key])
    for key in history.keys():
        text.write("%s\n" % history[key])
    for key in precipitation.keys():
        text.write("%s\n" % precipitation[key])
    text.write("%s, %s\n" % (city, region))
    text.write("%s\n" % country)
    text.write("%s\n" % now)
    text.write("%s\n" % out_scale)
    text.close()
    text = open("forecast", "w")
    for x in range(0, 5):
        for key in daily_forecasts[x].keys():
            text.write("%s\n" % daily_forecasts[x][key])
    for x in range(0, 5):
        for key in extended_forecasts[x].keys():
            text.write("%s\n" % extended_forecasts[x][key])
    text.close()
    return None


if __name__ == "__main__":
    main()
