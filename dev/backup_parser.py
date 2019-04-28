def parse_expression(self, node_stack, line):
    while not node_stack.is_empty():
        # ---- BINARY EXPRESSION ---- #
        print("Parsing an Expression...")
        print(node_stack.peek().node_type)
        if isinstance(node_stack.peek(), Expression_Node):
            print("   Found an expression node")
            if node_stack.peek().node_type == "BINARY_EXP":
                left = node_stack.pop()
                if node_stack.peek().node_type == "BINARY":
                    op = node_stack.pop()
                    if not node_stack.is_empty():
                        if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
                            right = Literal_Exp(node_stack.pop())
                        elif node_stack.peek().node_type == "BINARY":
                            raise SyntaxError("Unexpected start of binary expression on line " + line)
                        elif isinstance(node_stack.peek(), Expression_Node) or node_stack.peek().node_type in ["LEFT_PAREN"]:
                            right = self.parse_expression(node_stack, line)
                        else:
                            raise SyntaxError("Unexpected token on line " + line)
                    else:
                        raise SyntaxError("Unexpected end of expression on line " + line)
                    exp = Expression_Node(Binary_Exp(left, op, right), line=line)
                    if not node_stack.is_empty():
                        node_stack.push(exp)
                        return self.parse_expression(node_stack, line)
                    return exp
                elif node_stack.peek().node_type == "RIGHT_PAREN":
                    print("A: Finished Group")
                    print(left)
                    return left
                else:
                    raise Exception("Unexpected token " + node_stack.peek().node_type)
            else:
                print(node_stack.peek().node_type)
                raise SyntaxError("Unexpected Expression type on line " + line)    
        elif node_stack.peek().node_type == "LEFT_PAREN":
            print("   Starting a grouping expression node")
            start_group = node_stack.pop()
            while not node_stack.is_empty() and node_stack.peek().node_type != "RIGHT_PAREN":
                if node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
                    exp = self.parse_expression(node_stack, line)
                    if node_stack.is_empty():
                        raise SyntaxError("Unterminated group, missing ')' expected on line " + line)
                    end_group = node_stack.pop()
                    print("!!!! " + str(node_stack.count()))
                    if not node_stack.is_empty():
                        node_stack.push(exp)
                        return self.parse_expression(node_stack, line)
                    return Expression_Node(Grouping_Exp(start_group, exp, end_group), line)
                else:
                    raise Exception("Unexpected token")
        elif node_stack.peek().node_type in ["IDENTIFIER", "LITERAL"]:
            print("   Found an identifier node")
            left = Literal_Exp(node_stack.pop())
            if node_stack.peek().node_type == "BINARY":
                op = node_stack.pop()
                if node_stack.peek().node_type in ["IDENTIFIER","LITERAL"]:
                    right = Literal_Exp(node_stack.pop())
                    exp = Binary_Exp(left, op, right)
                    if node_stack.is_empty() or node_stack.peek().node_type == "RIGHT_PAREN":
                        print("B: Finished Group")
                        return exp
                    else:
                        node_stack.push(Expression_Node(exp, line=line))
                        return self.parse_expression(node_stack, line)
                else:
                    raise Exception("Unexpected token")
            elif node_stack.peek().node_type == "RIGHT_PAREN":
                node_stack.push(Expression_Node(left, line))
                if node_stack.is_empty():
                    return node_stack.pop()
                return self.parse_expression(node_stack, line)
            else:
                raise Exception("Unexpected token")
        else:
            print("ELSE " + node_stack.peek().node_type)
            print("DEBUG break out of parse_expression()") # TODO: DEBUG
            break # TODO:  DEBUG
    raise Exception("Parsing Expression failed for line " + line)

