import pymongo
from requests_html import HTMLSession


SESSION = HTMLSession()
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['product']
collection = db['bonjourhk']


def getProductType():
    """获取产品类型"""
    res = SESSION.get('https://www.bonjourhk.com/sc/skincare').html
    for item in res.find('.menu-col>a'):
        getProductList(item.attrs['href'], item.text)


def getProductList(url, type):
    """获取产品列表"""
    res = SESSION.get(url).html
    for item in res.find('.product-layout'):
        datadict = {
            'name': skipNullResult(item, '.item_name>a', ''),
            'brand': skipNullResult(item, '.item_unit', ''),
            'specification': skipNullResult(item, '.product-manufacturer>a', ''),
            'HKDPrice': skipNullResult(item, '.price price', '') + '.00',
            'image': skipNullResult(item, '.image>a>img', 'data-original'),
            'type': type,
            'shareUrl': skipNullResult(item, '.image>a', 'href'),
            'source':'卓悦网'
        }
        saveData(datadict)
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


if __name__ == '__main__':
    getProductType()
