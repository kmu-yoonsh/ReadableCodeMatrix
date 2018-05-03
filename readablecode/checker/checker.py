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
                        self.check_result[_file]['global'] = dict()
                        self.check_global_variable(_file)
                    except Exception as e:
                        print(e, traceback.extract_tb(sys.exc_info()[-1]))

            except Exception as e:
                print e

    def check_function_relation(self, using_func_set_list, function_set, file_name):
        for _ in range(3):
            past_size = -1
            while past_size != len(using_func_set_list):
                past_size = len(using_func_set_list)

                i = 1
                while i < len(using_func_set_list):
                    if using_func_set_list[0] & using_func_set_list[i]:
                        using_func_set_list[0] = using_func_set_list[0] | using_func_set_list[i]
                        using_func_set_list.pop(i)
                    else:
                        i += 1

            if len(using_func_set_list) is 1:
                break

            i = 0
            while i < len(function_set):
                set_to_list = list(function_set)
                for func in using_func_set_list:
                    if set_to_list[i] in func:
                        using_func_set_list.append(set([set_to_list[i]] + self.check_result[file_name][set_to_list[i]]['used_function']))
                        function_set.remove(set_to_list[i])
                        break
                i += 1

        else:
            return False    # can not connect functions each other within twice.

        return True

    def check_global_variable(self, file_name):
        for global_variable in self.analysis_data.global_variable:
            function_set = set(filter(lambda x: x != 'global', [func for func in self.check_result[file_name]]))
            using_func_set_list = list()
            using_func_total_set = set(list())
            using_type_check_num = 0

            for func in self.analysis_data.global_variable[global_variable]:
                using_type_check_num += self.analysis_data.global_variable[global_variable][func]
                using_func_set_list.append(set([func] + self.check_result[file_name][func]['used_function']))
                using_func_total_set = using_func_total_set | using_func_set_list[-1]
                function_set.remove(func)

            if using_type_check_num:    # assigned more than once in functions
                # functions that are using global variable is called by other functions using global variable, within twice.
                if self.check_function_relation(using_func_set_list, function_set, file_name):
                    self.check_result[file_name]['global'][global_variable] = 'change to function parameter'
            else:   # using as constant
                self.check_result[file_name]['global'][global_variable] = 'change to constant'

    def walk(self, ast, file_name):
        i = 0

        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data, file_name)
            else:
                if 'MACRO' in data.kind.name:
                    self.analysis_data.macro_list.append(data.spelling)

                elif data.kind is CursorKind.FUNCTION_DECL and type(ast[i + 1]) is list \
                        and filter(lambda x: x.kind is CursorKind.COMPOUND_STMT, filter(lambda y: type(y) is not list, ast[i + 1])):
                    i += 1

                    self.analysis_data.set_init_data()
                    self.function_checker.set_init_data(ast[i], data.spelling)
                    self.check_result[file_name][data.spelling] = self.function_checker.check_function()

                elif data.kind is CursorKind.VAR_DECL:
                    self.analysis_data.global_variable[data.spelling] = dict()

            i += 1
