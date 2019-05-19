import math, random, copy
from Stack import Stack
import Constants as constants

class Interpreter:

    def __init__(self):
        self.out_buffer = []
        self.identifiers = {}
        self.max_line = None
        self.lines = {}
        self.is_running = True
        self.print_newline = False
        self.subroutine_stack = Stack()

    def interpret_var_dec(self, nodes, line):
        ident = nodes[0].content
        if ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' has already been declared ; line " + str(line))
        self.identifiers[ident] = self.interpret_expression(nodes[2], line)

    def interpret_var_assign(self, nodes, line):
        ident = nodes[0].content
        if not ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' referenced before declaration ; line " + str(line))
        self.identifiers[ident] = self.interpret_expression(nodes[2], line) 

    def interpret_expression(self, exp, line):
        if    exp.node_type == "LITERAL_EXP" : return self.interpret_literal_exp(exp, line)
        elif  exp.node_type == "BINARY_EXP"  : return self.interpret_binary_exp(exp, line)
        elif  exp.node_type == "UNARY_EXP"   : return self.interpret_unary_exp(exp, line)
        elif  exp.node_type == "STRING_EXP"  : return exp.children[1].content
        elif  exp.node_type == "FUNCTION_EXP": return self.interpret_func_exp(exp, line)
        elif  exp.node_type == "GROUPING_EXP": return self.interpret_group_exp(exp, line)
        raise Exception("Invalid Expression type '" + exp.node_type + "' ; line " + line)

    def get_func_rules(self, func, line):
        if func in self.identifiers.keys():
            return ["ANY" for p in self.identifiers[func]["params"]]
        try:
            return constants.FUNCTION_RULES[func]
        except KeyError:
            raise Exception("Function '" + func + "' referenced before declaration ; line " + line)

    def validate_args(self, func, args, line):
        rules = self.get_func_rules(func, line)
        if len(args) != len(rules):
            msg = "Invalid number of parameters for '" + func + "'. Expected "
            raise Exception(msg + str(len(rules)) + " , got " + str(len(args)) + " ; line " + line)
        for i in range(len(args)):
            if rules[i] == "NUMERIC" and not isinstance(args[i], (int, float)):
                raise Exception("Invalid parameter '" + str(args[i]) + "'. Expected " + "NUMERIC ; line " + line)
            elif rules[i] == "ANY" and type(args[i]) is str:
                args[i] = args[i].replace('"', '')
        return args

    def interpret_args(self, exp, line):
        ignore = ["COMMA", "LEFT_PAREN", "RIGHT_PAREN"]
        return [self.interpret_expression(a, line) for a in exp.children[1].children if not a.node_type in ignore]

    def interpret_func_exp(self, exp, line):
        func = exp.children[0].content
        if not func in self.identifiers.keys():
            args = self.validate_args(func, self.interpret_args(exp, line), line)
            return self.function_handler(func, args, line)
        args = self.filter_nodes(exp.children[1].children[1:-1], ["COMMA"])
        if type(self.identifiers[func]) is list:
            return self.interpret_array_access(func, args, line)
        return self.interpret_udf(func, args, line)
    
    def interpret_group_exp(self, group, line):
        exp = group.children[1:-1]
        return self.interpret_nodes(exp, line)

    def filter_nodes(self, nodes, filter_types):
        cleaned = []
        for n in nodes:
            if not n.node_type in filter_types:
                cleaned.append(n)
        return cleaned

    def interpret_udf(self, func, args, line):
        params, fdef = self.identifiers[func]['params'], copy.deepcopy(self.identifiers[func]['def'])
        if len(args) != len(params): raise Exception(
          "Expected '" + str(len(params)) + "' param(s), but encountered '" + str(len(args)) + "' ; line " + str(line)
        )
        for i in range(len(args)):
            args[i] = self.interpret_expression(args[i], line)
        for n in range(0, len(fdef)):
            for j in range(len(params)):
                fdef[n] = self.inject_argument(fdef[n], params[j], args[j], line) 
        if fdef[0].node_type == "GO-DEF":  return self.go_handler(fdef, line)
        elif fdef[0].node_type == "PRINT": return self.print_to_buffer(fdef, line)
        return self.interpret_expression(fdef[0], line)

    def inject_argument(self, exp, param, arg, line):
        #print("  Injecting argument '" + str(arg) + "' into " + param)
        for i in range(len(exp.children)):
            if exp.children[i].content == param:
                exp.children[i].node_type = "LITERAL"
                exp.children[i].content = str(arg)
            if len(exp.children[i].children) > 0:
                exp.children[i] = self.inject_argument(exp.children[i], param, arg, line)
        return exp
        
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
        elif func == "RETURN": 
            if self.subroutine_stack.is_empty(): 
                raise Exception("No subroutines to return from ; line " + str(line))
            after_subr = int(self.subroutine_stack.pop())
            return self.go_handler(self.lines[after_subr].children, after_subr, True)
        else : raise Exception("Invalid function '" + func + "' ; line " + str(line))
        return None

    def print_to_buffer(self, nodes, line):
        s = ""
        for n in nodes[1].children:
            if not n.node_type == "STRING":
                s += str(self.interpret_expression(nodes[1], line))
                break
            else:
                s += n.content
        s = s.replace('"', '')
        if len(self.out_buffer) == 0 or self.print_newline:
            self.out_buffer.append(s)
        else:
            self.out_buffer[-1] += s
        self.print_newline = nodes[0].content == "PRINTL"

    def find_closest_line(self, line_num, forward=True):
        if line_num > self.max_line:
            return self.max_line
        for ln in self.lines.keys():
            if forward and ln > line_num:
                return ln

    def go_handler(self, nodes, line, to_next=False):
        #print("Going to line " + str(line))
        if nodes[0].content == "GOSUB":
            self.subroutine_stack.push(int(nodes[1].line))
        if to_next and not (line+1) in self.lines.keys():
            line_num = line + 1
        else:    
            line_num = self.interpret_expression(nodes[1], line)
        if line_num > self.max_line:
            self.is_running = False
            return None
        elif not line_num in self.lines.keys():
            line_num = self.find_closest_line(line_num)
        
        self.interpret_nodes(self.lines[int(line_num)].children, line_num)
        if not self.subroutine_stack.is_empty():
            next_line = int(line_num)+1
            if next_line > self.max_line:
                self.is_running = False
                return None
            elif not next_line in self.lines.keys():
                next_line = self.find_closest_line(next_line)
            self.interpret_nodes(self.lines[next_line].children, next_line)

    def interpret_literal_exp(self, exp, line):
        literal = exp.children[0]
        if literal.node_type == "LITERAL":
            if literal.content.isdigit():
                return int(literal.content)
            elif literal.content.replace("-", '', 1).replace('.','',1).isdigit():
                return float(literal.content)
            return str(literal.content).replace('"','')
        elif literal.node_type == "IDENTIFIER" and literal.content in self.identifiers.keys():
            return self.identifiers[literal.content]
        raise Exception("Identifier '" + literal.content + "' referenced before declaration ; line " + line)

    def interpret_binary_exp(self, exp, line):
        left = self.interpret_expression(exp.children[0], line)
        op = exp.children[1].content
        right = self.interpret_expression(exp.children[2], line)
        #print(str(left) + " " + str(op) + " " + str(right))
        if op in ["/", "%"] and right == 0:
            raise Exception("Cannot divide/modulo by zero ; line " + line)
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
    
    def declare_function(self, nodes, line):
        ident = nodes[2].content
        if ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' has already been declared ; line " + line)
        self.identifiers[ident] = { 
            "params": [p.content for p in nodes[4].children if p.content.replace("$","").isidentifier()],
            "def": nodes[7:]
        }

    def interpret_if(self, nodes, line):
        if self.interpret_expression(nodes[1], line) == 1:
            self.interpret_nodes(nodes[3:], line)
        #else: print(self.interpret_expression(nodes[1], line))

    def interpret_array_dec(self, nodes, line):
        ignore = ["COMMA", "LEFT_PAREN", "RIGHT_PAREN"]
        arr_def = nodes[1].children
        ident = arr_def[0].content
        indices = args = [self.interpret_expression(a, line) for a in arr_def[1].children if not a.node_type in ignore]
        if ident in self.identifiers.keys():
            raise Exception("Identifier '" + ident + "' has already been declared ; line " + line)
        elif len(indices) > 3: 
            raise Exception("Arrays have a maximum dimension of three ; line " + line)
        elif len(indices) == 0:
            raise Exception("Arrays must have a minimum dimension of one ; line " + line)
        cols = indices[0]
        rows = indices[1] if len(indices) > 1 else 1
        sheets = indices[2] if len(indices) == 3 else 1
        arr = [[[None for k in range(sheets)] for j in range(rows)] for i in range(cols)]
        self.identifiers[ident] = arr

    def interpret_array_access(self, identifier, args, line):
        indices = [0,0,0]
        for index in range(len(args)):
            indices[index] = self.interpret_expression(args[index], line)
        return self.identifiers[identifier][indices[0]][indices[1]][indices[2]]

    def interpret_array_assign(self, nodes, line):
        identifier = nodes[0].children[0].content
        exp = self.interpret_expression(nodes[2], line)
        indices = [0,0,0]
        args = self.interpret_args(nodes[0], line)
        for index in range(len(args)):
            indices[index] = args[index]
        self.identifiers[identifier][indices[0]][indices[1]][indices[2]] = exp

    def interpret_for(self, nodes, line):
        if not nodes[1].content in self.identifiers.keys():
            self.interpret_var_dec(nodes[1:], line)
        else:
            self.interpret_var_assign(nodes[1:], line)
        iter_id = nodes[1].content
        start = self.identifiers[iter_id]
        end = self.interpret_expression(nodes[5], line)
        step = self.interpret_expression(nodes[7], line)
        next_line = int(line)+1
        next_node = None

        while self.identifiers[iter_id] < end and self.is_running:
            #print("For loop iteration " + str(self.identifiers[iter_id]))
            next_line = self.find_closest_line(int(next_line))
            next_node = self.lines[next_line].children[0]
            if self.identifiers[iter_id] <= end:
                if next_node.node_type == "FOR-END":
                    self.identifiers[iter_id] += step
                    next_line = line
                elif not self.lines[next_line].children[0].node_type == "FOR-END":
                    self.interpret_nodes(self.lines[next_line].children, next_line)
                    next_line += 1
            else:
                raise Exception("For loop end not interpreted correctly ; line " + line)

    def interpret_nodes(self, nodes, line):
        nt = nodes[0].node_type
        #print("Interpreting line " + str(line) + "  -> " + nt)
        if not self.is_running:
            return None
        elif nt == "FUNC-DEC":
            return self.declare_function(nodes, line)
        elif nt == "VAR-DEC": 
            return self.interpret_var_dec(nodes[1:], line)
        elif nt == "IDENTIFIER":
            return self.interpret_var_assign(nodes, line)  
        elif nt == "NO-PARAM":
            return self.function_handler(nodes[0].content, [], line)
        elif nt == "PRINT":
            return self.print_to_buffer(nodes, line)
        elif nt == "GO-DEF":
            return self.go_handler(nodes, line)
        elif nt == "FUNCTION_EXP":
            func = nodes[0].children[0].content
            if func in self.identifiers.keys() and type(self.identifiers[func]) is list:
                return self.interpret_array_assign(nodes, line)
            else:
                return self.interpret_func_exp(nodes[0], line)
        elif nt in ["BINARY_EXP", "GROUPING_EXP", "UNARY_EXP"]:
            return self.interpret_expression(nodes[0], line)
        elif nt == "IF-DEF":
            return self.interpret_if(nodes, line)
        elif nt == "ARR-DEC":
            return self.interpret_array_dec(nodes, line)
        elif nt == "FOR-DEF":
            return self.interpret_for(nodes, line)
        elif nt == "FOR-END":
            return None
        raise Exception("Should never get here! Unhandled node type " + nt)

    def load_code(self, parse_tree):
        self.max_line = int(parse_tree.children[-1].line)
        for subtree in parse_tree.children:
            self.lines[int(subtree.line)] = subtree

    def debug(self, parse_tree):
        self.interpret(parse_tree)
        return {
          "out_buffer": self.out_buffer, "identifiers":   self.identifiers,
          "max_line":   self.max_line  , "lines":         self.lines,
          "is_running": self.is_running, "print_newline": self.print_newline
        }

    def interpret(self, parse_tree):
        #print(parse_tree)
        self.load_code(parse_tree)
        self.is_running = True
        line = -1
        try:
            for subtree in parse_tree.children:
                if self.is_running:
                    line = subtree.line
                    nodes = subtree.children
                    while not self.subroutine_stack.is_empty():
                        subr_line = self.subroutine_stack.pop()
                        self.interpret_nodes(self.lines[subr_line].children, subr_line)
                    self.interpret_nodes(nodes, line)
            return self.out_buffer
        except RecursionError:
            print("Interpreter failed. Max recursion depth exceeded ; line " + line)