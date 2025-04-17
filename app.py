from flask import Flask, render_template, request
import xlrd
from requests import get
from bs4 import BeautifulSoup as bs

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    imgs = []
    names = []
    prices = []
    urls = []
    if request.args.get('s') != None:
        search = request.args.get('s').lower()
        search_url = search.replace(' ', '+')
        data_sp_komp = get(f'https://www.sp-computer.ru/search/?q={search_url}')
        html = bs(data_sp_komp.content, 'html.parser')
        items = html.select(".product-item")
        for item in items:
            try:
                title = item.select('.product-item-title > a')[0].text[5:][:-4].replace('/', ' ')
                price_rub = int(item.select('.product-item-price-container > span')[0].text)
                url = 'https://www.sp-computer.ru' + item.select('.product-item-title > a')[0].get("href")
                img = f"https://www.sp-computer.ru{item.select('.product-item-image-alternative > img')[0].get('data-src')}"
                urls.append(url)
                imgs.append(img)
                names.append(title)
                prices.append(price_rub)

            except:
                pass
        data_dns = xlrd.open_workbook(r"price-spb.xls", ignore_workbook_corruption=True)
        sheet = data_dns.sheet_by_index(4)
        for i in range(95, 8764):
            if search in sheet.cell(i, 1).value.lower():
                if 'Процессор' in sheet.cell(i, 1).value:
                    imgs.append('/static/cpu.png')
                elif 'Видеокарта' in sheet.cell(i, 1).value:
                    imgs.append('/static/viduxa.png')
                elif 'Жесткий' in sheet.cell(i, 1).value:
                    imgs.append('/static/hdd.png')
                elif 'SSD' in sheet.cell(i, 1).value:
                    imgs.append('/static/ssd.png')
                elif 'Материнская' in sheet.cell(i, 1).value:
                    imgs.append('/static/mother.png')
                elif 'Оперативная память' in sheet.cell(i, 1).value:
                    imgs.append('/static/operativka.png')
                elif 'Блок питания' in sheet.cell(i, 1).value:
                    imgs.append('/static/Block_pitania.png')
                elif 'Кулер' in sheet.cell(i, 1).value:
                    imgs.append('/static/kyler.png')
                else:
                    imgs.append('/static/Data_img/noname.png')

                names.append(sheet.cell(i, 1).value)
                prices.append(sheet.cell(i, 94).value)

    return render_template('index.html', names=names, imgs=imgs, prices=prices, urls=urls)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
