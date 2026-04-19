# Mock 比价数据
# services/mock_prices.py
# Mock 商品数据及价格搜索服务，用于 MVP 阶段模拟比价功能

# 定义模拟商品库，每个商品包含名称、平台、价格和跳转链接
# services/mock_prices.py
# 广东医科大学校园周边外卖 Mock 数据（仅美团、饿了么平台）
# 数据特点：同一店铺同一商品在不同平台有独立价格条目，方便比价

MOCK_PRODUCTS = [
    # ---------- 披萨类 ----------
    {
        "shop_name": "尊宝比萨(广医店)",
        "item_name": "奥尔良烤鸡披萨 9寸",
        "location": "校外",
        "platform": "美团",
        "price": 39.9,
        "deeplink": "meituan://waimai/merchant/10001?goods=001"
    },
    {
        "shop_name": "尊宝比萨(广医店)",
        "item_name": "奥尔良烤鸡披萨 9寸",
        "location": "校外",
        "platform": "饿了么",
        "price": 42.0,
        "deeplink": "eleme://shop/20001?goods=001"
    },
    {
        "shop_name": "必胜客(东城万达店)",
        "item_name": "超级至尊披萨 10寸",
        "location": "校外",
        "platform": "美团",
        "price": 79.0,
        "deeplink": "meituan://waimai/merchant/10002?goods=002"
    },
    {
        "shop_name": "必胜客(东城万达店)",
        "item_name": "超级至尊披萨 10寸",
        "location": "校外",
        "platform": "饿了么",
        "price": 82.0,
        "deeplink": "eleme://shop/20002?goods=002"
    },
    {
        "shop_name": "达美乐比萨(莞城店)",
        "item_name": "照烧风味牛肉披萨 9寸",
        "location": "校外",
        "platform": "美团",
        "price": 59.0,
        "deeplink": "meituan://waimai/merchant/10003?goods=003"
    },
    {
        "shop_name": "达美乐比萨(莞城店)",
        "item_name": "照烧风味牛肉披萨 9寸",
        "location": "校外",
        "platform": "饿了么",
        "price": 62.0,
        "deeplink": "eleme://shop/20003?goods=003"
    },

    # ---------- 麻辣烫 / 香锅 ----------
    {
        "shop_name": "广医二饭麻辣香锅",
        "item_name": "自选麻辣烫单人套餐",
        "location": "校内",
        "platform": "美团",
        "price": 18.9,
        "deeplink": "meituan://waimai/merchant/10004?goods=004"
    },
    {
        "shop_name": "广医二饭麻辣香锅",
        "item_name": "自选麻辣烫单人套餐",
        "location": "校内",
        "platform": "饿了么",
        "price": 19.5,
        "deeplink": "eleme://shop/20004?goods=004"
    },
    {
        "shop_name": "杨国福麻辣烫(广医后街店)",
        "item_name": "招牌骨汤麻辣烫",
        "location": "校外",
        "platform": "美团",
        "price": 25.8,
        "deeplink": "meituan://waimai/merchant/10005?goods=005"
    },
    {
        "shop_name": "杨国福麻辣烫(广医后街店)",
        "item_name": "招牌骨汤麻辣烫",
        "location": "校外",
        "platform": "饿了么",
        "price": 27.5,
        "deeplink": "eleme://shop/20005?goods=005"
    },
    {
        "shop_name": "张亮麻辣烫(广医店)",
        "item_name": "番茄麻辣烫单人餐",
        "location": "校外",
        "platform": "美团",
        "price": 26.9,
        "deeplink": "meituan://waimai/merchant/10006?goods=006"
    },
    {
        "shop_name": "张亮麻辣烫(广医店)",
        "item_name": "番茄麻辣烫单人餐",
        "location": "校外",
        "platform": "饿了么",
        "price": 28.0,
        "deeplink": "eleme://shop/20006?goods=006"
    },

    # ---------- 奶茶果茶 ----------
    {
        "shop_name": "喜茶(广医店)",
        "item_name": "多肉葡萄(首创)",
        "location": "校内",
        "platform": "美团",
        "price": 19.0,
        "deeplink": "meituan://waimai/merchant/10007?goods=007"
    },
    {
        "shop_name": "喜茶(广医店)",
        "item_name": "多肉葡萄(首创)",
        "location": "校内",
        "platform": "饿了么",
        "price": 20.0,
        "deeplink": "eleme://shop/20007?goods=007"
    },
    {
        "shop_name": "瑞幸咖啡(广医图书馆店)",
        "item_name": "生椰拿铁",
        "location": "校内",
        "platform": "美团",
        "price": 13.5,
        "deeplink": "meituan://waimai/merchant/10008?goods=008"
    },
    {
        "shop_name": "瑞幸咖啡(广医图书馆店)",
        "item_name": "生椰拿铁",
        "location": "校内",
        "platform": "饿了么",
        "price": 14.5,
        "deeplink": "eleme://shop/20008?goods=008"
    },
    {
        "shop_name": "茶百道(广医后街店)",
        "item_name": "茉莉奶绿",
        "location": "校外",
        "platform": "美团",
        "price": 12.0,
        "deeplink": "meituan://waimai/merchant/10009?goods=009"
    },
    {
        "shop_name": "茶百道(广医后街店)",
        "item_name": "茉莉奶绿",
        "location": "校外",
        "platform": "饿了么",
        "price": 12.5,
        "deeplink": "eleme://shop/20009?goods=009"
    },

    # ---------- 中式快餐 ----------
    {
        "shop_name": "真功夫(广医店)",
        "item_name": "香菇鸡腿肉饭套餐",
        "location": "校内",
        "platform": "美团",
        "price": 29.9,
        "deeplink": "meituan://waimai/merchant/10010?goods=010"
    },
    {
        "shop_name": "真功夫(广医店)",
        "item_name": "香菇鸡腿肉饭套餐",
        "location": "校内",
        "platform": "饿了么",
        "price": 32.0,
        "deeplink": "eleme://shop/20010?goods=010"
    },
    {
        "shop_name": "大家乐(东城店)",
        "item_name": "一哥焗猪扒饭",
        "location": "校外",
        "platform": "美团",
        "price": 45.0,
        "deeplink": "meituan://waimai/merchant/10011?goods=011"
    },
    {
        "shop_name": "大家乐(东城店)",
        "item_name": "一哥焗猪扒饭",
        "location": "校外",
        "platform": "饿了么",
        "price": 48.0,
        "deeplink": "eleme://shop/20011?goods=011"
    },

    # ---------- 炸鸡汉堡 ----------
    {
        "shop_name": "麦当劳(广医店)",
        "item_name": "麦辣鸡腿堡套餐",
        "location": "校内",
        "platform": "美团",
        "price": 28.0,
        "deeplink": "meituan://waimai/merchant/10012?goods=012"
    },
    {
        "shop_name": "麦当劳(广医店)",
        "item_name": "麦辣鸡腿堡套餐",
        "location": "校内",
        "platform": "饿了么",
        "price": 29.5,
        "deeplink": "eleme://shop/20012?goods=012"
    },
    {
        "shop_name": "肯德基(东城万达店)",
        "item_name": "吮指原味鸡套餐",
        "location": "校外",
        "platform": "美团",
        "price": 38.5,
        "deeplink": "meituan://waimai/merchant/10013?goods=013"
    },
    {
        "shop_name": "肯德基(东城万达店)",
        "item_name": "吮指原味鸡套餐",
        "location": "校外",
        "platform": "饿了么",
        "price": 40.0,
        "deeplink": "eleme://shop/20013?goods=013"
    },
    {
        "shop_name": "华莱士(广医后街店)",
        "item_name": "香辣鸡腿堡+可乐",
        "location": "校外",
        "platform": "美团",
        "price": 15.9,
        "deeplink": "meituan://waimai/merchant/10014?goods=014"
    },
    {
        "shop_name": "华莱士(广医后街店)",
        "item_name": "香辣鸡腿堡+可乐",
        "location": "校外",
        "platform": "饿了么",
        "price": 16.5,
        "deeplink": "eleme://shop/20014?goods=014"
    },
]

