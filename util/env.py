import os

from config import student_result_path, test_data_path, root_path, stu_java_org_path, stu_list_file_path


def init_env_dir():
    add = []

    for p in [root_path, stu_java_org_path, test_data_path, student_result_path]:
        if not os.path.isdir(p):
            add.append(p)
            os.mkdir(p)

    if not os.path.exists(stu_list_file_path):
        add.append(stu_list_file_path)
        open(stu_list_file_path, 'w+', encoding='utf8')

    if len(add) > 0:
        print('The following path has been established:')
        for i, p in enumerate(add):
            print(f'{i + 1}. ' + p)

        print('\nPlease add files to the folder or update file')

        exit(0)
