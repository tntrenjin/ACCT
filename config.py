from threading import Semaphore


# 路徑設定 =================================

# 考試資料夾根目錄
root_path = './data'
# 學生程式碼 資料夾
stu_java_org_path = root_path + '/code'
# 學生名單 檔案
stu_list_file_path = root_path + '/stuList.txt'
# 測資 資料夾
test_data_path = root_path + '/test_data'
# 學生輸出結果 資料夾
student_result_path = root_path + '/student_result'

# 題目設定 =================================

# 總題數（題號由 1 開始）
question_number = 5
# 超時
TIME_LIMIT = 2
# 判分模式 0: 模糊比對, 1: 嚴格
JUDGE_MODE = 0

# 檔名設定 =================================

# 學生資料夾名稱格式（{stu_id} 將自動帶入學號）
stu_folder_name_format = 'ds{stu_id}'
# 學生程式碼 檔名格式（請使用正規表達式，題號須用括號）
stu_code_file_name = r'.*[Qq](\d*)\.java$'
# 測資檔名格式（{q_id} 將自動帶入 1 ~ question_number）
question_name_format = 'Q{q_id}'

# 執行緒設定 ===============================

# 題目執行緒數量
question_semaphore = Semaphore(5)
# 測資執行緒數量
test_case_semaphore = Semaphore(25)
