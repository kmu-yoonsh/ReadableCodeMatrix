from clang.cindex import CursorKind

class AnalysisData(object):
    """
    This class is data class that record result of analyze code by function.
    And, also record global variable in code and list used condition check.
    """
    def __init__(self):
        self.conditional_list = [CursorKind.IF_STMT, CursorKind.FOR_STMT, CursorKind.WHILE_STMT, CursorKind.DO_STMT]

        self.check_list = {'do/while': list(), 'goto': list()}

        self.variable = dict()  # element - 'variable name': {'declare': declare line, 'first': first using line, 'last': last using line}
        self.parameter = dict()  # element - 'variable name': 'using line'
        self.used_function = list() # element - 'function name'(called function in function)
        self.declared_variable_name = dict()    # element - 'variable name' : ['declare line']
        self.conditional = dict()   # element - 'conditional statement': [line, nested count]
        self.duplicated_variable = list()   # element - [variable name, line]
        self.nested_cnt_max = 0

        self.function_name = None

        self.global_variable = dict()   # element = 'global variable name': [using function name]


    def set_init_data(self):
        self.check_list = {'do/while': list(), 'goto': list()}

        self.variable = dict()
        self.parameter = dict()
        self.used_function = list()
        self.declared_variable_name = dict()
        self.conditional = dict()
        self.duplicated_variable = list()  # element - [variable name, line]
        self.nested_cnt_max = 0

        self.function_name = None