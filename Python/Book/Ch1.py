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

# iterate
fav_movie = ["The Holy Grail", "The Life of Brian"]

# 用while: 不建議
count = 0
while count < len(fav_movie):
    print(fav_movie[count])
    count = count + 1

# 用for
for each_flick in fav_movie:
    print(each_flick)
    
# 清單中嵌入清單
movie = [
    "The Holy Grail", 1975, "Terry Jone& Terry Gilliam", 91,
    ["Graham Chapman",
     ["Michael Palin", "John Cleee", "Terry Gilliam", "Eric Idle", "Terry Jone"]
        
    ]
]

print(movie[4][1][3])
# Answer: Eric Idle

# 檢查識別字是否保存特定型態的資料
name = ['Michael', 'Terry']
num_name = len(name)
isinstance(name, list)
isinstance(num_name, list)

# 顯示清單中的清單

movie = [
    "The Holy Grail", 1975, "Terry Jone& Terry Gilliam", 91,
    ["Graham Chapman",
     ["Michael Palin", "John Cleee", "Terry Gilliam", "Eric Idle", "Terry Jone"]
        
    ]
]

print(movie)

# 處理清單裡的清單
for each_item in movie:
    if isinstance(each_item, list):
        for nested_item in each_item:
            print(nested_item)
    else:
        print(each_item)
        
# BIF
dir(__builtins__)

# 三層套疊
for each_item in movie:
    if isinstance(each_item, list):
        for nested_item in each_item:
            if isinstance(nested_item, list):
                for deeper_item in nested_item:
                    print(deeper_item)
            else:
                print(nested_item)
    else:
        print(each_item)
        
