import re
from C3D.Type import Type

class Instruction:
    def __init__(self, type):
        self.type: Type = type
        self.target: str
        self.value: str
        self.id: str
        self.left: str
        self.operator: str
        self.right: str
        self.index: str
        self.lbl: str

    def changeLbl(self, lbls: dict[str, int]):
        self.lbl = 'L' + str(lbls.get(self.lbl))

    def changeTmp(self, tmps: dict[str, int]):
        if self.target is not None and self.target != "H" and self.target != "P":
            if re.match(r"[t][0-9]+", self.target):
                self.target = "t" + str(tmps.get(self.target))
            elif re.match(r"\((int|char|float)\) [t][0-9]+", self.target):
                self.target = self.target.split(" ")[0] + " t" + str(tmps.get(self.target.split(" ")[1]))

        if self.value is not None and self.value != "H" and self.value != "P":
            if re.match(r"[t][0-9]+", self.value):
                self.value = "t" + str(tmps.get(self.value))
            elif re.match(r"\((int|char|float)\) [t][0-9]+", self.value):
                self.value = self.value.split(" ")[0] + " t" + str(tmps.get(self.value.split(" ")[1]))
            elif re.match(r"\-[t][0-9]+", self.value):
                self.value = "-t" + str(tmps.get(self.value[1:]))

        if self.left is not None and self.left != "H" and self.left != "P":
            if re.match(r"[t][0-9]+", self.left):
                self.left = "t" + str(tmps.get(self.left))
            elif re.match(r"\((int|char|float)\) [t][0-9]+", self.left):
                self.left = self.left.split(" ")[0] + " t" + str(tmps.get(self.left.split(" ")[1]))

        if self.right is not None and self.right != "H" and self.right != "P":
            if re.match(r"[t][0-9]+", self.right):
                self.right = "t" + str(tmps.get(self.right))
            elif re.match(r"\((int|char|float)\) [t][0-9]+", self.right):
                self.right = self.right.split(" ")[0] + " t" + str(tmps.get(self.right.split(" ")[1]))

        if self.index is not None and self.index != "H" and self.index != "P":
            if re.match(r"[t][0-9]+", self.index):
                self.index = "t" + str(tmps.get(self.index))
            elif re.match(r"\((int|char|float)\) [t][0-9]+", self.index):
                self.index = self.index.split(" ")[0] + " t" + str(tmps.get(self.index.split(" ")[1]))
