from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def precedence(op):
    if op in ('+', '-'): return 1
    if op in ('*', '/'): return 2
    if op in ('^',): return 3
    return 0

def is_left_associative(op):
    return op in ('+', '-', '*', '/')  # '^' is right-associative

def infix_to_postfix(expression):
    output = []
    stack = []
    for char in expression:
        if char.isalnum():  # Operand
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif char == " ":
            continue
        else:  # Operator
            while (stack and stack[-1] != '(' and
                   (precedence(stack[-1]) > precedence(char) or
                   (precedence(stack[-1]) == precedence(char) and is_left_associative(char)))):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)

def infix_to_prefix(expression):
    stack = []
    output = []
    expression = expression[::-1]
    expression = ''.join(['(' if char == ')' else ')' if char == '(' else char for char in expression])
    
    for char in expression:
        if char.isalnum():  # Operand
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif char == " ":
            continue
        else:  # Operator
            while (stack and stack[-1] != '(' and
                   (precedence(stack[-1]) > precedence(char) or
                   (precedence(stack[-1]) == precedence(char) and not is_left_associative(char)))):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output[::-1])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    infix_expr = data.get('expression', '')
    postfix_expr = infix_to_postfix(infix_expr)
    prefix_expr = infix_to_prefix(infix_expr)
    return jsonify({"postfix": postfix_expr, "prefix": prefix_expr})

if __name__ == '__main__':
    app.run(debug=True)
