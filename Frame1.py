from R import R
from layout.Form import Form


class Frame1(Form):

    def __init__(self, accuweather):

        Form.__init__(self, "Frame1")
        weather = accuweather.get_current()
        city = accuweather.city
        forecast = accuweather.get_dailyforecast(0)
        icon_direction = self.children["iconDirection"]
        icon_direction.angle = weather.wind_degrees
        self.children["iconCondition"].file = weather.icon
        self.children["labelDate"].text = weather.date
        self.children["labelDescription"].text = weather.description
        self.children["labelSunrise"].text = forecast.sunrise
        self.children["labelSunset"].text = forecast.sunset
        self.children["labelMoonrise"].text = forecast.moonrise
        self.children["labelMoonset"].text = forecast.moonset
        self.children["labelCity"].text = city.localizedname
        self.children["labelLastUpdated"].text = u"{0}:{1} ".format(R.strings.LAST_UPDATED,
                                                                    weather.get_date("%m/%d %H:%M"))
        self.children["labelTemperature"].text = weather.stemperature
        self.children["labelMinTemperature"].text = u"{0}{1}".format(int(forecast.min_temperature),
                                                                     weather.temperatureunit)
        self.children["labelMaxTemperature"].text = u"{0}{1}".format(int(forecast.max_temperature),
                                                                     weather.temperatureunit)
        self.children["labelHumidity"].text = u"{0}:{1}%".format(R.strings.HUMIDITY, str(weather.humidity))
        self.children["labelPressure"].text = u"{0}:{1} {2}".format(R.strings.PRESSURE, weather.pressure,
                                                                    weather.pressureunit)
        self.children["labelRain"].text = u"{0}:{1}".format(R.strings.RAIN, weather.precipitation_1hr)
        self.children["labelUV"].text = u"{0}:{1}".format(R.strings.INDEX_UV, weather.uv_index)
        self.children["labelHoursOfSun"].text = u"{0}:{1}".format(R.strings.HOURS_OF_SUN, forecast.hours_of_sun )
        self.children["labelDirection"].text = u"{:^4}".format(weather.wind_degrees_description)
        # Forces the field to be centered within 4 spaces.
        self.children["labelDegress"].text = u"{:^4}".format(weather.swind_degrees)
        self.children["labelSpeed"].text = "{0}:{1}".format(R.strings.WIND, weather.swind)
        self.create_view()
