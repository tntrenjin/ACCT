import os
import re

import globalvar
from config import stu_code_file_name, student_result_path, JUDGE_MODE
from exam.file import JavaFile
from util.text import generate_scoreboard_box, clear_format


def encode_file(path):
    """
    Encode file from big5 to utf-8

    :param str path: The file path
    :rtype: bool
    """

    try:
        with open(path, 'r', encoding='ms950') as f:
            to_encode = f.read()
            # to_encode = to_encode.encode('utf-8').decode('utf-8')
        with open(path, 'w+', encoding='utf-8') as f:
            f.write(to_encode)

        return True

    except Exception as e:
        # print(e)
        return False


def remove_package(path):
    """
    Remove java file package

    :param str path: The java file path
    """

    new_file = ''
    with open(path, 'r', encoding='utf-8') as f:
        java_file = f.readlines()

        if java_file[0].startswith('package'):
            new_file = ''.join(java_file[1:])

    if new_file != '':
        with open(path, 'w+') as f:
            f.write(new_file)


def search_file(path):
    """
    Use dfs to search all java files in student folder

    :param str path: Student folder path
    :return: JavaFile[]
    """

    output_list = []

    def dfs(dfs_path):
        file_list = os.listdir(dfs_path)

        for name in file_list:
            temp_path = f'{dfs_path}/{name}'

            if name in ['bin', 'out'] or name.startswith('.'):
                continue

            if os.path.isdir(temp_path):
                dfs(temp_path)
            else:
                regex_result = re.compile(stu_code_file_name).search(name)

                if regex_result.group(1):
                    q_id = int(regex_result.group(1))
                    output_list.append(JavaFile(q_id, name, temp_path))

    dfs(path)

    return output_list


def output_stu_result(stu):
    """
    Output student execute final result and detail

    :param Student stu: Student
    """

    length = 70
    title = f'Folder ID: {stu.id}\n\n' + globalvar.title_box_str + \
            generate_scoreboard_box(stu.final_result)

    buffer = []
    for idx, r in enumerate(stu.result[1:]):
        question_output_buffer = f'>> Q{idx + 1} >>> {stu.final_result[idx + 1]}\n{"┌" + "─" * length}\n'

        if r[0].code == 'CE':
            question_output_buffer += '\n'.join(('│  ' + s) for s in ('\n' + r[0].err_output).split('\n'))
        elif r[0].code == 'MF':
            continue
        else:
            test_case_buffer = []
            for cr_idx, cr in enumerate(r):
                test_case_detail = '\n'
                test_case_detail += f'Q{idx + 1}: Test case #{cr_idx + 1} ' \
                                    f'({"Public" if cr.is_public else "Private"}) ' \
                                    f'>> {f"{round(cr.run_time, 4)}s " if cr.run_time != 0.0 else ""}' \
                                    f'>> {cr.code}\n\n'
                test_case_detail += f'# Input:\n{cr.ans_input}\n\n'
                test_case_detail += f'# Ans output:' \
                                    f'\n{clear_format(cr.ans_output) if JUDGE_MODE == 0 else cr.ans_output}\n\n'

                if cr.code in ['WA', 'AC']:
                    test_case_detail += f'# Stu output:' \
                                        f'\n{clear_format(cr.stu_output) if JUDGE_MODE == 0 else cr.stu_output}\n'
                elif cr.code == 'RE':
                    test_case_detail += f'# Err output: \n{cr.err_output}\n'

                test_case_buffer.append('\n'.join(('│  ' + s) for s in test_case_detail.split('\n')))

            question_output_buffer += ('\n├' + '─' * length + '\n').join(test_case_buffer)

        buffer.append(question_output_buffer + '\n└' + '─' * length + '\n\n\n')

    with open(stu.output_result_file_path, 'w+', encoding='utf-8') as f:
        f.write(title + ''.join(buffer))


def output_all_result():
    s = '\n'.join([stu.inf() for stu in globalvar.stu_list])

    with open(f'{student_result_path}/all.txt', 'w+', encoding='utf-8') as f:
        f.write(s)
