from requests_html import HTMLSession
from mongoData.SaveData import saveData
from comm.SkipNullResult import skipNullResult


Session = HTMLSession()


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
        # print()
        datadict = {    
            'name': skipNullResult(item, 'a:nth-child(3)>h2', ''),
            'brand': skipNullResult(item, 'a:nth-child(2)>h2', ''),
            'specification': item.find('a:nth-child(3)>h2', first=True).search('({})')[0],
            'HKDPrice': skipNullResult(item, '.fon-price>b', '') + '0',
            'image': 'https:' + item.find('img', first=True).search('https:{}.jpg')[0] + '.jpg',
            'type': type,
            'shareUrl': 'https://hongkong.sasa.com' + skipNullResult(item, 'a:nth-child(3)', 'href'),
            'source':'莎莎网'
        }
        print(datadict)
    nextpage = res.find('li>a:contains(">")', first=True)
    if nextpage:
        getProductList(nextpage.attrs['href'], type)


if __name__ == "__main__":
    getProductType('https://hongkong.sasa.com/SasaWeb/sch/sasa/home.jsp?cm_re=top_logo')