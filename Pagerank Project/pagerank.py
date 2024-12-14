import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    distribution = {}
    links = corpus[page]
    num_pages = len(corpus)

    if links:
        for p in corpus:
            distribution[p] = (1 - damping_factor) / num_pages
        for link in links:
            distribution[link] += damping_factor / len(links)
    else:
        for p in corpus:
            distribution[p] = 1 / num_pages

    return distribution



def sample_pagerank(corpus, damping_factor, n):
    page = random.choice(list(corpus.keys()))
    page_ranks = {p: 0 for p in corpus}

    for _ in range(n):
        page_ranks[page] += 1
        distribution = transition_model(corpus, page, damping_factor)
        page = random.choices(list(distribution.keys()), weights=distribution.values(), k=1)[0]

    page_ranks = {p: rank / n for p, rank in page_ranks.items()}
    return page_ranks



def iterate_pagerank(corpus, damping_factor, epsilon=0.001):
    num_pages = len(corpus)
    page_ranks = {page: 1 / num_pages for page in corpus}
    new_ranks = page_ranks.copy()

    while True:
        for page in corpus:
            rank = (1 - damping_factor) / num_pages
            for p in corpus:
                if page in corpus[p]:
                    rank += damping_factor * page_ranks[p] / len(corpus[p])
                elif not corpus[p]:
                    rank += damping_factor * page_ranks[p] / num_pages
            new_ranks[page] = rank

        if all(abs(new_ranks[page] - page_ranks[page]) < epsilon for page in corpus):
            break

        page_ranks = new_ranks.copy()

    return page_ranks



if __name__ == "__main__":
    main()
