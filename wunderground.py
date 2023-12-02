import bs4
import requests
import re


def numeric_from_elem(soup_elem):
    raw = soup_elem.text
    filtered = filter(type(raw).isdigit, raw)
    return "".join(filtered)


def alpha_from_elem(soup_elem):
    raw = soup_elem.text
    filtered = filter(type(raw).isalpha, raw)
    return "".join(filtered)


def find_high(soup: bs4.BeautifulSoup):
    high = ""
    high_elem = soup.select_one(".hi")
    if high_elem != None:
        high = numeric_from_elem(high_elem)
    return high


def find_low(soup: bs4.BeautifulSoup):
    low = ""
    low_elem = soup.select_one(".lo")
    if low_elem != None:
        low = numeric_from_elem(low_elem)
    return low


def find_coordinates(soup: bs4.BeautifulSoup):
    # ex: Harlingen, TX at 26.19N, 97.7W
    north = find_single_coordinate(soup, "°N")
    east = find_single_coordinate(soup, "°E")
    south = find_single_coordinate(soup, "°S")
    west = find_single_coordinate(soup, "°W")
    return {"north": north, "east": east, "south": south, "west": west}


def find_single_coordinate(soup: bs4.BeautifulSoup, search_text: str):
    coord = ""
    coord_parent = soup.find(string=re.compile(search_text))
    if coord_parent != None:
        coord_elem = coord_parent.previous_sibling
        if coord_elem != None:
            coord = coord_elem.text
    return coord


def find_elevation(soup: bs4.BeautifulSoup):
    elev = ""
    unit = ""

    elev_parent = soup.find(string=re.compile("^Elev"))
    elev_elem = elev_parent.next_sibling
    if elev_elem != None:
        elev = elev_elem.text
        unit = alpha_from_elem(elev_elem.next_sibling)
    return {"value": elev, "unit": unit}


def find_degree(soup: bs4.BeautifulSoup):
    degree = ""
    unit = ""
    degree_elem = soup.select_one(".current-temp .wu-value.wu-value-to")
    if degree_elem != None:
        degree = numeric_from_elem(degree_elem)
        unit_elem = soup.select_one(".wu-degree").next_sibling
        if unit_elem != None:
            unit = alpha_from_elem(unit_elem)
    return {"value": degree, "unit": unit}


def find_station_name(soup: bs4.BeautifulSoup):
    name = ""
    station_elem = soup.select_one(".station-name")
    if station_elem != None:
        contents = station_elem.contents
        if len(contents) > 1:
            name = contents[1].text.strip()
        elif len(contents > 0):
            name = contents[0].text.strip()
    return name


def find_location_name(soup: bs4.BeautifulSoup):
    search_text = "Weather Conditions"
    name = ""
    header_elem = soup.select_one(".city-header h1")
    if header_elem != None:
        contents = header_elem.contents
        if len(contents) > 0:
            temp = contents[0].text
            name = temp.replace(search_text, "").strip()
    return name


if __name__ == "__main__":
    # url = "https://www.wunderground.com/weather/us/tx/dallas"
    url = "https://www.wunderground.com/weather/za/johannesburg"
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    high = find_high(soup)
    print(f"High: {high}")
    low = find_low(soup)
    print(f"Low: {low}")
    degree = find_degree(soup)
    print(f"Now: {degree['value']} {degree['unit']}")
    coord = find_coordinates(soup)
    print(
        f"Coord: {coord['north']}N, {coord['south']}S, {coord['east']}E, {coord['west']}W"
    )
    elevation = find_elevation(soup)
    print(f"Elevation: {elevation['value']} {elevation['unit']}")
    station = find_station_name(soup)
    print(f"Station: {station}")
    location = find_location_name(soup)
    print(f"Location: {location}")