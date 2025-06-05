import requests
import time
import csv
import os
from dotenv import load_dotenv
import sys

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("YELP_API_KEY")

# Debugging: Check if key is loaded and clean
print(f"DEBUG: Loaded API key: {repr(API_KEY)}")
if not API_KEY:
    raise ValueError("❌ API key not loaded. Please check your .env file.")


CATEGORY = sys.argv[1] if len(sys.argv) > 1 else 'gardening'
print(f"📦 Using category: {CATEGORY}")
LIMIT = 50
MAX_RESULTS = 240
BASE_URL = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}

over_240_locations = []

# Towns mapped to regions
town_to_region = {
    "Nottingham": "Nottinghamshire", "Mansfield": "Nottinghamshire", "Worksop": "Nottinghamshire",
    "Newark-on-Trent": "Nottinghamshire", "Retford": "Nottinghamshire",
    "Stoke-on-Trent": "Staffordshire", "Stafford": "Staffordshire", "Burton upon Trent": "Staffordshire",
    "Cannock": "Staffordshire", "Lichfield": "Staffordshire", "Tamworth": "Staffordshire",
    "Leicester": "Leicestershire", "Loughborough": "Leicestershire", "Hinckley": "Leicestershire",
    "Coalville": "Leicestershire", "Melton Mowbray": "Leicestershire", "Market Harborough": "Leicestershire",
    "Lincoln": "Lincolnshire", "Grantham": "Lincolnshire", "Boston": "Lincolnshire", "Skegness": "Lincolnshire",
    "Spalding": "Lincolnshire", "Scunthorpe": "Lincolnshire", "Gainsborough": "Lincolnshire",
    "Chester": "Cheshire", "Crewe": "Cheshire", "Macclesfield": "Cheshire", "Warrington": "Cheshire",
    "Northwich": "Cheshire", "Ellesmere Port": "Cheshire",
    "Derby": "Derbyshire", "Chesterfield": "Derbyshire", "Ilkeston": "Derbyshire", "Buxton": "Derbyshire",
    "Glossop": "Derbyshire", "Swadlincote": "Derbyshire", "Matlock": "Derbyshire",
    "Northampton": "Northamptonshire", "Kettering": "Northamptonshire", "Wellingborough": "Northamptonshire",
    "Corby": "Northamptonshire", "Daventry": "Northamptonshire", "Rushden": "Northamptonshire",
    "Warwick": "Warwickshire", "Leamington Spa": "Warwickshire", "Stratford-upon-Avon": "Warwickshire",
    "Rugby": "Warwickshire", "Nuneaton": "Warwickshire", "Bedworth": "Warwickshire",
    "Durham": "Durham", "Peterlee": "Durham", "Bishop Auckland": "Durham", "Chester-le-Street": "Durham",
    "Seaham": "Durham", "Consett": "Durham",
    "Carlisle": "Cumbria", "Kendal": "Cumbria", "Barrow-in-Furness": "Cumbria",
    "Workington": "Cumbria", "Whitehaven": "Cumbria", "Penrith": "Cumbria",
    "Shrewsbury": "Shropshire", "Telford": "Shropshire", "Oswestry": "Shropshire", "Bridgnorth": "Shropshire",
    "Whitchurch": "Shropshire", "Ludlow": "Shropshire",
    "Morpeth": "Northumberland", "Alnwick": "Northumberland", "Hexham": "Northumberland",
    "Ashington": "Northumberland", "Berwick-upon-Tweed": "Northumberland", "Blyth": "Northumberland",
    "Armagh": "Armagh", "Portadown": "Armagh", "Lurgan": "Armagh", "Craigavon": "Armagh", "Banbridge": "Armagh",
    "Carmarthen": "Carmarthenshire", "Llanelli": "Carmarthenshire", "Ammanford": "Carmarthenshire",
    "Llandovery": "Carmarthenshire", "Kidwelly": "Carmarthenshire",
    "Newry": "Newry, Mourne and Down", "Downpatrick": "Newry, Mourne and Down", "Warrenpoint": "Newry, Mourne and Down",
    "Kilkeel": "Newry, Mourne and Down", "Ballynahinch": "Newry, Mourne and Down",
    "Derry": "Derry City and Strabane", "Strabane": "Derry City and Strabane", "Eglinton": "Derry City and Strabane",
    "Castlederg": "Derry City and Strabane", "Claudy": "Derry City and Strabane",
    "Cookstown": "Mid Ulster", "Dungannon": "Mid Ulster", "Magherafelt": "Mid Ulster",
    "Coalisland": "Mid Ulster", "Pomeroy": "Mid Ulster",
    "Coleraine": "Causeway Coast and Glens", "Ballymoney": "Causeway Coast and Glens", "Portrush": "Causeway Coast and Glens",
    "Portstewart": "Causeway Coast and Glens", "Limavady": "Causeway Coast and Glens",
    "Larne": "Mid and East Antrim", "Ballymena": "Mid and East Antrim", "Carrickfergus": "Mid and East Antrim", "Whitehead": "Mid and East Antrim",
    "Brecon": "Powys", "Newtown": "Powys", "Llandrindod Wells": "Powys", "Welshpool": "Powys", "Ystradgynlais": "Powys",
    "Bangor": "Gwynedd", "Caernarfon": "Gwynedd", "Porthmadog": "Gwynedd", "Pwllheli": "Gwynedd", "Blaenau Ffestiniog": "Gwynedd",
    "Enniskillen": "Fermanagh and Omagh", "Omagh": "Fermanagh and Omagh", "Lisnaskea": "Fermanagh and Omagh",
    "Irvinestown": "Fermanagh and Omagh", "Dromore": "Fermanagh and Omagh",
    "Aberystwyth": "Ceredigion", "Cardigan": "Ceredigion", "Lampeter": "Ceredigion", "Tregaron": "Ceredigion", "New Quay": "Ceredigion"
}

