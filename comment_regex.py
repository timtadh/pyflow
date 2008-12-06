#------------------------------------------------------------------------
import re, sys

def q(c):
    """Returns a regular expression that matches a region delimited by c,
    inside which c may be escaped with a backslash"""

    return r"%s(\\.|[^%s])*%s" % (c, c, c)

single_quoted_string = q('"')
double_quoted_string = q("'")
c_comment = r"/\*.*?\*/"
cxx_comment = r"//[^\n]*[\n]"

rx = "|".join([single_quoted_string, double_quoted_string,
                            c_comment, cxx_comment])

print rx