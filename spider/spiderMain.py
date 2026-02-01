import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import os
import random
from DrissionPage import ChromiumPage
import base64
import json
from DrissionPage.common import Actions

# 多个User-Agent列表，随机选择
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
]

def get_random_headers():
    """生成随机请求头"""
    user_agent = random.choice(USER_AGENTS)

    # 根据User-Agent判断浏览器类型
    if "Chrome" in user_agent:
        sec_ch_ua = '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"'
    elif "Firefox" in user_agent:
        sec_ch_ua = None
    elif "Edg" in user_agent:
        sec_ch_ua = '"Chromium";v="143", "Microsoft Edge";v="143", "Not A(Brand";v="24"'
    else:
        sec_ch_ua = '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://sz.lianjia.com/zufang/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": user_agent,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"' if "Windows" in user_agent else '"macOS"'
    }

    # 添加Chrome特有的请求头
    if sec_ch_ua:
        headers["sec-ch-ua"] = sec_ch_ua
        headers["Sec-Fetch-Dest"] = "document"
        headers["Sec-Fetch-Mode"] = "navigate"
        headers["Sec-Fetch-Site"] = random.choice(["same-origin", "none"])
        headers["Sec-Fetch-User"] = "?1"

    return headers
cookies = {
    "lianjia_ssid": "2fd6683d-f7a5-447c-920f-678c3ae23485",
    "lianjia_uuid": "6b8bab0d-f3f8-4dd8-925e-7cdb79e291c2",
    "b-user-id": "2cc0e19f-6c3b-cc0b-07b7-1a9af7791bd2",
    "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1768485090",
    "HMACCOUNT": "E3F84C3DA3E43C50",
    "_jzqc": "1",
    "_jzqckmp": "1",
    "_qzja": "1.1793775574.1768485089572.1768485089572.1768485089572.1768485089572.1768485089572.0.0.0.1.1",
    "_qzjc": "1",
    "_qzjto": "1.1.0",
    "sajssdk_2015_cross_new_user": "1",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%2219bc1ecf13c14d3-03245d5635afc08-26061a51-921600-19bc1ecf13d2191%22%2C%22%24device_id%22%3A%2219bc1ecf13c14d3-03245d5635afc08-26061a51-921600-19bc1ecf13d2191%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
    "_ga": "GA1.2.1627088792.1768485101",
    "_gid": "GA1.2.2021293092.1768485101",
    "_ga_C4R21H79WC": "GS2.2.s1768485101$o1$g0$t1768485101$j60$l0$h0",
    "GUARANTEE_POPUP_SHOW": "true",
    "GUARANTEE_BANNER_SHOW": "true",
    "crosSdkDT2019DeviceId": "mqpoir-1m89vp-mups4f7rniuolk5-3fgizpnxz",
    "login_ucid": "2000000514273381",
    "lianjia_token": "2.00147b3ebb4f59633205d6178af728d4db",
    "lianjia_token_secure": "2.00147b3ebb4f59633205d6178af728d4db",
    "security_ticket": "sw9odpJePgA5z9iqRVFNdfrQmiA+Gf6k3KDe1wwIdg1Bt5zNW2Q7LEO0vbmiWTYRTVykmXYafdxSh1nwh7LYtRywHy5iJR+P0RUD55aVvqvIIvE5kUVUQRPihjlMcxBJ7uxb8ufHwovXe7lNvV9Xtn4frm8spRSlYGMViL2wsP4=",
    "ftkrc_": "7fe172ab-196e-47cd-81af-683f95775918",
    "lfrc_": "8ce670b0-8207-4e29-a885-87a780de9ea2",
    "_jzqa": "1.997503600673443700.1768485090.1768485090.1768488301.2",
    "_ga_KJTRWRHDL1": "GS2.2.s1768488312$o1$g0$t1768488312$j60$l0$h0",
    "_ga_QJN1VP0CMS": "GS2.2.s1768488312$o1$g0$t1768488312$j60$l0$h0",
    "Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e": "1768489192",
    "select_city": "440300",
    "srcid": "eyJ0Ijoie1wiZGF0YVwiOlwiYTFkZDQ2MjE3M2E2MmQ0OWIwYjdlODA5NWI2YjQyY2M4NWYxYTBiNjk3Njg5MGM0NjMwMThlYThkOGY3NjkyMmM5ZmMyM2RlNzBlNTg1NGZmNTJlMGQwZmNkYzA1ZDZmMDNmYWM4OGZhY2Q2ODM3YmRkZWFlY2ZkNTkxMWMxNTdlMjQzZmRmYjJkMzY4YzkzZWJlMmE4Yzk4ZmM4Yjc5ZmUwMTk1YzJkOWU3M2Q2YTNiMDMyOTNhYjQyODhjYTcwYzZmNWUzZGNlZjA2N2UwN2M0NmNiNDYwOTViNzU1NGIzOWRmNGM3M2E3ZDljYmU3YmVlODM3N2RhNTM3NDY3YjJkMTAwNzM2NjcwNDc0YzQxMDEwMjQwMWJkZTc2MGQ5YzIxOTZmN2I0MTc5NjIwMjA1MjEzYTg5ZjFjNzg4MTRcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiNDc0OGUxYWFcIn0iLCJyIjoiaHR0cHM6Ly9zei5saWFuamlhLmNvbS96dWZhbmcvI2NvbnRlbnRMaXN0Iiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0="
}

