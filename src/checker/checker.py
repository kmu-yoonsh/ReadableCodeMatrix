import os
from .parsing import Parsing
from .function import Function

from clang.cindex import CursorKind


class Checker(object):
    def __init__(self, path, text, excel):
        self.path = path
        self.isDir = os.path.isdir(path)
        self.save_path = os.path.dirname(path)


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
            if type(ast[i]) is list:
                self.walk(ast[i])
            else:
                if ast[i].kind is CursorKind.FUNCTION_DECL:
                    func = Function(ast[i + 1])
                    print func.check_function(), func.variable_dict

                elif ast[i].kind is CursorKind.IF_STMT:
                    pass

                elif ast[i].kind is CursorKind.DO_STMT:
                    pass

                elif ast[i].kind is CursorKind.GOTO_STMT or ast[i].kind is CursorKind.INDIRECT_GOTO_STMT:
                    pass

            i += 1