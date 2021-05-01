import os

stu_list = []
questions = []

title_box_str = ''
java_vm_path = ''

rows, columns = [int(i) for i in os.popen('stty size', 'r').read().split()]
