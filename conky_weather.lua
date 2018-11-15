-- A Conky configuration file for Accuweather and Moongiant,
-- with a little history thrown in

conky.config = {

    background = true,
    update_interval = 1,
    double_buffer = true,
    no_buffers = true,
    imlib_cache_size = 10,

    draw_shades = false,
    draw_outline = false,
    draw_borders = false,
    draw_graph_borders = false,
    default_graph_height = 26,
    default_graph_width = 80,
    show_graph_scale = false,
    show_graph_range = false,

    gap_x = 10,
    gap_y = 0,
    minimum_height = 1400,
    minimum_width = 320,
    maximum_width = 320,
    own_window = true,
    own_window_class = 'Conky',
    own_window_type = 'normal',
    own_window_transparent = true,
    own_window_hints = 'sticky,below,undecorated,skip_taskbar,skip_pager',
    border_inner_margin = 0,
    border_outer_margin = 0,
    border_width = 0,
    stippled_borders = 0,
    alignment = 'top_right',

    use_xft = true,
    xftalpha = 0,
    font = 'Exo 2:size=10',
    text_buffer_size = 256,
    override_utf8_locale = true,
    use_spacer = 'none',
    uppercase = false,

    short_units = true,
    pad_percents = 2,
    top_name_width = 7,

    cpu_avg_samples = 2,
    net_avg_samples = 2,

    default_color = 'white',
    default_outline_color = 'white',
    default_shade_color = 'gray14',

    out_to_console = false,
    out_to_stderr = false,
    extra_newline = false,

    color2 = 'ivory2',
    color3 = "ivory3",
    color4 = "tan1",
    color7 = "DarkGray",
    color8 = "DimGray",
    color9 = 'tomato',

    lua_load = '~/.conky/conkyscraps/conky_draw.lua',
    lua_draw_hook_pre = 'main',

    template1 = '~/.conky/conkyscraps/weather/',
    template2 = '~/.conky/conkyscraps/wikipedia/',
    template3 = '/en/us/washington-dc/20006/weather-forecast/327659',
    template4 = 'C',  -- Changing this will require a change in the grades in weather_conky_draw.lua
    template5 = '50'
}

