import os
from .parser import Parser
from clang.cindex import CursorKind

class RuleChecker(object):
    def __init__(self, path):
        self.path = path
        self.isDir = os.path.isdir(path)
        self.savePath = path if self.isDir else './'
        self.parser = Parser(self.path).parser

        self.checkList = {'namingRule': list(), 'varName': list(), 'doWhile': list(), 'goto': list()}
        self.valueList = list()
        self.messageList = list()

        self.nestedCntInFunc = 0


    def checkRule(self):
        fileList = os.listdir(self.path) if self.isDir else [self.path]

        for file in fileList:
            try:
                ext = os.path.splitext(file)[-1]
                if ext != '.c' and ext != '.cpp' and ext != '.h':
                    ast = self.parser(os.path.join(self.savePath, file), ext)
                    self.walk(ast)

            except Exception as e:
                print e


    def _chcekFunction(self, ast):
        pass


    def _walk(self, ast):
        i = 0
        while i < len(ast):
            if type(ast[i]) is list:
                self.walk(ast[i])
            elif ast[i].kind is CursorKind.IF_STMT:
                pass
            elif ast[i].kind is CursorKind.DO_STMT:
                self.checkList['doWhile'].append(ast[i].location.line)
            elif ast[i].kind is CursorKind.GOTO_STMT or ast[i].kind is CursorKind.INDIRECT_GOTO_STMT:
                self.checkList['goto'].append(ast[i].location.line)
            i += 1
