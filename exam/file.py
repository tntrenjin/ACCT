class CodeFile:

    def __init__(self, q_id=-1, file_name='', file_path=''):
        self.q_id = q_id
        self.file_name = file_name
        self.file_path = file_path
        self.vm_file_path = ''


class JavaFile(CodeFile):

    def __init__(self, q_id=-1, file_name='', file_path=''):
        super().__init__(q_id, file_name, file_path)

        self.class_name = file_name.split('.')[0]
