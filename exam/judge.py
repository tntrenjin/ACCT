import tempfile
import time
from threading import Thread

import globalvar
from config import question_number, question_semaphore, test_case_semaphore, JUDGE_MODE
from exam.execute import Java
from exam.structure import Result
from loader import loader
from util import env, text, io, color, progress


class Judge:

    @staticmethod
    def start():
        with tempfile.TemporaryDirectory() as temp_dir:
            globalvar.java_vm_path = temp_dir

            env.init_env_dir()
            text.generate_title_box()

            loader.load_questions()
            loader.load_all_students()

            Judge.judge()

    @staticmethod
    def judge():
        length = 11 + 9 * question_number

        print('\n\n' + '=' * length)
        print('Folder ID' + ''.join(('\tQ' + str(i)) for i in range(1, question_number + 1)))
        print('-' * length)

        time_start = time.time()

        for stu in globalvar.stu_list:
            progress.show(stu.id_hidden)
            Judge.judge_student(stu)
            print(' ' * 50, end='\r')
            stu.inf(show=True)

        time_end = time.time()

        print('=' * length)
        print(color.render(f'\n\nTotal time: {round(time_end - time_start, 4)}s', 'INF'))

        print('\nSaving all student result ... ', end='')
        io.output_all_result()
        print('Done')

    @staticmethod
    def judge_student(stu):
        stu.reset_result()

        question_thread_list = []
        for question in globalvar.questions[1:]:
            if stu.files[question.id] != 'MF':
                question_thread_list.append(Thread(target=Judge.judge_question,
                                                   args=(stu, question.id, stu.files[question.id])))
                question_thread_list[-1].start()

        for t in question_thread_list:
            t.join()

        io.output_stu_result(stu)

    @staticmethod
    def judge_question(stu, q_id, file):
        question_semaphore.acquire()

        test_cases = globalvar.questions[q_id].test_cases
        test_cases_cnt = globalvar.questions[q_id].test_cases_cnt
        test_case_thread_list = []

        compile_result, compile_output = Java.compiler(file.vm_file_path)

        if compile_result:
            for idx, case in enumerate(test_cases):
                test_case_thread_list.append(Thread(target=Judge.judge_test_cases, args=(stu, q_id, idx, file)))
                test_case_thread_list[-1].start()

            for t in test_case_thread_list:
                t.join()

            all_public_cnt = globalvar.questions[q_id].public_test_cases_cnt
            all_test_case_cnt = globalvar.questions[q_id].test_cases_cnt
            correct_public_cnt = 0
            correct_cnt = 0
            result_arr = []

            for case, result in zip(test_cases, stu.result[q_id]):
                result_arr.append(result.code)
                if result.is_public and result.code == 'AC':
                    correct_public_cnt += 1
                if result.code == 'AC':
                    correct_cnt += 1

            if all_public_cnt == correct_public_cnt and correct_cnt != all_test_case_cnt:
                stu.final_result[q_id] = 'HC'
            else:
                for r in ['RE', 'TL', 'WA', 'AC']:
                    if r in result_arr:
                        stu.final_result[q_id] = r
                        break

        else:
            for i in range(test_cases_cnt):
                stu.final_result[q_id] = 'CE'
                stu.set_result(q_id, i, Result('CE', err_output=compile_output))

        question_semaphore.release()

    @staticmethod
    def judge_test_cases(stu, q_id, t_idx, file):
        test_case_semaphore.acquire()

        test_case = globalvar.questions[q_id].test_cases[t_idx]
        input_case = test_case.input_case
        output_case = test_case.output_case
        is_public = test_case.is_public

        compare_ans_output = output_case
        if JUDGE_MODE == 0:
            compare_ans_output = text.clear_format(output_case)

        code, stu_output, run_time = Java.execute(input_case, stu.vm_path, file.class_name)

        if code == 'RE':
            judge_result = Result('RE', ans_input=input_case, ans_output=compare_ans_output,
                                  err_output=stu_output, run_time=run_time, is_public=is_public)
        elif code == 'TL':
            judge_result = Result('TL', ans_input=input_case, ans_output=compare_ans_output,
                                  run_time=run_time, is_public=is_public)
        else:
            compare_stu_output = stu_output
            if JUDGE_MODE == 0:
                compare_stu_output = text.clear_format(stu_output)

            judge_result = Result('AC' if compare_ans_output == compare_stu_output else 'WA',
                                  ans_input=input_case, ans_output=compare_ans_output, run_time=run_time,
                                  stu_output=compare_stu_output, is_public=is_public)

        # print(f'{self.id} Q{q_id} #{t_idx} -> {judge_result.code}')
        stu.set_result(q_id, t_idx, judge_result)

        test_case_semaphore.release()
