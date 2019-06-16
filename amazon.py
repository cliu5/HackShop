from bs4 import BeautifulSoup
import ssl
import urllib.request


def get_data(keyphrase, url='https://www.amazon.com/s?k='):

    key_words = keyphrase.split(' ')
    for i in range(len(key_words)):
        url += key_words[i] + '+'
    context = ssl._create_unverified_context()
    page = urllib.request.urlopen(url,context=context)

    soup = BeautifulSoup(page, 'html.parser')

    titles = soup.find_all('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    titles = [i.text.strip() for i in titles]

    imgs = soup.find_all('img', attrs={'class': 's-image'})
    imgs = [i['src'] for i in imgs]

    return [(titles[i], imgs[i]) for i in range(len(titles))]
print(get_data('airpods'))
