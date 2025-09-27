# with open("D:\\poems\\corpus.txt", "r", encoding="utf-8") as f:
#     text = f.read()

# chars = sorted(list(set(text)))#sort得到稳定的字符数组list'，因为每次set后都不一样
# vocab_size = len(chars)
# filtered_chars =[ch for ch in chars if ch not in
#                   {"⻊", "⿰", "⿱", "□", "○", "●","*","+","-","0","1","2","3",
#                    "=","f","{","}","."}
#                 ]

# stoi = {ch: i for i, ch in enumerate(filtered_chars)}
# itos = {i: ch for i, ch in enumerate(filtered_chars)}

# print("词表大小:", vocab_size)

# for i in range(100):
#     print(itos[i])
import torch 
from torch import nn
import numpy

class Vocab:
    def __init__(self, filepath, remove_chars=None, encoding="utf-8",embed_dim=300):
        """
        构建一个 Vocab 类
        :param filepath: 文本路径
        :param remove_chars: 需要过滤掉的字符集合
        :param encoding: 文件编码，默认 utf-8
        """
        self.filepath = filepath
        self.remove_chars = remove_chars or set()
        
        # 读取文本
        with open(filepath, "r", encoding=encoding) as f:
            self.text = f.read()
        
        # 构建字符集合并排序
        chars = sorted(set(self.text))
        
        # 过滤掉指定字符
        self.chars = [ch for ch in chars if ch not in self.remove_chars]
        
        # 建立映射表
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}
        self.vocab_size = len(self.chars)
       

    def __len__(self):
        return self.vocab_size

    def encode(self, text):
        """将字符串转为索引序列"""
        return [self.stoi[ch] for ch in text if ch in self.stoi]

    def decode(self, indices):
        """将索引序列转为字符串"""
        return "".join(self.itos[i] for i in indices if i in self.itos)

    def show_sample(self, n=100):
        """打印前 n 个字符"""
        for i in range(min(n, self.vocab_size)):
            print(self.itos[i])
    def get_vector(self, ch):
        """获取单个字符的稠密向量"""
        if ch not in self.stoi:
            raise ValueError(f"字符 {ch} 不在词表中！")
        idx = torch.tensor([self.stoi[ch]], dtype=torch.long)
        return self.embedding(idx).detach().numpy()

    def get_sequence_vectors(self, text):
        """获取一个字符串的稠密向量序列"""
        ids = torch.tensor(self.encode(text), dtype=torch.long)
        return self.embedding(ids).detach().numpy()


# ========== 使用示例 ==========
if __name__ == "__main__":
    remove_chars = {"⻊", "⿰", "⿱", "□", "○", "●", "*", "+", "-", "0", "1", "2", "3", "=", "f", "{", "}", "."}
    vocab = Vocab("D:\\poems\\corpus.txt", remove_chars=remove_chars)

    print("词表大小:", len(vocab))
    vocab.show_sample(10)

    # 测试 encode / decode
    sample_text ="冷眼向洋看世界，熱风吹雨洒江天"
    encoded = vocab.encode(sample_text)
    decoded = vocab.decode(encoded)
    print("原文:", sample_text)
    print("编码:", encoded)
