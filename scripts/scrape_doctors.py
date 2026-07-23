import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.yashodahospitals.com/locations/hitec-city/doctors/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

doctors = []

cards = soup.find_all("div", class_="find-doc-list")

for card in cards:

    try:
        name = card.find("p", class_="doc-name").get_text(strip=True)

        qualification = card.find(
            "small",
            class_="text-muted"
        ).get_text(strip=True)

        speciality = card.find_all(
            "p"
        )[1].get_text(strip=True)

        languages = card.find(
            "p",
            class_="d-flex know-lang text-muted mb-0"
        ).get_text(
            " ",
            strip=True
        )

        experience = ""

        for small in card.find_all("small"):
            if "Yrs" in small.text:
                experience = small.text.strip()

        location = ""

        for small in card.find_all("small"):
            if "Hitec" in small.text:
                location = small.text.strip()

        timing_div = card.find(
            "div",
            id=lambda x: x and "timings" in x
        )

        timings = ""

        if timing_div:
            timings = timing_div.get_text(
                " ",
                strip=True
            )

        expertise_div = card.find(
            "div",
            id=lambda x: x and "expertise" in x
        )

        expertise = ""

        if expertise_div:
            expertise = expertise_div.get_text(
                " ",
                strip=True
            )

        service_div = card.find(
            "div",
            id=lambda x: x and "services-offered" in x
        )

        services = ""

        if service_div:
            services = service_div.get_text(
                " ",
                strip=True
            )

        profile_url = card.find(
            "a",
            title=True
        )["href"]

        doctors.append(
            {
                "name": name,
                "qualification": qualification,
                "speciality": speciality,
                "experience": experience,
                "languages": languages,
                "location": location,
                "opd_timings": timings,
                "expertise": expertise,
                "services": services,
                "profile_url": profile_url,
                "hospital": "Yashoda Hospital Hitec City"
            }
        )

    except Exception as e:
        print(e)

df = pd.DataFrame(doctors)

print(df.head())

df.to_csv(
    "data/doctors.csv",
    index=False
)