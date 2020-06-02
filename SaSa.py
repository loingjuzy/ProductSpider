import pymongo
from requests_html import HTMLSession


Session = HTMLSession()
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['product']
collection = db['Sasa']


def getProductType(url):
    """获取产品类型"""
    Res = Session.get(url).html
    for item in Res.find('.category_epand_column>h3>a'):
        getProductList('https://hongkong.sasa.com' + item.attrs['href'], item.text)
        break

def getProductList(url, type):
    """获取产品列表"""
    res = Session.get(url).html
    for item in res.find('.box_list>ul>li'):
        # print(item.find('a:nth-child(3)>h2', first=True).text)
        datadict = {
            'name': skipNullResult(item, 'a:nth-child(3)>h2', ''),
            'brand': skipNullResult(item, 'a:nth-child(2)>h2', ''),
            'specification': skipNullResult(item, '.product-manufacturer>a', ''),
            'HKDPrice': skipNullResult(item, '.fon-price>b', '') + '0',
            'image': skipNullResult(item, 'img', 'src'),
            'type': type,
            'shareUrl': 'https://hongkong.sasa.com' + skipNullResult(item, 'a:nth-child(3)', 'href'),
            'source':'莎莎网'
        }
        print(datadict)
    nextpage = res.find('li>a:contains(">")', first=True)
    if nextpage:
        getProductList(nextpage.attrs['href'], type)


def skipNullResult(obj, path, attr):
    try:
        if attr == '':
            return obj.find(path, first=True).text
        else:
            return obj.find(path, first=True).attrs[attr]
    except:
        return ''


def saveData(datadict):
    result = collection.insert(datadict)
    print(result)


if __name__ == "__main__":
    getProductType('https://hongkong.sasa.com/SasaWeb/sch/sasa/home.jsp?cm_re=top_logo')