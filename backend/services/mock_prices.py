# Mock 比价数据
# services/mock_prices.py
# Mock 商品数据及价格搜索服务，用于 MVP 阶段模拟比价功能

# 定义模拟商品库，每个商品包含名称、平台、价格和跳转链接
MOCK_PRODUCTS = [
    {
        "name": "必胜客 超级至尊披萨 9寸",
        "platform": "美团外卖",
        "price": 89.0,
        "url": "https://meituan.com/pizza/1"
    },
    {
        "name": "达美乐 照烧牛肉披萨 10寸",
        "platform": "饿了么",
        "price": 79.0,
        "url": "https://ele.me/pizza/2"
    },
    {
        "name": "山姆 Member's Mark 芝士披萨",
        "platform": "山姆极速达",
        "price": 65.8,
        "url": "https://samclub.com/pizza/3"
    },
    {
        "name": "棒约翰 意式肉肠披萨",
        "platform": "京东到家",
        "price": 99.0,
        "url": "https://jddj.com/pizza/4"
    },
    {
        "name": "索尼 WH-1000XM5 降噪耳机",
        "platform": "京东自营",
        "price": 1999.0,
        "url": "https://jd.com/sony-xm5"
    },
    {
        "name": "Bose QuietComfort 45 耳机",
        "platform": "天猫旗舰店",
        "price": 1899.0,
        "url": "https://tmall.com/bose-qc45"
    },
    {
        "name": "小米 Buds 4 Pro 耳机",
        "platform": "小米商城",
        "price": 699.0,
        "url": "https://mi.com/buds4pro"
    },
    {
        "name": "挪客 云尚 双人自动帐篷",
        "platform": "天猫户外专营",
        "price": 369.0,
        "url": "https://tmall.com/naturehike-tent"
    },
    {
        "name": "牧高笛 冷山 户外双人帐篷",
        "platform": "京东运动",
        "price": 459.0,
        "url": "https://jd.com/mobi-garden-tent"
    },
    {
        "name": "探路者 轻量化双人帐篷",
        "platform": "拼多多百亿补贴",
        "price": 289.0,
        "url": "https://pdd.com/toread-tent"
    },
]


# 兜底商品（关键词无匹配时返回）
EMPTY_PLACEHOLDER = [
    {
        "name": "暂无相关商品，试试“耳机”“披萨”“帐篷”吧～",
        "platform": "系统提示",
        "price": 0,
        "url": "#"
    }
]



def search_products_by_keywords(keywords: list) -> list:
    """
    根据关键词列表在 Mock 商品库中进行模糊搜索。
    返回匹配的商品列表，按价格升序排列，最多返回 5 条。
    """
    if not keywords or not isinstance(keywords, list):                     # 如果关键词列表为空，直接返回空列表
        return EMPTY_PLACEHOLDER

    results = []                         # 存储匹配到的商品
    lower_keywords = [kw.lower().strip() for kw in keywords]  # 将所有关键词转为小写，便于忽略大小写匹配

    for item in MOCK_PRODUCTS:
        name_lower = item["name"].lower()  # 商品名称转小写
        # 检查商品名称是否包含任一关键词（模糊匹配）
        if any(kw in name_lower for kw in lower_keywords):
            results.append(item)

    # 使用字典对结果去重（以 (平台, 名称) 为唯一标识），防止同一商品被多次添加
    seen = set()
    deduped_results = []
    for item in results:
        key = (item["platform"], item["name"])
        if key not in seen:
            seen.add(key)
            deduped_results.append(item)

    # 无结果兜底
    if not deduped_results:
        return EMPTY_PLACEHOLDER

    # 按价格升序排序
    deduped_results.sort(key=lambda x: x["price"])

    # 返回前 5 条，避免数据过多
    return deduped_results[:5]


# 保留旧的函数名以兼容已有代码（如 prices.py 中可能用到）
def get_mock_prices(keyword: str) -> list:
    """兼容旧接口：根据单个关键词精确匹配（已弃用，建议使用 search_products_by_keywords）"""
    # 直接调用新函数，传入包含单个关键词的列表
    if not keyword:
        return EMPTY_PLACEHOLDER
    return search_products_by_keywords([keyword])