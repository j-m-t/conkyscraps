# conkyscraps
A collection of scripts for Conky configurations

### Weather
Gathers weather and lunar forecasts, with thanks to TeoBigusGeekus for inspiration.

### History
Presents historical events for this day in history.

### Screenshot
[![screenshot](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)

### How to use
Paths need to be adjusted in 2 files before running this script:
In *conky_weather.lua*:
* `lua_load = '/path/to/conky_draw.lua'`: This needs to be directed to where the conky-draw script is located
* `lua_draw_hook_pre = 'main'`: No change needed
* `template1 = '/path/to/conkyscraps/weather/'`: This should point to where conditions_parse.py is located
* `template2 = '/path/to/conkyscraps/wikipedia/'`: This should point to where wikipedia_today_scrape.py is located
* `template3 = '/en/us/washington-dc/20006/weather-forecast/327659'`: This is from Accuweather 
* `template4 = 'C'`: Your choice of Celsius/metric (C) or Fahrenheit/imperial (F)
* `template5 = '50'`: The number of characters per line in the history section

In *weather_conky_draw.lua*:
* `scale = 'execpi 90 sed -n "40p" /path/to/weather/conditions'`: Change the path to the `weather` subdirectory
* `temp = 'execpi 90 sed -n "3p" /path/to/weather/conditions'`: Likewise, change the path to the `weather` subdirectory

This should be done for all the scale or temp paths in `weather_conky_draw.lua`.

### Fonts
I use `Exo 2` for most of the text, and `Orbitron` for the headers.  Both are available from Google Fonts.  For the Wiki text, I use `Linux Libertine`.  I also use Inconsolata for the calendar (a monospace font is needed). `conkyweather`, `ConkyWindNESW`, `MoonPhases`, and `CutOutsFor3DFX` are also used.
