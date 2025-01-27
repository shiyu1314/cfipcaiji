import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表，只保留 https://ip.164746.xyz
urls = [
    'https://ip.164746.xyz'
]

# 正则表达式用于匹配合法的IP地址
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 检查ip.txt文件是否存在，如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 用于存储所有抓取的IP地址
ip_addresses = []

# 遍历URL列表
for url in urls:
    try:
        # 发送HTTP请求获取网页内容
        response = requests.get(url, timeout=10)  # 加上超时时间防止请求卡住
        response.raise_for_status()  # 如果请求失败抛出异常
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根据网站的不同结构找到包含IP地址的元素
        if url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')  # 假设IP在tr标签中
        
        # 遍历所有元素，查找IP地址
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            
            # 如果找到IP地址，则加入列表
            ip_addresses.extend(ip_matches)
    
    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时出错: {e}")

# 去重并写入文件
ip_addresses = list(set(ip_addresses))  # 去重
with open('ip.txt', 'w') as file:
    for ip in ip_addresses:
        file.write(ip + '\n')

print('IP地址已保存到ip.txt文件中。')
