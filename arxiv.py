from bs4 import BeautifulSoup
import requests
import concurrent.futures

# declaring global variables
subjects = {"cs": 2000,          # Computer Science
            "physics": 1000,     # Physics
            "math": 1000,        # Mathematics
            "q-bio": 500,        # Quantitative Biology
            "q-fin": 500,         # Quantitative Finance
            "stat": 500,         # Statistics
            "eess": 500,         # Electrical Engineering and Systems Science
            "econ": 500}         # Economics

subjects_map = {subject: {} for subject in subjects}


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
            sub_url = f"{host}{link.get('href')}"
            title = get_title(sub_url)
            abstract = get_abstract(sub_url)
            if (title is not None) and (abstract is not None):
                subjects_map[subject][title] = abstract
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
    file = open("output/all.out", "w")
    for subject in subjects:
        home = f"https://export.arxiv.org/list/{subject}"
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

        for title in subjects_map[subject].keys():
            file.write(f"Title: {title}\n")
            file.write(f"{subjects_map[subject][title]}\n")
            file.write("\n")
            file.write("---------------------------------------------------------------------------")
            file.write("\n\n")

    file.close()


if __name__ == '__main__':
    main()
