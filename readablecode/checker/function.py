import os
import re
from clang.cindex import CursorKind
from .innerstmt import InnerStmt


class Function(object):
    def __init__(self, analysis_data):
        self.underscore = re.compile('^[_a-z]+$')
        self.camelcase = re.compile('^[a-z]+([A-Z][a-z]+)*$')

        self.analysis_data = analysis_data

        self.root = None
        self.function_name = None
        self.inner_stmt = None


    def set_init_data(self, root, function_name):
        self.root = root
        self.function_name = function_name
        self.inner_stmt = InnerStmt(self.analysis_data)


    # function for check variable
    def check_naming_rule(self):
        variable_list = self.analysis_data.variable.keys() + self.analysis_data.parameter.keys()

        # [result of underscore rule, result of camelcase rule] - True: pass, False: non-pass
        for variable in variable_list:
            if self.underscore.match(variable) is None:
                break
        else:
            return [True, False]

        for variable in variable_list:
            if self.camelcase.match(variable) is None:
                return [False, False]
        else:
            return [False, True]


    def check_unusing_variable(self):
        result = {'variable': list(), 'parameter': list()}

        for key in self.analysis_data.variable:
            if not self.analysis_data.variable[key]['last']:
                result['variable'].append({key: self.analysis_data.variable[key]['declare']})

        for key in self.analysis_data.parameter:
            if self.analysis_data.parameter[key] is 0:
                result['parameter'].append(key)

        return result

    def check_const_variable(self):
        temp_list = list()

        for i in self.analysis_data.variable:
            # print(i, self.analysis_data.reassign_variable)
            if i not in self.analysis_data.reassign_variable:
                temp_list.append(i)

        return temp_list

    def check_unsuitable_naming(self):
        result = {'too_short': list(), 'numbering': list()}
        variable_list = self.analysis_data.variable.keys() + self.analysis_data.parameter.keys()

        pattern_rex = re.compile('^[_a-z]+[0-9]+$', re.I)

        temp_numbering_count = dict()
        for variable in variable_list:
            if len(variable) < 3:
                result['too_short'].append(variable)

            if pattern_rex.match(variable):
                pattern = re.sub('[0-9]', '', variable).rstrip('_')
                if pattern in temp_numbering_count:
                    temp_numbering_count[pattern] += 1
                else:
                    temp_numbering_count[pattern] = 1

        for key in temp_numbering_count:
            if temp_numbering_count[key] > 1:
                result['numbering'].append(key)

        return result


    def check_function(self):
        self.walk(self.root)

        return {'variable': self.analysis_data.variable, 'naming_rule': self.check_naming_rule(),
                'unsuitable_naming': self.check_unsuitable_naming(), 'unused_variable': self.check_unusing_variable(),
                'const_variable': self.check_const_variable(), 'duplicate_variable': self.analysis_data.duplicated_variable,
                'condition_order': self.analysis_data.condition_order, 'condition_combine': self.analysis_data.condition_combine,
                'ternary_opt': self.analysis_data.ternary_operator, 'nested_count': self.analysis_data.nested_cnt_max,
                'do/while': self.analysis_data.check_list['do/while'], 'goto': self.analysis_data.check_list['goto'],
                'used_function': self.analysis_data.used_function}


    def walk(self, ast):
        i = 0

        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                if data.kind is CursorKind.VAR_DECL:# and data.kind.is_declaration():
                    if data.spelling in self.analysis_data.variable or data.spelling in self.analysis_data.global_variable:
                        if data.spelling not in self.analysis_data.duplicated_variable:
                            self.analysis_data.duplicated_variable[data.spelling] = list()
                        self.analysis_data.duplicated_variable[data.spelling].append(data.location.line)
                    else:
                        self.analysis_data.variable[data.spelling] = {'declare': data.location.line, 'last': 0}
                        self.analysis_data.variable[data.spelling]['assign'] = data.location.line if len(ast) is 2 else 0

                elif data.kind is CursorKind.PARM_DECL:
                    self.analysis_data.parameter[data.spelling] = 0

                elif data.kind is CursorKind.FUNCTION_DECL:
                    func = Function(ast[i + 1])
                    func.check_function()

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    self.analysis_data.check_list['goto'].append(data.location.line)

                elif data.kind in self.analysis_data.conditional_list:
                    if data.kind is CursorKind.DO_STMT:
                        self.analysis_data.check_list['do/while'].append(data.location.line)

                    self.inner_stmt.set_init_data(self.function_name)
                    self.inner_stmt.walk([data, ast[i + 1]])
                    i += 1

                elif data.kind is CursorKind.CALL_EXPR and data.spelling not in self.analysis_data.used_function:
                    self.analysis_data.used_function.append(data.spelling)

                elif data.kind is CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
                    if data.spelling in self.analysis_data.variable:
                        self.analysis_data.reassign_variable.append(
                            self.analysis_data.get_binary_operator(data.location.line,data.location.column)[2]
                        )
                    elif data.spelling in self.analysis_data.global_variable:
                        self.analysis_data.global_variable[data.spelling][self.function_name] = 1

                elif data.kind is CursorKind.BINARY_OPERATOR:
                    temp_data = self.analysis_data.get_binary_operator(data.location.line, data.location.column)
                    if temp_data[0] is 1:
                        if temp_data[2] in self.analysis_data.variable:
                            self.analysis_data.reassign_variable.append(temp_data[2])
                        elif temp_data[2] in self.analysis_data.global_variable:
                            self.analysis_data.global_variable[temp_data[2]][self.function_name] = 1

                elif data.spelling:
                    if (data.spelling in self.analysis_data.global_variable) and \
                            (self.function_name not in self.analysis_data.global_variable[data.spelling]):
                        self.analysis_data.global_variable[data.spelling][self.function_name] = 0

                    elif data.kind is CursorKind.DECL_REF_EXPR:# or data.kind is CursorKind.UNEXPOSED_EXPR:
                        if data.spelling in self.analysis_data.variable:
                            if self.analysis_data.variable[data.spelling]['assign']:
                                self.analysis_data.variable[data.spelling]['last'] = data.location.line
                            else:
                                self.analysis_data.variable[data.spelling]['assign'] = data.location.line

                        elif data.spelling in self.analysis_data.parameter:
                            self.analysis_data.parameter[data.spelling] = data.location.line

            i += 1