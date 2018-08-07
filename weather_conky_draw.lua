elements = {
  {
    -- Thermometer for current temperature
    kind = 'thermometer',
    temp = 'execpi 90 sed -n "3p" /path/to/weather/conditions',
    maxtemp = 40,
    center = {x = 120, y = 105},
    radius = 5,
    color = 0x00E5FF,
    alpha = 1,
    thickness = 1.5,
    height = 25,
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    grades = {10, 20, 30}
  },
  {
    -- Color variable text for current temperature
    kind = 'temperature_text',
    scale = 'execpi 90 sed -n "40p" /path/to/weather/conditions',
    temp = 'execpi 90 sed -n "3p" /path/to/weather/conditions',
    parentheses = false,
    from = {x = 126, y = 101},
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    grades = {10, 20, 30},
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
    parentheses = true,
    from = {x = 194, y = 101},
    colors = {0x00FFFF, 0xFFFFFF, 0xFFA500, 0xFF0000},
    grades = {10, 20, 30},
    rotation_angle = 0,
    font = "Exo 2",
    font_size = 28,
    bold = false,
    italic = false,
    alpha = 1
  }
}
