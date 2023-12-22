from ply.yacc import YaccProduction as Prod
from ply.lex import LexToken
# Tipos
from utils.Type import Type
# Instrucciones
from statements.Instructions.InitID import InitID
from statements.Instructions.AsignID import AsignID
from statements.Instructions.Select_prt import Select_prt
from statements.Instructions.If import If
from statements.Instructions.Block import Block
from statements.Instructions.While import While
from statements.Instructions.When import When
from statements.Instructions.Case import Case
from statements.Instructions.Function import Function
from statements.Instructions.CreateTable import CreateTable
from statements.Instructions.InsertTable import InsertTable
from statements.Instructions.UpdateTable import UpdateTable
from statements.Instructions.TruncateTable import TruncateTable
from statements.Instructions.DropTable import DropTable
from statements.Instructions.DeleteTable import DeleteTable
from statements.Instructions.Select import Select
from statements.Instructions.AlterTable import AlterTable
# Expresiones
from statements.Expressions.Primitive import Primitive
from statements.Expressions.AccessID import AccessID
from statements.Expressions.Field import Field
from statements.Expressions.Relational import Relational
from statements.Expressions.Arithmetic import Arithmetic
from statements.Expressions.Logic import Logic
from utils.Parameter import Parameter
from utils.Attribute import Attribute
from utils.ForeignKey import ForeignKey
from statements.Expressions.CallFunction import CallFunction
from statements.Expressions.Return import Return

precedence = (
    ('left', 'TK_or'),
    ('left', 'TK_and'),
    ('right', 'TK_not'),
    ('left', 'TK_equalequal', 'TK_notequal'),
    ('left', 'TK_less', 'TK_lessequal', 'TK_great', 'TK_greatequal'),
    ('left', 'TK_plus', 'TK_minus'),
    ('left', 'TK_mult', 'TK_div', 'TK_mod'),
    ('right', 'TK_uminus'),
)

def p_INIT(t: Prod):
    '''INIT : INSTRUCTIONS
            |'''
    if len(t) == 2 : t[0] = t[1]
    else           : t[0] = []

