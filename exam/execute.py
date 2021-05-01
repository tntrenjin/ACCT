import subprocess
import time

import psutil

from config import TIME_LIMIT


class Executor:
    @staticmethod
    def kill(proc_pid):
        parent_proc = psutil.Process(proc_pid)

        for child_proc in parent_proc.children(recursive=True):
            child_proc.kill()

        parent_proc.kill()

    @staticmethod
    def execute(cmd):
        out = []
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        start_time = time.time()

        try:
            stdout, stderr = process.communicate(timeout=TIME_LIMIT)
            if stderr.decode() != '':
                # print(stderr.decode())
                out.append(['RE', stderr.decode()])
            else:
                out.append(['', stdout.decode()])

        except subprocess.TimeoutExpired:
            out.append(['TL', ''])

            Executor.kill(process.pid)
            process.kill()

        run_time = time.time() - start_time

        return out[0][0], out[0][1], run_time  # result code, cmd output, run_time


class Java:

    @staticmethod
    def compiler(path):
        cmd = f'javac {path}'
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.communicate()[1].decode()
        return ': error:' not in out, out

    @staticmethod
    def execute(input_case, bytecode_path, class_name):
        cmd = f'echo "{input_case}" | java -classpath {bytecode_path} {class_name}'
        code, out, run_time = Executor.execute(cmd)

        return code, out, run_time
