from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import gzip
from urllib.request import urlopen
import uuid

def read_ngram_files(filenames):
    for fname in filenames:
        print('loading file {}'.format(fname))
        gzresp = urlopen(fname)
        unique_filename = "/tmp/" + str(uuid.uuid4())
        tempgz = open(unique_filename, "wb")
        tempgz.write(gzresp.read())
        tempgz.close()

        with gzip.open(unique_filename, 'rt') as f:
            '''
            fieldnames=['ngram', 'year', 'match_count', 'volume_count']
            reader = csv.DictReader(f, delimiter='\t', fieldnames=fieldnames)
            for row in reader:
                yield row
            '''
            for line in f:
                row = line.strip().split('\t')
                yield row


def get_fiction_filenames():
    url = "http://storage.googleapis.com/books/ngrams/books/datasetsv2.html"
    page = urlopen(url)
    soup = BeautifulSoup(page, "html.parser")

    for h1 in soup.findAll('h1'):
        if h1.text == "English Fiction":
            for x in h1.find_next_siblings():
                if x.b:
                    text = x.b.find(text=True, recursive=False)
                    if text == '5-grams':
                        urls = []
                        for a in x.find_all('a', href=True):
                            if a.text.isalpha():
                                urls.append(a['href'])
                        return(urls)


if __name__ == "__main__":
    urls = get_fiction_filenames()
    print(urls)
    for i,r in enumerate(read_ngram_files(urls)):
        print(r)
        if i > 10000:
            break

