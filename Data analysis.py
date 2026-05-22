import pandas as pd

def clean_size(x):
    if "M" in str(x):
        return float(x.replace("M", ""))
    elif "k" in str(x):
        return float(x.replace("k", "")) / 1024
    else:
        return None



#đọc dữ liệu và đưa vào python
#df = pd.read_csv("Data_googleplaystore.csv")
df: pd.DataFrame =pd.read_csv("Data_googleplaystore.csv")

#làm sạch dữ liệu cột Installs                                      #to_numeric là hàm của pandas dùng để chuyển dữ liệu sang kiểu số (number)
df["Installs"] = df["Installs"].str.replace("+", "",regex=False)               # xóa dấu + trong dữ liệu
df["Installs"] = df["Installs"].str.replace(",", "",regex=False)               #xóa dấu phẩy trong dữ liệu
df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")    #nếu không chuyển được thì chuyển thành NaN
df["Installs"] = df["Installs"].fillna(0)                          # đưa dữ liệu NaN về 0

#làm sạch dữ liệu cột price
df["Price"] = df["Price"].str.replace("$", "",regex=False)
df["Price"]=pd.to_numeric(df["Price"], errors="coerce")
df["Price"] =df["Price"].fillna(0)

#xử lý dữ liệu size
df["Size"] = df["Size"].apply(clean_size)

#df["Size"] = df["Size"].str.replace("M", "",regex=False)
#df["Size"] = df["Size"].str.replace("k", "",regex=False)
#df["Size"]=pd.to_numeric(df["Size"], errors="coerce")
#df["Size"]=df["Size"].fillna(0)

# xử lý rating,Review
df["Rating"]=pd.to_numeric(df["Rating"], errors="coerce")
df["Reviews"]=pd.to_numeric(df["Reviews"], errors="coerce")


# Kiểm tra lại dữ liệu
#print(df["Price"])
#print(df["Installs"])
#print(df["Size"])

#xóa dòng có dữ liệu NaN
df = df.dropna(subset=["Category", "Rating", "Reviews", "Installs", "Price"])
# Bắt đầu phân tích dữ liệu (tổng hợp Category)
data_Category=df.groupby("Category").agg({
    "Installs":"mean",
    "Rating":"mean",
    "Reviews":"mean",
    "Size":"mean",
    "Price":"mean"
}).round(2)

data_Category.to_csv("Overview_of_the_application_market_data.csv")

#kiểm tra dữ liệu
#print(data_Category)





top_result=[]  #Lặp qua từng cột ["Installs", "Rating", "Reviews", "Size", "Price"] trong data_Category
for col in data_Category.columns:

        top_category = data_Category[col].idxmax()                   #tìm tên hàng (Category) có giá trị lớn nhất
        top_value = data_Category[col].max()                         #lấy giá trị lớn nhất trong cột
        top_result.append([col,top_category, top_value])

df_result = pd.DataFrame(top_result, columns=["指標", "最高類別", "最大值"])
df_result.to_csv("top_category_result.csv", index=False, encoding="utf-8-sig")


#PHÂN TÍCH MỐI QUAN HỆ Reviews và Installs
corr_by_category = df.groupby("Category")[["Reviews", "Installs"]].corr().iloc[0::2, -1].round(2)
corr_by_category.to_csv("Correlation_Reviews_Installs.csv", index=True, encoding="utf-8-sig")
# Rating và Installs
corr_by_category = df.groupby("Category")[["Rating", "Installs"]].corr().iloc[0::2, -1].round(2)
corr_by_category.to_csv("Correlation_Rating_Installs.csv", index=True, encoding="utf-8-sig")


# ======================
# Tạo điểm thành công
# ======================

# công thức đơn giản:
# Success = Rating × Reviews × Installs

df["Success"] = (
    df["Rating"] *
    df["Reviews"] *
    df["Installs"]
)

# ======================
# Phân tích theo Category
# ======================

result = df.groupby("Category").agg({
    "Rating": "mean",
    "Reviews": "mean",
    "Installs": "mean",
    "Success": "mean",
    "Size": "mean"
}).round(2)

# sắp xếp từ cao xuống thấp
result = result.sort_values(
    by="Success",
    ascending=False
)

#print(result)
result.to_csv("result_data.csv")
