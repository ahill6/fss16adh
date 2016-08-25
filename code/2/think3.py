# This is the source code for homework 2.  Since most of the problems 
# really reuqire screenshots more than functional code, this is somewhat 
# unorganized and is provided just in case it is wanted.

#3.3
def right_justify(s):
    spaces = 70 - len(s)
    for i in range(spaces):
        s = " " + s
    print(s)

#3.4
def print_spam():
    print("spam")

def function_repeater(f, n, *args):
    for i in range(n):
        f(*args)
    
function_repeater(print_spam, 2)
print("\n Now print spam four times \n")
function_repeater(print_spam, 4)



#3.5
def draw_horizontal():
    print("+----"),

def draw_vertical():
    print("|    "),

def finish_horizontal():
    print("+")
    
def finish_vertical():
    print("|")

def function_repeater(f, n, *args):
    for i in range(n):
        f(*args)
        
def draw_one_row(n):
    function_repeater(draw_horizontal, n)
    finish_horizontal()
    
    for i in range(4):
        function_repeater(draw_vertical, n)
        finish_vertical()
        
def draw_box(n):
    function_repeater(draw_one_row, n, n)    
    function_repeater(draw_horizontal, n)
    finish_horizontal()
    
draw_box(4)