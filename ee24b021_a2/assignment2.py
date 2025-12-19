import csv

# ========================== BASIC UTILITIES ==========================

def get_city_temperatures(filename, city_name):
    """
    Extract temperature data for a specific city from CSV file.
    Returns dict: {'YYYY-MM': temperature}.
    """
    temperature_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'] == city_name and row['AverageTemperature']:
                try:
                    year_month = row['dt'][:7]  # YYYY-MM
                    temperature_data[year_month] = float(row['AverageTemperature'])
                except ValueError:
                    continue
    return temperature_data


def get_available_cities(filename, limit=None):
    """Return sorted list of unique city names."""
    cities = set()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cities.add(row['City'])
            if limit and len(cities) >= limit:
                break
    return sorted(cities)


def get_available_years(filename, limit=None):
    """Return sorted list of available years (as integers)."""
    years = set()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                year = int(row['dt'][:4])
                years.add(year)
            except ValueError:
                continue
            if limit and len(years) >= limit:
                break
    return sorted(years)


def avg_temperature_with_uncertainty(filename, city_name):
    """
    Weighted average of temperatures for a city, using uncertainty as weight.
    """
    num, den = 0.0, 0.0
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'] == city_name and row['AverageTemperature']:
                try:
                    temp = float(row['AverageTemperature'])
                    unc = float(row['AverageTemperatureUncertainty'])
                    weight = 1.0 / (unc if unc != 0 else 1.0)
                    num += temp * (weight ** 2)
                    den += weight ** 2
                except ValueError:
                    continue
    if den == 0:
        raise ValueError(f"No valid data found for city '{city_name}'")
    return num / den


def country_name(filename, city_name):
    """Return the country name for a given city."""
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'] == city_name:
                return row['Country']
    raise ValueError(f"City '{city_name}' not found in dataset")


# ========================== API FUNCTIONS ==========================

def find_temperature_extremes(filename, city_name):
    """Find the hottest and coldest months on record for a city."""
    date_temp = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'] == city_name and row['AverageTemperature']:
                date_temp[row['dt'][:7]] = float(row['AverageTemperature'])

    if not date_temp:
        raise ValueError(f"City '{city_name}' not found or has no data")

    min_key = min(date_temp, key=date_temp.get)
    max_key = max(date_temp, key=date_temp.get)
    return {
        'hottest': {'date': max_key, 'temperature': date_temp[max_key]},
        'coldest': {'date': min_key, 'temperature': date_temp[min_key]}
    }


def get_seasonal_averages(filename, city_name, season):
    """Compute weighted average temperature for a given season."""
    seasons = {
        'spring': ['03', '04', '05'],
        'summer': ['06', '07', '08'],
        'fall':   ['09', '10', '11'],
        'winter': ['12', '01', '02']
    }
    if season not in seasons:
        raise ValueError("Season must be one of: spring, summer, fall, winter")

    months = seasons[season]
    num, den = 0.0, 0.0
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['City'] == city_name and row['dt'][5:7] in months and row['AverageTemperature']:
                try:
                    temp = float(row['AverageTemperature'])
                    unc = float(row['AverageTemperatureUncertainty'])
                    weight = 1.0 / (unc if unc != 0 else 1.0)
                    num += temp * (weight ** 2)
                    den += weight ** 2
                except ValueError:
                    continue

    if den == 0:
        raise ValueError(f"No data found for city '{city_name}' in season '{season}'")
    return {
        'city': city_name,
        'season': season,
        'average_temperature': num / den
    }


def compare_decades(filename, city_name, decade1, decade2):
    """Compare average temperatures between two decades."""
    def avg_for_decade(decade):
        num, den, count = 0.0, 0.0, 0
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['City'] == city_name and row['AverageTemperature']:
                    year = int(row['dt'][:4])
                    if year // 10 * 10 == decade:
                        try:
                            temp = float(row['AverageTemperature'])
                            unc = float(row['AverageTemperatureUncertainty'])
                            weight = 1.0 / (unc if unc != 0 else 1.0)
                            num += temp * (weight ** 2)
                            den += weight ** 2
                            count += 1
                        except ValueError:
                            continue
        if den == 0:
            raise ValueError(f"No data for {city_name} in {decade}s")
        return num / den, count

    avg1, count1 = avg_for_decade(decade1)
    avg2, count2 = avg_for_decade(decade2)

    diff = avg2 - avg1
    trend = 'warming' if diff > 0 else 'cooling' if diff < 0 else 'stable'

    return {
        'city': city_name,
        'decade1': {'period': f"{decade1}s", 'avg_temp': avg1, 'data_points': count1},
        'decade2': {'period': f"{decade2}s", 'avg_temp': avg2, 'data_points': count2},
        'difference': diff,
        'trend': trend
    }


