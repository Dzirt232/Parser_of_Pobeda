import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html,'lxml')

    pages = soup.find('ul',class_='Pagination').find_all('li',class_='Pagination-item')[-1].find('a').get('href')
    total_pages = pages.split('/')[3]

    return int(total_pages)

def write_csv(data):
    with open('pobeda.csv','a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['title'],
                          data['price'],
                          data['url']) )


def get_page_data(html):
    soup = BeautifulSoup(html,'lxml')

    ads = soup.find('div',class_ = 'Product-list').find_all('div', attrs={"itemtype": "http://schema.org/Product"})

    for ad in ads:

        name = ad.find('div',class_ = 'Product-item-wrapper').find('div',class_ = 'annotation').find('span',class_ = 'name').text.strip().lower()

        if 'samsung galaxy s10' in name:
            try:
                title = ad.find('div',class_ = 'Product-item-wrapper').find('div',class_ = 'annotation').find('span',class_ = 'name').text.strip()
            except:
                title = ''
            try:
                url = ad.find('div',class_ = 'Product-item-wrapper').find('div',class_ = 'annotation').find('span',class_ = 'name').find('a').get('href')
            except:
                url = ''
            try:
                price = ad.find('div',class_ = 'Product-item-wrapper').find('div',class_ = 'annotation').find('span',class_ = 'price').text[:-1].strip()
            except:
                price = ''

            data = {'title':title,
                    'price':price,
                    'url':url}

            write_csv(data)
        else:
            continue


def main():
    url = 'https://xn--80adxhks.xn---63-5cdesg4ei.xn--p1ai/catalog/search/1/?cg=142&c=5&k=samsung%20galaxy%20s10'
    base_url = 'https://xn--80adxhks.xn---63-5cdesg4ei.xn--p1ai/catalog/search/'
    query_part = '/?cg=142&c=5&k=samsung%20galaxy%20s10'

    total_pages = get_total_pages(get_html(url))

    for i in range(1,total_pages+1):
        url_gen = base_url + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)
        


if __name__ == '__main__':
    main()
