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
All fonts should be placed in `/usr/local/share/fonts/` in order to be accessible by Conky.

The weather icons come from `ConkyWeather.ttf`, and the wind icons come from `ConkyWindNESW.otf`.  Both are included in [TeoBigusGeekus' original Accuweather shell scripts](http://bit.ly/1_11-11-17). The moon icons come from [`MoonPhases`](https://www.dafont.com/moon-phases.font) - thanks to [Curtis Clark](https://www.cpp.edu/~jcclark/) for providing these.

I use `Exo 2` for most of the text, `Orbitron` for the headers, and Inconsolata for the calendar (a monospace font is needed).  All are available at [Google Fonts](https://fonts.google.com/?selection.family=Exo+2|Inconsolata|Orbitron).

For the history text, I use `Linux Libertine`, which is available [here](http://libertine-fonts.org/download/).

Finally, `CutOutsFor3DFX` is also used.