def p_INSTRUCTIONS(t: Prod):
    '''INSTRUCTIONS : INSTRUCTIONS INSTRUCTION
                    | INSTRUCTION'''
    if len(t) == 3 : t[1].append(t[2]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_INSTRUCTION(t: Prod):
    '''INSTRUCTION  : CREATEDB TK_semicolon
                    | CREATETABLE TK_semicolon
                    | ALTERTAB TK_semicolon
                    | DROPTAB TK_semicolon
                    | INSERTREG TK_semicolon
                    | UPDATETAB TK_semicolon
                    | TRUNCATETAB TK_semicolon
                    | DELETETAB TK_semicolon
                    | SELECT TK_semicolon
                    | DECLAREID TK_semicolon
                    | ASIGNID TK_semicolon
                    | IFSTRUCT TK_semicolon
                    | CASESTRUCT_S TK_semicolon
                    | WHILESTRUCT TK_semicolon
                    | FORSTRUCT TK_semicolon
                    | FUNCDEC TK_semicolon
                    | CALLFUNC TK_semicolon
                    | ENCAP TK_semicolon
                    | PRINT TK_semicolon
                    | RW_break TK_semicolon
                    | RW_continue TK_semicolon
                    | RW_return EXP TK_semicolon
                    | RW_return TK_semicolon'''
    types = ['RW_break', 'RW_continue', 'RW_return']
    if not t.slice[1].type in types                     : t[0] = t[1]
    elif t.slice[1].type == 'RW_break'                  : pass
    elif t.slice[1].type == 'RW_continue'               : pass
    elif t.slice[1].type == 'RW_return' and len(t) == 4 : t[0] = Return(t.lineno(1), t.lexpos(1), t[2])
    elif t.slice[1].type == 'RW_return'                 : t[0] = Return(t.lineno(1), t.lexpos(1), None)

# Crear DB
def p_CREATEDB(t: Prod):
    '''CREATEDB     : RW_create RW_data RW_base TK_field'''

# Declaración de Variables
def p_DECLAREID(t: Prod):
    '''DECLAREID    : RW_declare DECLIDS
                    | RW_declare TK_id TYPE TK_equal EXP'''
    if len(t) == 3:   t[0] = InitID(t.lineno(1), t.lexpos(1), t[2][0], t[2][1], None)
    elif len(t) == 6: t[0] = InitID(t.lineno(1), t.lexpos(1), t[2],    t[3],    t[5])

def p_DECLIDS(t: Prod):
    '''DECLIDS  : DECLIDS TK_comma DECLID
                | DECLID'''
    if len(t) == 4: t[1][0].append(t[3][0]); t[1][1].append(t[3][1]); t[0] = t[1]
    else:           t[0] = [[t[1][0]], [t[1][1]]]

def p_DECLID(t: Prod):
    '''DECLID : TK_id TYPE'''
    t[0] = [t[1], t[2]]

# Asignación de Variables
def p_ASIGNID(t: Prod):
    '''ASIGNID : RW_set TK_id TK_equal EXP'''
    t[0] = AsignID(t.lineno(1), t.lexpos(1), t[2], t[4])

# Mostrar valores de Variables
def p_SELECT(t: Prod):
    '''SELECT   : RW_select FIELDS RW_from TK_field RW_where EXP
                | RW_select FIELDS RW_from TK_field
                | RW_select LIST_IDS'''
    if len(t) == 7   : t[0] = Select(t.lineno(1), t.lexpos(1), t[4], t[2], t[6])
    elif len(t) == 5 : t[0] = Select(t.lineno(1), t.lexpos(1), t[4], t[2], None)
    else             : t[0] = Select_prt(t.lineno(1), t.lexpos(1), t[2])

def p_FIELDS(t: Prod):
    '''FIELDS   : LIST_IDS
                | TK_mult'''
    t[0] = t[1]

def p_LIST_IDS(t: Prod):
    '''LIST_IDS : LIST_IDS TK_comma IDS
                | IDS'''
    if len(t) == 4 : t[1].append(t[3]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_IDS(t: Prod):
    '''IDS  : EXP RW_as TK_nvarchar
            | EXP RW_as TK_field
            | EXP'''
    if len(t) == 4 : t[0] = [t[1], t[3]]
    else           : t[0] = [t[1], '']

# Creación de Tablas
def p_CREATETABLE(t: Prod):
    '''CREATETABLE : RW_create RW_table TK_field TK_lpar ATTRIBUTES TK_rpar'''
    t[0] = CreateTable(t.lineno(1), t.lexpos(1), t[3], t[5])

def p_ATTRIBUTES(t: Prod):
    '''ATTRIBUTES   : ATTRIBUTES TK_comma ATTRIBUTE
                    | ATTRIBUTE'''
    if len(t) == 4: t[1].append(t[3]); t[0] = t[1]
    else:           t[0] = [t[1]]

def p_ATTRIBUTE(t: Prod):
    '''ATTRIBUTE    : TK_field TYPE TK_lpar TK_int TK_rpar PROPS
                    | TK_field TYPE PROPS
                    | TK_field TYPE TK_lpar TK_int TK_rpar
                    | TK_field TYPE
                    | RW_foreing RW_key TK_lpar TK_field TK_rpar RW_ref TK_field TK_lpar TK_field TK_rpar'''
    if len(t) == 7   : t[0] = Attribute(t.lineno(1), t.lexpos(1), t[1], t[2], t[4], t[6])
    elif len(t) == 4 : t[0] = Attribute(t.lineno(1), t.lexpos(1), t[1], t[2], None, t[3])
    elif len(t) == 6 : t[0] = Attribute(t.lineno(1), t.lexpos(1), t[1], t[2], t[4])
    elif len(t) == 3 : t[0] = Attribute(t.lineno(1), t.lexpos(1), t[1], t[2], None)
    else             : t[0] = ForeignKey(t.lineno(1), t.lexpos(1), t[4], t[7], t[9])

def p_PROPS(t: Prod):
    '''PROPS    : RW_not RW_null RW_primary RW_key
                | RW_primary RW_key RW_not RW_null
                | RW_not RW_null
                | RW_primary RW_key'''
    if len(t) == 5 and t.slice[1].type == 'RW_not'     : t[0] = {'notNull': True,  'primaryKey': True }
    if len(t) == 5 and t.slice[1].type == 'RW_primary' : t[0] = {'notNull': True,  'primaryKey': True }
    if len(t) == 3 and t.slice[1].type == 'RW_not'     : t[0] = {'notNull': True,  'primaryKey': False}
    if len(t) == 3 and t.slice[1].type == 'RW_primary' : t[0] = {'notNull': False, 'primaryKey': True }

# Alter Table
def p_ALTERTAB(t: Prod):
    '''ALTERTAB : RW_alter RW_table TK_field ACTION'''
    t[0] = AlterTable(t.lineno(1), t.lexpos(1), t[3], t[4][0], t[4][1], t[4][2], t[4][3])

def p_ACTION(t: Prod):
    '''ACTION   : RW_add TK_field TYPE
                | RW_drop TK_field
                | RW_rename RW_to TK_field
                | RW_rename RW_column TK_field RW_to TK_field'''
    if   t.slice[1].type == 'RW_add'    : t[0] = [t[1],        t[2], None, t[3]]
    elif t.slice[1].type == 'RW_drop'   : t[0] = [t[1],        t[2], None, None]
    elif t.slice[2].type == 'RW_to'     : t[0] = [t[1] + t[2], t[3], None, None]
    elif t.slice[2].type == 'RW_column' : t[0] = [t[1] + t[2], t[3], t[5], None]

# Eliminar Tabla
def p_DROPTAB(t: Prod):
    '''DROPTAB : RW_drop RW_table TK_field'''
    t[0] = DropTable(t.lineno(1), t.lexpos(1), t[3])

# Insertar registros
def p_INSERTREG(t: Prod):
    '''INSERTREG : RW_insert RW_into TK_field TK_lpar LIST_ATTRIBS TK_rpar RW_values TK_lpar LIST_EXPS TK_rpar'''
    t[0] = InsertTable(t.lineno(1), t.lexpos(1), t[3], t[5], t[9])


def p_LIST_ATTRIBS(t: Prod):
    '''LIST_ATTRIBS : LIST_ATTRIBS TK_comma TK_field
                    | TK_field'''
    if len(t) == 4 : t[1].append(t[3]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_LIST_EXPS(t: Prod):
    '''LIST_EXPS    : LIST_EXPS TK_comma EXP
                    | EXP'''
    if len(t) == 4 : t[1].append(t[3]); t[0] = t[1]
    else           : t[0] = [t[1]]

# Actualizar Tabla
def p_UPDATETAB(t: Prod):
    '''UPDATETAB : RW_update TK_field RW_set VALUESTAB RW_where EXP'''
    t[0] = UpdateTable(t.lineno(1), t.lexpos(1), t[2], t[4][0], t[4][1], t[6])

def p_VALUESTAB(t: Prod):
    '''VALUESTAB    : VALUESTAB TK_comma VALUETAB
                    | VALUETAB '''
    if len(t) == 4: t[1][0].append(t[3][0]); t[1][1].append(t[3][1]); t[0] = t[1]
    else:           t[0] = [[t[1][0]], [t[1][1]]]

def p_VALUETAB(t: Prod):
    '''VALUETAB : TK_field TK_equal EXP'''
    t[0] = [t[1], t[3]]

# Truncate
def p_TRUNCATETAB(t: Prod):
    '''TRUNCATETAB : RW_truncate RW_table TK_field'''
    t[0] = TruncateTable(t.lineno(1), t.lexpos(1), t[3])

# Eliminar Registros
def p_DELETETAB(t: Prod):
    '''DELETETAB : RW_delete RW_from TK_field RW_where EXP'''
    t[0] = DeleteTable(t.lineno(1), t.lexpos(1), t[3], t[5])

# Estructura IF
def p_IFSTRUCT(t: Prod):
    '''IFSTRUCT : RW_if EXP RW_then INSTRUCTIONS RW_else INSTRUCTIONS RW_end RW_if
                | RW_if EXP RW_then INSTRUCTIONS RW_end RW_if
                | RW_if EXP RW_begin INSTRUCTIONS RW_end'''
    if len(t) == 9   : t[0] = If(t.lineno(1), t.lexpos(1), t[2], Block(t.lineno(1), t.lexpos(1), t[4]), Block(t.lineno(1), t.lexpos(1), t[6]))
    elif len(t) == 7 : t[0] = If(t.lineno(1), t.lexpos(1), t[2], Block(t.lineno(1), t.lexpos(1), t[4]), None)
    elif len(t) == 6 : t[0] = If(t.lineno(1), t.lexpos(1), t[2], Block(t.lineno(1), t.lexpos(1), t[4]), None)

# Estructura CASE
def p_CASESTRUCT_S(t: Prod):
    '''CASESTRUCT_S : RW_case EXP WHENELSE RW_end RW_as TK_field
                    | RW_case EXP WHENELSE RW_end RW_as TK_nvarchar
                    | RW_case EXP WHENELSE RW_end
                    | RW_case WHENELSE RW_end RW_as TK_field
                    | RW_case WHENELSE RW_end RW_as TK_nvarchar
                    | RW_case WHENELSE RW_end'''
    if len(t) == 7   : t[0] = Case(t.lineno(1), t.lexpos(1), t[2], t[3][0], t[3][1], t[6])
    elif len(t) == 5 : t[0] = Case(t.lineno(1), t.lexpos(1), t[2], t[3][0], t[3][1], None)
    elif len(t) == 6 : t[0] = Case(t.lineno(1), t.lexpos(1), None, t[2][0], t[2][1], t[5])
    elif len(t) == 4 : t[0] = Case(t.lineno(1), t.lexpos(1), None, t[2][0], t[2][1], None)

def p_WHENELSE(t: Prod):
    '''WHENELSE : WHENS ELSE
                | WHENS
                | ELSE'''
    if len(t) == 3                                  : t[0] = [t[1], t[2]]
    elif len(t) == 2 and t.slice[1].type == 'WHENS' : t[0] = [t[1], None]
    else                                            : t[0] = [None, t[1]]

def p_WHENS(t: Prod):
    '''WHENS    : WHENS WHEN
                | WHEN'''
    if len(t) == 3 : t[1].append(t[2]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_WHEN(t: Prod):
    '''WHEN : RW_when EXP RW_then EXP'''
    t[0] = When(t.lineno(1), t.lexpos(1), t[2], t[4])

def p_ELSE(t: Prod):
    '''ELSE : RW_else RW_then EXP'''
    t[0] = t[3]

# PRINT
def p_PRINT(t: Prod):
    '''PRINT : RW_print EXP'''

# Estructura WHILE
def p_WHILESTRUCT(t: Prod):
    '''WHILESTRUCT : RW_while EXP ENCAP'''
    t[0] = While(t.lineno(1), t.lexpos(1), t[2], t[3])

# Estructura FOR
def p_FORSTRUCT(t: Prod):
    '''FORSTRUCT : RW_for TK_id RW_in EXP TK_dot EXP ENCAP RW_loop'''

# Funciones y métodos
def p_FUNCDEC(t: Prod):
    '''FUNCDEC  : RW_create RW_function TK_field TK_lpar PARAMS TK_rpar RW_returns TYPE ENCAP
                | RW_create RW_function TK_field TK_lpar TK_rpar RW_returns TYPE ENCAP
                | RW_create RW_procedure TK_field PARAMS RW_as ENCAP
                | RW_create RW_procedure TK_field RW_as ENCAP
                | RW_create RW_procedure TK_field PARAMS ENCAP
                | RW_create RW_procedure TK_field ENCAP'''
    if len(t) == 10                                 : t[0] = Function(t.lineno(1), t.lexpos(1), t[3], t[5], t[9], t[8])
    elif len(t) == 9                                : t[0] = Function(t.lineno(1), t.lexpos(1), t[3],   [], t[8], t[7])
    elif len(t) == 7                                : t[0] = Function(t.lineno(1), t.lexpos(1), t[3], t[4], t[6], Type.NULL)
    elif len(t) == 6 and t.slice[4].type == 'RW_as' : t[0] = Function(t.lineno(1), t.lexpos(1), t[3],   [], t[5], Type.NULL)
    elif len(t) == 6                                : t[0] = Function(t.lineno(1), t.lexpos(1), t[3], t[4], t[5], Type.NULL)
    else                                            : t[0] = Function(t.lineno(1), t.lexpos(1), t[3],   [], t[4], Type.NULL)

def p_PARAMS(t: Prod):
    '''PARAMS   : PARAMS TK_comma PARAM
                | PARAM'''
    if len(t) == 4 : t[1].append(t[3]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_PARAM(t: Prod):
    '''PARAM    : TK_id RW_as TYPE'''
    t[0] = Parameter(t.lineno(1), t.lexpos(1), t[1], t[3])

# Encapsulamiento de Sentencias
def p_ENCAP(t: Prod):
    '''ENCAP    : RW_begin INSTRUCTIONS RW_end
                | RW_begin RW_end'''
    if len(t) == 4 : t[0] = Block(t.lineno(1), t.lexpos(1), t[2])
    else           : t[0] = Block(t.lineno(1), t.lexpos(1), [])

# Llamada a funciones y métodos
def p_CALLFUNC(t: Prod):
    '''CALLFUNC : TK_field TK_lpar ARGS TK_rpar
                | TK_field TK_lpar TK_rpar'''
    if len(t) == 5 : t[0] = CallFunction(t.lineno(1), t.lexpos(1), t[1], t[3])
    else           : t[0] = CallFunction(t.lineno(1), t.lexpos(1), t[1],  [] )

def p_ARGS(t: Prod):
    '''ARGS : ARGS TK_comma EXP
            | EXP'''
    if len(t) == 4 : t[1].append(t[3]); t[0] = t[1]
    else           : t[0] = [t[1]]

def p_EXP(t: Prod):
    '''EXP  : ARITHMETICS
            | RELATIONALS
            | LOGICS
            | CAST
            | NATIVEFUNC
            | CALLFUNC
            | TERNARY
            | TK_id
            | TK_field
            | TK_nvarchar
            | TK_int
            | TK_decimal
            | TK_date
            | TK_datetime
            | RW_null
            | TK_lpar EXP TK_rpar'''
    types = ['ARITHMETICS', 'RELATIONALS', 'LOGICS', 'CAST', 'NATIVEFUNC', 'CALLFUNC', 'TERNARY']
    if t.slice[1].type in types           : t[0] = t[1]
    elif t.slice[1].type == 'TK_id'       : t[0] = AccessID(t.lineno(1), t.lexpos(1), t[1])
    elif t.slice[1].type == 'TK_field'    : t[0] = Field(t.lineno(1), t.lexpos(1), t[1])
    elif t.slice[1].type == 'TK_nvarchar' : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.NVARCHAR)
    elif t.slice[1].type == 'TK_int'      : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.INT)
    elif t.slice[1].type == 'TK_decimal'  : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.DECIMAL)
    elif t.slice[1].type == 'TK_date'     : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.DATE)
    elif t.slice[1].type == 'TK_datetime' : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.DATETIME)
    elif t.slice[1].type == 'RW_null'     : t[0] = Primitive(t.lineno(1), t.lexpos(1), t[1], Type.NULL)
    else                                  : t[0] = t[2]


