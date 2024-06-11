import logging

import requests
import json
import threading

API_LINK = "http://universities.hipolabs.com/search?country="

logger = logging.getLogger("University Fetcher")
logging.basicConfig(level=logging.INFO)


def fetch_university(session, country):
    with session.get(API_LINK + country) as response:
        json_content = json.loads(response.content)

        return json_content


def download_all_countries(countries):
    data = []
    with requests.Session() as session:
        threads = []
        for country in countries[0:9]:
            thread = threading.Thread(target=lambda: data.append(fetch_university(session, country )))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    return data


def main():
    countries = ["poland", "united kingdom", "france", "germany", "italy",
                 "belgium", "netherlands", "luxembourg", "spain", "portugal",
                 "switzerland", "czech republic", "slovakia", "austria", "hungary"]
    countries_data = download_all_countries(countries[0:9]) + download_all_countries(countries[10:14])
    for country in countries_data:
        logging_data = "{"+f"{country[0]['country']}: "
        for ind, university in enumerate(country):
            logging_data += university['name']
            if ind < len(country):
                logging_data += ", "
        logging_data += "}"
        logger.info(logging_data)


if __name__ == '__main__':
    main()
