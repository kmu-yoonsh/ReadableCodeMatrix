import os
import sys
import traceback
from .parsing import Parsing
from .function import Function
from .analysisdata import AnalysisData

from clang.cindex import CursorKind


class Checker(object):
    def __init__(self, path, text, excel):
        self.path = path
        self.isDir = os.path.isdir(path)
        self.save_path = os.path.dirname(path)

        self.check_result = dict()  # result by file

        self.analysis_data = AnalysisData()
        self.function_checker = Function(self.analysis_data)


    def check_code(self):
        file_list = os.listdir(self.path) if self.isDir else [os.path.split(self.path)[-1]]

        for _file in file_list:
            try:
                parser = Parsing(_file)
                ext = os.path.splitext(_file)[-1]

                if ext == '.c' or ext == '.cpp' or ext == '.h':
                    self.check_result[_file] = dict()
                    ast = parser.parser(os.path.join(self.save_path, _file))
                    self.analysis_data.codes = open(os.path.join(self.save_path, _file)).readlines()

                    # print(ast)
                    try:
                        self.walk(ast, _file)
                    except Exception as e:
                        print(e, traceback.extract_tb(sys.exc_info()[-1]))
                    self.check_result[_file]['global'] = self.analysis_data.global_variable

            except Exception as e:
                print e

    def walk(self, ast, file_name):
        i = 0

        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data, file_name)
            else:
                if data.kind is CursorKind.FUNCTION_DECL:
                    i += 1

                    self.analysis_data.set_init_data()
                    self.function_checker.set_init_data(ast[i], data.spelling)
                    self.check_result[file_name][data.spelling] = self.function_checker.check_function()

                elif data.kind is CursorKind.VAR_DECL:
                    self.analysis_data.global_variable[data.spelling] = list()

            i += 1