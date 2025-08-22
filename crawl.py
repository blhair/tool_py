import os
import re  # 1. 导入 re 模块
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdfs_with_filter(url, keywords=[], save_folder='downloads'):
    """
    从指定URL下载PDF文件，支持使用正则表达式进行关键词过滤。

    :param url: 目标网页的URL
    :param keywords: 关键词或正则表达式模式的列表。
    :param save_folder: 保存PDF文件的文件夹名称。
    """

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"创建文件夹: {save_folder}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        pdf_links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.pdf'):
                full_url = urljoin(url, href)
                link_text = link.text.strip()
                file_name = os.path.basename(full_url)

                # 2. 修改过滤逻辑以使用 re.search
                if not keywords or any(re.search(keyword, link_text, re.IGNORECASE) or re.search(keyword, file_name, re.IGNORECASE) for keyword in keywords):
                    pdf_links.append(full_url)
                    
        if not pdf_links:
            print("未能找到任何符合条件的PDF文件。")
            return

        print(f"找到 {len(pdf_links)} 个符合条件的PDF文件，准备下载...")

        for pdf_url in pdf_links:
            try:
                file_name = os.path.basename(pdf_url)
                file_path = os.path.join(save_folder, file_name)
                
                print(f"正在下载: {file_name}")
                pdf_response = requests.get(pdf_url, headers=headers)
                pdf_response.raise_for_status()

                with open(file_path, 'wb') as f:
                    f.write(pdf_response.content)
                print(f"下载完成: {file_path}")

            except requests.exceptions.RequestException as e:
                print(f"下载失败: {pdf_url}, 错误: {e}")

    except requests.exceptions.RequestException as e:
        print(f"无法访问网页: {url}, 错误: {e}")

# --- 使用示例 ---
if __name__ == '__main__':
    # 替换为您要爬取的网页URL
    target_url = "https://www.eecs70.org/" 
    
    # 设置您感兴趣的关键词，例如 ['report', 'annual']
    # 如果想下载所有PDF，可以将keywords设置为空列表 []
    filter_keywords = ['hw','n\d+','dis'] 

    # 设置保存PDF的文件夹名称
    download_folder = "/mnt/d/学习笔记/all_in_one/pdf/cs70"

    download_pdfs_with_filter(target_url, filter_keywords, download_folder)