# Towns plus counties to search
locations = list(town_to_region.keys()) + [
    "Tyne and Wear", "Norfolk", "Cambridgeshire", "Worcestershire", "Cardiff", "Belfast", "Swansea",
    "Caerphilly", "Ards and North Down", "Newport", "Flintshire", "Lisburn and Castlereagh",
    "Bridgend", "Antrim and Newtownabbey", "Neath Port Talbot", "Wrexham", "Vale of Glamorgan",
    "Pembrokeshire", "Conwy", "Denbighshire", "Monmouthshire", "Torfaen", "Blaenau Gwent",
    "Merthyr Tydfil", "Rutland"
]

# Begin search
for location in locations:
    all_results = []
    print(f"\n🔍 Searching: {location}")

    for offset in range(0, MAX_RESULTS, LIMIT):
        params = {
            'location': f"{location}, UK",
            'categories': CATEGORY,
            'limit': LIMIT,
            'offset': offset,
            'country': 'GB'
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json()
            businesses = data.get('businesses', [])
            all_results.extend(businesses)
            print(f"  Fetched {len(businesses)} at offset {offset}")

            if len(businesses) < LIMIT:
                break

            if offset + LIMIT >= MAX_RESULTS:
                over_240_locations.append(location)
        else:
            print(f"  ❌ Error for {location} at offset {offset}: {response.status_code} - {response.text}")
            break

        time.sleep(1)

    # Save CSV
    parent_region = town_to_region.get(location, location)
    output_folder = f"{CATEGORY}-yelp-output"
    folder_path = os.path.join(output_folder, parent_region)

    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, f"{location.replace(',', '').replace(' ', '_')}.csv")

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'alias', 'name', 'category_alias', 'category_title',
            'latitude', 'longitude',
            'address1', 'address2', 'address3',
            'city', 'zip_code', 'country', 'state',
            'display_address_0', 'display_address_1', 'display_address_2', 'display_address_3',
            'display_phone'
        ])

        for b in all_results:
            categories = b.get('categories', [{}])
            category = categories[0] if categories else {}
            loc = b.get('location', {})
            display_address = loc.get('display_address', [])

            writer.writerow([
                b.get('alias', ''),
                b.get('name', ''),
                category.get('alias', ''),
                category.get('title', ''),
                b.get('coordinates', {}).get('latitude', ''),
                b.get('coordinates', {}).get('longitude', ''),
                loc.get('address1', ''),
                loc.get('address2', ''),
                loc.get('address3', ''),
                loc.get('city', ''),
                loc.get('zip_code', ''),
                loc.get('country', ''),
                loc.get('state', ''),
                display_address[0] if len(display_address) > 0 else '',
                display_address[1] if len(display_address) > 1 else '',
                display_address[2] if len(display_address) > 2 else '',
                display_address[3] if len(display_address) > 3 else '',
                b.get('display_phone', '')
            ])

    print(f"  ✅ Saved {len(all_results)} results to {filename}")

# Log capped results
if over_240_locations:
    print("\n⚠️ Locations that hit Yelp's 240 result cap:")
    for loc in over_240_locations:
        print(f" - {loc}")
    with open("yelp_output/locations_over_240.txt", "w", encoding="utf-8") as f:
        for loc in over_240_locations:
            f.write(loc + "\n")
else:
    print("\n✅ No locations hit the 240 result limit.")
