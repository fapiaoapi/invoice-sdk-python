
from decimal import Decimal, ROUND_HALF_UP, getcontext
import json
from tax.invoice.utils.other import calculate_tax

getcontext().prec = 28


def to_decimal(value):
    return value if isinstance(value, Decimal) else Decimal(str(value))


def quantize(value, scale):
    return to_decimal(value).quantize(Decimal("0." + "0" * scale), rounding=ROUND_HALF_UP)


def bcadd(a, b, scale=2):
    return quantize(to_decimal(a) + to_decimal(b), scale)


def bcsub(a, b, scale=2):
    return quantize(to_decimal(a) - to_decimal(b), scale)


def bcmul(a, b, scale=2):
    return quantize(to_decimal(a) * to_decimal(b), scale)


def bcdiv(a, b, scale=2):
    return quantize(to_decimal(a) / to_decimal(b), scale)


def normalize_totals(data):
    for key in ("hjje", "hjse", "jshj"):
        if isinstance(data.get(key), Decimal):
            data[key] = float(data[key])
    return data


"""
/**
 * 含税金额计算示例
 *
 *   不含税单价 = 含税单价/(1+ 税率)  noTaxDj = dj / (1 + sl)
 *   不含税金额 = 不含税单价*数量  noTaxJe = noTaxDj * spsl
 *   含税金额 = 含税单价*数量  je = dj * spsl
 *   税额 = 税额 = 1 / (1 + 税率) * 税率 * 含税金额  se = 1  / (1 + sl) * sl * je
 *    hjse= se1 + se2 + ... + seN
 *    jshj= je1 + je2 + ... + jeN
 *   价税合计 =合计金额+合计税额 jshj = hjje + hjse
 *
 */
"""

"""
/**
 * 含税计算示例1  无价格  无数量
 * @link `https://fa-piao.com/fapiao.html?action=data1&source=github`
 *
 */
"""

hsbz = 1
amount = 200
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))
data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*软件维护服务*接口服务费",
            "spbm": "3040201030000000000",
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}

for item in data["fyxm"]:
    data["jshj"] = bcadd(data["jshj"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["hjje"] = bcsub(data["jshj"], data["hjse"], 2)

data["hjje"] = float(data["hjje"])
data["hjse"] = float(data["hjse"])
data["jshj"] = float(data["jshj"])
print("含税计算示例1  无价格  无数量:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 含税计算示例2  有价格 有数量
 * @link `https://fa-piao.com/fapiao.html?action=data3&source=github`
 *
 */
"""

hsbz = 1
spsl = 1
dj = 2
sl = 0.03

spsl2 = 1
dj2 = 3
sl2 = 0.01

je = bcmul(dj, spsl, 2)
se = calculate_tax(je, sl, bool(hsbz))

je2 = bcmul(dj2, spsl2, 2)
se2 = calculate_tax(je2, sl2, bool(hsbz))
data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*水冰雪*一阶水费",
            "spbm": "1100301030000000000",
            "ggxh": "",
            "dw": "吨",
            "dj": dj,
            "spsl": spsl,
            "je": float(je),
            "sl": sl,
            "se": float(se),
        },
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*水冰雪*二阶水费",
            "spbm": "1100301030000000000",
            "ggxh": "",
            "dw": "吨",
            "dj": dj2,
            "spsl": spsl2,
            "je": float(je2),
            "sl": sl2,
            "se": float(se2),
        },
    ],
}

for item in data["fyxm"]:
    data["jshj"] = bcadd(data["jshj"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["hjje"] = bcsub(data["jshj"], data["hjse"], 2)

data["hjje"] = float(data["hjje"])
data["hjse"] = float(data["hjse"])
data["jshj"] = float(data["jshj"])

print("含税计算示例2  有价格 有数量:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 含税计算示例3  有价格自动算数量  购买猪肉1000元,16.8元/斤
 * @link `https://fa-piao.com/fapiao.html?action=data5&source=github`
 *
 */
"""
hsbz = 1
amount = 1000
dj = 16.8
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))

data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*肉类*猪肉",
            "spbm": "1030107010100000000",
            "ggxh": "",
            "dw": "斤",
            "dj": dj,
            "spsl": float(bcdiv(amount, dj, 13)),
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}
for item in data["fyxm"]:
    data["jshj"] = bcadd(data["jshj"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["hjje"] = bcsub(data["jshj"], data["hjse"], 2)

data["hjje"] = float(data["hjje"])
data["hjse"] = float(data["hjse"])
data["jshj"] = float(data["jshj"])
print("含税计算示例3  有价格自动算数量 购买猪肉1000元,16.8元/斤:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 含税计算示例4  有数量自动算价格  购买接口服务1000元7次
 * @link `https://fa-piao.com/fapiao.html?action=data7&source=github`
 *
 */
"""

hsbz = 1
amount = 1000
spsl = 7
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))

data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*软件维护服务*接口服务费",
            "spbm": "3040201030000000000",
            "ggxh": "",
            "dw": "次",
            "dj": float(bcdiv(amount, spsl, 13)),
            "spsl": spsl,
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}
for item in data["fyxm"]:
    data["jshj"] = bcadd(data["jshj"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["hjje"] = bcsub(data["jshj"], data["hjse"], 2)

data["hjje"] = float(data["hjje"])
data["hjse"] = float(data["hjse"])
data["jshj"] = float(data["jshj"])
print("含税计算示例4  有数量自动算价格 购买接口服务1000元7次:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 不含税计算示例
 *  金额 = 单价 * 数量  je = dj * spsl
 *  税额 = 金额 * 税率  se = je * sl
 *   hjse= se1 + se2 + ... + seN
 *   hjje= je1 + je2 + ... + jeN
 *  价税合计 =合计金额+合计税额 jshj = hjje + hjse
 *
 */
"""

"""
/**
 *
 * 不含税计算示例1 无价格 无数量
 * @link `https://fa-piao.com/fapiao.html?action=data2&source=github`
 */
"""

hsbz = 0
amount = 200
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))
data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*软件维护服务*接口服务费",
            "spbm": "3040201030000000000",
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}

