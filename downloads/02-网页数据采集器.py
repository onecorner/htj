"""
====================================
 网页数据采集器（通用爬虫框架）
====================================
功能： 从目标网站批量采集公开数据
用法： 修改 TARGET_URL 为目标网站，运行脚本
适用： 商品信息采集、文章采集、公开数据收集

作者： AI编程助手
交付日期： 2024-06-07

客户需求：
  采集某电商网站的商品标题、价格、销量数据
====================================
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ========== 配置区（根据目标网站修改）==========
TARGET_URL = "https://example.com/products"  # 改为你要采集的网址
OUTPUT_FILE = "采集结果.xlsx"
DELAY = 2  # 每次请求间隔（秒），防止被封
# ============================================

def fetch_page(url):
    """获取网页内容"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding  # 自动识别编码
        return resp.text
    except Exception as e:
        print(f"❌ 请求失败: {url} - {e}")
        return None

def parse_products(html):
    """解析网页提取数据——这个函数需要根据目标网站修改"""
    soup = BeautifulSoup(html, 'html.parser')
    products = []

    # ★ 下面的选择器需要根据实际网页结构调整 ★
    items = soup.select('.product-item')  # 商品容器的CSS选择器

    for item in items:
        title_elem = item.select_one('.product-title a')  # 标题选择器
        price_elem = item.select_one('.price')             # 价格选择器

        if title_elem and price_elem:
            products.append({
                '标题': title_elem.get_text(strip=True),
                '链接': title_elem.get('href', ''),
                '价格': price_elem.get_text(strip=True),
            })

    return products

def main():
    print(f"🔍 开始采集: {TARGET_URL}")
    print(f"⏱️  请求间隔: {DELAY}秒")
    print("-" * 40)

    all_products = []

    # 采集第一页
    html = fetch_page(TARGET_URL)
    if html:
        products = parse_products(html)
        all_products.extend(products)
        print(f"  第1页: 采集到 {len(products)} 条数据")

    # ★ 如果有分页，在这里循环采集后面页面 ★
    # for page in range(2, 11):
    #     time.sleep(DELAY + random.random())
    #     html = fetch_page(f"{TARGET_URL}?page={page}")
    #     if html:
    #         products = parse_products(html)
    #         all_products.extend(products)
    #         print(f"  第{page}页: 采集到 {len(products)} 条数据")

    # 保存结果
    if all_products:
        df = pd.DataFrame(all_products)
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"\n✅ 采集完成！共 {len(all_products)} 条数据")
        print(f"📁 保存至: {OUTPUT_FILE}")
    else:
        print("\n❌ 未采集到数据，请检查网页选择器")

if __name__ == "__main__":
    main()
