from collections import Counter
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import jieba
from spellchecker import SpellChecker

# mpl.rcParams['font.family'] = 'SimHei'
# plt.rcParams['axes.unicode_minus'] = False  

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def clean_text(text):
    spell = SpellChecker()
    words = text.split()  # 假设每个单词之间用空格分隔
    
    # 过滤掉拼写错误的单词和单个字母，保留 "a"
    corrected_words = [
        word for word in words 
        if (len(word) > 1 or word == "a") and word in spell and word != "de" and word != "la"
    ]
    
    return corrected_words

def plot_zipf_law(text, file_size):
    word_counts = Counter(text)
    sorted_word_counts = sorted(word_counts.values(), reverse=True)
    
    ranks = np.arange(1, len(sorted_word_counts) + 1)
    frequencies = np.array(sorted_word_counts)

    print(f"Ranks: {ranks}")
    print(f"Frequencies: {frequencies}")

    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, marker=".", color="blue")
    plt.title(f"Zipf's Law {file_size}", fontsize=16)
    plt.xlabel("Rank", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True)
    plt.savefig(f"ZipfLaw_{file_size}.png")
    plt.show()

def calculate_character_statistics(text, file_size):
    # 计算字符频率
    word_counts = Counter(text)

    # 获取总字符数
    total_chars = sum(word_counts.values())

    # 获取高频字符（前十个）
    most_common_chars = word_counts.most_common(10)

    # 打印高频字符及其出现次数
    print("Character Frequencies (Top 10):")
    for char, count in most_common_chars:
        probability = count / total_chars
        print(f"{char}", end=" ")

    # 计算熵
    entropy = -sum((count / total_chars) * math.log2(count / total_chars) for count in word_counts.values())

    # 打印熵    
    print(f"\nEntropy of the text: {entropy:.4f}")

    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(range(10), [count for char, count in most_common_chars])
    plt.xticks(range(10), [char for char, count in most_common_chars])
    plt.title("Character Frequencies (Top 10)", fontsize=16)
    plt.xlabel("Character", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True)
    plt.savefig(f"Character_Frequencies_{file_size}.png")
    plt.show()

if __name__ == "__main__":
    file_names = ['4.77MB']
    for file_name in file_names:
        file_path = f'data_en/cleaned_news_content_en_{file_name}.txt'
        text = read_file(file_path)
        
        # 清理文本，删除拼写错误的单词
        cleaned_text = clean_text(text)
        
        plot_zipf_law(cleaned_text, file_name)
        calculate_character_statistics(cleaned_text, file_name)
