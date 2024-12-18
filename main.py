import pandas as pd
import os

def read_excel_file(file_path, req_columns):
    try:
        if not os.path.exists(file_path):
            print(f"[INFO -] Ошибка: Файл '{file_path}' не существует.")
            return None

        data = pd.read_excel(file_path)
        missing_columns = [col for col in req_columns if col not in data.columns]
        if missing_columns:
            print(f"[INFO -] Ошибка: Нету столбца {missing_columns} в файле '{file_path}'.")
            print(f"[INFO +] Доступные столбцы в '{file_path}': {list(data.columns)}")
            return None

        print(f"[INFO +] Файл был успешно прочитан '{file_path}'.")
        return data

    except Exception as e:
        print(f"[INFO -] Ошибка при чтении файла '{file_path}': {e}")
        return None

def definition_product_type(supplier_data, category_tree):
    try:
        print("[INFO +]: Столбцы в поставщике_данных", supplier_data.columns)
        print("[INFO +]: Столбцы в категории_дерева", category_tree.columns)

        
        mapped_data = pd.merge(
            supplier_data, 
            category_tree, 
            on=['Дочерняя категория'], 
            how='left'
        )

        matched = mapped_data[~mapped_data['Тип товара'].isna()]
        print(f"[INFO +] Успешно определены типы для {len(matched)} продукты из данных поставщика.")
        return matched

    except Exception as e:
        print(f"[INFO -] Ошибка при определении типа продукта: {e}")
        return None

def map_product_type(category_tree, product_list):
    try:
        print("Столбцы в категории_дерева::", category_tree.columns)
        print("Столбцы в Product_list:", product_list.columns)

        final_data = pd.merge(
            product_list, 
            category_tree, 
            on='Тип товара', 
            how='left'
        )

        matched = final_data[~final_data['Главная категория'].isna()]
        print(f"[INFO +] Успешно сопоставлено {len(matched)} продукты.")
        return matched

    except Exception as e:
        print(f"[INFO -] Error during mapping: {e}")
        return None

def main():
    
    product_list_file = "Список товаров.xlsx"
    category_tree_file = "Дерево категорий.xlsx"
    vendor_data_file = "Данные поставщика.xlsx"

   
    product_list_columns = ['Наименование', 'Тип товара']
    category_tree_columns = ['Главная категория', 'Дочерняя категория', 'Тип товара']
    supplier_data_columns = ['Наименование']

   
    product_list = read_excel_file(product_list_file, product_list_columns)
    category_tree = read_excel_file(category_tree_file, category_tree_columns)
    vendor_data = read_excel_file(vendor_data_file, supplier_data_columns)

    if product_list is None or category_tree is None or vendor_data is None:
        print("[INFO -] Error: Не удалось обработать один или несколько необходимых файлов.")
        return

    
    supplier_mapped = definition_product_type(vendor_data, category_tree)

    
    result = map_product_type(category_tree, product_list)

    if supplier_mapped is not None:
        output_supplier_file = "Supplier_Mapped_Product_Types.xlsx"
        supplier_mapped.to_excel(output_supplier_file, index=False)
        print(f"Mapped product types from supplier data saved to '{output_supplier_file}'.")

    if result is not None:
        output_file = "Mapped_Product_Types.xlsx"
        result.to_excel(output_file, index=False)
        print(f"Mapped product types saved to '{output_file}'.")

if __name__ == "__main__":
    main()
