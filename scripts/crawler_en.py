import requests
from bs4 import BeautifulSoup
import re

def crawl_content(base_url, max_num=100, output_file="output.txt"):
    """
    爬取指定网址的内容并保存到文件中
    :param base_url: 需要爬取的基础网址
    :param max_num: 最大爬取数量，默认为100
    :param output_file: 爬取内容保存的文件路径，默认为"output.txt"
    """
    pending_urls = []  # 存放待爬取的网址
    visited_urls = []  # 存放所有已经爬取过的网址

    try:
        u = requests.get(base_url)
        u.encoding = 'utf-8'
        web = u.text
        soup = BeautifulSoup(web, "lxml")

        # 爬取第一页中的所有链接
        for link in soup.find_all(name='a', href=re.compile(r'https?://')):
            if len(pending_urls) > max_num:
                break
            url = link.get('href')
            if url in pending_urls:
                continue
            pending_urls.append(url)
            visited_urls.append(url)
            print(f"Added URL: {url}")

            req = requests.get(url=url)
            req.encoding = 'utf-8'
            html = req.text
            bes = BeautifulSoup(html, "lxml")
            texts_list = bes.text.split("\xa0" * 4)

            # 将爬取内容写入文件
            with open(output_file, "a", encoding='utf-8') as file:
                for line in texts_list:
                    file.write(line + "\n")

        # 爬取已经获取到的网址中的其他链接
        for uurl in pending_urls:
            double_url = []
            u = requests.get(url=uurl)
            u.encoding = 'utf-8'
            web = u.text
            soup = BeautifulSoup(web, "lxml")

            for link in soup.find_all(name='a', href=re.compile(r'https?://')):
                if len(double_url) > max_num:
                    break
                url = link.get('href')
                if url in visited_urls:
                    continue
                double_url.append(url)
                visited_urls.append(url)
                print(f"Added nested URL: {url}")

                req = requests.get(url=url)
                req.encoding = 'utf-8'
                html = req.text
                bes = BeautifulSoup(html, "lxml")
                texts_list = bes.text.split("\xa0" * 4)

                with open(output_file, "a", encoding='utf-8') as file:
                    for line in texts_list:
                        file.write(line + "\n")

        print(f"Crawling complete. Content saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# def fetch_html(url):
#     """获取指定 URL 的 HTML 内容"""
#     response = requests.get(url)
#     response.encoding = 'utf-8'
#     return response.text

# def extract_links(soup):
#     """从 BeautifulSoup 对象中提取所有超链接"""
#     return [link.get('href') for link in soup.find_all(name='a', href=re.compile(r'https?://'))]

# def crawl_url(url, max_num, visited_urls, output_file):
#     """爬取单个 URL 的内容并保存到文件中"""
#     html = fetch_html(url)
#     soup = BeautifulSoup(html, "lxml")
#     texts = soup.text.split("\xa0" * 4)

#     with open(output_file, "a", encoding='utf-8') as file:
#         for line in texts:
#             file.write(line + "\n")

# def crawl_content(base_url, max_num=100, output_file="output.txt"):
#     """
#     爬取指定网址的内容并保存到文件中
#     :param base_url: 需要爬取的基础网址
#     :param max_num: 最大爬取数量，默认为100
#     :param output_file: 爬取内容保存的文件路径，默认为"output.txt"
#     """
#     pending_urls = [base_url]  # 存放待爬取的网址
#     visited_urls = set()  # 存放已经爬取过的网址

#     while pending_urls and len(visited_urls) < max_num:
#         current_url = pending_urls.pop(0)
#         if current_url in visited_urls:
#             continue
        
#         print(f"Crawling: {current_url}")
#         visited_urls.add(current_url)
#         crawl_url(current_url, max_num, visited_urls, output_file)
        
#         # 提取链接并添加到待爬取列表
#         soup = BeautifulSoup(fetch_html(current_url), "lxml")
#         links = extract_links(soup)
#         for link in links:
#             if link not in visited_urls and link not in pending_urls:
#                 pending_urls.append(link)
#                 print(f"Added URL: {link}")

#     print(f"Crawling complete. Content saved to {output_file}")

import re
def clean_data(input_file="news_output.txt", output_file="cleaned_news_output.txt"):
    """
    清洗爬取的数据
    :param input_file: 需要清洗的文件路径，默认为"news_output.txt"
    :param output_file: 清洗后的文件路径，默认为"cleaned_news_output.txt"
    """
    try:
        with open(input_file, "r", encoding='utf-8') as file:
            content = file.read()

        # 将多个空格替换为一个空格
        content = re.sub(r'\s+', ' ', content)

        # 使用正则表达式清洗数据,清除非英文字符,但是保留空格
        cleaned_content = re.sub(r'[^a-zA-Z ]', '', content)

        # 将所有字母小写
        cleaned_content = cleaned_content.lower()

        with open(output_file, "w", encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"Data cleaned. Cleaned content saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    import os
    # 如果不存在 news_output.txt 文件，则爬取数据
    if not os.path.exists("data_en/news_content_en.txt"):
        print("Crawling data...")
        crawl_content(base_url='https://en.wikipedia.org/wiki/Main_Page/', max_num=200, output_file="data_en/news_content_en.txt")
        
    print("Data crawled.")
    if not os.path.exists("data_en/cleaned_news_content_en.txt"):
        clean_data(input_file="data_en/news_content_en.txt", output_file="data_en/cleaned_news_content_en.txt")

        file_size = os.path.getsize("data_en/cleaned_news_content_en.txt")
        print(f"cleaned_news_output.txt文件大小为: {file_size} bytes")
        # 将 bytes 转换成 MB
        file_size_MB = file_size / 1024 / 1024
        print(f"cleaned_news_output.txt文件大小为: {file_size_MB} MB")

        # 以 file_size_MB 重命名文件
        os.rename("data_en/cleaned_news_content_en.txt", f"data_en/cleaned_news_content_en_{file_size_MB:.2f}MB.txt")
        os.rename("data_en/news_content_en.txt", f"data_en/news_content_en_{file_size_MB:.2f}MB.txt")

    

    

