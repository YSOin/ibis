import requests
from bs4 import BeautifulSoup as bs
import csv
from multiprocessing import Pool
import codecs


headers = {'user-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}


def soup_item(url):
    page_html = requests.get(url, headers = headers)
    soup = bs(page_html.text, 'lxml')
    return soup

def get_all_pages(url):
    pages_count = soup_item(url).find_all("a", attrs={'class':"page_num"})[-1].get_text()
    return int(pages_count)


def get_urls(url):
    main_url = 'https://ibis.net.ua'
    pages = soup_item(url).find_all("a", attrs={'class':"pb_product_name"})
    all_pages_url = [main_url+i.get("href") for i in pages]
    return all_pages_url

def generate_pages_urls(url):
    pages_count = get_all_pages(url)
    pages_list = []
    for i in range(pages_count+1):
        get_page_param =  i*20
        pages_list.append(f'{url}offset{get_page_param}')
    return pages_list

def get_content(url):
    soup = soup_item(url)
    prod_extra_table = soup.find('table', class_='prod_extra_table')
    rows = prod_extra_table.find_all("tr")
    d = {row.get_text(strip=True).split(':')[0] : row.get_text(strip=True).split(':')[1]  for row in rows}
    pb_stock = soup.find("span", class_='red')
    product_code = soup.find('div', class_='product_code').get_text(strip=True).split(':')[1] #Получаем код товара
    price = soup.find('div', class_='pb_price').get_text().split(' ')[0].strip()
    product_h1 = soup.find('h1', class_='product_name').get_text() # название товара
    try:
        imgwrp = url[0:19] + soup.find('a', class_='imgwrp jqzoom').get('href')
    except AttributeError:
        imgwrp = 'Нет изображения'
    try:
        maxreadmoar_wrp = soup.find("span", attrs={'itemprop':"description"}).get_text(strip=True) # описание товара
    except AttributeError:
        maxreadmoar_wrp = f'Не найден текст описания для урла {url}'
    if not pb_stock:
        pb_stock = '+'
    else:
        pb_stock = '-'
    category = d['Підкатегорія']
    manufacturer = d['Виробник']
    try:
        c_manufacturer = d['Країна походження']
    except KeyError:
        c_manufacturer = '-'
    return {
            'img':imgwrp, 'stock':pb_stock, 'manufacturer':c_manufacturer, 'description':maxreadmoar_wrp, 
            'category':category, 'c_manufacturer':manufacturer, 'h1':product_h1, 'price':price,
            'product_code':product_code, 'ibis_url':url #'characteristics':d,
            }


def writeHeader():
    with codecs.open ('ibis-fishing.csv', 'a', 'utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow((
                        'Код_товара','Название_позиции', 'Поисковые_запросы','Описание',
                        'Тип_товара', 'Цена', 'Валюта', 'Единица_измерения', 'Минимальный_объем_заказа',
                        'Оптовая_цена', 'Минимальный_заказ_опт', 'Ссылка_изображения', 'Наличие',
                        'Номер_группы', 'Название_группы', 'Адрес_подраздела', 'Возможность_поставки',
                        'Срок_поставки', 'Способ_упаковки', 'Уникальный_идентификатор', 'Идентификатор_товара',
                        'Идентификатор_подраздела', 'Идентификатор_группы', 'Производитель', 'Страна_производитель',
                        'Скидка', 'ID_группы_разновидностей', 'Личные_заметки', 'Продукт_на_сайте',
                        'Cрок действия скидки от', 'Cрок действия скидки до', 'Цена_от', 'Ярлык', 'HTML_заголовок',
                        'HTML_описание', 'HTML_ключевые_слова', 'Вес_г', 'Ширина_м', 'Высота_м', 'Глубина_м',
                        'Код_маркировки_(GTIN)', 'Номер_устройства_(MPN)', 'Ibis_url'#'Харрактеристики',
                        ))

def writer(items):
    with codecs.open('ibis-fishing.csv', 'a', 'utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow([
        items['product_code'], items['h1'], '', items['description'], items['category'], items['price'],
        'uah', '', '', '', '', items['img'], items['stock'], '', '', '', '', '', '', '', '', '', '', items['c_manufacturer'],
        items['manufacturer'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',items['ibis_url'] ]) #, items['characteristics']


def make_all(url):
    urls = get_urls(url)
    for url in urls:
        print(url)
        # try:
        items = get_content(url)
        writer(items)
