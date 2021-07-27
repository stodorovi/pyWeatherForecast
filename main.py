from weather import ForecastType, Weather

if __name__ == "__main__":
    Weather.getForecast(ForecastType.TEXT)

    Weather.writeMBROLAText(Weather.getForecast(ForecastType.MBROLA))