import pandas as pd

data = pd.read_csv("dataset.csv")
string = data.iloc[0, 3]

refTable = {
    43:  [data.iloc[0, 1], data.iloc[0, 2]],
    15:  [data.iloc[1, 1], data.iloc[1, 2]],
    100: [data.iloc[2, 1], data.iloc[2, 2]],
    54:  [data.iloc[3, 1], data.iloc[3, 2]],
    33:  [data.iloc[4, 1], data.iloc[4, 2]],
    19:  [data.iloc[5, 1], data.iloc[5, 2]],
    97:  [data.iloc[6, 1], data.iloc[6, 2]],
    13:  [data.iloc[7, 1], data.iloc[7, 2]]
}

windowCount = 0
print(string)

for i in range(0, len(string), 5):
    volatileStr = list(string) 
    for j in range(i, min(i + 9, len(string))):
        if j in refTable:
            ref = refTable[j]
            if len(ref) > 1:
                volatileStr[j] = ref[1]
                editedStr = "".join(volatileStr)
                print(editedStr)