# 读取城市配置
city_dict = {}
try:
    with open('city.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                code, name = line.strip().split(':', 1)
                city_dict[code] = name
except FileNotFoundError:
    print("未找到city.txt文件，请确保该文件存在于当前目录中")
    city_dict = {'sz': '深圳', 'bj': '北京', 'sh': '上海', 'gz': '广州'}

# 选择要爬取的城市，这里以深圳为例，您可以修改为其他城市代码
selected_city_code = 'sz'  # 可改为 'gz', 'fs', 'dg' 等
selected_city_name = city_dict.get(selected_city_code, '深圳')

city = selected_city_name
csv_file = "house.csv"


def parse_floor_info(floor_text):
    """解析楼层信息，返回楼层类型和楼层数"""
    floor_type = ""
    floor_num = ""

    if floor_text:
        # 提取楼层类型（高楼层、中楼层、低楼层）
        if "高楼层" in floor_text:
            floor_type = "高楼层"
        elif "中楼层" in floor_text:
            floor_type = "中楼层"
        elif "低楼层" in floor_text:
            floor_type = "低楼层"

        # 提取楼层数，例如（41层）
        floor_match = re.search(r'（(\d+)层）', floor_text)
        if floor_match:
            floor_num = floor_match.group(1) + "层"

    return floor_type, floor_num


def extract_rental_type(title_text):
    """从标题中提取租赁方式（整租/合租/不限）"""
    if "整租" in title_text:
        return "整租"
    elif "合租" in title_text:
        return "合租"
    else:
        return "不限"


def extract_building_name(title_text):
    """从标题中提取楼盘名称"""
    # 标题格式：整租·佳华领悦广场 3室2厅 南
    # 提取·或·后面的部分，直到遇到数字（户型）或空格
    # 先尝试匹配·或·后面的内容
    match = re.search(r'[整租合租不限]*[··]?\s*([^0-9]+?)(?:\s+\d+室|\s*$)', title_text)
    if match:
        name = match.group(1).strip()
        # 去除可能的标点符号
        name = re.sub(r'^[·\s]+|[·\s]+$', '', name)
        return name
    return ""


def parse_item(item, city):
    """解析单个房源item，返回字典"""
    data = {
        '城市': city,
        '方式': '',
        '楼盘名称': '',
        '户型': '',
        '城市地区': '',
        '区内地段': '',
        '面积': '',
        '朝向': '',
        '标签': '',
        '价格': '',
        '楼层类型': '',
        '楼层数': '',
        '封面图': '',
        '详情链接': ''
    }

    # 标题信息
    title_elem = item.find('p', class_='content__list--item--title')
    title_text = ""
    if title_elem:
        title_link = title_elem.find('a', class_='twoline')
        if title_link:
            title_text = title_link.get_text(strip=True)
            # 方式（整租/合租）
            data['方式'] = extract_rental_type(title_text)
            # 详情链接
            href = title_link.get('href', '')
            data['详情链接'] = href if href.startswith('http') else f"https://sz.lianjia.com{href}"

    # 描述信息
    des_elem = item.find('p', class_='content__list--item--des')
    if des_elem:
        des_text = des_elem.get_text()

        # 城市地区（坪山区）
        district_link = des_elem.find('a', href=re.compile(r'/zufang/\w+qu/'))
        data['城市地区'] = district_link.get_text(strip=True) if district_link else ""

        # 区内地段（坪山）
        area_links = des_elem.find_all('a', href=re.compile(r'/zufang/\w+/'))
        area_link = None
        for link in area_links:
            if link != district_link and not link.get('href', '').startswith('/zufang/c'):
                area_link = link
                break
        data['区内地段'] = area_link.get_text(strip=True) if area_link else ""

        # 楼盘名称（优先从描述中的链接提取，更准确）
        building_link = des_elem.find('a', href=re.compile(r'/zufang/c\d+/'))
        if building_link:
            building_name = building_link.get('title') or building_link.get_text(strip=True)
            if building_name:
                data['楼盘名称'] = building_name
            else:
                # 如果描述中没有，从标题提取
                data['楼盘名称'] = extract_building_name(title_text)
        else:
            # 如果描述中没有，从标题提取
            data['楼盘名称'] = extract_building_name(title_text)

        # 面积
        area_match = re.search(r'(\d+\.?\d*)\s*㎡', des_text)
        data['面积'] = area_match.group(1) + "㎡" if area_match else ""

        # 朝向
        direction_match = re.search(r'([东西南北]+)', des_text)
        data['朝向'] = direction_match.group(1) if direction_match else ""

        # 户型（3室2厅2卫）
        house_type_match = re.search(r'(\d+室\d+厅\d*卫?)', des_text)
        data['户型'] = house_type_match.group(1) if house_type_match else ""

        # 楼层信息
        floor_span = des_elem.find('span', class_='hide')
        floor_text = floor_span.get_text(strip=True) if floor_span else ""
        floor_type, floor_num = parse_floor_info(floor_text)
        data['楼层类型'] = floor_type
        data['楼层数'] = floor_num

    # 标签
    bottom_elem = item.find('p', class_='content__list--item--bottom')
    tags = []
    if bottom_elem:
        tag_elems = bottom_elem.find_all('i')
        for tag in tag_elems:
            tag_text = tag.get_text(strip=True)
            if tag_text:
                tags.append(tag_text)
    data['标签'] = "、".join(tags) if tags else ""

    # 价格
    price_elem = item.find('span', class_='content__list--item-price')
    if price_elem:
        em_elem = price_elem.find('em')
        if em_elem:
            price = em_elem.get_text(strip=True)
            data['价格'] = price + "元/月"
        else:
            data['价格'] = ""
    else:
        data['价格'] = ""

    # 封面图
    aside_elem = item.find('a', class_='content__list--item--aside')
    if aside_elem:
        img_elem = aside_elem.find('img')
        if img_elem:
            # 优先使用data-src，如果没有则使用src
            img_url = img_elem.get('data-src') or img_elem.get('src', '')
            data['封面图'] = img_url
        else:
            data['封面图'] = ""
    else:
        data['封面图'] = ""

    return data


def scrape_page(page_num, city):
    """爬取指定页码的数据"""
    url = f"https://sz.lianjia.com/zufang/pg{page_num}/"

    try:
        # 每次请求使用随机请求头
        random_headers = get_random_headers()
        response = requests.get(url, headers=random_headers, cookies=cookies, timeout=15)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='content__list--item')

        if not items:
            print(f"第 {page_num} 页没有找到数据，可能已到最后一页")
            return None

        data_list = []
        for item in items:
            data = parse_item(item, city)
            data_list.append(data)

        print(f"第 {page_num} 页成功爬取 {len(data_list)} 条数据")
        return data_list

    except Exception as e:
        print(f"爬取第 {page_num} 页时出错: {str(e)}")
        return []