def p_ARITHMETICS(t: Prod):
    '''ARITHMETICS  : EXP TK_plus EXP
                    | EXP TK_minus EXP
                    | EXP TK_mult EXP
                    | EXP TK_div EXP
                    | EXP TK_mod EXP
                    | TK_minus EXP %prec TK_uminus'''
    if t.slice[1].type != 'TK_minus' : t[0] = Arithmetic(t.lineno(1), t.lexpos(1), t[1], t[2], t[3])
    else                             : t[0] = Arithmetic(t.lineno(1), t.lexpos(1), None, t[1], t[2])

def p_RELATIONALS(t: Prod):  
    '''RELATIONALS  : EXP TK_equalequal EXP
                    | EXP TK_equal EXP
                    | EXP TK_notequal EXP
                    | EXP TK_lessequal EXP
                    | EXP TK_greatequal EXP
                    | EXP TK_less EXP
                    | EXP TK_great EXP'''
    t[0] = Relational(t.lineno(1), t.lexpos(1), t[1], t[2], t[3])

def p_LOGICS(t: Prod):
    '''LOGICS   : EXP TK_and EXP
                | EXP TK_or EXP
                | TK_not EXP'''
    if t.slice[2].type != 'RW_not'   : t[0] = Logic(t.lineno(1), t.lexpos(1), t[1], t[2], t[3])
    else                             : t[0] = Logic(t.lineno(1), t.lexpos(1), None, t[2], t[3])

