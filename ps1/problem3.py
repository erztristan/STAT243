import subprocess
from bs4 import BeautifulSoup
import pandas as pd


def download_html_with_curl(url, savepath):
    """
    This function determines the HTML content for a given URL and saves under the given path

    Args:
        url: Valid url as string
        savepath: Valid savepath for the html-file

    Returns:
        Returns the HTML content
    """
    result = subprocess.run(["curl", "-L", url], capture_output=True)
    html_content = result.stdout.decode("utf-8", errors="replace")

    with open(savepath, "w", encoding="utf-8") as file:
        file.write(html_content)
    return html_content


# Defining the variables
id = "yxUduqMAAAAJ"
url = f"https://scholar.google.com/citations?user={id}&hl=en"
savepath = f"{id}.html"

# Calls the function and receives the HTML content back
html_content = download_html_with_curl(url, savepath)


def parse_citation_info(html_content=None, path=None):
    """
    This function receives the HTML content either as a memory path or directly as input and converts it into a Pandas dataframe

    Args:
        html_content: Valid html content
        path: Valid path to a html file

    Returns:
        Returns the relevant html content in a pandas dataframe
    """

    # If the content is not specified directly, the content is determined from the path
    if html_content is None:
        with open(path, "r", encoding="utf-8") as file:
            html_content = file.read()

    # Parsing the HTML content and find all rows with content
    soup = BeautifulSoup(html_content, "html.parser")
    rows = soup.find_all("tr", class_="gsc_a_tr")

    # Definition of all relevant information
    titles, authors, journals, years, citations = [], [], [], [], []

    # Extraction of relevant information from the individual content rows
    for row in rows:
        # Extract titel
        title = row.find("a", class_="gsc_a_at").text
        titles.append(title)

        # Extract authors and journal
        author_journal_info = row.find("div", class_="gs_gray").text
        authors.append(author_journal_info.split(" - ")[0])
        journals.append(
            author_journal_info.split(" - ")[1] if " - " in author_journal_info else ""
        )

        # Extract year
        year = row.find("span", class_="gsc_a_hc").text
        years.append(year)

        # Extract citation count
        citation = row.find("a", class_="gsc_a_ac").text
        citations.append(citation)

    # Create Pandas Dataframe from the single arrays
    df = pd.DataFrame(
        {
            "Title": titles,
            "Authors": authors,
            "Journal": journals,
            "Year": years,
            "Citations": citations,
        }
    )

    return df


# Call of the function with the html_content
df = parse_citation_info(html_content=html_content)

# Call of the function with the savepath
df = parse_citation_info(path=savepath)
print(df)
