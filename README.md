# conkyscraps
A collection of Python scripts for Conky configurations

### Screenshot
[![screenshot](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)

### Requirements
These scripts are set up to run with Python 3. ```Selenium``` is used to access Accuweather, ```requests``` is used to access other sites, and ```BeautifulSoup``` is used to scrape them all.  You also need ```Conky```, of course.

* `Selenium` requires a webdriver - I use [Gecko](https://github.com/mozilla/geckodriver/releases) from Mozilla. After the webdriver is installed, `Selenium` can be installed via `pip` or `conda`.
* `requests` and `BeautifulSoup` can also be installed via `pip` or `conda`.

### How to use
The easiest way to use this is to clone the repository in `~/.conky`:

```bash
mkdir ~/.conky && cd ~/.conky
git clone https://github.com/j-m-t/conkyscraps.git
```

Next, there are some default options in `conky_weather.lua` that you might want to adjust:

* `template3 = '/en/us/washington-dc/20006/weather-forecast/327659'`: This is the trailing URL information from the Accuweather address (`https://www.accuweather.com/`) for your city of choice.
* `template4 = 'C'`: Your choice of Celsius/metric (C) or Fahrenheit/imperial (F)
* `template5 = '50'`: The number of characters per line in the history section, to make it easier to tweak your Conky configuration.

The first time this script runs, there will be a short lag as Python scrapes the websites and generates the raw text files.

### Fonts
All fonts should be placed in `/usr/local/share/fonts/` in order to be accessible by Conky.

The weather icons come from `ConkyWeather.ttf`, and the wind icons come from `ConkyWindNESW.otf`.  Both are included in [TeoBigusGeekus' original Accuweather shell scripts](http://bit.ly/1_11-11-17). The moon icons come from [`MoonPhases`](https://www.dafont.com/moon-phases.font) - thanks to [Curtis Clark](https://www.cpp.edu/~jcclark/) for providing these.

I use `Exo 2` for most of the text, `Orbitron` for the headers, and Inconsolata for the calendar (a monospace font is needed).  All are available at [Google Fonts](https://fonts.google.com/?selection.family=Exo+2|Inconsolata|Orbitron).

For the history text, I use `Linux Libertine`, which is available [here](http://libertine-fonts.org/download/).

Finally, `CutOutsFor3DFX` is also used.

## Python script details

The arguments needed for the Python scripts are passed from the `conky_weather.lua` Conky configuration, but these Python scripts can be used on their own.

### weather
The `weather` directory contains the Python script `conditions_parse.py`, which scrapes Accuweather for current conditions and seven-day forecasts.  The script also scrapes Moongiant for lunar data.  Many thanks to TeoBigusGeekus for inspiration.  The basic usage of the scripts follows:
```bash
python3 conditions_parse.py -h
usage: conditions_parse.py [-h] outputpath [loc] [scale]

Scrape and parse Accuweather and Moongiant websites

positional arguments:
  outputpath  Directory where output from script will be saved
  loc         Info for Accuweather localization
  scale       Desired temperature scale; either 'C' or 'F'

optional arguments:
  -h, --help  show this help message and exit
```
The only required argument is the directory to save the raw data - it is a good idea to test this script with `python3 conditions_parse.py .` to make sure that it works on your system.

### History
The `wikipedia` directory contains the script `wikipedia_today_scrape.py`, which scrapes Wikipedia for historical events for this day in history.  So far there is only support for English, but I'm thinking of adding other languages as well.

The basic usage of the scripts follows:
```bash
python3 wikipedia_today_scrape.py -h
usage: wikipedia_today_scrape.py [-h] outputpath [width]

Scrape and parse Wikipedia history information

positional arguments:
  outputpath  Directory where output from script will be saved
  width       Length of lines in output

optional arguments:
  -h, --help  show this help message and exit
```
Like before, the only required argument is the directory to save the raw data.

## Lua script details

I extended [`conky-draw`](https://github.com/fisadev/conky-draw) to create custom graphics for my Conky configuration.  These functions can change color based on the `colors` and `grades` arguments passed into it via the configuration in `weather_conky_draw.lua`.

### thermometer

This generates a thermometer that reflects the temperature passed into it, both by the color of the graphic and the 'mercury' level in the thermometer.

[![screenshot](https://github.com/j-m-t/conkyscraps/blob/master/img/thermometer.png)](https://github.com/j-m-t/conkyscraps/blob/master/img/thermometer.png)

```lua
  {
    kind = 'thermometer',
    temp = 'execpi 90 sed -n "3p" ~/.conky/conkyscraps/weather/conditions',
    maxtemp = 100,
    center = {x = 120, y = 405},
    radius = 25,
    color = 0x00E5FF,
    alpha = 1,
    thickness = 5,
    height = 100,
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    grades = {50, 70, 90}
  }
```

### temperature_text

This is a simple function that changes the text color according to an variable value (such as temperature).  I also included an argument that captures the scale of the variable so that it changes color too.

[![screenshot](https://github.com/j-m-t/conkyscraps/blob/master/img/temperature.png)](https://github.com/j-m-t/conkyscraps/blob/master/img/temperature.png)

```lua
  {
    kind = 'temperature_text',
    scale = 'execpi 90 sed -n "40p" ~/.conky/conkyscraps/weather/conditions',
    temp = 'execpi 90 sed -n "3p" ~/.conky/conkyscraps/weather/conditions',
    parentheses = false,
    from = {x = 126, y = 101},
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    grades = {40, 60, 80},
    rotation_angle = 0,
    font = "Exo 2",
    font_size = 48,
    bold = false,
    italic = false,
    alpha = 1
  }
```
