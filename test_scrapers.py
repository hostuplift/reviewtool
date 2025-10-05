import json
import requests
from apify_client import ApifyClient
import csv

API_TOKEN = "YOUR_APIFY_API_TOKEN"

def get_dataset_id(run_url):
    resp = requests.get(run_url)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["items"][0]["defaultDatasetId"]

def test_all_scrapers_raw():
    # Apify actor run URLs
    booking_run_url = "https://api.apify.com/v2/acts/voyager~booking-reviews-scraper/runs?token=" + API_TOKEN
    expedia_run_url = "https://api.apify.com/v2/acts/tri_angle~expedia-hotels-com-reviews-scraper/runs?token=" + API_TOKEN
    tripadvisor_run_url = "https://api.apify.com/v2/acts/maxcopell~tripadvisor-reviews/runs?token=" + API_TOKEN
    google_run_url = "https://api.apify.com/v2/acts/compass~google-maps-reviews-scraper/runs?token=" + API_TOKEN

    # Get dataset IDs
    booking_dataset_id = get_dataset_id(booking_run_url)
    expedia_dataset_id = get_dataset_id(expedia_run_url)
    tripadvisor_dataset_id = get_dataset_id(tripadvisor_run_url)
    google_dataset_id = get_dataset_id(google_run_url)

    # Construct dataset URLs
    booking_dataset_url = f"https://api.apify.com/v2/datasets/{booking_dataset_id}/items?token={API_TOKEN}"
    expedia_dataset_url = f"https://api.apify.com/v2/datasets/{expedia_dataset_id}/items?token={API_TOKEN}"
    tripadvisor_dataset_url = f"https://api.apify.com/v2/datasets/{tripadvisor_dataset_id}/items?token={API_TOKEN}"
    google_dataset_url = f"https://api.apify.com/v2/datasets/{google_dataset_id}/items?token={API_TOKEN}"

    print("\n=== RAW Booking.com Review ===")
    try:
        resp = requests.get(booking_dataset_url)
        resp.raise_for_status()
        reviews = resp.json()
        if reviews:
            print(json.dumps(reviews[0], indent=2))
    except Exception as e:
        print(f"Booking.com Error: {str(e)}")

    print("\n=== RAW Expedia Review ===")
    try:
        resp = requests.get(expedia_dataset_url)
        resp.raise_for_status()
        reviews = resp.json()
        if reviews:
            print(json.dumps(reviews[0], indent=2))
    except Exception as e:
        print(f"Expedia Error: {str(e)}")

    print("\n=== RAW TripAdvisor Review ===")
    try:
        resp = requests.get(tripadvisor_dataset_url)
        resp.raise_for_status()
        reviews = resp.json()
        if reviews:
            print(json.dumps(reviews[0], indent=2))
    except Exception as e:
        print(f"TripAdvisor Error: {str(e)}")

    print("\n=== RAW Google Maps Review ===")
    try:
        resp = requests.get(google_dataset_url)
        resp.raise_for_status()
        reviews = resp.json()
        if reviews:
            print(json.dumps(reviews[0], indent=2))
    except Exception as e:
        print(f"Google Maps Error: {str(e)}")

# Initialize the ApifyClient with your API token
client = ApifyClient("YOUR_APIFY_API_TOKEN")

# Prepare the Actor input
run_input = {
    "searchStringsArray": ["restaurant"],
    "locationQuery": "brockenhurst UK",
    "maxCrawledPlacesPerSearch": 100,
    "skipClosedPlaces": True,
}

# Run the Actor and wait for it to finish
run = client.actor("nwua9Gu5YrADL7ZDj").call(run_input=run_input)

# Fetch Actor results from the run's dataset (if there are any)
results = list(client.dataset(run["defaultDatasetId"]).iterate_items())

# Save results to CSV
if results:
    keys = set()
    for item in results:
        keys.update(item.keys())
    keys = list(keys)
    with open("apify_results.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {len(results)} results to apify_results.csv")
else:
    print("No results found.")

if __name__ == "__main__":
    test_all_scrapers_raw() 