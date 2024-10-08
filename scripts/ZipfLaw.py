from collections import Counter
import numpy as np
import math

import matplotlib.pyplot as plt

import matplotlib as mpl
import jieba

mpl.rcParams['font.family'] = 'SimHei'

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def plot_zipf_law(word_counts, file_size):
    sorted_word_counts = sorted(word_counts.values(), reverse=True)
    
    ranks = np.arange(1, len(sorted_word_counts) + 1)
    frequencies = np.array(sorted_word_counts)

    print(f"Ranks: {ranks}")
    print(f"Frequencies: {frequencies}")

    plt.figure(figsize=(10, 6))
    # plt.loglog(ranks[mask], fit_line, color="red",label='线性拟合')
    plt.loglog(ranks, frequencies, marker=".", color="blue")
    plt.title(f"Zipf's Law {file_size}", fontsize=16)
    plt.xlabel("Rank", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True)
    # save fig
    plt.savefig(f"ZipfLaw_{file_size}.png")
    plt.show()

def plot_zipf_law_phrases(phrases, file_size="Example"):
    # 使用 jieba 分词
    word_list = list(jieba.cut(phrases))
    filtered_words = [word for word in word_list if len(word) > 1]
    word_list = filtered_words
    
    # 统计词频
    word_counts = Counter(word_list)

    sorted_word_counts = sorted(word_counts.values(), reverse=True)
    
    ranks = np.arange(1, len(sorted_word_counts) + 1)
    frequencies = np.array(sorted_word_counts)

    print(f"Ranks: {ranks}")
    print(f"Frequencies: {frequencies}")

    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, marker=".")
    plt.title(f"After Filter : Zipf's Law for Phrases {file_size}")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.legend()
    # save fig
    plt.savefig(f"ZipfLaw_Phrases_filter_{file_size}.png")
    plt.show()

def calculate_character_statistics_phrases(phrases, file_size="Example"):
    # 使用 jieba 分词
    word_list = list(jieba.cut(phrases))
    # 过滤掉特定的词语
    filtered_words = [word for word in word_list if len(word) > 1]
    word_list = filtered_words
    
    # 统计词频
    word_counts = Counter(word_list)

    # 获取总字符数
    total_chars = sum(word_counts.values())

    # 获取高频字符（前十个）
    most_common_phrases = word_counts.most_common(10)

    # 打印高频字符及其出现次数
    print("Character Frequencies (Top 10):")
    for phrase, count in most_common_phrases:
        probability = count / total_chars
        print(f"{phrase}", end=" ")
        # print(f"Character: '{char}' | Count: {count} | Probability: {probability:.4f}")

    # 计算熵

    entropy = -sum((count / total_chars) * math.log2(count / total_chars) for count in word_counts.values())

    # 打印熵    
    print(f"\nEntropy of the text: {entropy:.4f}")

    # 绘制柱状图

    plt.figure(figsize=(10, 6))

    plt.bar(range(10), [count for char, count in most_common_phrases])
    plt.xticks(range(10), [char for char, count in most_common_phrases])
    plt.title("After Filter : Phrases Frequencies (Top 10)", fontsize=16)
    plt.xlabel("Phrases", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(True)
    plt.savefig(f"Phrases_Frequencies_filter_{file_size}.png")
    plt.show()

def calculate_character_statistics(word_counts: Counter):
    # 计算字符频率
    # word_counts = Counter(text)

    # 获取总字符数
    total_chars = sum(word_counts.values())

    # 获取高频字符（前十个）
    most_common_chars = word_counts.most_common(10)

    # 打印高频字符及其出现次数
    print("Character Frequencies (Top 10):")
    for char, count in most_common_chars:
        probability = count / total_chars
        print(f"{char}", end=" ")
        # print(f"Character: '{char}' | Count: {count} | Probability: {probability:.4f}")

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
    plt.savefig("Character Frequencies (Top 10).png")
    plt.show()


if __name__ == "__main__":
    # file_names = ['0.10MB', '0.70MB', '1.00MB', "1.50MB" , '2.00MB', "2.50MB", "3.00MB", '4.50MB', '6.00MB']
    file_names = ['6.00MB']
    for file_name in file_names:
        file_path = f'data/cleaned_news_content_{file_name}.txt'
        #获取 file path 最后一个 _ 的内容
        text = read_file(file_path)

        # plot_zipf_law(text_counts, file_size)
        plot_zipf_law_phrases(text, file_name)

        calculate_character_statistics_phrases(text, file_name)