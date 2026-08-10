COUNTRY_FLAGS = {
    "USA": "🇺🇸",
    "United States": "🇺🇸",
    "United Kingdom": "🇬🇧",
    "UK": "🇬🇧",
    "Canada": "🇨🇦",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "West Germany": "🇩🇪",
    "Italy": "🇮🇹",
    "Spain": "🇪🇸",
    "Japan": "🇯🇵",
    "South Korea": "🇰🇷",
    "China": "🇨🇳",
    "Hong Kong": "🇭🇰",
    "India": "🇮🇳",
    "Australia": "🇦🇺",
    "New Zealand": "🇳🇿",
    "Ireland": "🇮🇪",
    "Mexico": "🇲🇽",
    "Brazil": "🇧🇷",
    "Argentina": "🇦🇷",
    "Sweden": "🇸🇪",
    "Norway": "🇳🇴",
    "Denmark": "🇩🇰",
    "Netherlands": "🇳🇱",
    "Belgium": "🇧🇪",
    "Switzerland": "🇨🇭",
    "Austria": "🇦🇹",
    "Russia": "🇷🇺",
    "Soviet Union": "🇷🇺",
    "Poland": "🇵🇱",
    "Czech Republic": "🇨🇿",
    "Greece": "🇬🇷",
    "Turkey": "🇹🇷",
    "South Africa": "🇿🇦",
}


def get_flag(country):
    """Returns a flag emoji for a country name, or an empty string if unknown."""
    if not country:
        return ""
    return COUNTRY_FLAGS.get(country, "")
