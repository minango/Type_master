import random
import csv

with open("stars.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["x", "y", "mag"])

    for _ in range(500):
        x = random.randint(-2000, 2000)
        y = random.randint(-2000, 2000)
        mag = round(random.uniform(0.0, 2.5), 2)  # 明るい星だけ
        writer.writerow([x, y, mag])

print("stars.csv 作成完了！")