def find_similar_cities(filename, target_city, tolerance=2.0):
    """Find cities with similar average temps within tolerance."""
    target_temp = avg_temperature_with_uncertainty(filename, target_city)
    similar = []
    for city in get_available_cities(filename):
        try:
            temp = avg_temperature_with_uncertainty(filename, city)
            diff = abs(target_temp - temp)
            if diff <= tolerance and city != target_city:
                similar.append({
                    'city': city,
                    'country': country_name(filename, city),
                    'avg_temp': temp,
                    'difference': diff
                })
        except ValueError:
            continue

    return {
        'target_city': target_city,
        'target_avg_temp': target_temp,
        'similar_cities': similar,
        'tolerance': tolerance
    }


def get_temperature_trends(filename, city_name, window_size=5):
    """Calculate annual averages, moving averages, and warming/cooling trends."""
    years = get_available_years(filename)
    city_data = get_city_temperatures(filename, city_name)

    # ---- Annual averages ----
    annual = {}
    for y in years:
        vals = [v for k, v in city_data.items() if int(k[:4]) == y]
        if vals:
            annual[y] = sum(vals) / len(vals)

    yrs = list(annual.keys())
    temps = list(annual.values())

    # ---- Moving averages ----
    moving = {}
    if len(temps) >= window_size:
        for i in range(window_size-1, len(temps)):
            window = temps[i-window_size+1:i+1]
            moving[yrs[i]] = sum(window) / window_size

    # ---- Overall slope ----
    slope = None
    if len(yrs) >= 2:
        slope = (temps[-1] - temps[0]) / (yrs[-1] - yrs[0])

    # ---- Warming/cooling streaks ----
    warming, cooling = [], []
    i = 0
    while i < len(temps) - 1:
        if temps[i+1] > temps[i]:
            start = i
            while i+1 < len(temps) and temps[i+1] > temps[i]:
                i += 1
            end = i
            year_diff = yrs[end] - yrs[start]
            rate = (temps[end] - temps[start]) / year_diff if year_diff else 0.0
            warming.append({'start': yrs[start], 'end': yrs[end], 'rate': rate})
        elif temps[i+1] < temps[i]:
            start = i
            while i+1 < len(temps) and temps[i+1] < temps[i]:
                i += 1
            end = i
            year_diff = yrs[end] - yrs[start]
            rate = (temps[start] - temps[end]) / year_diff if year_diff else 0.0
            cooling.append({'start': yrs[start], 'end': yrs[end], 'rate': rate})
        else:
            i += 1

    return {
        'city': city_name,
        'raw_annual_data': annual,
        'moving_averages': moving,
        'trend_analysis': {
            'overall_slope': slope,
            'warming_periods': warming,
            'cooling_periods': cooling
        }
    }


# ========================== TESTING ==========================

def test_api_functions():
    """
    Test all API functions with sample data.
    """
    filename = 'GlobalLandTemperaturesByMajorCity.csv'
    test_city = 'Madras'

    print("Testing Temperature Data API")
    print("=" * 40)

    
    """
    Test all API functions with sample data.
    """
    filename = 'GlobalLandTemperaturesByMajorCity.csv'
    test_city = 'Madras'

    print("Testing Temperature Data API")
    print("=" * 40)

    #Test basic function
    temps = get_city_temperatures(filename, test_city)
    print(f"Basic function: Found {len(temps)} temperature records")

    #Test extremes
    extremes = find_temperature_extremes(filename, test_city)
    print(f"Extremes: Hottest = {extremes['hottest']['temperature']}°C")

    #Test seasonal averages
    summer_avg = get_seasonal_averages(filename, test_city, 'summer')
    print(f"Seasonal: Summer average = {summer_avg['average_temperature']:.1f}°C")

    #Test decade comparison
    comparison = compare_decades(filename, test_city, 1980, 2000)
    print(f"Decades: Temperature change = {comparison['difference']:.2f}°C")

    #Test similar cities
    similar = find_similar_cities(filename, test_city, tolerance=3.0)
    print(f"Similar cities: Found {len(similar['similar_cities'])} matches")

    #Test trends
    trends = get_temperature_trends(filename, test_city)
    slope = trends['trend_analysis']['overall_slope']
    print(f"Trends: Overall slope = {slope:.4f}°C/year")


if __name__ == "__main__":
    test_api_functions()




