import pandas as pd

file_path = 'Данные поставщика.xlsx'

df = pd.read_excel(file_path)
print(df.columns)

with open('столбцы.txt', 'w', encoding='utf-8') as w:
    for colum in df.columns:
        w.write(colum +'\n')