def save_to_csv(data_list, csv_file):
    """将数据追加保存到CSV文件"""
    if not data_list:
        return

    # CSV字段名
    fieldnames = ['城市', '方式', '楼盘名称', '户型', '城市地区', '区内地段', '面积',
                  '朝向', '标签', '价格', '楼层类型', '楼层数', '封面图', '详情链接']

    # 检查文件是否存在
    file_exists = os.path.exists(csv_file)

    # 追加模式写入CSV
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()

        # 写入数据
        writer.writerows(data_list)

    print(f"已保存 {len(data_list)} 条数据到 {csv_file}")


def scrape_with_browser(city_code='sz', max_pages=10):
    """使用浏览器自动化爬取数据，包含人机验证处理"""
    # 初始化浏览器
    dp = ChromiumPage()
    ac = Actions(dp)
    
    # 访问目标网站
    dp.get(f'https://{city_code}.lianjia.com/zufang/')
    
    # 定义CSV文件头
    fieldnames = ['城市', '方式', '楼盘名称', '户型', '城市地区', '区内地段', '面积',
                  '朝向', '标签', '价格', '楼层类型', '楼层数', '封面图', '详情链接']
    
    total_count = 0
    
    # 打开CSV文件进行追加写入
    with open(csv_file, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 只在文件为空时写入表头
        if csvfile.tell() == 0:
            writer.writeheader()
        
        for page in range(1, max_pages + 1):
            print(f"正在处理第 {page} 页...")
            
            # 检查是否出现验证码
            current_url = dp.url
            if 'captcha' in current_url.lower() or '验证码' in dp.title:
                print("检测到验证码，正在处理...")
                check_result = handle_captcha(dp, ac)
                if check_result != '成功':
                    print("验证码处理失败，停止爬取")
                    break
            
            # 滚动到底部加载更多内容
            dp.scroll.to_bottom()
            time.sleep(2)  # 等待内容加载
            
            # 获取页面内容
            data_list = get_content_from_browser(dp, city_dict.get(city_code, city_code))
            
            if not data_list:
                print(f"第 {page} 页没有获取到数据")
                continue
            
            # 写入CSV
            for data_row in data_list:
                writer.writerow(data_row)
                
            total_count += len(data_list)
            print(f"第 {page} 页成功爬取 {len(data_list)} 条数据")
            
            # 尝试点击下一页
            try:
                next_btn = dp.ele('text=下一页')
                if next_btn:
                    next_btn.click()
                    time.sleep(random.uniform(2, 4))  # 随机延时
                else:
                    print("已到达最后一页")
                    break
            except Exception as e:
                print(f"点击下一页时出错: {str(e)}")
                break
    
    dp.quit()
    print(f"浏览器爬取完成！共爬取 {total_count} 条数据")


def get_content_from_browser(dp, city_name):
    """从浏览器页面获取房源数据"""
    divs = dp.eles('css:.content__list--item')
    
    data_list = []
    for div in divs:
        # 解析单个房源信息
        data = {
            '城市': city_name,
            '方式': '',
            '楼盘名称': '',
            '户型': '',
            '城市地区': '',
            '区内地段': '',
            '面积': '',
            '朝向': '',
            '标签': '',
            '价格': '',
            '楼层类型': '',
            '楼层数': '',
            '封面图': '',
            '详情链接': ''
        }
        
        # 标题信息
        title_element = div.ele('css:.content__list--item--title a')
        title_text = title_element.text if title_element else ''
        if title_text:
            # 方式（整租/合租）
            if "整租" in title_text:
                data['方式'] = "整租"
            elif "合租" in title_text:
                data['方式'] = "合租"
            else:
                data['方式'] = "不限"
            
            # 详情链接
            data['详情链接'] = title_element.attr('href')
            if data['详情链接'] and not data['详情链接'].startswith('http'):
                data['详情链接'] = f"https://{selected_city_code}.lianjia.com{data['详情链接']}"

        # 描述信息
        des_elements = div.eles('css:.content__list--item--des a')
        if len(des_elements) >= 3:
            data['城市地区'] = des_elements[0].text if des_elements[0] else ''  # 城市地区
            data['区内地段'] = des_elements[1].text if des_elements[1] else ''  # 区内地段
            data['楼盘名称'] = des_elements[2].text if des_elements[2] else ''  # 楼盘名称
        else:
            # 备用方案：从文本中解析
            des_elem = div.ele('css:.content__list--item--des')
            if des_elem:
                des_text = des_elem.text
                # 解析城市地区（如坪山区）
                district_match = re.search(r'/zufang/(\w+qu)/', des_text)
                if district_match:
                    data['城市地区'] = district_match.group(1)
                
                # 从标题中提取楼盘名称
                data['楼盘名称'] = extract_building_name(title_text)

        # 从描述文本中提取户型、面积、朝向等信息
        des_elem = div.ele('css:.content__list--item--des')
        if des_elem:
            des_text = des_elem.text
            
            # 面积
            area_match = re.search(r'(\d+\.?\d*)\s*㎡', des_text)
            data['面积'] = area_match.group(1) + "㎡" if area_match else ""

            # 朝向
            direction_match = re.search(r'([东西南北]+)', des_text)
            data['朝向'] = direction_match.group(1) if direction_match else ""

            # 户型（3室2厅2卫）
            house_type_match = re.search(r'(\d+室\d+厅\d*卫?)', des_text)
            data['户型'] = house_type_match.group(1) if house_type_match else ""

            # 楼层信息
            floor_text = div.ele('css:.content__list--item--des .hide').text if div.ele('css:.content__list--item--des .hide') else ""
            floor_type, floor_num = parse_floor_info(floor_text)
            data['楼层类型'] = floor_type
            data['楼层数'] = floor_num

        # 标签
        bottom_elem = div.ele('css:.content__list--item--bottom')
        tags = []
        if bottom_elem:
            tag_elems = bottom_elem.eles('tag:i')
            for tag in tag_elems:
                tag_text = tag.text if tag else ''
                if tag_text:
                    tags.append(tag_text)
        data['标签'] = "、".join(tags) if tags else ""

        # 价格
        price_elem = div.ele('css:.content__list--item-price')
        if price_elem:
            em_elem = price_elem.ele('tag:em')
            if em_elem:
                price = em_elem.text
                data['价格'] = price + "元/月"
            else:
                data['价格'] = ""
        else:
            data['价格'] = ""

        # 封面图
        aside_elem = div.ele('css:.content__list--item--aside')
        if aside_elem:
            img_elem = aside_elem.ele('tag:img')
            if img_elem:
                # 优先使用data-src，如果没有则使用src
                img_url = img_elem.attr('data-src') or img_elem.attr('src', '')
                data['封面图'] = img_url
            else:
                data['封面图'] = ""
        else:
            data['封面图'] = ""
        
        data_list.append(data)
        print(f"解析到房源: {data['楼盘名称']}")
    
    return data_list


def handle_captcha(dp, ac):
    """处理人机验证"""
    try:
        # 查找验证按钮并点击
        captcha_btn = dp.ele('text=点击按钮开始验证')
        if captcha_btn:
            captcha_btn.click()
            time.sleep(3)
            
            # 截取验证码图片
            img_element = dp.ele('css:.geetest_widget')
            if not img_element:
                img_element = dp.ele('css:.geetest_box')
            if img_element:
                img_element.get_screenshot(path='bg.jpg')
                
                # 获取验证码坐标
                coordinates = get_captcha_coordinates()
                if coordinates:
                    coord_list = coordinates.split('|')
                    for coord in coord_list:
                        x, y = map(int, coord.split(','))
                        ac.move_to(img_element, offset_x=x, offset_y=y).click()
                    
                    # 点击提交按钮
                    submit_btn = dp.ele('css:.geetest_submit')
                    if submit_btn:
                        submit_btn.click()
                    
                    # 检查是否通过验证
                    time.sleep(2)
                    if 'captcha' not in dp.url and '验证码' not in dp.title:
                        return '成功'
        
        return '重试'
    except Exception as e:
        print(f"处理验证码时出错: {str(e)}")
        return '重试'


def get_captcha_coordinates():
    """获取验证码坐标 - 这里使用模拟API调用，实际使用时请替换为真实API"""
    # 注意：以下API密钥仅为示例，请替换为您自己的API
    api = 'http://api.jfbym.com/api/YmServer/customApi'
    
    try:
        # 读取验证码图片
        with open('bg.jpg', 'rb') as f:
            img_content = f.read()
        img_base64 = base64.b64encode(img_content).decode()
        
        # 通用图标点选
        data = {
            'image': img_base64,
            'direction': 'top',
            'token': 'kkMm_p6uSEmeP2myODwFaVTStUm_Z-KJK_noz7ND8aQ',
            'type': '30332'
        }
        result = requests.post(url=api, data=data).json()

        # 定制文字点选3
        data_1 = {
            'image': img_base64,
            'extra': 'je4_click',
            'token': 'kkMm_p6uSEmeP2myODwFaVTStUm_Z-KJK_noz7ND8aQ',
            'type': '30112'
        }
        result_1 = requests.post(url=api, data=data_1).json()

        data_2 = {
            'image': img_base64,
            'token': 'kkMm_p6uSEmeP2myODwFaVTStUm_Z-KJK_noz7ND8aQ',
            'type': '30116'
        }
        result_2 = requests.post(url=api, data=data_2).json()

        if result['msg'] == '识别成功' and len(result['data']['data'].split('|')) == 3:
            return result['data']['data']
        elif result_1['msg'] == '识别成功' and len(result_1['data']['data'].split('|')) == 3:
            return result_1['data']['data']
        elif result_2['msg'] == '识别成功' and len(result_2['data']['data'].split('|')) == 3:
            return result_2['data']['data']
        
        return None
    except Exception as e:
        print(f"获取验证码坐标时出错: {str(e)}")
        return None


def main():
    """主函数 - 支持两种爬取方式：requests方式（原版）和浏览器自动化方式（新增）"""
    print("开始爬取链家租房数据...")
    
    # 询问用户选择爬取方式
    choice = input("请选择爬取方式 (1: 原始requests方式, 2: 浏览器自动化带人机验证): ")
    
    if choice == '2':
        # 使用浏览器自动化方式
        max_pages_input = input("请输入最大爬取页数 (默认10页): ")
        max_pages = int(max_pages_input) if max_pages_input.isdigit() else 10
        scrape_with_browser(selected_city_code, max_pages)
    else:
        # 使用原始requests方式
        print("使用原始requests方式爬取...")
        
        # 如果CSV文件已存在，询问是否清空
        if os.path.exists(csv_file):
            print(f"检测到已存在的文件 {csv_file}，将追加数据")

        page_num = 1
        total_count = 0

        while True:
            # 爬取当前页
            data_list = scrape_page(page_num, city)

            # 如果返回None，说明没有数据了，停止爬取
            if data_list is None:
                print("已到达最后一页，爬取结束")
                break

            # 如果返回空列表，可能是网络错误，继续尝试下一页
            if len(data_list) == 0:
                print(f"第 {page_num} 页没有数据，跳过")
                page_num += 1
                # 如果连续几页都没有数据，则认为已结束
                no_data_count = 0
                while len(data_list) == 0 and no_data_count < 3:
                    data_list = scrape_page(page_num, city)
                    if len(data_list) == 0:
                        no_data_count += 1
                        page_num += 1
                    else:
                        no_data_count = 0  # 重置计数器
                
                if no_data_count >= 3:
                    print("连续3页没有数据，停止爬取")
                    break
                continue

            # 保存数据
            save_to_csv(data_list, csv_file)
            total_count += len(data_list)

            print(f"已爬取第 {page_num} 页，累计 {total_count} 条数据")
            
            # 继续下一页
            page_num += 1
            
            # 可选：限制最大页数
            if page_num > 100:  # 设置一个上限防止无限爬取
                print("已达到最大页数限制，停止爬取")
                break

    print(f"爬取完成！共爬取 {total_count} 条数据，已保存到 {csv_file}")


if __name__ == "__main__":
    main()