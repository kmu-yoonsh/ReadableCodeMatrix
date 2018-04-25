from clang.cindex import CursorKind, Cursor


class InnerStmt(object):
    def __init__(self, analysis_data):
        self.current_cnt = 0
        self.function_name = None
        self.if_stmt_depth = 0
        self.condition_list = list()

        self.analysis_data = analysis_data


    def set_init_data(self, function_name):
        self.current_cnt = 0
        self.if_stmt_depth = 0
        self.condition_list = list()
        self.function_name = function_name


    # def get_condition(self, ast):
    #     i = 0
    #     condition_list = list()
    #     while i < len(ast):
    #         data = ast[i]
    #         if type(data) is list:
    #             self.get_condition(data)
    #         pass


    def check_if_condition(self, condition_stmt):
        check_line = condition_stmt[0].location.line
        if len(condition_stmt) > 4:
            operation = target = None
            # if statement check
            temp_stmt = condition_stmt[2:]  # remove conditional statement
            if temp_stmt[0].kind is CursorKind.COMPOUND_STMT:
                if len(temp_stmt[1]) > 2:
                    return
                temp_stmt = temp_stmt[1]
            if temp_stmt[0].kind is CursorKind.BINARY_OPERATOR or temp_stmt[0].kind is CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
                operation, target = temp_stmt[0].kind, temp_stmt[1][0].spelling

            # else statement check
            temp_stmt = condition_stmt[4:]  # remove conditional statement & if statement
            if temp_stmt[0].kind is CursorKind.COMPOUND_STMT:
                if len(temp_stmt[1]) > 2:
                    return
                temp_stmt = temp_stmt[1]
            if temp_stmt[0].kind is CursorKind.BINARY_OPERATOR or temp_stmt[0].kind is CursorKind.COMPOUND_ASSIGNMENT_OPERATOR:
                if operation == temp_stmt[0].kind and target == temp_stmt[1][0].spelling:
                    self.analysis_data.ternary_operator.append(check_line)
            return

        temp_stmt = condition_stmt[2:]
        if temp_stmt[0].kind is CursorKind.COMPOUND_STMT:
            try:
                temp_stmt = temp_stmt[1]
            except IndexError as e:
                return
        if temp_stmt[0].kind is CursorKind.IF_STMT and len(temp_stmt[1]) <= 4:
            self.analysis_data.condition_combine.append(check_line)


    def check_condition_order(self, ast):
        i = 0
        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.check_condition_order(data)
            else:
                if data.kind is CursorKind.BINARY_OPERATOR:
                    # if [data.kind, ast[i + 1]] in self.condition_list:
                    #     pass
                    # else:
                    #     pass
                    # if
                    if (isinstance(ast[i + 1][0], Cursor) and not (105 < ast[i + 1][0].kind.value < 111)) or \
                            (isinstance(ast[i + 1][1], Cursor) and (105 < ast[i + 1][1].kind.value < 111)):
                        if self.analysis_data.get_binary_operator(data.location.line, data.location.column)[0] is 3:
                            self.analysis_data.condition_order.append(data.location.line)
            i += 1


    def walk(self, ast):
        i = 0
        while i < len(ast):
            data = ast[i]
            if type(data) is list:
                self.walk(data)
            else:
                if data.kind is CursorKind.VAR_DECL and data.kind.is_declaration():
                    if data.spelling in self.analysis_data.variable or data.spelling in self.analysis_data.global_variable:
                        if data.spelling not in self.analysis_data.duplicated_variable:
                            self.analysis_data.duplicated_variable[data.spelling] = list()
                        self.analysis_data.duplicated_variable[data.spelling].append(data.location.line)
                    else:
                        self.analysis_data.variable[data.spelling] = {'declare': data.location.line, 'last': 0}
                        self.analysis_data.variable[data.spelling]['assign'] = data.location.line if len(ast) is 2 else 0

                elif data.kind is CursorKind.GOTO_STMT or data.kind is CursorKind.INDIRECT_GOTO_STMT:
                    self.analysis_data.check_list['goto'].append(data.location.line)

                elif data.kind in self.analysis_data.conditional_list:
                    self.current_cnt += 1
                    self.analysis_data.inner_stmt.append([data.kind.name, data.location.line, self.current_cnt])

                    if data.kind is CursorKind.DO_STMT:
                        self.analysis_data.check_list['do/while'].append(data.location.line)
                        self.walk(ast[i + 1])
                        i += 1

                    elif data.kind is CursorKind.IF_STMT or data.kind is CursorKind.WHILE_STMT:
                        self.check_condition_order([ast[i + 1][0], ast[i + 1][1]])
                        if data.kind is CursorKind.IF_STMT:
                            self.check_if_condition(ast[i + 1])

                        self.walk(ast[i + 1])
                        i += 1

                    self.current_cnt -= 1

                elif data.kind is CursorKind.CALL_EXPR and data.spelling not in self.analysis_data.used_function:
                    self.analysis_data.used_function.append(data.spelling)

                elif data.spelling:
                    if (data.spelling in self.analysis_data.global_variable) and (
                            self.function_name not in self.analysis_data.global_variable[data.spelling]):
                        self.analysis_data.global_variable[data.spelling].append(self.function_name)

                    elif data.kind is CursorKind.DECL_REF_EXPR:# or data.kind is CursorKind.UNEXPOSED_EXPR:
                        if data.spelling in self.analysis_data.variable:
                            if self.analysis_data.variable[data.spelling]['assign']:
                                self.analysis_data.variable[data.spelling]['last'] = data.location.line
                            else:
                                self.analysis_data.variable[data.spelling]['assign'] = data.location.line

                        elif data.spelling in self.analysis_data.parameter:
                            self.analysis_data.parameter[data.spelling] = data.location.line

            i += 1

        if self.analysis_data.nested_cnt_max < self.current_cnt:
            self.analysis_data.nested_cnt_max = self.current_cnt
