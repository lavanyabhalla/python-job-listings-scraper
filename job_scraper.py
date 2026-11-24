
import requests
from bs4 import BeautifulSoup
import csv

# Website URL
URL = "https://realpython.github.io/fake-jobs/"

def scrape_jobs():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = soup.find_all("div", class_="card-content")

    job_list = []

    for job in jobs:
        title = job.find("h2", class_="title")
        company = job.find("h3", class_="company")
        location = job.find("p", class_="location")
        link = job.find("a", string="Apply")

        job_list.append({
            "Job Title": title.get_text(strip=True) if title else "N/A",
            "Company": company.get_text(strip=True) if company else "N/A",
            "Location": location.get_text(strip=True) if location else "N/A",
            "Job URL": link["href"] if link and link.has_attr("href") else "N/A"
        })

    return job_list


def save_to_csv(jobs):
    with open("job_listings.csv", "w", newline="", encoding="utf-8") as file:
        fieldnames = ["Job Title", "Company", "Location", "Job URL"]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"Successfully saved {len(jobs)} jobs!")


if __name__ == "__main__":
    jobs = scrape_jobs()
    save_to_csv(jobs)
