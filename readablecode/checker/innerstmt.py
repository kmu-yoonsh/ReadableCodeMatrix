import os
import re
from clang.cindex import CursorKind


class InnerStmt(object):
    def __init__(self, analysis_data):
        self.current_cnt = 0
        self.function_name = None

        self.analysis_data = analysis_data


    def set_init_data(self, function_name):
        self.current_cnt = 0
        self.function_name = function_name


    def walk(self, ast):
        i = 0
        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                position_in_code = data.location.line

                if data.kind is CursorKind.VAR_DECL:
                    if data.spelling in self.analysis_data.variable:
                        self.analysis_data.duplicated_variable.append([data.spelling, position_in_code])
                    else:
                        self.analysis_data.variable[data.spelling] = {'declare': position_in_code, 'first': 0, 'last': 0}

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    self.analysis_data.check_list['goto'].append(position_in_code)

                elif data.kind in self.analysis_data.conditional_list:
                    self.current_cnt += 1

                    if data.kind is CursorKind.DO_STMT:
                        self.analysis_data.check_list['do/while'].append(position_in_code)

                    self.analysis_data.conditional[data.kind] = [position_in_code, self.current_cnt]

                    self.walk(ast[i + 1])
                    self.current_cnt -= 1
                    i += 1

                elif data.kind is CursorKind.CALL_EXPR and data.spelling not in self.analysis_data.used_function:
                    self.analysis_data.used_function.append(data.spelling)

                elif data.spelling:
                    if (data.spelling in self.analysis_data.global_variable) and (
                            self.function_name not in self.analysis_data.global_variable[data.spelling]):
                        self.analysis_data.global_variable[data.spelling].append(self.function_name)

                    elif data.kind is CursorKind.DECL_REF_EXPR or data.kind is CursorKind.UNEXPOSED_EXPR:
                        if data.spelling in self.analysis_data.variable:
                            self.analysis_data.variable[data.spelling]['last'] = position_in_code
                            if not self.analysis_data.variable[data.spelling]['first']:
                                self.analysis_data.variable[data.spelling]['first'] = position_in_code

                        elif data.spelling in self.analysis_data.parameter:
                            self.analysis_data.parameter[data.spelling] = position_in_code

            i += 1

        if self.analysis_data.nested_cnt_max < self.current_cnt:
            self.analysis_data.nested_cnt_max = self.current_cnt