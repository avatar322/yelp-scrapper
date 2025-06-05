# 🧹 UK Yelp Business Scraper

This Python script uses the Yelp Fusion API to scrape business listings by town or region across the UK, grouped by **category** and **location**. It's great for building business databases, doing regional research, or prospecting leads.

---

## 🚀 What It Does

- Queries Yelp’s API using a specified **business category**
- Searches by **UK town/city/county names**, broken into manageable locations
- Automatically handles Yelp's **240-result limit** by breaking up areas
- Saves each location’s results into neatly structured CSVs, organised by region
- Logs any location that hits the result cap so you know where you might be missing data

---

## 🛠 Requirements

- Python 3.7+
- Yelp API Key (free from https://www.yelp.com/developers/v3/manage_app)

### Python Libraries
Install required packages with:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, these are the packages:

```bash
pip install requests pandas python-dotenv
```

---

## 🔑 Setup

1. **Create a `.env` file in the project folder**, and add your Yelp API key:

   ```env
   YELP_API_KEY=your_actual_api_key_here
   ```

   ⚠️ Be careful — the file must be saved (not just open in an editor), and should have no quotes or extra spaces.

2. **Run the script** with a Yelp category as an argument:

   ```bash
   python scrapper.py gardening
   ```

   If you don’t specify a category, it will default to `'gardening'`.

---

## 🔄 Changing the Search Category

To switch categories, just pass it as a command-line argument:

```bash
python scrapper.py football
```

This will look for businesses in the "football" category across all locations. The results will be saved in:

```
football-yelp-output/
```

You can change the category to anything supported by Yelp — examples:
- `florists`
- `hairdressers`
- `coffee`
- `petservices`
- `accountants`

Check the [Yelp category list](https://www.yelp.com/developers/documentation/v3/all_category_list) to find valid values.

---

## 🌍 Changing the Locations

The script uses a dictionary called `town_to_region` to map UK towns to their counties or unitary authorities.

You can **edit or expand it** directly in the Python file like this:

```python
town_to_region = {
    "Nottingham": "Nottinghamshire",
    "Mansfield": "Nottinghamshire",
    "Worksop": "Nottinghamshire",
    ...
}
```

To add more locations:
1. Add more entries to this dictionary.
2. Or expand the `locations = [...]` list below it with other counties or cities (e.g. `"Greater London"`, `"Cornwall"`).

🧠 **Tip**: If you're hitting the 240-result cap often, break large cities into boroughs (e.g. `"Camden"`, `"Hackney"` instead of `"London"`).

---

## 📁 Output

Each town/county gets its own CSV file inside a category-named folder:

```
gardening-yelp-output/
└── Nottinghamshire/
    └── Nottingham.csv
```

Each file contains:
- Business name, alias
- Coordinates
- Address
- Category info
- Display phone

A log file is created for areas that hit the **Yelp 240-result cap**:

```
gardening-yelp-output/locations_over_240.txt
```

---

## 🧪 Troubleshooting & Gotchas

### 🐛 My API key isn’t working
- Check that `.env` is **saved** and in the **same folder** as your Python file.
- Make sure there’s **no extra whitespace** or quote marks.
- Use `print(repr(API_KEY))` to debug what’s loading from `.env`.

### 🔄 I changed the locations, but it’s not working
- Ensure your location names are valid for Yelp (e.g. `"Bath, UK"` works, `"The Moon"` doesn't).
- Avoid spelling errors.
- Use small locations for large areas (break “London” into boroughs).

### ❌ Yelp says I’ve hit a limit
- Yelp only gives up to **240 results per location** — this is a known cap.
- Check the `locations_over_240.txt` file — these areas may need to be broken down more.

---

## 📌 Future Ideas

- Load locations from an external CSV file
- Auto-split large cities based on population or postcode
- Build a small GUI for non-tech users
- Push data to a database or Airtable

---

## 🧾 Licence

MIT — use freely, but respect Yelp’s [terms of service](https://www.yelp.com/developers/api_terms).

---

## 🙌 Credits

Powered by the [Yelp Fusion API](https://www.yelp.com/developers/documentation/v3).

Built with Python, by someone just trying to get useful data out of a fussy API.
