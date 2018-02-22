import os
from .parsing import Parsing
from .function import Function

from clang.cindex import CursorKind


class Checker(object):
    def __init__(self, path, text, excel):
        self.path = path
        self.isDir = os.path.isdir(path)
        self.save_path = os.path.dirname(path)
        self.global_variable = dict()   # 'variable name': [function list]

        self.function_checker = Function()


    def check_code(self):
        file_list = os.listdir(self.path) if self.isDir else [self.path]

        for file in file_list:
            try:
                parser = Parsing(self.save_path)
                ext = os.path.splitext(file)[-1]

                if ext == '.c' or ext == '.cpp' or ext == '.h':
                    ast = parser.parser(os.path.join(self.save_path, file), ext)
                    self.walk(ast)

                # del parser
            except Exception as e:
                print e

    def walk(self, ast):
        i = 0

        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                if data.kind is CursorKind.FUNCTION_DECL:
                    i += 1
                    self.function_checker.set_init_data(ast[i], data.spelling, self.global_variable)
                    print self.function_checker.check_function()

                elif data.kind is CursorKind.IF_STMT:
                    pass

                elif data.kind is CursorKind.DO_STMT:
                    pass

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    pass

                elif data.kind is CursorKind.VAR_DECL:
                    self.global_variable['data.spelling'] = list()

                    print(self.global_variable, data.kind, data.spelling)

            i += 1