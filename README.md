# conkyscraps
A collection of Python scripts for Conky configurations

### Weather
Gathers weather and lunar forecasts, with thanks to TeoBigusGeekus for inspiration.

### History
Presents historical events for this day in history.

### Screenshot
[![screenshot](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)](https://github.com/j-m-t/conkyscraps/blob/master/img/conky_weather.png)

### Requirements
These scripts are set up to run with Python 3. The only extra packment requirement is ```BeautifulSoup```.  You also need ```Conky```, of course.

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
I use `Exo 2` for most of the text, and `Orbitron` for the headers.  Both are available from Google Fonts.  For the Wiki text, I use `Linux Libertine`.  I also use Inconsolata for the calendar (a monospace font is needed). `conkyweather`, `ConkyWindNESW`, `MoonPhases`, and `CutOutsFor3DFX` are also used.