def p_CAST(t: Prod):
    '''CAST : RW_cas TK_lpar EXP RW_as TYPE TK_rpar'''

# Funciones Nativas
def p_NATIVEFUNC(t: Prod):
    '''NATIVEFUNC : RW_truncate TK_lpar EXP TK_comma EXP TK_rpar'''

def p_TERNARY(t: Prod):
    '''TERNARY : RW_if TK_lpar EXP TK_comma EXP TK_comma EXP TK_rpar'''

def p_TYPE(t: Prod):
    '''TYPE : RW_int
            | RW_bit
            | RW_decimal
            | RW_date
            | RW_datetime
            | RW_nchar
            | RW_nvarchar'''
    if t.slice[1].type == 'RW_int'        : t[0] = Type.INT
    elif t.slice[1].type == 'RW_bit'      : t[0] = Type.BIT
    elif t.slice[1].type == 'RW_decimal'  : t[0] = Type.DECIMAL
    elif t.slice[1].type == 'RW_date'     : t[0] = Type.DATE
    elif t.slice[1].type == 'RW_datetime' : t[0] = Type.DATETIME
    elif t.slice[1].type == 'RW_nchar'    : t[0] = Type.NCHAR
    elif t.slice[1].type == 'RW_nvarchar' : t[0] = Type.NVARCHAR

from interpreter.Scanner import *

def p_error(t: LexToken):
    errors.append(Error(t.lineno, t.lexpos + 1, TypeError.SYNTAX, f'No se esperaba «{t.value}»'))

import ply.yacc as Parser
parser = Parser.yacc()