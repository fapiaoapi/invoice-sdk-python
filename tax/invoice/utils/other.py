

def calculate_tax(amount, tax_rate, is_include_tax=False, scale=2):
    """
    计算税额
    
    Args:
        amount (float|Decimal): 金额
        tax_rate (float|Decimal): 税率
        is_include_tax (bool): 是否含税，默认为False
        scale (int): 小数位数，默认为2
    Returns:
        Decimal: 税额（保留指定位小数）
    """
    # 新增 Decimal 计算逻辑
    from decimal import Decimal, getcontext, ROUND_HALF_UP
    getcontext().rounding = ROUND_HALF_UP  # 添加银行家舍入法
    getcontext().prec = 28  # 设置更高的精度以确保计算准确性

    # 替换原有的 float 转换
    amount = Decimal(str(amount)) if not isinstance(amount, Decimal) else amount
    tax_rate = Decimal(str(tax_rate)) if not isinstance(tax_rate, Decimal) else tax_rate

    if is_include_tax:
        # 旧 税额 = 含税金额 ÷ (1 + 税率) × 税率
        # tax = (amount * tax_rate) / (Decimal('1') + tax_rate)

        # 新 含税计算：税额 = 1 / (1 + 税率) * 税率 * 含税金额
        tax = Decimal('1') / (Decimal('1') + tax_rate) * tax_rate * amount
    else:
        # 不含税计算
        tax = amount * tax_rate
    
    # 根据scale参数设置小数位数
    return tax.quantize(Decimal('0.' + '0' * scale))




