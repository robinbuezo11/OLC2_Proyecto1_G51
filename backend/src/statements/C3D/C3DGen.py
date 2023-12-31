from statements.C3D.Instruction import Instruction
from statements.C3D.Type import Type
from utils.Type import Type as TypeData
from statements.C3D.Label import Label
from statements.C3D.If import If
from statements.C3D.Goto import Goto
from statements.C3D.Asign import Asign
from statements.C3D.Expression import Expression
from statements.C3D.Generic import Generic
from statements.C3D.Printf import Printf
from statements.C3D.Function import Function
from statements.C3D.Return import Return
from statements.C3D.End import End
from statements.C3D.CallFunction import CallFunction
from statements.C3D.SetHeap import SetHeap
from statements.C3D.GetHeap import GetHeap
from statements.C3D.SetStack import SetStack
from statements.C3D.GetStack import GetStack

class C3DGen:
    def __init__(self):
        self.labelCount: int = 0
        self.temporalCount: int = 0
        self.name: str
        self.C3DCode: list[Instruction] = []
        self.C3DMain: list[Instruction] = []
        self.C3DNatives: list[Instruction] = []
        self.C3DFunctions: list[Instruction] = []
        self.C3DGlobals: list[Instruction] = []
        self.temporalsSaved: dict[str, str] = {}
        self.temporals: list = []
        self.thereIsPow: bool = False
        self.thereIsMod: bool = False
        self.thereIsPrintString = False
        self.thereIsConcatString = False
        self.thereIsIntToString = False
        self.thereIsDoubleToString = False
        self.thereIsCharToString = False
        self.thereAreDeclarations = False
        self.keys: list[bool] = [False, False, False, False]
        self.tmpKeys: list[bool] = [k for k in self.keys]

    def thereAreDeclarations(self) -> bool:
        return self.thereAreDeclarations

    def setFileName(self, name: str):
        self.name = name

    def enableMain(self):
        self.keys = [True, False, False, False]

    def enableNatives(self):
        self.keys = [False, True, False, False]

    def enableFunction(self):
        self.keys = [False, False, True, False]

    def enableGlobal(self):
        self.keys = [False, False, False, True]

    def isMain(self):
        return self.keys[0]

    def isNative(self):
        return self.keys[1]

    def isFunction(self):
        return self.keys[2]

    def isGlobal(self):
        return self.keys[3]

    def saveSetting(self):
        for i in range(len(self.keys)):
            self.tmpKeys[i] = self.keys[i]

    def restoreSetting(self):
        for i in range(len(self.tmpKeys)):
            self.keys[i] = self.tmpKeys[i]

    def newTmp(self):
        tmp: str = f't{self.temporalCount}'
        self.temporalCount += 1
        self.temporals.append(tmp)
        self.temporalsSaved[tmp] = tmp
        return tmp

    def newLbl(self):
        lbl: str = f'L{self.labelCount}'
        self.labelCount += 1
        return lbl

    def validLabel(self, lbl: str):
        if lbl == None:
            return self.newLbl()
        return lbl

    def addInstruction(self, instruction: Instruction):
        if self.keys[0]:
            self.C3DMain.append(instruction)
        elif self.keys[1]:
            self.C3DNatives.append(instruction)
        elif self.keys[2]:
            self.C3DFunctions.append(instruction)
        elif self.keys[3]:
            self.C3DGlobals.append(instruction)

    def repeatedGoto(self, instruction: Instruction):
        if self.keys[0]:
            if self.C3DMain[len(self.C3DMain) - 1].type == Type.GOTO and str(self.C3DMain[len(self.C3DMain) - 1]) == str(instruction):
                return True
        elif self.keys[1]:
            if self.C3DNatives[len(self.C3DNatives) - 1].type == Type.GOTO and str(self.C3DNatives[len(self.C3DNatives) - 1]) == str(instruction):
                return True
        elif self.keys[2]:
            if self.C3DNatives[len(self.C3DFunctions) - 1].type == Type.GOTO and str(self.C3DFunctions[len(self.C3DFunctions) - 1]) == str(instruction):
                return True
        elif self.keys[3]:
            if self.C3DGlobals[len(self.C3DGlobals) - 1].type == Type.GOTO and str(self.C3DGlobals[len(self.C3DGlobals) - 1]) == str(instruction):
                return True
        return False

    def addLabel(self, lbl: str):
        self.addInstruction(Label(lbl))

    def addIf(self, left: str, operator: str, right: str, lbl: str):
        self.addInstruction(If(left, operator, right, lbl))

    def addGoto(self, lbl: str):
        if not self.repeatedGoto(Goto(lbl)):
            self.addInstruction(Goto(lbl))

    def addAsign(self, target: str, value: str):
        self.addInstruction(Asign(target, value))

    def addExpression(self, target: str, left: str, operator: str, right: str):
        self.addInstruction(Expression(target, left, operator, right))

    def addComment(self, comment: str):
        self.addInstruction(Generic('\t/* ' + comment + ' */'))

    def addPrintf(self, type: str, value: str):
        self.addInstruction(Printf(type, value))

    def addPrint(self, value: str):
        for ascii in value:
            self.addPrintf('c', '(char) ' + str(ord(ascii)))

    def addFunction(self, id: str):
        self.addInstruction(Function(id))

    def addEnd(self):
        self.addInstruction(Return())
        self.addInstruction(End())

    def addCall(self, id: str):
        self.addInstruction(CallFunction(id))

    def addSetHeap(self, index: str, value: str):
        self.addInstruction(SetHeap(index, value))

    def addGetHeap(self, target: str, index: str):
        self.addInstruction(GetHeap(target, index))

    def addSetStack(self, index: str, value: str):
        self.addInstruction(SetStack(index, value))

    def addSetStackB(self, index: str, value: str):
        self.addInstruction(SetStack(index, value))

    def addGetStack(self, target: str, index: str):
        self.addInstruction(GetStack(target, index))

    def nextHeap(self):
        self.addInstruction(Expression('H','H','+','1'))

    def newEnv(self, size: int):
        self.addInstruction(Expression('P','P','+',str(size)))

    def prevEnv(self, size: int):
        self.addInstruction(Expression('P','P','-',str(size)))

    def addDeclaration(self, declaration: str):
        self.declarations.append(declaration)

    def generatePrintString(self):
        if not self.thereIsPrintString:
            # Temporales y etiquetas
            tmp1: str = self.newTmp()
            tmp2: str = self.newTmp()
            tmp3: str = self.newTmp()
            lbl1: str = self.newLbl()
            lbl2: str = self.newLbl()
            # =========
            self.saveSetting()
            self.enableNatives()
            # =========
            self.addFunction('_printString')
            self.addExpression(tmp1, 'P', '+', '1')
            self.addGetStack(tmp2, tmp1)
            self.addLabel(lbl1)
            self.addGetHeap(tmp3, tmp2)
            self.addIf(tmp3, '==', '-1', lbl2)
            self.addPrintf('c', '(char) ' + tmp3)
            self.addExpression(tmp2, tmp2, '+', '1')
            self.addGoto(lbl1)
            self.addLabel(lbl2)
            self.addEnd()
            # =========
            self.restoreSetting()
            self.thereIsPrintString = True

    def generateConcatString(self):
        if not self.thereIsConcatString:
            # Temporales y etiquetas
            tmp1: str = self.newTmp()
            tmp2: str = self.newTmp()
            tmp3: str = self.newTmp()
            tmp4: str = self.newTmp()
            lbl1: str = self.newLbl()
            lbl2: str = self.newLbl()
            lbl3: str = self.newLbl()
            lbl4: str = self.newLbl()
            # =========
            self.saveSetting()
            self.enableNatives()
            # =========
            self.addFunction('_concatstring')
            self.addAsign(tmp1, 'H')
            self.addExpression(tmp2, 'P', '+', '1')
            self.addGetStack(tmp3, tmp2)
            self.addLabel(lbl1)
            self.addGetHeap(tmp4, tmp3)
            self.addIf(tmp4, '==', '-1', lbl2)
            self.addSetHeap('H', tmp4)
            self.nextHeap()
            self.addExpression(tmp3, tmp3, '+', '1')
            self.addGoto(lbl1)
            self.addLabel(lbl2)
            self.addExpression(tmp2, 'P', '+', '2')
            self.addGetStack(tmp3, tmp2)
            self.addLabel(lbl3)
            self.addGetHeap(tmp4, tmp3)
            self.addIf(tmp4, '==', '-1', lbl4)
            self.addSetHeap('H', tmp4)
            self.nextHeap()
            self.addExpression(tmp3, tmp3, '+', '1')
            self.addGoto(lbl3)
            self.addLabel(lbl4)
            self.addSetHeap('H', '-1')
            self.nextHeap()
            self.addSetStack('P', tmp1)
            self.addEnd()
            # =========
            self.restoreSetting()
            self.thereIsConcatString = True

    def generateIntToString(self):
        if not self.thereIsIntToString:
            # Temporales y etiquetas
            tmp1: str = self.newTmp()
            tmp2: str = self.newTmp()
            tmp3: str = self.newTmp()
            tmp4: str = self.newTmp()
            tmp5: str = self.newTmp()
            tmp6: str = self.newTmp()
            tmp7: str = self.newTmp()
            lbl1: str = self.newLbl()
            lbl2: str = self.newLbl()
            lbl3: str = self.newLbl()
            lbl4: str = self.newLbl()
            lbl5: str = self.newLbl()
            lbl6: str = self.newLbl()
            # =========
            self.saveSetting()
            self.enableNatives()
            # =========
            self.addFunction('_intToString')
            self.addAsign(tmp1, 'H')
            self.addExpression(tmp2, 'P', '+', '1')
            self.addGetStack(tmp3, tmp2)
            self.addIf(tmp3, '==', '0', lbl5)
            self.addIf(tmp3, '>', '0', lbl1)
            self.addAsign(tmp3, '-' + tmp3)
            self.addSetHeap('H', '45')
            self.nextHeap()
            self.addLabel(lbl1)
            self.addAsign(tmp4, tmp3)
            self.addAsign(tmp5, tmp3)
            self.addAsign(tmp6, '0')
            self.addAsign(tmp7, '1')
            self.addLabel(lbl2)
            self.addIf(tmp4, '<', '1', lbl3)
            self.addExpression(tmp7, tmp7, '*', '10')
            self.addExpression(tmp4, tmp4, '/', '10')
            self.addGoto(lbl2)
            self.addLabel(lbl3)
            self.addExpression(tmp7, tmp7, '/', '10')
            self.addLabel(lbl4)
            self.addIf(tmp7, '<', '1', lbl6)
            self.addExpression(tmp5, tmp3, '/', tmp7)
            self.addExpression(tmp6, tmp5, '+', '48')
            self.addSetHeap('H', tmp6)
            self.nextHeap()
            self.addExpression(tmp3, '(int) ' + tmp3, '%', '(int) ' + tmp7)
            self.addExpression(tmp7, tmp7, '/', '10')
            self.addGoto(lbl4)
            self.addLabel(lbl5)
            self.addSetHeap('H', '48')
            self.nextHeap()
            self.addLabel(lbl6)
            self.addSetHeap('H', '-1')
            self.nextHeap()
            self.addSetStack('P', tmp1)
            self.addEnd()
            # =========
            self.restoreSetting()
            self.thereIsIntToString = True

    def generateDoubleToString(self):
        if not self.thereIsDoubleToString:
            # Temporales y etiquetas
            tmp1: str = self.newTmp()
            tmp2: str = self.newTmp()
            tmp3: str = self.newTmp()
            tmp4: str = self.newTmp()
            tmp5: str = self.newTmp()
            tmp6: str = self.newTmp()
            tmp7: str = self.newTmp()
            tmp8: str = self.newTmp()
            lbl1: str = self.newLbl()
            lbl2: str = self.newLbl()
            lbl3: str = self.newLbl()
            lbl4: str = self.newLbl()
            lbl5: str = self.newLbl()
            lbl6: str = self.newLbl()
            lbl7: str = self.newLbl()
            lbl8: str = self.newLbl()
            lbl9: str = self.newLbl()
            lblA: str = self.newLbl()
            # =========
            self.saveSetting()
            self.enableNatives()
            # =========
            self.addFunction('_doubleToString')
            self.addAsign(tmp1, 'H')
            self.addExpression(tmp2, 'P', '+', '1')
            self.addGetStack(tmp3, tmp2)
            self.addAsign(tmp8, '(int) ' + tmp3)
            self.addIf(tmp8, '==', '0', lbl5)
            self.addIf(tmp3, '>', '0', lbl1)
            self.addAsign(tmp3, '-' + tmp3)
            self.addSetHeap('H', '45')
            self.nextHeap()
            self.addLabel(lbl1)
            self.addAsign(tmp4, tmp3)
            self.addAsign(tmp5, tmp3)
            self.addAsign(tmp6, '0')
            self.addAsign(tmp7, '1')
            self.addLabel(lbl2)
            self.addIf(tmp4, '<', '1', lbl3)
            self.addExpression(tmp7, tmp7, '*', '10')
            self.addExpression(tmp4, tmp4, '/', '10')
            self.addGoto(lbl2)
            self.addLabel(lbl3)
            self.addExpression(tmp7, tmp7, '/', '10')
            self.addLabel(lbl4)
            self.addIf(tmp7, '<', '1', lbl6)
            self.addExpression(tmp5, tmp3, '/', tmp7)
            self.addExpression(tmp6, tmp5, '+', '48')
            self.addSetHeap('H', tmp6)
            self.nextHeap()
            self.addExpression(tmp3, tmp3, '-', '(int) ' + tmp5)
            self.addExpression(tmp7, tmp7, '/', '10')
            self.addGoto(lbl4)
            self.addLabel(lbl5)
            self.addSetHeap('H', '48')
            self.nextHeap()
            self.addLabel(lbl6)
            self.addSetHeap('H', '46')
            self.nextHeap()
            self.addIf(tmp3, '==', '0', lbl7)
            self.addGoto(lbl8)
            self.addLabel(lbl7)
            self.addSetHeap('H', '48')
            self.nextHeap()
            self.addGoto(lblA)
            self.addLabel(lbl8)
            self.addAsign(tmp4, '0')
            self.addLabel(lbl9)
            self.addIf(tmp4, '>=', '4', lblA)
            self.addIf(tmp3, '==', '0', lblA)
            self.addExpression(tmp3, tmp3, '*', '10')
            self.addExpression(tmp6, tmp3, '+', '48')
            self.addSetHeap('H', tmp6)
            self.nextHeap()
            self.addExpression(tmp3, tmp3, '-', '(int) ' + tmp3)
            self.addExpression(tmp4, tmp4, '+', '1')
            self.addGoto(lbl9)
            self.addLabel(lblA)
            self.addSetHeap('H', '-1')
            self.nextHeap()
            self.addSetStack('P', tmp1)
            self.addEnd()
            # =========
            self.restoreSetting()
            self.thereIsDoubleToString = True

    def generateCharToString(self):
        if not self.thereIsCharToString:
            # Temporales y etiquetas
            tmp1: str = self.newTmp()
            tmp2: str = self.newTmp()
            tmp3: str = self.newTmp()
            tmp4: str = self.newTmp()
            # =========
            self.saveSetting()
            self.enableNatives()
            # =========
            self.addFunction("_charToString")
            self.addExpression(tmp1, "P", "+", "1")
            self.addGetStack(tmp2, tmp1)
            self.addAsign(tmp3, "H")
            self.addAsign(tmp4, "H")
            self.addSetHeap(tmp3, tmp2)
            self.nextHeap()
            self.addExpression(tmp3, tmp3, "+", "1")
            self.addSetHeap(tmp3, "-1")
            self.nextHeap()
            self.addSetStack("P", tmp4)
            self.addEnd()
            # =========
            self.restoreSetting()
            self.thereIsCharToString = True

    def generateParserString(self, type: TypeData):
        match type:
            case TypeData.INT:
                self.generateIntToString()
            case TypeData.DECIMAL:
                self.generateDoubleToString()
            case TypeData.NVARCHAR:
                self.generateCharToString()
            case _:
                pass

    def addCallParserString(self, type: TypeData):
        match type:
            case TypeData.INT:
                self.addCall('_intToString')
            case TypeData.DECIMAL:
                self.addCall('_doubleToString')
            case TypeData.NVARCHAR:
                self.addCall('_charToString')
            case _:
                pass

    def generateFinalCode(self):
        self.C3DCode.append(Generic("/* ----- HEADER ----- */"))
        self.C3DCode.append(Generic("#include <stdio.h>"))
        self.C3DCode.append(Generic(""))
        self.C3DCode.append(Generic("float heap[30101999];"))
        self.C3DCode.append(Generic("float stack[30101999];"))
        self.C3DCode.append(Generic("float P;"))
        self.C3DCode.append(Generic("float H;"))
        if len(self.temporals) > 0:
            self.C3DCode.append(Generic(f"float {', '.join(map(str, self.temporals))};"))
        self.C3DCode.append(Generic(''))
        # Native
        if len(self.C3DNatives) > 0:
            self.C3DCode.append(Generic("/* ------ NATIVES ------ */"))
            for s in self.C3DNatives:
                self.C3DCode.append(s)
        # Main
        self.C3DCode.append(Generic("/* ------ MAIN ------ */"))
        self.C3DCode.append(Generic("int main() {"))
        self.C3DCode.append(Generic("\tP = 0;"))
        self.C3DCode.append(Generic("\tH = 0;"))
        if len(self.C3DGlobals) > 0:
            self.C3DCode.append(Generic("/* ---- GLOBALES ---- */"))
            for s in self.C3DGlobals:
                self.C3DCode.append(s)
            self.C3DCode.append(Generic("/* -- END GLOBALES -- */"))
        if len(self.C3DCode) > 0:
            for s in self.C3DMain:
                self.C3DCode.append(s)
        self.C3DCode.append(Generic("\treturn 0;\n}"))

    def getFinalCode(self):
        newLabels: dict[str, int] = {}
        id: int = 0
        for i in range(len(self.C3DCode)):
            if self.C3DCode[i].type == Type.LABEL:
                newLabels[self.C3DCode[i].lbl] = id
                id += 1
        for i in range(len(self.C3DCode)):
            if self.C3DCode[i].type == Type.GOTO or self.C3DCode[i].type == Type.IF or self.C3DCode[i].type == Type.LABEL:
                self.C3DCode[i].changeLbl(newLabels)
        newTemps: dict[str, int] = {}
        types: list[Type] = [Type.CALLFUNCTION, Type.END, Type.FUNCTION, Type.GENERIC, Type.GOTO, Type.LABEL, Type.RETURN]
        id = 0
        for i in range(len(self.C3DCode)):
            # Verificar si el tipo no está en la lista types
            if not self.C3DCode[i].type in types:
                # Verificar otras condiciones
                if (
                    self.C3DCode[i].target and
                    not self.C3DCode[i].target in newTemps and
                    self.C3DCode[i].target != "H" and
                    self.C3DCode[i].target != "P"
                ):
                    # Agregar la entrada al diccionario newTemps y actualizar id
                    newTemps[self.C3DCode[i].target] = id
                    id += 1
        for i in range(len(self.C3DCode)):
            if not self.C3DCode[i].type in types:
                self.C3DCode[i].changeTmp(newTemps)
        return "\n".join(str(instruction) for instruction in self.C3DCode)