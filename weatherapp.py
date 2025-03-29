#Weather API app using Flet UI
import flet
from flet import *
#import flet_audio as fta
import requests
from datetime import datetime, timedelta
import json


#Random Flet tips: You don't need to use the 'Row' keyword for the first and last rows of a column


#also to be replaced with my own data later
#current = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat=43.6534817&lon=-79.3839347&exclude=minutely,hourly,alerts&units=metric&appid={api_key}")
#api key from OpenWeather, to be replaced later with mine - has been replaced
api_key = "0f71419bc1914e70b7d4084c84eff8b9"

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

#prompts user to enter city name
city_name = "Nairobi"

#base url with remaining parameters
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

#to webscrape the page with the weather data for that city
response = requests.get(complete_url)

#to retrieve the data
x = response.json()
#to check if the api has data for the city inputted by the user
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = int(y["temp"])
    current_temperature_celcius = int(current_temperature - 273)

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidity = y["humidity"]

    temp_max = y["temp_max"]
    temp_min = y["temp_min"]

    #value for wind
    wind_data = x["wind"]
    wind_speed = wind_data["speed"]
    wind_deg = wind_data["deg"]
    #feels like
    feels_like_data = y["feels_like"]
    feels_like_celsius = feels_like_data - 273.15  # Corrected conversion
    #clouds
    clouds =x["clouds"]["all"]
    #rain
    rain =x["coord"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding 
    # to the "description" key at 
    # the 0th index of z
    weather_description = z[0]["description"]
    # Extract timezone offset from API (seconds)
    timezone_offset = x["timezone"]

    # Convert Unix timestamps to local time
    sunrise_utc = datetime.utcfromtimestamp(x["sys"]["sunrise"])
    sunset_utc = datetime.utcfromtimestamp(x["sys"]["sunset"])

    # Apply timezone offset
    sunrise_local = sunrise_utc + timedelta(seconds=timezone_offset)
    sunset_local = sunset_utc + timedelta(seconds=timezone_offset)

    # Format as human-readable time
    sunrise_time = sunrise_local.strftime('%Y-%m-%d %H:%M:%S')
    sunset_time = sunset_local.strftime('%Y-%m-%d %H:%M:%S')

#app
def main(page: Page):
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'


    #sounds

    #audio_one = Audio(src="assets\calming-rain-257596.mp3", autoplay=True)
    
    #submit from search bar
    
    def handle_submit(e):
        search_value = e.control.value
        if search_value:
            city_name = search_value
        else:
            city_name = 'Nairobi'
        '''if e.data == "true":
            city_name = str(e.control.value)
        else:
            city_name = "Nairobi"
        return city_name'''

   
    
    

    #hover animation

    def expand(e):
        if e.data == "true":
            c.content.controls[1].height = 560
            c.content.controls[1].update()
        else:
            c.content.controls[1].height = 660 * 0.40
            c.content.controls[1].update()
    
    #search bar create
    bar_search = SearchBar(
        view_elevation=3,
        bar_bgcolor='white10',
        bar_scroll_padding=30,
        bar_overlay_color='grey350',
        bar_hint_text='Search cities',
        view_hint_text='Search cities',
        bar_leading=IconButton(icon='search'),
        on_submit=handle_submit,
        #bar_trailing=[Text("Search here", color='white')]
    )
    

    #top container
    def top():

        #today = _current_temp() - not used (containers were created individually and not as a grid)
        _today_extra = GridView(
            max_extent=150,
            expand=1,
            run_spacing=5,
            spacing=5,
        )
        #defines the top colored container
        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.bottom_right,
                colors=['black', 'indigo300'] #colors=["lightblue600", 'lightblue900']"deeppurple800", 'deeppurple900'
            ),
            border_radius=35,
            animate=animation.Animation(duration=450, curve='decelerate'),
            on_hover=lambda e: expand(e),
            padding=15,
            #to initialize the content of the colored container
            content=Column(
                alignment='start',
                spacing=10,
                controls=[
                    #city name displayed at the top
                    Row(
                        alignment='center',
                        controls=[Text(city_name, size=16, weight='w500', color='white')]

                    ),
                    
                    Container(
                        padding=padding.only(bottom=5)
                    ),
                    #the row containing the images, main temperature, day, and description
                    Row(
                        alignment='center',
                        spacing=30,
                        controls=[
                            Column(
                                controls=[
                                    #the image
                                    Container(
                                        flet.Image("/cloudy.png",fit=flet.ImageFit.CONTAIN,),
                                        width=90,
                                        height=90,
                                        
                                    )
                                ]
                            ),
                            #column for the day, temperature, and description
                            Column(
                                spacing=5,
                                horizontal_alignment='center',
                                #day
                                controls=[
                                    Text("Today", size=13, text_align='center', color='white'),
                                    Row(
                                        vertical_alignment='start',
                                        spacing=0,
                                        controls=[
                                            #main temperature
                                            Container(
                                                content=Text(current_temperature_celcius, size=45, color='white')
                                            ),
                                            Container(
                                                content=Text("°C", size=45, color='white', text_align='center')
                                            )
                                        ]
                                    ),
                                    #description
                                    Text(weather_description, size=10, color='white54', text_align='center')  
                                ],
                            )
                        ]
                    ),
                    #thin white line divider
                    Divider(
                        height=8,
                        thickness=1,
                        color='white10',),
                    #initializes the row for wind, humidity, and feels like data
                    Row(
                        alignment='spaceAround',
                        controls=[
                            #wind data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            image=flet.Image("assets/weather-app.png"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(str(wind_deg) + "°", size=11, color='white'),
                                        Text("Wind", size=9, color='white54', )
                                    ]
                                )
                            ),
                            #humidity data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            image=flet.Image("assets\weather-app.png"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(str(current_humidity) + "g/kg",  size=11, color='white'),
                                        Text("Humidity", size=9, color='white54', )
                                    ]
                                )
                            ),
                            #feels like data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            image=flet.Image("assets\weather-app.png"),
                                            width=20,
                                            height=20
                                        ),
                                        Text(str(int(feels_like_celsius)) + "°C", size=11, color='white'),
                                        Text("Feels Like", size=9, color='white54', )
                                    ]
                                )
                            ),
                        ]
                    ),
                    #to initialize four containers for clouds, max temp, min temp, and coordinates data
                    #first row of containers for clouds and max temp
                    Row(
                        alignment='spaceAround',
                        controls=[
                            #container for clouds data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/cloud.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text("  "+str(clouds), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text(""+"Clouds", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                            #container for max temp data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/dashboard.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text("  "+str(temp_max), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("Max Temp", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                        ]
                    ),
                    #row for last two containers - min temp and coordinates
                    Row(
                        alignment='center',
                        controls=[
                            #container for min temp data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/humidity (1).png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text("  "+str(temp_min), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("Min Temp", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                            #container for coordinates data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/rain.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text("  "+str(rain), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("            Lon/Lan", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                        ]
                    )

                ],
            ),
        )
        return top
    #to initialize bottom section with pressure, wind speed, sunrise, and sunset data, as well as search bar
    def bottom():
        #to initialize bottom container parameters (might be discarded later and entered directly rather than as a variable)
        bottom_column = Column(
            alignment='center',
            horizontal_alignment='center',
            spacing=25,
        )
        #bottom container with parameters entered directly
        bottom = Container(
            padding=padding.only(top=250, left=-9, right=0, bottom=0),
            margin=25,
            content=Column(
                  #alignment='center',
                  horizontal_alignment='center',
                  spacing=20,
                  controls=[
                      #to add search bar
                      bar_search,
                      #to add row for first two containers - pressure and wind speed data
                      Row(
                        alignment='spaceAround',
                        controls=[
                            #container for pressure
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/blood-pressure.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text(str(current_pressure) + "Pa", size=11, color='white'),
                                                        Text("Pressure", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                ),
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                            #container for wind speed
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/wind-farm.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment='center', controls=[
                                                        Text(" "+str(wind_speed) + " " + "km/h", size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("Wind Speed", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                        ]
                    ),
                    #row for last two containers - sunrise and sunset data
                    Row(
                        alignment='spaceAround',
                        controls=[
                            #container for sunrise data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/sunrise.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text(" "+str(sunrise_time), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("          "+"Sunrise", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                            #container for sunset data
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        #Text("Pressure", size=6, color='white54',),
                                        Container(
                                            Column(spacing=2, alignment='center',controls=[
                                                Container(
                                                alignment=alignment.center,
                                                content=flet.Image("/sunset.png", color='white', width=30, height=30),
                                                ),
                                                Container(
                                                    alignment=alignment.center,
                                                    content=Column(spacing=2, alignment=alignment.center, controls=[
                                                        Text(" "+str(sunset_time), size=11, color='white',text_align=TextAlign.CENTER),
                                                        Text("           "+"Sunset", size=11, color='white54', text_align=TextAlign.CENTER),
                                                    ])
                                                )
                                                
                                            ]),
                                            #Text(str(current_pressure) + "Pa", size=11, color='white',),
                                            #Text("Wind", size=6, color='white54',),
                                            #padding=30,
                                            alignment=alignment.center,
                                            width=120,
                                            height=120,
                                            bgcolor='white12',
                                            border_radius=12,
                                            margin=2,
                                            
                                            
                                            

                                        ),
                                        ]
                                ),
                                
                            ),
                        ]
                    )
                      
                      
                      
                      
                      
                      
                      
                  ]
                ),
                
                   
                
            
        )
        return bottom
    #container for entire app - containing top and bottom
    c = Container(
        #Image(src='assets/back.jpg', width=300, height=670, fit=ImageFit.CONTAIN),
        width=310,
        height=660,
        border_radius=35,
        bgcolor='black',
        padding=10,
        content= Stack(
            width=300,
            height=550,
            controls=[
                #bottom to top in terms of hiearchy of the controls for the stack
                bottom(),
                top(),
                
            ]
        ),
    )

    page.add(c)
    #page.overlay.append(audio_one)

#if __name__ == "__main__":
    #flet.app(target=main, assets_dir='assets')
#initializes the app
flet.app(target=main, assets_dir = 'assets')

#to fix image problem, change assets_dir folder
#ignore the weather values for now until you finish the weather api part itself
#timestamp 16:56