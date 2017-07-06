
Group 2xx: Thunderstorm
ID Meaning Icon
200 thunderstorm with light rain
201 thunderstorm with rain
202 thunderstorm with heavy rain
210 light thunderstorm
211 thunderstorm
212 heavy thunderstorm
221 ragged thunderstorm
230 thunderstorm with light drizzle
231 thunderstorm with drizzle
232 thunderstorm with heavy drizzle

Group 3xx: Drizzle
ID Meaning Icon
300 light intensity drizzle
301 drizzle
302 heavy intensity drizzle
310 light intensity drizzle rain
311 drizzle rain
312 heavy intensity drizzle rain
313 shower rain and drizzle
314 heavy shower rain and drizzle
321 shower drizzle

Group 5xx: Rain
ID Meaning Icon
500 light rain
501 moderate rain
502 heavy intensity rain
503 very heavy rain
504 extreme rain
511 freezing rain
520 light intensity shower rain
521 shower rain
522 heavy intensity shower rain
531 ragged shower rain

Group 6xx: Snow
ID Meaning Icon
{"600":[{"text:"light snow","icon":emoji}],
601 snow
602 heavy snow
611 sleet
612 shower sleet
615 light rain and snow
616 rain and snow
620 light shower snow
621 shower snow
622 heavy shower snow

Group 7xx: Atmosphere
ID Meaning Icon
701 mist
711 smoke
721 haze
731 sand, dust whirls
741 fog
751 sand
761 dust
762 volcanic ash
771 squalls
781 tornado

Group 800: Clear
ID Meaning Icon
800 clear sky

Group 80x: Clouds
ID Meaning Icon
801 few clouds
802 scattered clouds
803 broken clouds
804 overcast clouds

Group 90x: Extreme
ID Meaning
900 tornado
901 tropical storm
902 hurricane
903 cold
904 hot
905 windy
906 hail

Group 9xx: Additional
ID Meaning
951 calm
952 light breeze
953 gentle breeze
954 moderate breeze
955 fresh breeze
956 strong breeze
957 high wind, near gale
958 gale
959 severe gale
960 storm
961 violent storm
962 hurricane


# Works so far
(\d{3})(\s)(.*$)

# Wrong
{"$1":[{"text:"$3","icon":emoji}],

[
"conditions": [ {"id":[ {"text":description, "icon":emoji} ]} ]
]
