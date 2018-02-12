import os
import clang.cindex


class Parser(object):
    def __init__(self, path):
        self.path = path
        self.isDir = os.path.isdir(path)
        self.savePath = path if self.isDir else './'


    # Exclude header file from parsing
    def _preprocess(self, file, ext):
        fileName = 'readableCheckTemporaryFile' + ext
        with open(os.path.join(self.savePath, fileName), 'w') as fw:
            fp = open(file)
            lines = fp.readlines()
            for line in lines:
                if '#include' not in line:
                    fw.write(line)
        return fileName


    def _toList(self, ast):
        temp = list()
        for child in ast.get_children():
            temp.append(child)
            if len(list(child.get_children())) > 0:
                temp.append(self.toList(child))

        return temp


    def parser(self, file, ext):
        try:
            fileName = self.preprocess(os.path.join(self.savePath, file), ext)

            index = clang.cindex.Index.create()
            tu = index.parse(os.path.join(self.savePath, fileName))
            ast = tu.cursor

        except Exception as e:
            print e

        return self.toList(ast)