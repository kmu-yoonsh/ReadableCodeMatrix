import os
import clang.cindex
from message import TEMP_FILE_NAME


class Parsing(object):
    def __init__(self, save_path):
        self.save_path = save_path
        self.delete_line_count = 0


    # Exclude header file from parsing
    def _preprocess(self, file, ext):
        fileName = TEMP_FILE_NAME + ext

        with open(os.path.join(self.save_path, fileName), 'w') as fw:
            fp = open(file)
            code = fp.read()
            fw.write(code)

        return fileName


    def _toList(self, ast):
        temp = list()
        for child in ast.get_children():
            if str(child.location.file).find(TEMP_FILE_NAME) != -1:
                # temp.append("{}-{}".format(child.spelling, child.kind))
                temp.append(child)
                if len(list(child.get_children())) > 0:
                    temp.append(self._toList(child))

        return temp

    def parser(self, file, ext):
        try:
            file_name = self._preprocess(os.path.join(self.save_path, file), ext)

            index = clang.cindex.Index.create()
            tu = index.parse(os.path.join(self.save_path, file_name))
            ast = tu.cursor

            return self._toList(ast)
        except Exception as e:
            print e
