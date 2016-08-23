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
    

    