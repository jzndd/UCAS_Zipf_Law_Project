# UCAS Zipf Law Project

## 项目简介
本项目旨在研究 Zipf 定律在自然语言处理中的应用。通过分析文本数据，验证 Zipf 定律在词频分布中的表现。

## 项目结构
```
UCAS_Zipf_Law_Project/
│
├── data/               # 中文爬虫所得的数据文件夹
├── data_en/            # 英文爬虫所得的数据文件夹
├── scripts/            # 代码文件夹
├── 技术报告.pdf         
└── README.md        
```
其中，data/, data_en/ 与 技术报告.pdf 不包含在 github 的仓库中，如需获取数据，欢迎联系 jiangzhennan2024@ia.ac.cn 或 stjzn0410@gmail.com 

## 复现报告中的结果

+ 克隆项目
```bash
git clone https://github.com/yourusername/UCAS_Zipf_Law_Project.git
```

+ 爬取数据

你可以通过指定爬虫代码中的 **max_num** 参数与爬虫网页数量来决定爬取数据量的大小
```bash
python scripts/crawler.py # for chinese crawler

python scripts/crawler_en.py # for english crawler
```

+ 齐夫定律的分析
```bash
python scripts/ZipfLaw.py # for chinese analyse

python scripts/ZipfLaw_en.py # for english analyse
```

## 许可证
本项目采用 MIT 许可证