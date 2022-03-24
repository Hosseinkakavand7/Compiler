def lex(source):
    tokens = []
    words = []
    separator = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',', ';']
    operator = ['=', '+', '-', '*', '/', '%', '^', '<', '>', '==', '!=', '++', '--', '<=', '>=', '&&', '||']
    keywords = ['char', 'int', 'float', 'if', 'else', "while", "break", "return",'bool']
    syms = separator + operator
    KEYWORDS = separator + operator + keywords
    word = ""
    for i in range(0, len(source)):
        if source[i] != " ":
            word += source[i]
        if i + 1 < len(source):
            if source[i + 1] in KEYWORDS or source[i + 1] == " " or word in syms:
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
                    words[i] == "&" and words[i + 1] == "&") or (words[i] == "|" and words[i + 1] == "|"):
                words[i] = words[i] + words[i + 1]
                words.pop(i + 1)
                i -= 1
        i += 1
        limit = len(words)
    for i in range(0, len(words)):
        if words[i] in separator:
            tokens.append({"Type": "Separator", "Word": words[i]})
        elif words[i] in operator:
            tokens.append({"Type": "Operator", "Word": words[i]})
        elif words[i] in keywords:
            tokens.append({"Type": "Keyword", "Word": words[i]})
        elif words[i][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            tokens.append({"Type": "Number", "Word": words[i]})
        else:
            tokens.append({"Type": "id", "Word": words[i]})
    return tokens


def program(token, count):
    while token[count[0]] in ["int", "float", "char", "bool", "void"] and token[count[0] + 1] == "id" and token[
                count[0] + 2] == "(":
        methoddec(token, count)
        if count[0] == len(token):
            break
        if count[0] + 2 >= len(token):
            break
    if count[0] != len(token):
        while token[count[0]] in ["int", "float", "char", "bool"] and token[count[0] + 1] == "id" and token[
                    count[0] + 2] in ["["]:
            vardec(token, count[0])
    print("Tokens parsed by Grammar")


def vardec(token, count):
    type(token, count)
    varlist(token, count)
    proceed_next_token(token, count, ";")


def varlist(token, count):
    while token[count[0]] in ["[", "int", "id"]:
        proceed_next_token("[")
        if token[count[0]] == "int":
            proceed_next_token(token, count, "int")
        elif token[count[0]] == "id":
            proceed_next_token(token, count, "id")
        proceed_next_token(token, count, "]")
    if token[count[0]] == ",":
        proceed_next_token(token, count, ",")
        varlist(token, count)
    if token[count[0]] == "=":
        proceed_next_token(token, count, "=")
        if token[count[0]] in ["int", "float", "char", "bool"]:
            type(token, count)
        elif token[count[0]] == "id":
            location(token, count)
            # proceed_next_token(token,count,";")


def methoddec(token, count):
    vectype(token, count)
    proceed_next_token(token, count, "id")
    proceed_next_token(token, count, "(")
    if token[count[0]] != ")":
        methodlist(token, count)
    proceed_next_token(token, count, ")")
    block(token, count)


def block(token, count):
    proceed_next_token(token, count, "{")
    while token[count[0]] in ["int", "float", "char", "bool", "id", "if", "while", "for", "return", "continue", "{"]:
        if token[count[0]] in ["int", "float", "char", "bool"]:
            vardec(token, count)
        elif token[count[0]] in ["id", "if", "while", "for", "return", "continue", "{"]:
            statement(token, count)
    proceed_next_token(token, count, "}")


def type(token, count):
    if token[count[0]] == "int":
        proceed_next_token(token, count, "int")
    elif token[count[0]] == "float":
        proceed_next_token(token, count, "float")
    elif token[count[0]] == "char":
        proceed_next_token(token, count, "char")
    elif token[count[0]] == "bool":
        proceed_next_token(token, count, "bool")
    else:
        pass


def vectype(token, count):
    if token[count[0]] == "void":
        proceed_next_token(token, count, "void")
    else:
        type(token, count)


def methodlist(token, count):
    type(token, count)
    proceed_next_token(token, count, "id")
    if token[count[0]] == ",":
        proceed_next_token(token, count, ",")
        methodlist()


def statement(token, count):
    if token[count[0]] == "id":
        if token[count[0] + 1] == "=":
            assignment(token, count)
            proceed_next_token(token, count, ";")
        else:
            methodcall(token, count)
            proceed_next_token(token, count, ";")
    elif token[count[0]] == "if":
        proceed_next_token(token, count, "if")
        proceed_next_token(token, count, "(")
        expr(token, count, 0)
        proceed_next_token(token, count, ")")
        block(token, count)
        if token[count[0]] == "else":
            proceed_next_token(token, count, "else")
            block(token, count)
    elif token[count[0]] == "while":
        proceed_next_token(token, count, "while")
        proceed_next_token(token, count, "(")
        expr(token, count, 0)
        proceed_next_token(token, count, ")")
        block(token, count)
    elif token[count[0]] == "return":
        proceed_next_token(token, count, "return")
        if token[count[0]] in ["id", "-", "!", "("]:
            expr(token, count, 0)
        proceed_next_token(token, count, ";")
    elif token[count[0]] == "break":
        proceed_next_token(token, count, "break")
        proceed_next_token(token, count, ";")
    elif token[count[0]] == "continue":
        proceed_next_token(token, count, "continue")
        proceed_next_token(token, count, ";")
    elif token[count[0]] == "{":
        block(token, count)
    else:
        pass


def assignment(token, count):
    location(token, count)
    proceed_next_token(token, count, "=")
    expr(token, count, 0)


def methodcall(token, count):
    methodname(token, count)
    if token[count[0]] in ["id", "-", "!", "("]:
        proceed_next_token(token, count, ",")
        calllist(token, count)


def methodname(token, count):
    proceed_next_token(token, count, "id")


def calllist(token, count):
    expr(token, count, 0)
    if token[count[0]] in ["id", "-", "!", "("]:
        proceed_next_token(token, count, ",")
        calllist(token, count)


def location(token, count):
    proceed_next_token(token, count, "id")


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
        proceed_next_token(token, count, "-")
        expr(token, count, 0)
    elif token[count[0]] == "!":
        proceed_next_token(token, count, "!")
        expr(token, count, 0)
    elif token[count[0]] == "(":
        proceed_next_token(token, count, "(")
        expr(token, count, 0)
        proceed_next_token(token, count, ")")
    elif token[count[0]] in ["int", "float", "bool", "char"]:
        proceed_next_token(token, count, token[count[0]])


def binop(token, count):
    if token[count[0]] in ["+", "-", "*", "/"]:
        arthop(token, count)
    elif token[count[0]] in ["==", "<=", ">=", ">", "<"]:
        condop(token, count)


def arthop(token, count):
    if token[count[0]] in ["+", "-", "*", "/"]:
        proceed_next_token(token, count, token[count[0]])


def condop(token, count):
    if token[count[0]] in ["==", "<=", ">=", ">", "<"]:
        proceed_next_token(token, count, token[count[0]])


def proceed_next_token(token, count, tok):
    if token[count[0]] == tok:
        count[0] += 1
    else:
        print("error")


code = open("text.txt", "r")
text = code.read()
text = text.replace("\n", " ")
code.close()
tokens= lex(text)
token_list = []
for i in tokens:
    if i["Type"] == "id":
        token_list.append("id")
    elif i["Type"] == "Number":
        if "." in i["Word"]:
            token_list.append("float")
        else:
            token_list.append("int")
    else:
        token_list.append(i["Word"])
print("Tokens:",tokens)
print("Tokens:",token_list)
counter = [0]
program(token_list, counter)