# ---------- 搜索函数（适配新数据结构）----------
def search_products_by_keywords(keywords: list) -> list:
    """根据关键词模糊搜索，返回聚合后的商品组（同一商品不同平台价格）"""
    if not keywords or not isinstance(keywords, list):
        return []

    lower_kws = [kw.lower().strip() for kw in keywords]
    matched = []

    for item in MOCK_PRODUCTS:
        name_lower = item["item_name"].lower()
        if any(kw in name_lower for kw in lower_kws):
            matched.append(item)

    # 按 (shop_name, item_name) 聚合
    groups = {}
    for item in matched:
        key = (item["shop_name"], item["item_name"])
        if key not in groups:
            groups[key] = {
                "shop_name": item["shop_name"],
                "item_name": item["item_name"],
                "location": item["location"],
                "platforms": []
            }
        groups[key]["platforms"].append({
            "platform": item["platform"],
            "price": item["price"],
            "deeplink": item["deeplink"]
        })

    result_groups = list(groups.values())

    # 对每个 group 内的 platform 按价格排序，并记录最低价平台
    for g in result_groups:
        g["platforms"].sort(key=lambda x: x["price"])
        g["lowest_price"] = g["platforms"][0]["price"]
        g["lowest_platform"] = g["platforms"][0]["platform"]

    # 按最低价全局排序
    result_groups.sort(key=lambda x: x["lowest_price"])

    return result_groups[:8]  # 返回前8组

# 兼容旧接口
def get_mock_prices(keyword: str) -> list:
    if not keyword:
        return []
    groups = search_products_by_keywords([keyword])
    # 兼容旧格式：展开为扁平列表
    flat = []
    for g in groups:
        for p in g["platforms"]:
            flat.append({
                "name": f"{g['shop_name']} {g['item_name']}",
                "platform": p["platform"],
                "price": p["price"],
                "url": p["deeplink"]
            })
    return flat