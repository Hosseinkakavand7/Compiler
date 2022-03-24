string=open("code.txt","r").read()
symbols = ['{', '}', '(', ')', '[', ']', '.', '"', '*', '\n', ':', ',','='] # single-char keywords
other_symbols = ['\\', '/*', '*/'] # multi-char keywords
keywords = ['public', 'class', 'void', 'main', 'String', 'int']
KEYWORDS = symbols + other_symbols + keywords

white_space = ' '
lexeme = ''

for i,char in enumerate(string):
    if char != white_space:
        lexeme += char # adding a char each time
    if (i+1 < len(string)): # prevents error
        if string[i+1] == white_space or string[i+1] in KEYWORDS or lexeme in KEYWORDS: # if next char == ' '
            if lexeme != '':
                print(lexeme.replace('\n', '<newline>'))
                lexeme = ''
