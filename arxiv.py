from bs4 import BeautifulSoup
import requests
import concurrent.futures

# declaring global variables
cs_map = {}
subjects = {"cs": cs_map}


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


def concurrent_populate(host, links, num_threads):
    def process_link(link):
        if link.get('title') == "Abstract":
            print("#", end="")
            sub_url = f"{host}{link.get('href')}"
            title = get_title(sub_url)
            abstract = get_abstract(sub_url)
            if (title is not None) and (abstract is not None):
                cs_map[title] = abstract

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
    home = "https://export.arxiv.org/list/cs/pastweek"
    subject = "cs"
    url_host = home.replace("https://export.", "")
    if url_host[0:5] == "arxiv":
        host = "https://export.arxiv.org"
    else:
        exit(1)
    for i in range(0, 2751, 250):
        visiting = f"{home}?skip={i}&show=250"
        print(f"Extracting abstracts of essays on: {visiting}")
        concurrent_populate(host, extract_article_links(visiting), 250)

    print("--------------------------------- Crawling Complete ---------------------------------")

    file = open("output/cs.out", "w")

    for title in subjects[subject].keys():
        file.write(f"Title: {title}\n")
        file.write(f"{subjects[subject][title]}\n")
        file.write("\n")
        file.write("------------------------------------------------------------------------------")
        file.write("\n\n")

    file.close()
    return 1


if __name__ == '__main__':
    main()
