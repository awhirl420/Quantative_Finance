# 清單
movie = ["The Holy Grail", "The Life of Brian", "The Meaning of Life"]

# 清單特性
[1,2,3]+[1,2,3]
# [1, 2, 3, 1, 2, 3]

print(movie[1])

len(movie)
len(movie[1])

# 清單方法
cat = ["Cleee", "Palin", "Jone", "Idle"]
print(cat)
print(len(cat))

# 附加到末端
cat.append("Gilliam")

# 移除末端資料
cat.pop()

# 清單 + 一群資料項
cat.extend(["Gilliam", "Chapman"])

# 移除特定資料項
cat.remove("Chapman")

# 把資料加到特定槽位前面
cat.insert(0, "Chapman")

