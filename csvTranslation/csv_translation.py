import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from deep_translator import GoogleTranslator

def translate_row(row_tuple, columns_to_translate, error_count):
    index, row = row_tuple
    translator = GoogleTranslator(source='auto', target='zh-CN')
    for column in columns_to_translate:
        translated_column = f'{column}_翻译'
        # 检查翻译列是否已经有值，如果有则跳过翻译
        if pd.notna(row.get(translated_column)):
            continue
        try:
            translated_text = translator.translate(row[column])
            row[translated_column] = translated_text
            error_count[0] = 0  # 重置错误计数
        except Exception as e:
            print(
                f"第 {index + 1} 行 '{column}' 列翻译时出现错误: {e}，将此单元格留空。")
            error_count[0] += 1  # 增加错误计数
    print(f"第 {index + 1} 行数据处理完成。")
    return row

# 读取 CSV 文件，你需要替换为实际的文件路径
file_path = 'Mental-Health-Twitter.csv'
print(f"正在读取文件: {file_path}")
df = pd.read_csv(file_path)
print("文件读取完成。")

# 假设需要翻译的列是 '创建时间' 和 '帖子内容'，你可以根据实际情况修改
columns_to_translate = ['post_text']

# 初始化错误计数
error_count = [0]

# 创建线程池
with ThreadPoolExecutor() as executor:
    futures = []
    for row_tuple in df.iterrows():
        future = executor.submit(translate_row, row_tuple, columns_to_translate, error_count)
        futures.append(future)
        if error_count[0] >= 5:
            print("连续出现五个请求问题，程序结束。")
            # 取消所有未完成的任务
            for f in futures:
                f.cancel()
            break

    results = []
    for future in futures:
        if future.cancelled():
            break  # 如果任务已取消，跳出循环
        if not future.cancelled():
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                pass

# 更新 DataFrame
df = pd.DataFrame(results)

# 保存翻译后的 DataFrame 为新的 CSV 文件
output_file_path = 'translated_file.csv'
print(f"正在保存翻译后的文件到: {output_file_path}")
df.to_csv(output_file_path, index=False)
print("文件保存完成。")