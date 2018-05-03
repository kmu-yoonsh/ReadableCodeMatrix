import re
from clang.cindex import CursorKind

class AnalysisData(object):
    """
    This class is data class that record result of analyze code by function.
    And, also record global variable in code and list used condition check.
    """
    def __init__(self):
        self.codes = None
        self.conditional_list = [CursorKind.IF_STMT, CursorKind.FOR_STMT, CursorKind.WHILE_STMT, CursorKind.DO_STMT]

        self.check_list = {'do/while': list(), 'goto': list()}

        self.global_variable = dict()  # element = 'global variable name': {'using function name': 'using type'} (using type - 0: normal, 1: assigned)
        self.macro_list = list()    # element = 'macro name'

        self.variable = dict()  # element - 'variable name': {'declare': declare line, 'first': first using line, 'last': last using line}
        self.declared_variable_name = dict()  # element - 'variable name' : ['declare line']
        self.duplicated_variable = dict()  # element - [line]
        self.index_variable = list()  # element - [variable name, line]
        self.parameter = dict()  # element - 'variable name': 'using line'
        self.reassign_variable = list() # element 'variable name'

        self.inner_stmt = list()  # element - [conditional statement, line, nested count]
        self.condition_order = list()  # element - line
        self.ternary_operator = list()  # element - if statement line
        self.condition_combine = list()  # element - if statement line

        self.nested_cnt_max = 0
        self.used_function = list()  # element - 'function name'(called function in function)

        self.function_name = None




    def set_init_data(self):
        self.check_list = {'do/while': list(), 'goto': list()}

        self.variable = dict()  # element - 'variable name': {'declare': declare line, 'first': first using line, 'last': last using line}
        self.declared_variable_name = dict()  # element - 'variable name' : ['declare line']
        self.duplicated_variable = dict()  # element - [line]
        self.index_variable = list()  # element - [variable name, line]
        self.parameter = dict()  # element - 'variable name': 'using line'
        self.reassign_variable = list()  # element 'variable name'

        self.inner_stmt = list()  # element - [conditional statement, line, nested count]
        self.condition_order = list()  # element - line
        self.ternary_operator = list()  # element - if statement line
        self.condition_combine = list()  # element - if statement line

        self.nested_cnt_max = 0
        self.used_function = list()  # element - 'function name'(called function in function)

        self.function_name = None


    def get_binary_operator(self, line, column):
        assign_opt = '[+-/*%]?='
        arithmetic_opt = '[+-/*%^]'
        etc_opt = '[-~!%^&*+=|/<>]+'
        # bit_opt = '[&~<<!|>>]'
        # comparison_opt = '(<>!)(=){0,2}'

        temp_code = self.codes[line - 1][column - 1:].replace(' ', '').strip()
        opts = re.findall(etc_opt, temp_code)[0]

        if opts:
            if re.search(assign_opt, opts[0]):
                return [1, opts[0]] + temp_code.split(opts[0], 1)
            elif re.search(arithmetic_opt, opts[0]):
                return [2, opts[0]] + temp_code.split(opts[0], 1)
            else:
                return [3, opts[0]] + temp_code.split(opts[0], 1)

        return [None, None, None, None]


    def __str__(self):
        return 'variabale: {}, parameter: {}, reassign_variabe: {}, used_function: {}, innerStmt: {}, duplicated_variable: {}, condition_order: {}, condition_combine: {}, ternary_opt: {}'.\
            format(self.variable, self.parameter, self.reassign_variable, self.used_function, self.inner_stmt,
                   self.duplicated_variable, self.condition_order, self.condition_combine, self.ternary_operator)