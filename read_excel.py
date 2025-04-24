import pandas as pd

# Excelファイルのパスを指定
excel_file = 'base/家計簿2025.xlsx'

# すべてのシートを読み込む
xls = pd.ExcelFile(excel_file)
sheet_names = xls.sheet_names

# 各シートのデータを表示
for sheet_name in sheet_names:
    print(f"シート名: {sheet_name}")
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(df)
    print("\n") 