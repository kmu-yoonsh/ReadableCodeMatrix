import os
import re
from clang.cindex import CursorKind



class Function(object):
    def __init__(self, root):
        self.nestedCount = 0
        self.maximumNestedCount = 0
        self.lineCount = 0

        self.check_list = {'namingRule': list(), 'varName': list(), 'doWhile': list(), 'goto': list()}
        self.variable_dict = dict()    # element: 'value name': {'declare': declare line, 'first': first using line, 'last': last using line}

        self.underscore = re.compile('[_a-z]+')
        self.camelcase = re.compile('[a-z]+([A-Z][a-z]+)*')

        self.root = root


    def check_naming_rule(self):
        underscore = [1 if self.underscore.match(variable) else 0 for variable in self.variable_dict]
        camelcase = [1 if self.camelcase.match(variable) else 0 for variable in self.variable_dict]

        return True if sum(underscore) == len(self.variable_dict) or sum(camelcase) == len(self.variable_dict) else False

    def check_unusing_variable(self):
        for key in self.variable_dict:
            if not self.variable_dict[key]['first']:
                return False

        return True

    def check_function(self):
        self.walk(self.root)

        return self.check_naming_rule(), self.check_unusing_variable()


    def walk(self, ast):
        i = 0
        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                # print '{} - {} : {}'.format(data.spelling, data.kind, data.location.line)
                if not(data.spelling in self.variable_dict) and data.kind is CursorKind.VAR_DECL:
                    self.variable_dict[data.spelling] = {'declare': data.location.line, 'first': 0, 'last': 0}

                elif data.kind is CursorKind.FUNCTION_DECL:
                    func = Function(ast[i + 1])
                    print func.check_function()

                elif data.kind is CursorKind.IF_STMT:
                    pass

                elif data.kind is CursorKind.DO_STMT:
                    pass

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    pass

                elif data.spelling and data.spelling in self.variable_dict:
                    self.variable_dict[data.spelling]['last'] = data.location.line
                    if not self.variable_dict[data.spelling]['first']: self.variable_dict[data.spelling]['first'] = data.location.line

            i += 1



# is_declaration, is_reference, is_expression, is_statement, is_attribute