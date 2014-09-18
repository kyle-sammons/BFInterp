import sys

class Interp():
    def __init__(self, tokens):
        self.ptr = 0
        self.pos = 0
        self.mem = [0]
        self.tokens = tokens
        self.brace_map = build_brace_map(tokens)

    def next(self):
        self.ptr += 1
        self.mem.append(0) 

    def prev(self):
        self.ptr -= 1

    def add(self):
        self.mem[self.ptr] = (self.mem[self.ptr] + 1) % 256

    def sub(self):
        self.mem[self.ptr] = (self.mem[self.ptr] - 1) % 256

    def output(self):
        print(chr(self.mem[self.ptr]), end="")

    def user_input(self):
        ui = input("")
        self.mem[self.ptr] = ord(ui[0])

    def get_token(self):
        return self.tokens[self.pos]

    def atEnd(self):
        return len(self.tokens) == self.pos

    def test_while(self):
        return self.mem[self.ptr] != 0

    def end_brace(self):
        return self.brace_map[self.pos]

def build_brace_map(tokens):

    lbrace_stack = []
    brace_map = {}

    for i, token in enumerate(tokens):

        if token == '[':
            lbrace_stack.append(i)

        elif token == ']':
            lbrace = lbrace_stack.pop()
            brace_map[lbrace] = i

    return brace_map
            

def execute(interp):

    call_stack = []

    while(not interp.atEnd()):
        token = interp.get_token()

        if(token == '>'):
            interp.next()

        elif(token == '<'):
            interp.prev()

        elif(token == '.'):
            interp.output()

        elif(token == ','):
            interp.user_input()

        elif(token == '+'):
            interp.add()

        elif(token == '-'):
            interp.sub()

        elif(token == '['):
            if(interp.test_while()):
                call_stack.append(interp.pos)
            else:
                interp.pos = interp.end_brace()

        elif(token == ']'):
            interp.pos = call_stack.pop() - 1

        else:
            pass

        interp.pos += 1
            
def main():

    if len(sys.argv) == 2:
        fp = open(sys.argv[1], 'r')
        text = fp.read()
        bf = Interp(text)
        execute(bf)

    else:
        print("ERROR")

if __name__ == "__main__":
    main()