for item in data["fyxm"]:
    data["hjje"] = bcadd(data["hjje"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["jshj"] = bcadd(data["hjje"], data["hjse"], 2)

normalize_totals(data)

print("不含税计算示例1 无价格 无数量:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 *
 * 不含税计算示例2  有价格 有数量
 * @link `https://fa-piao.com/fapiao.html?action=data4&source=github`
 */
"""
# 一阶水费 1吨，单价2元/吨，税率0.03
# 二阶水费 1吨，单价3元/吨，税率0.01
hsbz = 0
spsl = 1
dj = 2
sl = 0.03

spsl2 = 1
dj2 = 3
sl2 = 0.01

je = bcmul(dj, spsl, 2)
se = calculate_tax(je, sl, bool(hsbz))

je2 = bcmul(dj2, spsl2, 2)
se2 = calculate_tax(je2, sl2, bool(hsbz))
data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*水冰雪*一阶水费",
            "spbm": "1100301030000000000",
            "ggxh": "",
            "dw": "吨",
            "dj": dj,
            "spsl": spsl,
            "je": float(je),
            "sl": sl,
            "se": float(se),
        },
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*水冰雪*而阶水费",
            "spbm": "1100301030000000000",
            "ggxh": "",
            "dw": "吨",
            "dj": dj2,
            "spsl": spsl2,
            "je": float(je2),
            "sl": sl2,
            "se": float(se2),
        },
    ],
}

for item in data["fyxm"]:
    data["hjje"] = bcadd(data["hjje"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["jshj"] = bcadd(data["hjje"], data["hjse"], 2)

normalize_totals(data)

print("不含税计算示例2  有价格 有数量:")
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 不含税计算示例3  有价格自动算数量  购买猪肉1000元,16.8元/斤
 * @link `https://fa-piao.com/fapiao.html?action=data6&source=github`
 *
 */
"""
hsbz = 0
amount = 1000
dj = 16.8
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))

data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*肉类*猪肉",
            "spbm": "1030107010100000000",
            "ggxh": "",
            "dw": "斤",
            "dj": dj,
            "spsl": float(bcdiv(amount, dj, 13)),
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}
for item in data["fyxm"]:
    data["hjje"] = bcadd(data["hjje"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["jshj"] = bcadd(data["hjje"], data["hjse"], 2)
print("不含税计算示例3  有价格自动算数量 购买猪肉1000元,16.8元/斤:")
normalize_totals(data)
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 不含税计算示例4  有数量自动算价格  购买接口服务1000元7次
 *
 * @link `https://fa-piao.com/fapiao.html?action=data8&source=github`
 *
 */
"""

hsbz = 0
amount = 1000
spsl = 7
sl = 0.01
se = calculate_tax(amount, sl, bool(hsbz))

data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*软件维护服务*接口服务费",
            "spbm": "1030107010100000000",
            "ggxh": "",
            "dw": "次",
            "dj": float(bcdiv(amount, spsl, 13)),
            "spsl": spsl,
            "je": float(amount),
            "sl": sl,
            "se": float(se),
        }
    ],
}
for item in data["fyxm"]:
    data["hjje"] = bcadd(data["hjje"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)
data["jshj"] = bcadd(data["hjje"], data["hjse"], 2)
print("不含税计算示例4  有数量自动算价格 购买接口服务1000元7次:")
normalize_totals(data)
print(json.dumps(data, ensure_ascii=False, indent=4))
print("---------------------------------------------")

"""
/**
 * 免税计算示例
 *  金额 = 单价 * 数量  je = dj * spsl
 *  税额 = 0
 *  hjse = se1 + se2 + ... + seN
 *  jshj = je1 + je2 + ... + jeN
 *  价税合计 =合计金额+合计税额 jshj = hjje + hjse
 * @link `https://fa-piao.com/fapiao.html?action=data9&source=github`
 */
"""

hsbz = 0
dj = 32263.98
sl = 0
se = 0
data = {
    "hjje": Decimal("0"),
    "hjse": Decimal("0"),
    "jshj": Decimal("0"),
    "fyxm": [
        {
            "fphxz": 0,
            "hsbz": hsbz,
            "spmc": "*经纪代理服务*国际货物运输代理服务",
            "spbm": "3040802010200000000",
            "ggxh": "",
            "dw": "次",
            "spsl": 1,
            "dj": float(dj),
            "je": float(dj),
            "sl": sl,
            "se": se,
            "yhzcbs": 1,
            "lslbs": 1,
            "zzstsgl": "免税",
        }
    ],
}
for item in data["fyxm"]:
    data["hjje"] = bcadd(data["hjje"], item["je"], 2)
    data["hjse"] = bcadd(data["hjse"], item["se"], 2)

data["jshj"] = bcadd(data["hjje"], data["hjse"], 2)

normalize_totals(data)
print("免税计算示例:" + json.dumps(data, ensure_ascii=False, indent=4))
