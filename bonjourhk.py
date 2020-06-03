from requests_html import HTMLSession
from mongoData.SaveData import saveData
from comm.SkipNullResult import skipNullResult


SESSION = HTMLSession()


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
        saveData(datadict, 'product', 'bonjourhk')
    nextpage = res.find('li>a:contains(">")', first=True)
    if nextpage:
        getProductList(nextpage.attrs['href'], type)


if __name__ == '__main__':
    getProductType()
