import torch
from torch import nn
from vocab import Vocab
from train import LSTMTextModel  # 直接复用你定义的模型类

def generate_text(model, vocab, start_text="白日依山尽", length=100, device="cpu"):
    model.eval()
    hidden = None
    result = [ch for ch in start_text]

    # 将起始文本转为 ID
    input_ids = torch.tensor([vocab.encode(start_text)], dtype=torch.long).to(device)

    with torch.no_grad():
        for _ in range(length):
            out, hidden = model(input_ids, hidden)  # (B, L, V)
            last_logits = out[:, -1, :]  # 取最后一个时间步的输出
            prob = torch.softmax(last_logits, dim=-1)

            # 采样下一个 token（也可以用 argmax 取最大概率）
            next_id = torch.multinomial(prob, num_samples=1).item()
            next_char = vocab.decode([next_id])[0]

            result.append(next_char)

            # 下一次输入就是新预测的 token
            input_ids = torch.tensor([[next_id]], dtype=torch.long).to(device)

    return "".join(result)

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    remove_chars = {"⻊", "⿰", "⿱", "□", "○", "●", "*", "+", "-", "0", "1", "2", "3", "=", "f", "{", "}", "."}
    vocab = Vocab("E:\\LSTM\\poem-LSTM\\corpus.txt", remove_chars=remove_chars)

    # 加载模型
    model = LSTMTextModel(vocab).to(device)
    checkpoint = torch.load("E:\\LSTM\\poem-LSTM\\lstm_poem_epoch3.pth", map_location=device)
    model.load_state_dict(checkpoint["model"])

    # 生成诗句
    start = "大鹏一日同风起，"
    generated = generate_text(model, vocab, start_text=start, length=56, device=device)
    print("生成结果：", generated)
