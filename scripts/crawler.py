import requests
from bs4 import BeautifulSoup
import re

def fetch_html(url):
    """获取指定 URL 的 HTML 内容"""
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response.text

def extract_links(soup):
    """从 BeautifulSoup 对象中提取所有超链接"""
    return [link.get('href') for link in soup.find_all(name='a', href=re.compile(r'https?://'))]

def crawl_url(url, max_num, visited_urls, output_file):
    """爬取单个 URL 的内容并保存到文件中"""
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")
    texts = soup.text.split("\xa0" * 4)

    with open(output_file, "a", encoding='utf-8') as file:
        for line in texts:
            file.write(line + "\n")

def crawl_content(base_url, max_num=100, output_file="output.txt"):
    """
    爬取指定网址的内容并保存到文件中
    :param base_url: 需要爬取的基础网址
    :param max_num: 最大爬取数量，默认为100
    :param output_file: 爬取内容保存的文件路径，默认为"output.txt"
    """
    pending_urls = [base_url]  # 存放待爬取的网址
    visited_urls = set()  # 存放已经爬取过的网址

    while pending_urls and len(visited_urls) < max_num:
        current_url = pending_urls.pop(0)
        if current_url in visited_urls:
            continue
        
        print(f"Crawling: {current_url}")
        visited_urls.add(current_url)
        crawl_url(current_url, max_num, visited_urls, output_file)
        
        # 提取链接并添加到待爬取列表
        soup = BeautifulSoup(fetch_html(current_url), "lxml")
        links = extract_links(soup)
        for link in links:
            if link not in visited_urls and link not in pending_urls:
                pending_urls.append(link)
                print(f"Added URL: {link}")

    print(f"Crawling complete. Content saved to {output_file}")

def clean_data(input_file="news_output.txt", output_file="cleaned_news_output.txt"):
    """
    清洗爬取的数据
    :param input_file: 需要清洗的文件路径，默认为"news_output.txt"
    :param output_file: 清洗后的文件路径，默认为"cleaned_news_output.txt"
    """
    try:
        with open(input_file, "r", encoding='utf-8') as file:
            content = file.read()

        # 使用正则表达式清洗数据
        cleaned_content = re.sub(r'[^\u4e00-\u9fa5]', '', content)

        with open(output_file, "w", encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"Data cleaned. Cleaned content saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    import os
    # 如果不存在 news_output.txt 文件，则爬取数据
    if not os.path.exists("data/news_content.txt"):
        print("Crawling data...")
        crawl_content(base_url='https://news.sina.com.cn/', max_num=300, output_file="data/news_content.txt")
        crawl_content(base_url='https://zh.wikipedia.org/wiki/Wikipedia/', max_num=300, output_file="data/news_content.txt")
        crawl_content(base_url='https://news.cctv.com/life/', max_num=300, output_file="data/news_content.txt")
        crawl_content(base_url='https://www.xinhuanet.com/', max_num=300, output_file="data/news_content.txt")
        crawl_content(base_url='https://www.people.com.cn/', max_num=300, output_file="data/news_content.txt")
        crawl_content(base_url='https://www.msn.cn/zh-cn/channel/topic/%E8%B5%84%E8%AE%AF/tp-Y_77f04c37-b63e-46b4-a990-e926f7d129ff', max_num=500, output_file="data/news_content.txt")
        
    print("Data crawled.")
    if not os.path.exists("data/cleaned_news_content.txt"):
        clean_data(input_file="data/news_content.txt", output_file="data/cleaned_news_content.txt")

        file_size = os.path.getsize("data/cleaned_news_content.txt")
        print(f"cleaned_news_output.txt文件大小为: {file_size} bytes")
        # 将 bytes 转换成 MB
        file_size_MB = file_size / 1024 / 1024
        print(f"cleaned_news_output.txt文件大小为: {file_size_MB} MB")

        # 以 file_size_MB 重命名文件
        os.rename("data/cleaned_news_content.txt", f"data/cleaned_news_content_{file_size_MB:.2f}MB.txt")
        os.rename("data/news_content.txt", f"data/news_content_{file_size_MB:.2f}MB.txt")
    

