import globalvar
from config import student_result_path, stu_java_org_path
from util import progress


class Result:

    def __init__(self, code, ans_input='', ans_output='', stu_output='',
                 err_output='', run_time=0.0, is_public=False):
        self.code = code
        self.ans_input = ans_input
        self.ans_output = ans_output
        self.stu_output = stu_output
        self.err_output = err_output
        self.is_public = is_public
        self.run_time = run_time


class TestCase:

    def __init__(self, input_case, output_case, is_public):
        self.input_case = input_case
        self.output_case = output_case
        self.is_public = is_public


class Question:

    def __init__(self, q_id):
        self.id = q_id
        self.test_cases = []
        self.test_cases_cnt = 0
        self.public_test_cases_cnt = 0

    def add(self, input_case, output_case, is_public):
        self.test_cases.append(TestCase(input_case, output_case, is_public))
        self.test_cases_cnt += 1

        if is_public:
            self.public_test_cases_cnt += 1


class Student:

    def __init__(self, std_id):
        self.id = std_id
        self.id_hidden = (len(self.id) - 3) * '*' + self.id[-3:]
        self.org_path = f'{stu_java_org_path}/{std_id}'
        self.vm_path = f'{globalvar.java_vm_path}/{std_id}'
        self.output_result_file_path = f'{student_result_path}/{std_id}.txt'
        self.files = []
        self.result = []
        self.final_result = []
        self.progress = 0.
        self.progress_unit = 0.

    def inf(self, show=False):
        s = self.id_hidden if show else self.id

        for r in self.final_result[1:]:
            s += '\t' + (r if r != 'MF' else '  ')

        if show:
            print(' ' * globalvar.columns + '\r' + s)

        return s

    def reset_result(self):
        self.result = [None]
        self.final_result = [None]
        self.progress = 0.

        cnt = 0
        for idx, f in enumerate(self.files[1:]):
            if f != 'MF':
                cnt += globalvar.questions[idx + 1].test_cases_cnt

        if cnt != 0:
            self.progress_unit = 1. / cnt

        for q in globalvar.questions[1:]:
            self.result.append([])
            self.final_result.append('MF')
            for _ in range(len(globalvar.questions[q.id].test_cases)):
                self.result[-1].append(Result('MF'))

    def set_result(self, q_id, t_idx, r):
        self.result[q_id][t_idx] = r
        self.progress = min(self.progress + self.progress_unit, 1.)

        progress.show(self.id_hidden, self.progress)
