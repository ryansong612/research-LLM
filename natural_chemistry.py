from bs4 import BeautifulSoup
import requests
import concurrent.futures

chemistry_map = {}
subjects = {"chem": chemistry_map}


def next_page(domain, url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    button = soup.find(attrs={"class": "c-pagination"}).find('li', attrs={"data-page": "next"})
    if button.find('a') is None:
        return None
    return f"{domain}{button.find('a').get('href')}"


def get_section(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all('section')
    return sections


def extract_article_links(url):
    sections = get_section(url)
    for section in sections:
        if section.get('id') == "new-article-list":
            links = section.find_all('li')
            return links
    return None


def extract_article_description(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(attrs={"name": "dc.description"}).get('content')


def concurrent_populate(domain, pages, num_threads):
    def process_page(page):
        lks = extract_article_links(page)
        for lk in lks:
            process_link(lk)
        print("#", end="")

    def process_link(lk):
        articles = lk.find_all('article')
        for article in articles:
            title_block = article.find('h3')
            article_link = f"{domain}{title_block.find('a').get('href')}"
            chemistry_map[title_block.text] = extract_article_description(article_link)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks to the executor using the process_link function
        future_to_link = {executor.submit(process_page, page): page for page in pages}

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
    domain = "https://www.nature.com"
    url = domain + "/nchem/research-articles?searchType=journalSearch&sort=PubDate&page=1"
    page = url
    subject = "chem"
    pages = []

    print("Appending pages...")

    print('#' * 95, end=" ")
    print("")

    while page is not None:
        pages.append(page)
        print("#", end="")
        page = next_page(domain, page)

    print("\n------------------------- FINISHED ADDING PAGES -----------------------------")

    print("Populating:")

    concurrent_populate(domain, pages, 95)

    print("------------------------- FINISHED POPULATING -----------------------------")

    print("Writing:")

    file = open("output/chemistry.out", "w")

    for title in subjects[subject].keys():
        print("#", end="")
        file.write(f"Title: {title}\n")
        file.write(f"{subjects[subject][title]}\n")
        file.write("\n")
        file.write("------------------------------------------------------------------------------")
        file.write("\n\n")

    file.close()

    print("\n--------------------------- FINISHED WRITING -------------------------------")


if __name__ == "__main__":
    main()
