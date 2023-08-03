import os

def rename_files_in_dir(dir_path, new_name_template="downtoup_%05d.mp4"):
    # 列出指定資料夾下的所有檔案
    files = os.listdir(dir_path)

    # 確保只取 .mp4 檔案
    files = [f for f in files if f.endswith(".mp4")]

    # 根據檔案的原始順序進行排序
    files.sort()

    # 遍歷每一個檔案，並且按照新的名字模板進行命名
    for i, filename in enumerate(files):
        new_name = new_name_template % i
        old_file_path = os.path.join(dir_path, filename)
        new_file_path = os.path.join(dir_path, new_name)
        os.rename(old_file_path, new_file_path)

    print(f"Renamed {len(files)} files.")

# 使用上面的函數，只需替換為您要修改的資料夾路徑
rename_files_in_dir("D:\project\mp4")
