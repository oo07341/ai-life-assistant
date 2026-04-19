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
        "platform": "淘宝闪购",
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
        "platform": "淘宝闪购",
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
    """根据关键词模糊搜索，返回前端期望的扁平商品列表"""
    if not keywords or not isinstance(keywords, list):
        return []

    lower_kws = [kw.lower().strip() for kw in keywords]
    matched = []

    for item in MOCK_PRODUCTS:
        name_lower = item["item_name"].lower()
        if any(kw in name_lower for kw in lower_kws):
            matched.append(item)

    # 按 (shop_name, item_name) 聚合，找出每个商品的最低价格
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

    # 转换为前端期望的扁平格式
    import random
    flat_products = []
    product_id = 1
    
    for group in result_groups[:8]:  # 只返回前8个商品
        # 为每个平台创建一个独立的商品条目
        for i, platform_info in enumerate(group["platforms"]):
            price = platform_info["price"]
            original_price = round(price * random.uniform(1.1, 1.3), 1)  # 模拟原价
            discount = round(price / original_price, 2)  # 计算折扣
            
            # 生成随机评分和配送时间
            rating = round(random.uniform(4.0, 5.0), 1)
            delivery_times = ["20-30分钟", "30-40分钟", "40-50分钟", "50-60分钟"]
            delivery_time = random.choice(delivery_times)
            
            # 判断是否是最佳性价比（同一商品中价格最低的平台）
            is_best_value = (i == 0)  # 第一个平台是最低价的
            
            product = {
                "id": product_id,
                "name": f"{group['shop_name']} {group['item_name']}",
                "platform": platform_info["platform"],
                "price": price,
                "originalPrice": original_price,
                "discount": discount,
                "shopName": group["shop_name"],
                "rating": rating,
                "deliveryTime": delivery_time,
                "description": f"{group['item_name']}，{group['location']}，{platform_info['platform']}专享",
                "isBestValue": is_best_value,
                "url": platform_info["deeplink"]
            }
            flat_products.append(product)
            product_id += 1

    return flat_products

# 兼容旧接口
def get_mock_prices(keyword: str) -> list:
    """兼容旧接口，返回扁平商品列表"""
    if not keyword:
        return []
    # 直接使用新的搜索函数，它已经返回扁平格式
    return search_products_by_keywords([keyword])
