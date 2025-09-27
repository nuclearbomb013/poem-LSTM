import torch
from torch.utils.data import Dataset, DataLoader
from vocab import Vocab
class TextDataSet():
    def __init__(self,filepath,vocab,seq_lenth=50,encoding='utf-8'):
        self.vocab=vocab
        with open(filepath,'r',encoding=encoding) as f:
            text=f.read()
        self.data=vocab.encode(text)
        self.seq_len=seq_lenth
    def __len__(self):
        return len(self.data) - self.seq_len
    def __getitem__(self, idx):
        # 输入序列 X
        x = torch.tensor(self.data[idx:idx+self.seq_len], dtype=torch.long)
        # 目标序列 Y (通常是预测下一个字符)
        y = torch.tensor(self.data[idx+1:idx+self.seq_len+1], dtype=torch.long)
        return x, y
if __name__ =='__main__':
    remove_chars = {"⻊", "⿰", "⿱", "□", "○", "●", "*", "+", "-", "0", "1", "2", "3", "=", "f", "{", "}", "."}
    vocab = Vocab("D:\\poems\\corpus.txt", remove_chars=remove_chars)


    dataset = TextDataSet("D:\\poems\\corpus.txt", vocab, seq_lenth=50)

    # 构建 dataloader
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    # 查看一个 batch
    for X, Y in dataloader:
        print("输入:", X)   # (batch_size, seq_len)
        print("标签:", Y)   # (batch_size, seq_len)
        break    