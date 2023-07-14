from bs4 import BeautifulSoup
import requests
import concurrent.futures
import json

# declaring global variables
subjects = {"cs": 2500,         # Computer Science
            "physics": 1000,     # Physics
            "math": 1000,        # Mathematics
            "q-bio": 500,        # Quantitative Biology
            "q-fin": 500,         # Quantitative Finance
            "stat": 500,         # Statistics
            "eess": 500,         # Electrical Engineering and Systems Science
            "econ": 500}         # Economics

subjects_map = {subject: [] for subject in subjects}


def get_title(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    for candidate in soup.find_all('h1'):
        if candidate.get('class') == ['title', 'mathjax']:
            return candidate.text.replace("Title:", "")
    return None


def get_abstract(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('blockquote') is None:
        return None
    else:
        return soup.find('blockquote').text


def extract_article_links(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    return links


def concurrent_populate(subject, host, links, num_threads):
    def process_link(link):
        if link.get('title') == "Abstract":
            article_id = link.get('href')
            sub_url = f"{host}{article_id}"
            title = get_title(sub_url).lstrip("\n")
            abstract = get_abstract(sub_url).lstrip("\nAbstract: ")
            if (title is not None) and (abstract is not None):
                article = {'title': title,
                           'abstract': abstract,
                           'id': article_id.lstrip("/abs/")}
                subjects_map[subject].append(article)
            print("#", end="")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor using the process_link function
        future_to_link = {executor.submit(process_link, link): link for link in links}

        # Wait for the tasks to complete
        for future in concurrent.futures.as_completed(future_to_link):
            link = future_to_link[future]
            try:
                future.result()  # Retrieve the result of the task
            except Exception as e:
                print(f"Error processing link: {link}\n{e}")
    print("\n")
    return


def main():
    year = 23
    month = 5
    for subject in subjects:
        number = "{:02d}".format(month) if month >= 10 else "0{}".format(month)
        home = f"https://export.arxiv.org/list/{subject}/{year}{number}"
        url_host = home.replace("https://export.", "")
        if url_host[0:5] == "arxiv":
            host = "https://export.arxiv.org"
        else:
            exit(1)
        for i in range(0, subjects[subject], 500):
            visiting = f"{home}?skip={i}&show=500"
            print(f"Extracting abstracts of essays on: {visiting}")
            concurrent_populate(subject, host, extract_article_links(visiting), 250)

    print("-------------------------------- Crawling Complete --------------------------------")

    json_object = json.dumps(subjects_map, indent=4)

    with open("/Users/ryansong612/Desktop/research-LLM/output/all.json", "w") as file:
        file.write(json_object)


if __name__ == '__main__':
    main()
