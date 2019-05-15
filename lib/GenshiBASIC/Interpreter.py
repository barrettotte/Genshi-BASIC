import math, random
import Constants as constants

class Interpreter:

    def __init__(self):
        self.out_buffer = []
        self.identifiers = {}
        self.is_running = True
        self.print_newline = False

    def interpret_var_dec(self, nodes, line):
        ident = nodes[0].content
        if ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' has already been declared ; line " + line)
        self.identifiers[ident] = self.interpret_expression(nodes[2], line)

    def interpret_var_assign(self, nodes, line):
        ident = nodes[0].content
        if not ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' referenced before declaration ; line " + line)
        self.identifiers[ident] = self.interpret_expression(nodes[2], line) 

    def interpret_expression(self, exp, line):
        if    exp.node_type == "LITERAL_EXP" : return self.interpret_literal_exp(exp, line)
        elif  exp.node_type == "BINARY_EXP"  : return self.interpret_binary_exp(exp, line)
        elif  exp.node_type == "UNARY_EXP"   : return self.interpret_unary_exp(exp, line)
        elif  exp.node_type == "STRING_EXP"  : return '"' + exp.children[1].content + '"'
        elif  exp.node_type == "FUNCTION_EXP": return self.interpret_func_exp(exp, line)
        raise Exception("Invalid Expression type '" + exp.node_type + "' ; line " + line)

    def validate_args(self, func, args, line):
        rules = constants.FUNCTION_RULES[func]
        if len(args) != len(rules):
            msg = "Invalid number of parameters for '" + func + "'. Expected "
            raise Exception(msg + str(len(rules)) + " , got " + str(len(args)) + " ; line " + line)
        for i in range(len(args)):
            if rules[i] == "NUMERIC" and not isinstance(args[i], (int, float)):
                raise Exception("Invalid parameter '" + args[i] + "'. Expected " + "NUMERIC ; line " + line)
            elif rules[i] == "STRING":
                if not isinstance(args[i], (int, float)) and (args[i].isidentifier() or '"' in args[i]):
                    args[i] = args[i].replace('"', '')
                else:
                    raise Exception("Invalid parameter '" + str(args[i]) + "'. Expected " + "STRING or IDENTIFIER ; line " + line)
            elif rules[i] == "ANY" and type(args[i]) is str:
                args[i] = args[i].replace('"', '')
        return args

    def interpret_func_exp(self, exp, line):
        ignore = ["COMMA", "LEFT_PAREN", "RIGHT_PAREN"]
        func = exp.children[0].content
        args = [self.interpret_expression(a, line) for a in exp.children[1].children if not a.node_type in ignore]
        args = self.validate_args(func, args, line)
        return self.function_handler(func, args, line)

    def function_handler(self, func, args, line):
        if   func == "ABS":    return abs(args[0])
        elif func == "ASC":    return ord(args[0][0])
        elif func == "CAT$":   return str(args[0]) + str(args[1])
        elif func == "BIN$":   return bin(args[0])
        elif func == "CHR$":   return str(chr(args[0]))
        elif func == "CLR":    self.identifiers, self.out_buffer = {},[]
        elif func == "COS":    return math.cos(args[0])
        elif func == "HEX$":   return hex(args[0])
        elif func == "END":    self.is_running = False
        elif func == "EXP":    return math.exp(args[0])
        elif func == "INT":    return int(args[0])
        elif func == "LEFT$":  return args[0][0:args[1]]
        elif func == "LEN":    return len(args[0])
        elif func == "LOG":    return math.log(args[0])
        elif func == "PI" :    return math.pi * args[0]
        elif func == "MID$":   return args[0][args[1]:args[2]]
        elif func == "RIGHT$": return args[0][-args[1]:]
        elif func == "RND":    return random.uniform(0, args[0])
        elif func == "SIN":    return math.sin(args[0])
        elif func == "SGN":    return 0 if args[0] == 0 else 1 if args[0] > 0 else -1
        elif func == "SPC$":   return " " * args[0]
        elif func == "SQR":    return math.sqrt(args[0])
        elif func == "STR$":   return str(args[0])
        elif func == "TAN":    return math.tan(args[0])
        else : raise Exception("Invalid function '" + func + "' ; line " + line)
        return None

    def print_to_buffer(self, nodes, line):
        s = ""
        for n in nodes[0].children:
            if not n.node_type == "STRING":
                s += str(self.interpret_expression(nodes[0], line))
                break
            else:
                s += n.content
        s = s.replace('"', '')
        if len(self.out_buffer) == 0 or self.print_newline:
            self.out_buffer.append(s)
        else:
            self.out_buffer[-1] += s
            
    def interpret_literal_exp(self, exp, line):
        literal = exp.children[0]
        if literal.node_type == "LITERAL":
            if literal.content.isdigit():
                return int(literal.content)
            elif literal.content.replace('.','',1).isdigit():
                return float(literal.content)
            raise Exception("Invalid Literal type '" + literal.content + "' ; line " + line)
        elif literal.node_type == "IDENTIFIER" and literal.content in self.identifiers.keys():
            return self.identifiers[literal.content]
        raise Exception("Identifier '" + literal.content + "' referenced before declaration ; line " + line)

    def interpret_binary_exp(self, exp, line):
        left = self.interpret_expression(exp.children[0], line)
        op = exp.children[1].content
        right = self.interpret_expression(exp.children[2], line)
        if type(left) is str or type(right) is str: 
            raise Exception("Invalid operation. Cannot use '" + op + "' with strings ; line " + line)
        if   op == "+":   return left +  right
        elif op == "-":   return left -  right
        elif op == "/":   return left /  right
        elif op == "*":   return left *  right
        elif op == "%":   return left %  right
        elif op == "^":   return left ** right
        elif op == "EQ":  return int(left == right)
        elif op == "LT":  return int(left < right)
        elif op == "GT":  return int(left > right)
        elif op == "LE":  return int(left <= right)
        elif op == "GE":  return int(left >= right)
        elif op == "NE":  return int(left != right)
        elif op == "AND": return int(left and right)
        elif op == "OR":  return int(left or right)
        elif op == "XOR": return int((left and not right) or (not left and right))
        raise Exception("Invalid operator '" + op + "' ; line " + line)
    
    def interpret_unary_exp(self, exp, line):
        left = exp.children[0].content
        right = self.interpret_expression(exp.children[1], line)
        if   left == "-":   return -right
        elif left == "NOT": return int(not right)
        raise Exception("Invalid operator '" + left + "' ; line " + line)
    
    def interpret_line(self, line_tree):
        line = line_tree.line
        nodes = line_tree.children
        for i in range(len(nodes)):
            if not self.is_running:
                return
            elif nodes[i].node_type == "VAR-DEC": 
                self.interpret_var_dec(nodes[i+1:], line)
            elif nodes[i].node_type == "IDENTIFIER":
                self.interpret_var_assign(nodes[i:], line)
            elif nodes[i].node_type == "NO-PARAM":
                self.function_handler(nodes[i].content, [], line)
            elif nodes[i].node_type == "PRINT":
                self.print_to_buffer(nodes[i+1:], line)
                self.print_newline = nodes[i].content == "PRINTL"

    def interpret(self, parse_tree):
        self.is_running = True
        #print(parse_tree)
        for subtree in parse_tree.children:
            if self.is_running:
                print("\nInterpreting line " + subtree.line)
                self.interpret_line(subtree)
        #return self.out_buffer
        return {"identifiers": self.identifiers, "out_buffer": self.out_buffer}