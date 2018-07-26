elements = {
  {
    -- Color variable text for current temperature
    kind = 'temperature_text',
    scale = 'execpi 90 sed -n "40p" /path/to/weather/conditions',
    temp = 'execpi 90 sed -n "3p" /path/to/weather/conditions',
    thermometer = true,
    parentheses = false,
    from = {x = 126, y = 101},
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    rotation_angle = 0,
    font = "Exo 2",
    font_size = 28,
    bold = false,
    italic = false,
    alpha = 1
  },
  {
    -- Color variable text for current feel
    kind = 'temperature_text',
    scale = 'execpi 90 sed -n "40p" /path/to/weather/conditions',
    temp = 'execpi 90 sed -n "4p" /path/to/weather/conditions',
    thermometer = false,
    parentheses = true,
    from = {x = 194, y = 101},
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    rotation_angle = 0,
    font = "Exo 2",
    font_size = 28,
    bold = false,
    italic = false,
    alpha = 1
  }
}




