import os
import re
from clang.cindex import CursorKind


class Function(object):
    def __init__(self):
        self.underscore = re.compile('[_a-z]+')
        self.camelcase = re.compile('[a-z]+([A-Z][a-z]+)*')

        self.line_count = 0
        self.nested_count = 0
        self.maximum_nested_count = 0
        self.check_list = {'do/while': list(), 'goto': list()}

        self.variable = dict()    # element: 'value name': {'declare': declare line, 'first': first using line, 'last': last using line}

        self.root = None
        self.global_variable = None
        self.function_name = None


    def set_init_data(self, root, function_name, global_variable):
        self.root = root
        self.global_variable = global_variable
        self.function_name = function_name

        self.line_count = 0
        self.nested_count = 0
        self.maximum_nested_count = 0
        self.check_list = {'do/while': list(), 'goto': list()}

        self.variable = dict()


    def check_naming_rule(self):
        result = list()

        for variable in self.variable:
            if self.underscore.match(variable) is None:
                result.append(False)
                break
        else:
            result.append(True)

        for variable in self.variable:
            if self.camelcase.match(variable) is None:
                result.append(False)
                break
        else:
            result.append(True)

        return result   # [result of underscore rule, result of camelcase rule] - True: pass, False: non-pass


    def check_unusing_variable(self):
        result = list()

        for key in self.variable:
            if self.variable[key]['first'] == self.variable[key]['declare']:
                result.append(self.variable[key]['declare'])

        return result

    def check_function(self):
        self.walk(self.root)

        return {'variable': self.variable, 'naming_rule': self.check_naming_rule(),
                'unused_variable': self.check_unusing_variable(), 'nested_count': self.maximum_nested_count,
                'do/while': self.check_list['do/while'], 'goto': self.check_list['goto']}


    def walk(self, ast):
        i = 0
        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                position_in_code = data.location.line

                if not(data.spelling in self.variable) and data.kind is CursorKind.VAR_DECL:
                    self.variable[data.spelling] = {'declare': position_in_code, 'first': position_in_code, 'last': 0}

                if data.kind is CursorKind.FUNCTION_DECL:
                    func = Function(ast[i + 1])
                    print func.check_function()

                elif data.kind is CursorKind.IF_STMT:
                    pass

                elif data.kind is CursorKind.DO_STMT:
                    self.check_list['do/while'].append(position_in_code)

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    self.check_list['goto'].append(position_in_code)

                elif data.spelling:
                    if (data.spelling in self.global_variable) and (self.function_name not in self.global_variable[data.spelling]):
                        self.global_variable[data.spelling].append(position_in_code)

                    elif data.spelling in self.variable:
                        self.variable[data.spelling]['last'] = position_in_code
                        if not self.variable[data.spelling]['first']:
                            self.variable[data.spelling]['first'] = position_in_code

            i += 1



# is_declaration, is_reference, is_expression, is_statement, is_attribute