import os
import clang.cindex


class Parsing(object):
    def __init__(self, file_name):
        self.file_name = file_name


    def _toList(self, ast):
        temp = list()
        for child in ast.get_children():
            if str(child.location.file).find(self.file_name) != -1:
                # temp.append('{}-{}'.format(child.kind, child.spelling))
                temp.append(child)
                if len(list(child.get_children())) > 0:
                    temp.append(self._toList(child))

        return temp

    def parser(self, file_path):
        try:
            index = clang.cindex.Index.create()
            tu = index.parse(file_path)
            ast = tu.cursor

            return self._toList(ast)
        except Exception as e:
            print e
