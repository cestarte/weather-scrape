import bs4
import requests
import re
from weather import Weather


def numeric_from_str(text: str):
    filtered = filter(type(text).isdigit, text)
    return "".join(filtered)


def find_condition(soup: bs4.BeautifulSoup):
    value = ""
    elem = soup.select_one(".myforecast-current")
    if elem != None:
        value = elem.text
    return value


def find_station_name(soup: bs4.BeautifulSoup):
    value = ""
    elem = soup.select_one("#current-conditions .panel-header .panel-title")
    if elem != None:
        value = elem.text
    return value


def find_high(soup: bs4.BeautifulSoup):
    value = ""
    # TODO: there are multiple .temp-high
    elem = soup.select_one(".temp-high")
    if elem != None:
        value = numeric_from_str(elem.text)
    return value


def find_low(soup: bs4.BeautifulSoup):
    value = ""
    # TODO: there are multiple .temp-low
    elem = soup.select_one(".temp-low")
    if elem != None:
        value = numeric_from_str(elem.text)
    return value


def find_degree(soup: bs4.BeautifulSoup):
    value = ""
    unit = ""

    elem = soup.select_one("myforecast-current-lrg")
    if elem != None:
        raw = elem.text
        temp = raw.split("°")
        if len(temp) > 0:
            value = temp[0]
        if len(temp) >= 2:
            unit = temp[-1]

    return {"value": value, "unit": unit}


def scrape(url: str):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    w = Weather()
    w.high_temp = find_high(soup)
    w.low_temp = find_low(soup)
    degree = find_degree(soup)
    w.current_temp = degree["value"]
    w.degree_unit = degree["unit"]
    w.condition = find_condition(soup)
    # w.humidity = find_humidity(soup)
    # coord = find_coordinates(soup)
    # w.north = coord["north"]
    # w.south = coord["south"]
    # w.west = coord["west"]
    # w.east = coord["east"]
    # elevation = find_elevation(soup)
    # w.elevation = elevation["value"]
    # w.elevation_unit = elevation["unit"]
    w.station = find_station_name(soup)
    # w.location = find_location_name(soup)
    w.url = url

    return w


if __name__ == "__main__":
    url = "https://forecast.weather.gov/MapClick.php?lat=26.189630000000022&lon=-97.69505999999996"

    w = scrape(url)
    w.print()
