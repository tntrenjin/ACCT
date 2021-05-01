import json
import os
import shutil

import globalvar
from config import question_number, test_data_path, question_name_format, stu_list_file_path, stu_folder_name_format
from exam.structure import Question, Student
from util import io, color


def load_questions():
    globalvar.questions = [None]

    print('Loading question list ...')

    for idx in range(1, question_number + 1):

        print(f' - Loading: {test_data_path}/Q{idx}.json ...... ', end='')

        with open(f'{test_data_path}/{question_name_format.format(q_id=idx)}.json', 'r') as f:
            json_data = json.loads(f.read())
            q = Question(idx)

            for data in json_data:
                q.add(data['in'], data['out'], data['public'])

            globalvar.questions.append(q)

        print(color.render('Done', 'OK'))
    print('\n')


def load_all_students():
    shutil.rmtree(globalvar.java_vm_path)
    os.mkdir(globalvar.java_vm_path)

    with open(stu_list_file_path, 'r') as fp:
        students = fp.read().strip().split('\n')

    if students[0] == '':
        print('Student list is empty')
        exit(0)

    for stu_id in students:
        globalvar.stu_list.append(Student(stu_folder_name_format.format(stu_id=stu_id)))
        search(globalvar.stu_list[-1])
        move(globalvar.stu_list[-1])


def search(stu):
    stu.files = [None]
    for _ in range(question_number):
        stu.files.append('MF')

    if os.path.exists(stu.org_path):
        search_files = io.search_file(stu.org_path)

        for f in search_files:
            if 0 < f.q_id <= question_number:
                stu.files[f.q_id] = f
                stu.files[f.q_id].vm_file_path = f'{globalvar.java_vm_path}/{stu.id}/{f.file_name}'


def move(stu):
    if not os.path.exists(stu.vm_path):
        os.mkdir(stu.vm_path)

    print(f'Move "{stu.id}" files to vm ...')

    for i, f in enumerate(stu.files[1:]):
        print(f' - Move Q{i + 1} to vm ... ', end='')
        if f != 'MF':
            shutil.copyfile(f.file_path, f.vm_file_path)
            io.encode_file(f.vm_file_path)
            io.remove_package(f.vm_file_path)
            print(color.render('Done', 'OK'))
        else:
            print(color.render('Missing file', 'MF'))

    print('')
