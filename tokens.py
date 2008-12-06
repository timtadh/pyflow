literals = []
for i in range(256): literals.append(chr(i))
literals = tuple(literals)

tokens = (
#/* yacc error tokens */
    "ERRORCODE",
#if (IDENTIFIER == 258)
    "ERRORCODE2",
#endif
#/* yacc %tokens */
    "IDENTIFIER", "CONSTANT", "STRING_LITERAL", "SIZEOF",
    "PTR_OP", "INC_OP", "DEC_OP", "LEFT_OP", "RIGHT_OP", "LE_OP",
    "GE_OP", "EQ_OP", "NE_OP", "AND_OP", "OR_OP", "MUL_ASSIGN",
    "DIV_ASSIGN", "MOD_ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN",
    "LEFT_ASSIGN", "RIGHT_ASSIGN", "AND_ASSIGN", "XOR_ASSIGN",
    "OR_ASSIGN", "TYPE_NAME", "TYPEDEF", "EXTERN", "STATIC",
    "AUTO", "REGISTER", "CHAR", "SHORT", "INT", "LONG", "SIGNED",
    "UNSIGNED", "FLOAT", "DOUBLE", "CONST", "VOLATILE", "VOID",
    "STRUCT", "UNION", "ENUM", "ELIPSIS", "RANGE", "CASE",
    "DEFAULT", "IF", "ELSE", "SWITCH", "WHILE", "DO", "FOR",
    "GOTO", "CONTINUE", "BREAK", "RETURN", "UNSIGNED_CHAR",
    "UNSIGNED_INT", "TYPEDEF_CHAR", "TYPEDEF_INT",
)

reserved = {"auto":"AUTO",
"break":"BREAK",
"case":"CASE",
"char":"CHAR",
"const":"CONST",
"continue":"CONTINUE",
"default":"DEFAULT",
"do":"DO",
"double":"DOUBLE",
"else":"ELSE",
"enum":"ENUM",
"extern":"EXTERN",
"float":"FLOAT",
"for":"FOR",
"goto":"GOTO",
"if":"IF",
"int":"INT",
"long":"LONG",
"register":"REGISTER",
"return":"RETURN",
"short":"SHORT",
"signed":"SIGNED",
"sizeof":"SIZEOF",
"static":"STATIC",
"struct":"STRUCT",
"switch":"SWITCH",
"typedef":"TYPEDEF",
"union":"UNION",
"unsigned":"UNSIGNED",
"void":"VOID",
"volatile":"VOLATILE",
"while":"WHILE" 
}

class Tokens(object):
    ERRORCODE = 256
    ERRORCODE2 = 257
    IDENTIFIER = 258
    CONSTANT = 259
    STRING_LITERAL = 260,
    SIZEOF = 261
    PTR_OP = 262
    INC_OP = 263
    DEC_OP = 264
    LEFT_OP = 265
    RIGHT_OP = 266
    LE_OP = 267
    GE_OP = 268
    EQ_OP = 269
    NE_OP = 270
    AND_OP = 271
    OR_OP = 272
    MUL_ASSIGN = 273
    DIV_ASSIGN = 274
    MOD_ASSIGN = 275
    ADD_ASSIGN = 276
    SUB_ASSIGN = 277
    LEFT_ASSIGN = 278
    RIGHT_ASSIGN = 279
    AND_ASSIGN = 280
    XOR_ASSIGN = 281
    OR_ASSIGN = 282
    TYPE_NAME = 283
    TYPEDEF = 284
    EXTERN = 285
    STATIC = 286
    AUTO = 287
    REGISTER = 288
    CHAR = 289
    SHORT = 290
    INT = 291
    LONG = 292
    SIGNED = 293
    UNSIGNED = 294
    FLOAT = 295
    DOUBLE = 296
    CONST = 297
    VOLATILE = 298
    VOID = 299
    STRUCT = 300
    UNION = 301
    ENUM = 302
    ELIPSIS = 303
    RANGE = 304
    CASE = 305
    DEFAULT = 306
    IF = 307
    ELSE = 308
    SWITCH = 309
    WHILE = 310
    DO = 311
    FOR = 312
    GOTO = 313
    CONTINUE = 314
    BREAK = 315
    RETURN = 316
    UNSIGNED_CHAR = 317
    UNSIGNED_INT = 318
    TYPEDEF_CHAR = 319
    TYPEDEF_INT = 320
