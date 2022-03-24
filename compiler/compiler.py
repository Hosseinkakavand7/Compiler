def lex(source):
    tokens = []
    words = []
    separator = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',', ';']  # single-char keywords
    operator = ['=', '+', '-', '*', '/', '%', '^', '<', '>', '==', '!=', '++', '--', '<=', '>=', '&&', '||']
    coments = ['/*', '*/']  # multi-char keywords
    keywords = ['char', 'int', 'float', 'if', 'for', 'else', "while", "break", "return","continue"]
    syms = separator + operator + coments
    KEYWORDS = separator + operator + coments + keywords
    word = ""
    for i in range(0, len(source)):
        if source[i] != " ":
            word += source[i]
        if i + 1 < len(source):
            if source_text[i + 1] in KEYWORDS or source_text[i + 1] == " " or word in syms:
                if word != "":
                    words.append(word)
                    word = ""
    if word!="":
        words.append(word)
    i = 0
    limit = len(words)
    while i < limit:
        if i + 1 < len(words):
            if (words[i] == "=" and words[i + 1] == "=") or (words[i] == "+" and words[i + 1] == "+") or (
                    words[i] == "-" and words[i + 1] == "-") or (words[i] == "!" and words[i + 1] == "=") or (
                    words[i] == "<" and words[i + 1] == "=") or (words[i] == ">" and words[i + 1] == "=") or (
                    words[i] == "&" and words[i + 1] == "&") or (words[i] == "|" and words[i + 1] == "|") or (
                    words[i] == "/" and words[i + 1] =="*") or (words[i] == "*" and words[i + 1] == "/"):
                words[i] = words[i] + words[i + 1]
                words.pop(i + 1)
                i -= 1
        i += 1
        limit = len(words)
    comment_flag = False
    for i in range(0, len(words)):
        if words[i] == coments[0]:
            comment_flag = True
        if words[i] == coments[1]:
            comment_flag = False
        if not comment_flag:
            if words[i] in separator:
                tokens.append({"type": "Separator", "word": words[i]})
            elif words[i] in operator:
                tokens.append({"type": "Operator", "word": words[i]})
            elif words[i] in keywords:
                tokens.append({"type": "Keyword", "word": words[i]})
            elif words[i][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                tokens.append({"type": "Number", "word": words[i]})
            else:
                tokens.append({"type": "Identifier", "word": words[i]})
    print(tokens)
    return tokens


def program(token, count):
    flat=False
    while  token[count[0]] in ["int", "float", "char", "bool", "void"] and token[count[0] + 1] == "id" and token[
                count[0] + 2] == "(":
        methoddec(token, count)
        if count[0] == len(token):
            flat=True
            break
        if count[0] + 2 >= len(token):
            flat=True
            break
        flat=True
    if count[0] != len(token):
        while token[count[0]] in ["int", "float", "char", "bool"] and token[count[0] + 1] == "id" and token[
                    count[0] + 2] in ["["]:
            vardec(token, count[0])
            flat=True
    if flat!=False:
        print("True")
    else:
        print("False")


def vardec(token, count):
    type(token, count)
    varlist(token, count)
    eat(token, count, ";")


def varlist(token, count):
    eat(token, count, "id")
    while token[count[0]] in ["[", "int", "id"]:
        eat("[")
        if token[count[0]] == "int":
            eat(token, count, "int")
        elif token[count[0]] == "id":
            eat(token, count, "id")
        eat(token, count, "]")
    if token[count[0]] == ",":
        eat(token, count, ",")
        varlist(token, count)
    if token[count[0]] == "=":
        eat(token, count, "=")
        if token[count[0]] in ["int", "float", "char", "bool"]:
            type(token, count)
        elif token[count[0]] == "id":
            location(token, count)
            # eat(token,count,";")


def methoddec(token, count):
    vectype(token, count)
    eat(token, count, "id")
    eat(token, count, "(")
    if token[count[0]] != ")":
        methodlist(token, count)
    eat(token, count, ")")
    block(token, count)


def block(token, count):
    eat(token, count, "{")
    while token[count[0]] in ["int", "float", "char", "bool", "id", "if", "while", "for", "return", "continue", "{"]:
        if token[count[0]] in ["int", "float", "char", "bool"]:
            vardec(token, count)
        elif token[count[0]] in ["id", "if", "while", "for", "return", "continue", "{"]:
            statement(token, count)
    eat(token, count, "}")


def type(token, count):
    if token[count[0]] == "int":
        eat(token, count, "int")
    elif token[count[0]] == "float":
        eat(token, count, "float")
    elif token[count[0]] == "char":
        eat(token, count, "char")
    elif token[count[0]] == "bool":
        eat(token, count, "bool")
    else:
        pass


def vectype(token, count):
    if token[count[0]] == "void":
        eat(token, count, "void")
    else:
        type(token, count)


def methodlist(token, count):
    type(token, count)
    eat(token, count, "id")
    if token[count[0]] == ",":
        eat(token, count, ",")
        methodlist()


def statement(token, count):
    if token[count[0]] == "id":
        if token[count[0] + 1] == "=":
            assignment(token, count)
            eat(token, count, ";")
        elif token[count[0]+1]=="(":
            methodcall(token, count)
            eat(token, count, ";")
    elif token[count[0]] == "if":
        eat(token, count, "if")
        eat(token, count, "(")
        expr(token, count, 0)
        eat(token, count, ")")
        block(token, count)
        if token[count[0]] == "else":
            eat(token, count, "else")
            block(token, count)
    elif token[count[0]] == "while":
        eat(token, count, "while")
        eat(token, count, "(")
        expr(token, count, 0)
        eat(token, count, ")")
        block(token, count)
    elif token[count[0]] == "for":
        eat(token, count, "for")
        eat(token, count, "(")
        assignment(token, count)
        eat(token, count, ";")
        expr(token, count, 0)
        eat(token, count, ";")
        assignment(token, count)
        eat(token, count, ")")
        block(token, count)
    elif token[count[0]] == "return":
        eat(token, count, "return")
        if token[count[0]] in ["id", "-", "!", "("]:
            expr(token, count, 0)
        eat(token, count, ";")
    elif token[count[0]] == "break":
        eat(token, count, "break")
        eat(token, count, ";")
    elif token[count[0]] == "continue":
        eat(token, count, "continue")
        eat(token, count, ";")
    elif token[count[0]] == "{":
        block(token, count)
    else:
        pass


def assignment(token, count):
    location(token, count)
    eat(token, count, "=")
    expr(token, count, 0)


def methodcall(token, count):
    methodname(token, count)
    if token[count[0]] in ["id", "-", "!", "("]:
        eat(token, count, ",")
        calllist(token, count)


def methodname(token, count):
    eat(token, count, "id")


def calllist(token, count):
    expr(token, count, 0)
    if token[count[0]] in ["id", "-", "!", "("]:
        eat(token, count, ",")
        calllist(token, count)


def location(token, count):
    eat(token, count, "id")


def expr(token, count, time):
    if token[count[0]] == "id":
        if token[count[0] + 1] == "(":
            methodcall(token, count)
        elif token[count[0] + 1] in ["+", "-", "/", "*", "<", ">", "<=", ">=", "=="] and time == 0:
            expr(token, count, time + 1)
            binop(token, count)
            expr(token, count, 0)
        else:
            location(token, count)
    elif token[count[0]] == "-":
        eat(token, count, "-")
        expr(token, count, 0)
    elif token[count[0]] == "!":
        eat(token, count, "!")
        expr(token, count, 0)
    elif token[count[0]] == "(":
        eat(token, count, "(")
        expr(token, count, 0)
        eat(token, count, ")")
    elif token[count[0]] in ["int", "float", "bool", "char"]:
        eat(token, count, token[count[0]])


def binop(token, count):
    if token[count[0]] in ["+", "-", "*", "/"]:
        arthop(token, count)
    elif token[count[0]] in ["==", "<=", ">=", ">", "<"]:
        condop(token, count)


def arthop(token, count):
    if token[count[0]] in ["+", "-", "*", "/"]:
        eat(token, count, token[count[0]])


def condop(token, count):
    if token[count[0]] in ["==", "<=", ">=", ">", "<"]:
        eat(token, count, token[count[0]])


def eat(token, count, tok):
    # print(tok, token[count[0]])
    if token[count[0]] == tok:
        count[0] += 1
    else:
        print("error")


source_code = open("code.txt", "r")
source_text = source_code.read()
source_text = source_text.replace("\n", " ")
source_code.close()
a = lex(source_text)
token = []
for i in a:
    if i["type"] == "Identifier":
        token.append("id")
    elif i["type"] == "Number":
        if "." in i["word"]:
            token.append("float")
        else:
            token.append("int")
    else:
        token.append(i["word"])
print(token)
count = [0]
program(token, count)