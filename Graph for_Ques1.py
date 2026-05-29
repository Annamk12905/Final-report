import matplotlib.pyplot as plt
import pandas as pd

# ===== ĐỌC DỮ LIỆU =====
df = pd.read_csv("Ques1_ques2_Overview_of_the_application_market_data.csv")

# ===== CHẤT LƯỢNG HÌNH (NÉT HƠN) =====
plt.rcParams['figure.dpi'] = 150

# ===== KÍCH THƯỚC LỚN ĐỂ KHÔNG ĐÈ CHỮ =====
fig, ax1 = plt.subplots(figsize=(20, 8))

# ===== BIỂU ĐỒ CỘT =====
ax1.bar(df["Category"], df["Installs"], color="skyblue")
ax1.set_xlabel("Category")
ax1.set_ylabel("Installs")

# FIX CHỮ KHÔNG BỊ ĐÈ
ax1.tick_params(axis='x', rotation=90, labelsize=8)

# ===== BIỂU ĐỒ ĐƯỜNG =====
ax2 = ax1.twinx()
ax2.plot(df["Category"], df["Total_Apps"], color="red", marker="o", linewidth=2)
ax2.set_ylabel("Number of Apps")

# ===== TITLE =====
plt.title("Top Categories: Installs vs Number of Apps", fontsize=14)

# ===== CĂN BỐ CỤC =====
plt.tight_layout()

# ===== LƯU ẢNH (NÉT NHẤT) =====
plt.savefig("chart.png", dpi=300, bbox_inches='tight')

# ===== HIỂN THỊ =====
plt.show()