def skipNullResult(obj, path, attr):
    """跳过空值报错"""
    try:
        if attr == '':
            return obj.find(path, first=True).text
        else:
            return obj.find(path, first=True).attrs[attr]
    except:
        return ''
