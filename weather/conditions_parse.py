#!/usr/bin/env python
# coding: utf-8
import argparse
import json
import os
import requests
import sys
from bs4 import BeautifulSoup
from collections import OrderedDict
from datetime import datetime

# Parse output path argument for script
scriptinfo = 'Scrape and parse Accuweather and Moongiant websites'
parser = argparse.ArgumentParser(description=scriptinfo)
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

BASEADDRESS = 'http://www.accuweather.com/'
MOON_ADDRESS = 'http://www.moongiant.com/phase/today'
HEADERS = {'user-agent': 'my-app/0.0.1'}

# Dictionary for matching the Accuweather image label with the
# Conkyweather font letters
image_conkyweather = {'1': 'a', '2': 'b', '3': 'b', '4': 'c', '5': 'c',
                      '6': 'd', '7': 'e', '8': 'f', '11': '0', '12': 'h',
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
    duration = skyobject("span")[2].text.split(' ')[0]
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


def strain_forecast(soup):
    """
    'Strains' the daily forecasts from the data in Accuweather websites.

    Args:
        soup (bs4.element.ResultSet): BeautifulSoup object created with
            '.find_all' command.

    Returns:
        dict: Dictionary of daily weather forecast with the following keys:
            day: Day of the forecast
            high: High temperature of the day
            icon: Character for the Conkyweather font
            line1: First line of the wordwrapped weather description
            line2: Second line of the wordwrapped weather description
            low: Low temperature of the day

    """
    forecast = {}
    for x in range(0, 5):
        dailysoup = soup[x].find_all("div")[0]
        dailyinfo = OrderedDict()
        dailyinfo['day'] = dailysoup('a')[0].text
        dailyinfo['icon'] = image_conkyweather[dailysoup('div')[0]['class'][1]
                                               .split('-')[1]]
        # NOTE: We use 'split' because sometimes we have Fahrenheit unit ('F')
        #       after the degree symbol (°), which causes 'strip' to fail.
        if 'Lo' in dailysoup('span')[1].text:
            dailyinfo['high'] = dailysoup('span')[1].text
            dailyinfo['low'] = dailysoup('span')[0].text.split('°')[0]
        else:
            dailyinfo['high'] = dailysoup('span')[0].text.split('°')[0]
            dailyinfo['low'] = dailysoup('span')[1].text.split('°')[0]
        description = wordwrap(dailysoup('span')[-1].text)
        dailyinfo['line1'] = description[0]
        dailyinfo['line2'] = description[1]
        forecast[x] = dailyinfo
    return forecast


if __name__ == "__main__":
    # Check that we have interent connection
    try:
        response = requests.get(BASEADDRESS, headers=HEADERS)
    except Exception as e:
        sys.exit()

    # The address for the local weather
    localaddress = args.loc
    address = BASEADDRESS + localaddress

    # Get identifier from address
    loc_id = address.split('/')[-1]
    # Parse the Accuweather websites: Most data is collected from this page
    curr_address = (address.split('weather-forecast')[0]
                    + 'current-weather/' + loc_id)
    curr_cond = BeautifulSoup(requests.get(curr_address,
                                           headers=HEADERS).text, 'lxml')
    # Precipitation data is collected from this page
    daily_address = (address.split('weather-forecast')[0]
                     + 'daily-weather-forecast/' + loc_id)
    daily_cond = BeautifulSoup(requests.get(daily_address,
                                            headers=HEADERS).text, 'lxml')
    # Extended forecasts are collected from this page
    final_address = daily_address + '?day=6'
    final_cond = BeautifulSoup(requests.get(final_address,
                                            headers=HEADERS).text, 'lxml')

    # Strain 'curr_cond' soup
    forecast = curr_cond.find(id="detail-now").find_all("div")
    sun = curr_cond.find_all(class_='time-period')[0]
    moon = curr_cond.find_all(class_='time-period')[1]
    records = curr_cond.find(id='feature-history').find_all('td')

    # Strain soup for daily forecasts
    panel_list = curr_cond.find_all("div",
                                    class_="panel-list")[1].find_all("li")
    extended_list = final_cond.find_all("div",
                                        class_="panel-list")[1].find_all("li")

    # Get moon phase info
    moon_info = BeautifulSoup(requests.get(MOON_ADDRESS,
                                           headers=HEADERS).text, 'lxml')

    # Get geolocation info for forecast
    city = curr_cond.find(class_="locality").find().get("title")
    region = curr_cond.find("abbr").get("title")
    country = curr_cond.find(class_="country-name").get("title")

    # Transformations for the forecast data
    wind_icon = forecast[5].find(class_='wind-point').get("class")[1]
    temp = forecast[4]('span')
    misc = forecast[5]('li')

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
    scale = curr_cond.find(checked="checked").get("value")
    if scale == 'celsius':
        scale = 'C'
    else:
        # I think Accuweather misspells Fahrenheit (as 'farenheit).
        # I don't see Accuweather using Kelvin or other scales anytime soon.
        scale = 'F'

    # Collect the weather information
    # Note: '\xc2' is part of the UTF8 representation of the degree symbol
    weather = OrderedDict()
    weather['current_icon'] = image_conkyweather[forecast[2]['class'][1]
                                                 .split('-')[1]]
    weather['current_cond'] = forecast[3]("span")[-1].text
    weather['current_temp'] = temp[0].text.strip('°')
    weather['current_feel'] = temp[1].text.split(' ')[1].strip('°')
    weather['windicon'] = image_conkywindnesw[wind_icon]
    weather['wind_spd'] = misc[1].text
    weather['humidity'] = misc[-7].text.split(': ')[1]
    weather['pressure'] = misc[-6].text.split(': ')[1]
    weather['uv_index'] = misc[-5].text.split(': ')[1]
    weather['cloudcov'] = misc[-4].text.split(': ')[1]
    weather['dewpoint'] = misc[-2].text.split(': ')[1].split('°')[0]
    weather['visiblty'] = misc[-1].text.split(': ')[1]
    weather['sunrise'] = convert_time(sun("span")[0].text)
    weather['sunset'] = convert_time(sun("span")[1].text)
    weather['suntime'] = skytime(sun, weather['sunrise'],
                                 weather['sunset'])
    weather['moonrise'] = convert_time(moon("span")[0].text)
    weather['moonset'] = convert_time(moon("span")[1].text)
    weather['moontime'] = skytime(moon, weather['moonrise'],
                                  weather['moonset'])
    weather['moon_phase'] = moon_dict[7]
    weather['moonshine'] = ''.join(d for d in moon_dict[1] if d.isdigit())+'%'
    weather['moon_minus'] = image_moongiant[moon_minus]
    weather['moon_icon'] = image_moongiant[moon_icon]
    weather['moon_plus'] = image_moongiant[moon_plus]

    # Make separate dictionary for temperature history
    history = OrderedDict()
    history['high_today'] = records[0].text.strip('°')
    history['high_mean'] = records[1].text.strip('°')
    if records[2].text == 'N/A':
        history['high_record'] = 'No record'
        history['high_record_year'] = ''
    else:
        history['high_record'] = records[2].text.split('°')[0]
        history['high_record_year'] = records[2].text.split(' ')[1]
    history['high_last_year'] = records[3].text.strip('°')
    history['low_today'] = records[4].text.strip('°')
    history['low_mean'] = records[5].text.strip('°')
    if records[6].text == 'N/A':
        history['low_record'] = 'No record'
        history['low_record_year'] = ''
    else:
        history['low_record'] = records[6].text.split('°')[0]
        history['low_record_year'] = records[6].text.split(' ')[1]
    history['low_last_year'] = records[7].text.strip('°')

    # Make a dictionary for the precipitation info
    precipitation = OrderedDict()
    precipitation['percent'] = daily_cond.find("span", class_="precip").text
    precipitation['inches'] = (daily_cond.find(class_="stats")('li')[2]
                               .text.split(': ')[1])
    precipitation['hours'] = (daily_cond.find(class_="stats")('li')[-2]
                              .text.split(': ')[1])

    # Collect forecast information and store in nested dictionaries)
    daily_forecasts = strain_forecast(panel_list)
    extended_forecasts = strain_forecast(extended_list)

    # Create a timestamp
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Change directory
    os.chdir(args.outputpath)

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
    text.write("%s\n" % args.scale)
    text.close()
    text = open("forecast", "w")
    for x in range(0, 5):
        for key in daily_forecasts[x].keys():
            text.write("%s\n" % daily_forecasts[x][key])
    for x in range(0, 5):
        for key in extended_forecasts[x].keys():
            text.write("%s\n" % extended_forecasts[x][key])
    text.close()
