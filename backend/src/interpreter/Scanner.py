from utils.Outs import errors
from utils.Error import Error
from utils.TypeError import TypeError

reserveds = {
    # EJECUCION DDL
    'BEGIN'      : 'RW_begin',
    'END'        : 'RW_end',
    'SELECT'     : 'RW_select',
    'FROM'       : 'RW_from',
    'WHERE'      : 'RW_where',
    'DECLARE'    : 'RW_declare',
    'SET'        : 'RW_set',
    'CREATE'     : 'RW_create',
    'TABLE'      : 'RW_table',
    'PRIMARY'    : 'RW_primary',
    'FOREING'    : 'RW_foreing',
    'KEY'        : 'RW_key',
    'REFERENCE'  : 'RW_ref',
    'ALTER'      : 'RW_alter',
    'ADD'        : 'RW_add',
    'DROP'       : 'RW_drop',
    'COLUMN'     : 'RW_column',
    'RENAME'     : 'RW_rename',
    'TO'         : 'RW_to',
    'INSERT'     : 'RW_insert',
    'INTO'       : 'RW_into',
    'VALUES'     : 'RW_values',
    'AS'         : 'RW_as',
    'UPDATE'     : 'RW_update',
    'TRUNCATE'   : 'RW_truncate',
    'DELETE'     : 'RW_delete',
    'THEN'       : 'RW_then',
    'WHEN'       : 'RW_when',
    'NOT'        : 'RW_not',
    # EJECUCION DML
    'IF'         : 'RW_if',
    'ELSE'       : 'RW_else',
    'CASE'       : 'RW_case',
    'WHILE'      : 'RW_while',
    'FOR'        : 'RW_for',
    'IN'         : 'RW_in',
    'LOOP'       : 'RW_loop',
    'BREAK'      : 'RW_break',
    'CONTINUE'   : 'RW_continue',
    'FUNCTION'   : 'RW_function',
    'RETURNS'    : 'RW_returns',
    'RETURN'     : 'RW_return',
    'PROCEDURE'  : 'RW_procedure',
    'PRINT'      : 'RW_print',
    'TRUNCATE'   : 'RW_truncate',
    'CONCATENA'  : 'RW_concatena',
    'SUMBSTRAER' : 'RW_substraer',
    'HOY'        : 'RW_hoy',
    'CONTAR'     : 'RW_contar',
    'CAS'        : 'RW_cas',
    # TIPOS DE DATOS
    'INT'        : 'RW_int',
    'BIT'        : 'RW_bit',
    'DECIMAL'    : 'RW_decimal',
    'DATE'       : 'RW_date',
    'DATETIME'   : 'RW_datetime',
    'NCHAR'      : 'RW_nchar',
    'NVARCHAR'   : 'RW_nvarchar',
    'NULL'       : 'RW_null',
}

tokens = tuple(reserveds.values()) + (
    'TK_lpar',
    'TK_rpar',
    'TK_semicolon',
    'TK_comma',
    'TK_dot',
    'TK_plus',
    'TK_minus',
    'TK_mult',
    'TK_div',
    'TK_mod',
    'TK_equalequal',
    'TK_equal',
    'TK_notequal',
    'TK_lessequal',
    'TK_greatequal',
    'TK_less',
    'TK_great',
    'TK_and',
    'TK_or',
    'TK_not',
    'TK_id',
    'TK_field',
    'TK_date',
    'TK_datetime',
    'TK_nvarchar',
    'TK_decimal',
    'TK_int',
)
# SIGNOS DE AGRUPACIÓN Y FINALIZACIÓN
t_TK_lpar       = r'\('
t_TK_rpar       = r'\)'
t_TK_semicolon  = r'\;'
t_TK_comma      = r'\,'
t_TK_dot        = r'\.\.'
# OPERACIONES ARITMETICAS
t_TK_plus       = r'\+'
t_TK_minus      = r'\-'
t_TK_mult       = r'\*'
t_TK_div        = r'\/'
t_TK_mod        = r'\%'
# OPERADORES RELACIONALES
t_TK_equalequal = r'\=\='
t_TK_equal      = r'\='
t_TK_notequal   = r'\!\='
t_TK_lessequal  = r'\<\='
t_TK_greatequal = r'\>\='
t_TK_less       = r'\<'
t_TK_great      = r'\>'
t_TK_and        = r'\&\&'
t_TK_or         = r'\|\|'
t_TK_not        = r'\!'

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

t_ignore = ' \t'

def t_comments(t):
    r'\-\-([^\r\n]*)?'
    t.lexer.lineno += 1
    t.lexer.skip(1)

def t_commentm(t):
    r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]'
    t.lexer.lineno += len(t.value.split('\n'))
    t.lexer.skip(1)

def t_TK_id(t):
    r'\@(\_)*[a-zA-Z][a-zA-Z0-9\_]*'
    return t

def t_TK_field(t):
    r'(\_)*[a-zA-Z][a-zA-Z0-9\_]*'
    t.type = reserveds.get(t.value.upper(), 'TK_field')
    return t

def t_TK_date(t):
    r'\"\d\d\-\d\d\-\d\d\d\d\"'
    t.value = t.value[1 : len(t.value) - 1]
    return t

def t_TK_datetime(t):
    r'\"\d\d\-\d\d\-\d\d\d\d\ \d\d\:\d\d"'
    t.value = t.value[1 : len(t.value) - 1]
    return t

def t_TK_nvarchar(t):
    r'\"(([^\n\"\\]|\\.)*)\"'
    t.value = t.value[1 : len(t.value) - 1]
    return t

def t_TK_decimal(t):
    r'[0-9]+\.[0-9]+'
    return t

def t_TK_int(t):
    r'[0-9]+'
    return t

def t_error(t):
    errors.append(Error(t.lexer.lineno, t.lexer.lexpos + 1, TypeError.LEXICAL, f'Caracter no reconocido. «{t.value[0]}»'))
    t.lexer.skip(1)

import ply.lex as Scanner
scanner = Scanner.lex()