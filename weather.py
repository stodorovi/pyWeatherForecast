import urllib.request
import json
from enum import Enum
from typing import Union

class ForecastType(Enum):
    TEXT   = 0,
    MBROLA = 1

class Data(Enum):
    WIND_DIRECTION = 0,
    WIND_SPEED     = 1,
    WIND_NAME      = 2,
    TEMPERATURE    = 3,
    WEATHER_ID     = 4,
    HOUR           = 6,
    MINUTE         = 7

class Weather:
    """
    Weather forecasting class for Zagreb in croatian language.

    Functions:
    --------
        __retrieveData              : Function for retrieving weather data for Zagreb from OpenWeatherMap.
        __getWindDirection          : Function for retrieving wind direction name.
        __getWindName               : Function for retrieving wind name based on Beaufort scale.
        __getWeatherDescription     : Function for retrieving weather description based on weather id.
        __splitNumberIntoPowerOfTen : Function that splits a number into sections of power of ten.
        __numberIntoWords           : Function that returns words of a given number in croatian.
        __getHourAndMinute          : Function for retrieving current hour and minute.
        __getIntro                  : Function that returns forecast intro.
        getForecast                 : Function that returns current weather forecast text.
        writeMBROLAText             : Function that returns a text in croatian converted into a MBROLA ready format.
    """

    __openWeatherMapToken = ""
    __weatherData = json.loads(urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=" + __openWeatherMapToken + "&units=metric").read().decode())
    __timeData = str(urllib.request.urlopen('http://worldtimeapi.org/api/timezone/Europe/Zagreb.txt').read())


    def __retrieveData(self, dataType : Data) -> Union[int, float, str]:
        """
        Retrieves weather data for Zagreb from OpenWeatherMap API-a.

        Parameter:
        --------
            dataType : Data - Type of data needed.

        Returns:
        -----
            if dataType:
                Data.WIND_DIRECTION 
                    int : Angle of the wind.
                        
                Data.WIND_SPEED
                    float : Wind speed.
                        
                Data.WIND_NAME
                    string : Wind direction name (8 directions).

                Data.TEMPERATURE
                    float : Air temperature.

                WEATHER_ID
                    int : Weather ID
        """

        windDirection = 0 if "deg" not in Weather.__weatherData["wind"] else Weather.__weatherData["wind"]["deg"]
        windDirectionName = Weather().__getWindDirection(windDirection)
        windSpeed = 0 if "speed" not in Weather.__weatherData["wind"] else Weather.__weatherData["wind"]["speed"]
        temperature = 0 if "temp" not in Weather.__weatherData["main"] else Weather.__weatherData["main"]["temp"]

        mainWeatherData = Weather.__weatherData["weather"]
        weatherIDs = []

        for i in range(len(mainWeatherData)):
            weatherIDs.append(mainWeatherData[i]["id"])

        dataReturn = {
            Data.WIND_DIRECTION : windDirection,
            Data.WIND_SPEED : windSpeed,
            Data.WIND_NAME : windDirectionName,
            Data.TEMPERATURE : temperature,
            Data.WEATHER_ID : weatherIDs
        }
        
        return dataReturn[dataType]


    def __getWindDirection(self, angle : Union[int, str]) -> str:
        """
        Function retrieves wind direction name based on the given angle.
        
        Parameter:
        --------
            angle : int / string - Wind angle.
        
        Returns:
        -----
            string : Direction name (0° -> 12h -> 'sjeverni' (en. 'northern')).
        """

        windDirections = ["sjeverni", "sjeveroistočni", "istočni", "jugoistočni", "južni", "jugozapadni", "zapadni", "sjeverozapadni"]
        windName = windDirections[int( ((float(angle) + (360 / (len(windDirections)*2))) % 360) /
                                       (360 / len(windDirections)) )]

        return windName


    def __getWindName(self, windSpeed : float, windAngle : int) -> str:
        """
        Function returns wind name based on Beaufort scale.

        Returns:
        -----
            string  : Wind name.
        """

        windNames = ["tišina", "lahor", "povjetarac", "slab vjetar", "umjeren vjetar", "umjereno jak vjetar",
                     "jak vjetar", "žestoki vjetar", "olujni vjetar", "jak olujni vjetar", "orkanski vjetar", "jak orkanski vjetar", "orkan"]


        windIndex = ( (0 * (windSpeed <= 0.3)) +
                    (1 * (0.3 < windSpeed <= 1.5)) +
                    (2 * (1.5 < windSpeed <= 3.3)) +
                    (3 * (3.3 < windSpeed <= 5.5)) +
                    (4 * (5.5 < windSpeed <= 7.9)) +
                    (5 * (7.9 < windSpeed <= 10.7)) +
                    (6 * (10.7 < windSpeed <= 13.8)) +
                    (7 * (13.8 < windSpeed <= 17.1)) +
                    (8 * (17.1 < windSpeed <= 20.7)) +
                    (9 * (17.1 < windSpeed <= 20.7)) +
                    (10 * (24.4 < windSpeed <= 28.4)) +
                    (11 * (28.4 < windSpeed <= 32.6)) +
                    (12 * (windSpeed > 32.6)) )

        windDirections = Weather().__getWindDirection(windAngle)
        forecastText = "." if (windIndex == 0) else ", te puše {0} {1}.".format(windDirections, windNames[windIndex])

        return forecastText


    def __getWeatherDescription(self, weatherID : int) -> str:
        """
        Function returns current weather description.

        Parameter:
        ---------
            weatherID : int - Weather ID to use for weather description retrieval.

        Returns:
        -----
            string  : Current weather description.        
        """

        descriptionsList = {
            200: "grmljavina s malo kiše",
            201: "grmljavina s kišom",
            202: "grmljavina s obilnom kišom",
            210: "slaba grmljavina",
            211: "grmljavina",
            212: "razbijena grmljavina",
            221: "grmljavina s laganom rosuljom",
            231: "grmljavina s rosuljom ",
            232: "grmljavina s jakom rosuljom",
            300: "slaba sitna kiša",
            301: "sitna kiša",
            302: "jaka sitna kiša",
            310: "slaba rosulja",
            311: "rosulja",
            312: "jaka rosulja",
            313: "rosulja uz pljuskove",
            314: "jaki pljuskovi i rosulja",
            321: "pljusak i rosulja",
            500: "lagana kiša",
            501: "kiša",
            502: "pljuskovi",
            503: "obilni pljuskovi",
            504: "ekstremni pljuskovi",
            511: "ledena kiša",
            520: "lagani pljusak",
            521: "pljusak",
            522: "jaki pljusak",
            531: "isprekidani pljuskovi",
            600: "lagani snijeg",
            601: "snijeg",
            602: "obilni snijeg",
            611: "susnježica",
            612: "promjenjivo oblačno uz laganu susnježicu",
            613: "promjenjivo oblačno uz susnježicu",
            615: "blaga susnježica",
            616: "susnježica",
            620: "promjenjivo oblačno uz lagani snijeg",
            621: "mećava",
            622: "jaka mećava",
            701: "izmaglica",
            711: "dim",
            721: "sumaglica",
            731: "pješčani ili prašinski vrtlog",
            741: "magla",
            751: "pijesak",
            761: "prašina",
            762: "vulkanski pepeo",
            771: "naleti vjetra",
            781: "tornado",
            800: "vedro",
            801: "blaga naoblaka",
            802: "pretežno vedro",
            803: "promjenjivo oblačno",
            804: "oblačno"
        }

        weatherDescriptions = []

        for i in  range(len(weatherID)):
            weatherDescriptions.append(descriptionsList[weatherID[i]])

        return "".join(weatherDescriptions) if (len(weatherDescriptions) == 1) else " i ".join(weatherDescriptions)


    def __splitNumberIntoPowerOfTen(self, number : Union[int, str]) -> list[str]:
        """
        Function splits a number into sections of power of ten.

        Parameter:
        --------
            number : int / string

        Returns:
        -----
            list (string) : List of split numbers.
                                e.g. 158 -> ["100", "50", "8"]
        """

        number = list(str(number))
        isNegative = number[0] == "-"

        if (isNegative):
            number.remove(number[0])

        i = 0
        for digit in number:
            digit = int(digit) * pow(10, (len(number) - (i + 1)))
            number[i] = str(digit)
            i += 1
        i = 0

        if (len(number) > 1 and int(number[-2]) + int(number[-1]) > 10 and int(number[-2]) + int(number[-1]) < 20):
            number[-2] = str(int(number[-2]) + int(number[-1]))
            number.remove(number[-1])

        number = [digit for digit in number if digit != '0' or (number[0] == '0' and len(number) == 1)]

        if (isNegative):
            number.insert(0, "minus")

        return number


    def __numberIntoWords(self, numbers : Union[int, list[str]]) -> list[str]:
        """
        Function returns a word(s) equivalent of a given number in croatian.

        Parameter:
        --------
            numbers : int / list (string)
            
        Returns:
        -----
            list (string) : List of words.
                                e.g. 218 -> ["dvjesto", "osamnaest"]

        """

        if (type(numbers) == int):
            numbers = Weather().__splitNumberIntoPowerOfTen(numbers)

        returnWords = []

        lastIsSingleDigit = len(numbers[-1]) == 1 and (len(numbers) > 1)

        numberWords = {
            0   : "nula",
            1   : "jedan",
            2   : "dva",
            3   : "tri",
            4   : "četiri",
            5   : "pet",
            6   : "šest",
            7   : "sedam",
            8   : "osam",
            9   : "devet",
            10  : "deset",
            -10 : "naest",
            100 : "sto"
        }

        for number in numbers:
            
            if (int(number) in [11, 12, 13, 14, 15, 16, 17, 18, 19]):
                if (int(number) == 11):
                    returnWords.append(numberWords[int(number[-1])] + numberWords[-10][1:])
                elif (int(number) == 14):
                    returnWords.append(numberWords[int(number[-1])][0:3] + 'r' + numberWords[-10])
                elif (int(number) == 16):
                    returnWords.append(numberWords[int(number[-1])][0:-1] + numberWords[-10])
                else:
                    returnWords.append(numberWords[int(number[-1])] + numberWords[-10])

            elif (len(number) == 2):
                if (int(number[0]) == 4):
                    returnWords.append(numberWords[int(number[0])][:3] + 'r' + numberWords[int(number) / int(number[0])])
                elif (int(number[0]) in [5,6,9]):
                    returnWords.append(numberWords[int(number[0])][:-1] + numberWords[int(number) / int(number[0])])
                else:
                    returnWords.append(numberWords[int(number[0])] + numberWords[int(number) / int(number[0])])

            elif (len(number) == 3):
                if (int(number[0]) == 1):
                    returnWords.append(numberWords[int(number)])
                elif (int(number[0]) == 2):
                    returnWords.append(numberWords[int(number[0])][:2] + 'je' + numberWords[int(number) / int(number[0])])
                elif (int(number[0]) == 4):
                    returnWords.append(numberWords[int(number[0])][:3] + 'r' + numberWords[int(number) / int(number[0])])
                elif (int(number[0]) == 6):
                    returnWords.append(numberWords[int(number[0])][:2] + numberWords[int(number) / int(number[0])])
                else:
                    returnWords.append(numberWords[int(number[0])] + numberWords[int(number) / int(number[0])])
            else:
                returnWords.append(numberWords[int(number)])
            
        if (lastIsSingleDigit):
            returnWords.insert(-1, "i")

        return returnWords


    def __getHourAndMinute(self, data : Data) -> int:
        """
        Function retries current hour and minute.

        Parameter:
        --------
            data : Data - Data type to return.

        Returns:
        -----
            if data:
                Data.HOUR
                    int : Returns current hour.
                Data.MINUTE
                    int : Returns current minute.
        """

        hour = int(Weather.__timeData.split()[3][11:13])
        minute = int(Weather.__timeData.split()[3][14:16])

        returnData = {
            Data.HOUR : hour,
            Data.MINUTE : minute
        }

        return returnData[data]


    def __getIntro(self, sat : int) -> str:
        """
        Function returns forecast intro depending on the current hour.

        Parameter:
        ---------
            hour : int - Current hour to determine time of day.

        Returns:
        -----
            string : Returns intro depending on the time of day.
        """

        introText = "Dobro jutro dragi slušatelji" if 5 <= sat < 12 else "Dobar dan dragi slušatelji" if 12 <= sat < 17 else "Dobra večer dragi slušatelji"

        return introText
    

    @staticmethod
    def getForecast(forecastType : ForecastType) -> str:
        """
        Function returns current weather forecast text.

        Parameter:
        --------
            forecastType : Data

        Returns:
        -----
            if forecastType:
                Data.TEXT
                    string : Returns weather forecast in croatian.
                Data.MBROLA
                    string : Return weather forecast in MBROLA compatible format.
        """

        windSpeed = float(Weather().__retrieveData(Data.WIND_SPEED))
        windDirection = Weather().__retrieveData(Data.WIND_DIRECTION)
        hour = Weather().__getHourAndMinute(Data.HOUR)
        weatherID = Weather().__retrieveData(Data.WEATHER_ID)
        introText = Weather().__getIntro(hour)
        windName = Weather().__getWindName(windSpeed, windDirection)
        hourSuffix = "" if (int(str(hour)[-1]) == 1 and hour != 11) else "a" if (int(str(hour)[-1]) in [2, 3, 4] and int(str(hour)[0]) != 1) else "i"
        minute = Weather().__getHourAndMinute(Data.MINUTE)
        minuteSuffix = "e" if (int(str(minute)[-1]) in [2, 3, 4] and int(str(minute)[0]) != 1) else "a"
        minuteText = "i {0} minut{1}".format(Weather().__getHourAndMinute(Data.MINUTE), minuteSuffix) if (minute != 0) else ""
        temperature = Weather().__retrieveData(Data.TEMPERATURE)
        temperatureSuffix = "anj" if (int(str(int(Weather().__retrieveData(Data.TEMPERATURE)))[-1]) == 1 and int(str(int(Weather().__retrieveData(Data.TEMPERATURE)))) != 11) else "nja"
        weatherDescription = Weather().__getWeatherDescription(weatherID)

        mbrolaHour = " ".join(Weather().__numberIntoWords(Weather().__splitNumberIntoPowerOfTen(hour)))
        mbrolaMinute = " ".join(Weather().__numberIntoWords(Weather().__splitNumberIntoPowerOfTen(minute)))
        mbrolaMinuteText = "i {0} minut{1}".format(mbrolaMinute, minuteSuffix) if (minute != 0) else ""
        mbrolaTexteratureData = Weather().__splitNumberIntoPowerOfTen(int(Weather().__retrieveData(Data.TEMPERATURE)))
        isMbrolaTexteratureNegative = mbrolaTexteratureData[0] == "minus"
        mbrolaTexteratureText = (mbrolaTexteratureData[0] + " " if (isMbrolaTexteratureNegative) else "") + (" ".join(Weather().__numberIntoWords(mbrolaTexteratureData)) if (not isMbrolaTexteratureNegative) else " ".join(Weather().__numberIntoWords(mbrolaTexteratureData[1:])))


        if (forecastType == ForecastType.TEXT):
            print("{0}. {1} je sat{2} {3}. Vani je {4}°C, {5} je{6}".format(introText, hour, hourSuffix, minuteText, temperature, weatherDescription, windName))
        elif (forecastType == ForecastType.MBROLA):
            return "{0} {1} je sat{2} {3} vani je {4} stup{5} {6} je{7}".format(introText, mbrolaHour, hourSuffix, mbrolaMinuteText, mbrolaTexteratureText, temperatureSuffix, weatherDescription, windName[1:-1])


    @staticmethod
    def writeMBROLAText(text : str) -> None:
        """
        Function writes a text in croatian converted into a MBROLA ready format into a file in which each sound is paired with it's duration (ms).

        Parameter:
        --------
            text : string - Text to convert.
        """

        text = text.lower()
        letterSoundDuration = {
            "a"  : 61,
            "b"  : 65,
            "c"  : 113,
            "č"  : 90,
            "ć"  : 98,
            "d"  : 54,
            "dž" : 56,
            "đ"  : 61,
            "e"  : 53,
            "f"  : 86,
            "g"  : 56,
            "h"  : 68,
            "i"  : 49,
            "j"  : 53,
            "k"  : 81,
            "l"  : 35,
            "lj" : 59,
            "m"  : 56,
            "n"  : 45,
            "nj" : 60,
            "o"  : 54,
            "p"  : 85,
            "r"  : 25,
            "s"  : 91,
            "š"  : 99,
            "t"  : 76,
            "u"  : 50,
            "v"  : 40,
            "z"  : 68,
            "ž"  : 74
        }

        file = open("mbrola_text.txt", 'w+', encoding = "UTF-8")

        text = list("".join(text.split()))
        textLength = len(text)

        for i in range(textLength):
            digraph = text[i - 1] + text[i]
            if (digraph in ["dž","lj","nj"]):
                file.write("{0} - {1}".format(digraph, letterSoundDuration[digraph]))
                i += 1
            else:
                letter = text[i]
                file.write("{0} - {1}".format(letter, letterSoundDuration[letter]))
            if (i < textLength - 1):
                file.write('\n')

        file.close()