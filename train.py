import torch
from torch.utils.data import Dataset, DataLoader
from vocab import Vocab
from torch import nn
class TextDataSet(Dataset):
    def __init__(self,filepath,vocab,seq_lenth=50,encoding='utf-8'):
        self.vocab=vocab
        with open(filepath,'r',encoding=encoding) as f:
            text=f.read()
        self.data=vocab.encode(text)
        self.seq_lenth=seq_lenth
    def __len__(self):
        return len(self.data) - self.seq_lenth
    def __getitem__(self, idx):
        # 输入序列 X
        x = torch.tensor(self.data[idx:idx+self.seq_lenth], dtype=torch.long)
        # 目标序列 Y (通常是预测下一个字符)
        y = torch.tensor(self.data[idx+1:idx+self.seq_lenth+1], dtype=torch.long)
        return x, y
class LSTMTextModel(nn.Module):
    def __init__(self, vocab, embed_size=128, hidden_size=256, num_layers=2):
        super().__init__()
        vocab_size = len(vocab)
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        x = self.embed(x)  # (B,L,E)
        out, hidden = self.lstm(x, hidden)  # (B,L,H)
        logits = self.fc(out)  # (B,L,V)
        return logits, hidden

if __name__ =='__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    remove_chars = {"⻊", "⿰", "⿱", "□", "○", "●", "*", "+", "-", "0", "1", "2", "3", "=", "f", "{", "}", "."}
    vocab = Vocab("C:\\poems\\corpus.txt", remove_chars=remove_chars)

    num_steps=64
    dataset = TextDataSet("C:\\poems\\corpus.txt", vocab, seq_lenth=num_steps)#seq_

    # 构建 dataloader
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    model = LSTMTextModel(vocab).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    num_epochs = 10

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        print(f"Epoch {epoch + 1}/{num_epochs} starting...")

        for step, (x, y) in enumerate(dataloader, start=1):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            out, _ = model(x)
            loss = criterion(out.reshape(-1, out.size(-1)), y.reshape(-1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            # 每 100 步打印一次信息
            if step % 100 == 0:
                print(f"  Step [{step}/{len(dataloader)}], "
                      f"Batch Loss: {loss.item():.4f}, "
                      f"Avg Loss: {total_loss / step:.4f}")

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1} completed. Average Loss: {avg_loss:.4f}\n")

    torch.save(model.state_dict(), "lstm_poem.pth")
    print("Model saved as lstm_poem.pth")