conky.text = [[
##################################
##           WEATHER            ##
##################################
\
${voffset 15}${font Orbitron:size=12}${color4}Weather${offset 4}${voffset -1}${color8}${hr 2}\
${texeci 90 python3 ${template1}conditions_parse.py ${template1} ${template3} ${template 4}}\
${font Exo 2:size=10.5}
${goto 107}${color3}${execi 90 sed -n '37p' ${template1}conditions}
${goto 107}${color3}${execi 90 sed -n '38p' ${template1}conditions}
${voffset 15}${goto 5}${font conkyweather:size=70}${color2}${execi 90 sed -n '1p' ${template1}conditions}${font}
\
\
## TEMPERATURE COLORS ############
# This is controlled by the configuration weather_conky_draw.lua, via conky_draw.lua
\
${voffset -70}${goto 107}${font Exo 2 Medium:size=15}${color3}${execpi 90 sed -n '2p' ${template1}conditions}
\
\
## DAYTIME INFO ##################
${voffset 2}${font Exo 2:size=9}\
${goto 107}${color3}Visibility: ${color2}${alignr 30}${execpi 90 sed -n '12p' ${template1}conditions}\
${goto 220}${color3}Sunrise: ${color2}${alignr}${execpi 90 sed -n '13p' ${template1}conditions}
${goto 107}${color3}UV Index: ${color2}${alignr 26}${execpi 90 sed -n '9p' ${template1}conditions}\
${goto 220}${color3}Duration: ${color2}${alignr}${execpi 90 sed -n '15p' ${template1}conditions}
${goto 220}${color3}Sunset: ${color2}${alignr}${execpi 90 sed -n '14p' ${template1}conditions}
\
\
## PRECIPITATION INFO ############
${voffset 7}${goto 107}${color3}${font Exo 2:size=13}${execpi 90 sed -n '34p' ${template1}conditions}
\
${voffset 2}${goto 107}${font Exo 2:size=9}Amount: ${color2}\
${alignr 45}${execpi 90 sed -n '35p' ${template1}conditions}\
${goto 220}${color3}Time: ${color2}\
${alignr}${execpi 90 sed -n '36p' ${template1}conditions}
\
${voffset 0}${goto 107}${color3}${font Exo 2:size=9}Humidity: ${color2}\
${alignr 28}${execpi 90 sed -n '7p' ${template1}conditions}\
${goto 220}${color3}Dew Point: ${color2}\
${alignr}${execpi 90 sed -n '11p' ${template1}conditions}°
\
\
## MOON INFO #####################
${voffset 40}${goto 6}${font MoonPhases:size=14}${execpi 90 sed -n '21p' ${template1}conditions}
${voffset -50}${goto 26}${font MoonPhases:size=33}${execpi 90 sed -n '22p' ${template1}conditions}
${voffset -38}${goto 71}${font MoonPhases:size=14}${execpi 90 sed -n '23p' ${template1}conditions}
${voffset -44}${goto 107}${color3}${font Exo 2:size=13}${execpi 90 sed -n '19p' ${template1}conditions}
\
${voffset 2}${font Exo 2:size=9}\
${goto 107}${color3}Cloud Cover: ${color2}\
${alignr 19}${execpi 90 sed -n '10p' ${template1}conditions}\
${goto 220}${color3}Moonrise: ${color2}\
${alignr}${execpi 90 sed -n '16p' ${template1}conditions}
\
${goto 107}${color3}Illumination: ${color2}\
${alignr 24}${execpi 90 sed -n '20p' ${template1}conditions}\
${goto 220}${color3}Duration: ${color2}\
${alignr}${execpi 90 sed -n '18p' ${template1}conditions}
\
${goto 220}${color3}Moonset: ${color2}\
${alignr}${execpi 90 sed -n '17p' ${template1}conditions}
\
\
## WIND INFO #####################
${voffset 10}${goto 18}${font ConkyWindNESW:size=45}${execpi 90 sed -n '5p' ${template1}conditions}${font}
${voffset -45}${goto 107}${color3}${font Exo 2:size=13}Wind speed: ${execpi 90 sed -n '6p' ${template1}conditions}
\
${goto 107}${font Exo 2:size=9}${color3}Pressure: ${color2}\
${goto 165}${execpi 90 sed -n '8p' ${template1}conditions}
# NOTE: Conky doesn't seem to process text arrows
\
\
## EXTENDED FORECAST #############
## 7-day forecast: First 3 days
${voffset 13}${font Orbitron:size=12}${color4}Forecast${offset 4}${voffset -1}${color8}${hr 2}\
\
## LABELS
${voffset 19}${goto 30}${font Exo 2:size=9}${color3}${execpi 90 sed -n '1p' ${template1}forecast}\
${goto 140}${execpi 90 sed -n '7p' ${template1}forecast}\
${goto 245}${execpi 90 sed -n '13p' ${template1}forecast}${color2}${font}
\
## ICONS
${voffset 6}${goto 10}${font conkyweather:size=50}${execi 90  sed -n '2p' ${template1}forecast}\
${goto 119}${execi 90  sed -n '8p' ${template1}forecast}\
${goto 222}${execi 600  sed -n '14p' ${template1}forecast}${font Exo 2:size=9}
\
## HIGHS
${voffset -55}${goto 83}${execpi 90 sed -n '3p' ${template1}forecast}°\
${goto 187}${execpi 90 sed -n '9p' ${template1}forecast}°\
${goto 293}${execpi 90 sed -n '15p' ${template1}forecast}°
\
## LOWS
${goto 83}${execpi 90 sed -n '4p' ${template1}forecast}°\
${goto 187}${execpi 90 sed -n '10p' ${template1}forecast}°\
${goto 293}${execpi 90 sed -n '16p' ${template1}forecast}°
\
## DESCRIPTION
${voffset 25}${goto 15}${font Exo 2:size=8}${execpi 90 sed -n '5p' ${template1}forecast}$\
{goto 125}${execpi 90 sed -n '11p' ${template1}forecast}\
${goto 230}${execpi 90 sed -n '17p' ${template1}forecast}
${goto 15}${execpi 90 sed -n '6p' ${template1}forecast}\
${goto 125}${execpi 90 sed -n '12p' ${template1}forecast}\
${goto 230}${execpi 90 sed -n '18p' ${template1}forecast}
##################################
## 7-day forecast: Last 4 days
${color8}${hr 2}
\
## LABELS
${voffset 3}${goto 25}${color3}${font Exo 2:size=9}${execpi 90 sed -n '19p' ${template1}forecast}\
${goto 108}${execpi 90 sed -n '25p' ${template1}forecast}\
${goto 187}${execpi 90 sed -n '31p' ${template1}forecast}\
${goto 267}${execpi 90 sed -n '37p' ${template1}forecast}${color2}
\
## ICONS
${voffset 4}${goto 6}${font conkyweather:size=30}${execi 90  sed -n '20p' ${template1}forecast}\
${goto 89}${execi 90  sed -n '26p' ${template1}forecast}\
${goto 169}${execi 90  sed -n '32p' ${template1}forecast}\
${goto 247}${execi 90  sed -n '38p' ${template1}forecast}${font Exo 2:size=9}
\
## HIGHS
${voffset -35}${goto 50}${execpi 90 sed -n '21p' ${template1}forecast}°\
${goto 134}${execpi 90 sed -n '27p' ${template1}forecast}°\
${goto 212}${execpi 90 sed -n '33p' ${template1}forecast}°\
${goto 287}${execpi 90 sed -n '39p' ${template1}forecast}°
\
## LOWS
${goto 50}${execpi 90 sed -n '22p' ${template1}forecast}°\
${goto 134}${execpi 90 sed -n '28p' ${template1}forecast}°\
${goto 212}${execpi 90 sed -n '34p' ${template1}forecast}°\
${goto 287}${execpi 90 sed -n '40p' ${template1}forecast}°
\
\
## HISTORY #######################
${voffset 12}${font Orbitron:size=12}${color4}History${offset 4}${voffset -1}${color8}${hr 2}\
\
## LABELS
${voffset 19}${font Exo 2:size=9}${color3}${goto 61}Today\
${goto 126}Mean\
${goto 187}Record\
${alignr}Last Year
\
## HIGHS
${voffset 4}High${goto 61}${execpi 90 sed -n '24p' ${template1}conditions}°\
${goto 126}${execpi 90 sed -n '25p' ${template1}conditions}°\
${goto 187}${execpi 90 sed -n '26p' ${template1}conditions}°\
${goto 214}${execpi 90 sed -n '27p' ${template1}conditions}\
${alignr}${execpi 90 sed -n '28p' ${template1}conditions}°
\
## LOWS
${voffset 4}Low${goto 61}${execpi 90 sed -n '29p' ${template1}conditions}°\
${goto 126}${execpi 90 sed -n '30p' ${template1}conditions}°\
${goto 187}${execpi 90 sed -n '31p' ${template1}conditions}°\
${goto 214}${execpi 90 sed -n '32p' ${template1}conditions}\
${alignr}${execpi 90 sed -n '33p' ${template1}conditions}°
\
\
## TODAY IN HISTORY
${texeci 180 python3 ${template2}wikipedia_today_scrape.py ${template2} ${template5}}\
${voffset 8}${font Linux Libertine:size=10.5}${execpi 5 sed -n '1p' ${template2}history}
${execpi 5 sed -n '2p' ${template2}history}
${execpi 5 sed -n '3p' ${template2}history}
${execpi 5 sed -n '4p' ${template2}history}
${execpi 5 sed -n '5p' ${template2}history}
${execpi 5 sed -n '6p' ${template2}history}
\
\
##################################
##             TIME             ##
##################################
\
\
${voffset 14}${font Orbitron:size=12}${color4}Time${offset 4}${color8}${voffset -2}${hr 2}${font}
${voffset 3}${font Orbitron:size=25}${color3}\
${if_match ${time %l}<=9}${alignc 7}${time %l:%M%p}\
${else}${if_match ${time %l}>=10}${alignc -1}${time %l:%M%p}\
${endif}${endif}${font}
\
\
##################################
##      CALENDAR (5-Line)       ##
##################################
\
\
####
${voffset 4}${font Orbitron:size=12}${color4}Date${offset 4}${color8}${voffset -2}${hr 2}${font}
\
## The calendar
${voffset 10}${font Inconsolata:size=11}${color3}\
${execpi 60 ncal -bh | sed -e '1d' -e s/^/"\$\{goto 40\}"/ -e 's/\<'`date +%-d`'\>/${color9}&${color3}/'}
\
## The day, date, month, and year box
${voffset -115}${font CutOutsFor3DFX:size=80}${color8}${alignc -53.5}2${font}
${voffset -71}${font Exo 2:size=10}${color3}${alignc -98}${time %A}${font}
${voffset 4}${font Orbitron:bold:size=16}\
${if_match ${time %e}<=9}${color5}${alignc -96}${time %e}${font}\
${else}\
${if_match ${time %e}>=10}${color5}${alignc -98}${time %e}\
${endif}${endif}${font}
${voffset 1}${font Exo 2:size=10}${color3}${alignc -98}${time %B}${font}
${voffset 1}${font Exo2:size=9}${color3}${alignc -98}${time %Y}${font}
${voffset 20}${offset 4}${color8}${voffset -2}${hr 2}
\
\
## TIMESTAMP
${color7}Last update: ${execpi 10 sed -n '39p' ${template1}conditions}
####
]]
