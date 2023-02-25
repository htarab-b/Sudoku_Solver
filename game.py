import pygame
import random
import sudoku
from tkinter import filedialog

M = 9
di = 2

pygame.font.init()

screen = pygame.display.set_mode((500, 640))

pygame.display.set_caption("SUDOKU Game")
img = pygame.image.load('icon.png')
pygame.display.set_icon(img)

x = 0
y = 0
dif = 500 / 9
val = 0

grid =[
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

stars = [
    "X",
    "X X",
    "X X X",
    "X X X X",
    "X X X X X"
]

font1 = pygame.font.SysFont("Copperplate Gothic", 40)
font2 = pygame.font.SysFont("Lucida Console", 20)
def get_cord(pos):
	global x
	x = pos[0]//dif
	global y
	y = pos[1]//dif

def draw_box():
	for i in range(2):
		pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
		pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)

def draw():		
	for i in range (9):
		for j in range (9):
			if grid[i][j]!= 0:
				pygame.draw.rect(screen, (30, 144, 255), (i * dif, j * dif, dif + 1, dif + 1))
				text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
				screen.blit(text1, (i * dif + 15, j * dif + 15))
	for i in range(10):
		if i % 3 == 0 :
			thick = 7
		else:
			thick = 1
		pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
		pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)	

def draw_val(val):
	text1 = font1.render(str(val), 1, (0, 0, 0))
	screen.blit(text1, (x * dif + 15, y * dif + 15))

def raise_error1():
	text1 = font1.render("WRONG !!!", 1, (0, 0, 0))
	screen.blit(text1, (20, 570))
def raise_error2():
	text1 = font1.render("Wrong !!! Not a valid Key", 1, (0, 0, 0))
	screen.blit(text1, (20, 570))

def valid(m, i, j, val):
	for it in range(9):
		if m[i][it]== val:
			return False
		if m[it][j]== val:
			return False
	it = i//3
	jt = j//3
	for i in range(it * 3, it * 3 + 3):
		for j in range (jt * 3, jt * 3 + 3):
			if m[i][j]== val:
				return False
	return True

# From app.py
def puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j],end = " ")
        print()
    print()

def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
    startRow = row - row % 3
    startCol = col - col % 3

    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False

    return True

def Suduko(grid, row, col):
    if (row == M - 1 and col == M):
        return True

    if col == M:
        row += 1
        col = 0

    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)

    for num in range(1, M + 1, 1): 
        if solve(grid, row, col, num):
            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                return True
        grid[row][col] = 0

    return False

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("JPG files",
														"*.jpg*"),
                                                    ("JPEG files",
														"*.jpeg*"),
													("PNG files",
														"*.png*")))
	
    sudoku.imgsudoku(filename)

def reset():
    for i in range(9):
        for j in range(9):
            grid[i][j] = 0

def submit():
    if (Suduko(grid, 0, 0)):
        puzzle(grid)
    else:
        print("Solution does not exist:(")

def generate():
    reset()
    star = stars[di]

    if star == 'X':
        starval = 46
    elif star == 'X X':
        starval = 50
    elif star == 'X X X':
        starval = 55
    elif star == 'X X X X':
        starval = 59
    elif star == 'X X X X X':
        starval = 62

    grid[0][0]=(random.randint(6,9))
    grid[8][0]=(random.randint(1,5))
    grid[0][8]=(random.randint(1,5))
    grid[8][8]=(random.randint(6,9))
    grid[4][4]=(random.randint(1,9))
    grid[2][2]=(random.randint(1,5))
    grid[2][6]=(random.randint(6,9))
    grid[6][2]=(random.randint(6,9))
    grid[6][6]=(random.randint(1,5))
    
    submit()

    rang = starval
    ini = 0
    while ini < rang:
        r = random.randint(0,8)
        c = random.randint(0,8)
        if grid[r][c] == 0:
            rang = rang + 1
        else:
            grid[r][c] = 0
        ini = ini + 1

# Program Functions
def instruction():
    text1 = font2.render("PRESS D TO GENERATE / R TO RESET", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO SOLVE", 1, (0, 0, 0))
    text3 = font2.render("PRESS O TO SOLVE SCANNED IMAGE", 1, (0, 0, 0))
    text4 = font2.render("PRESS SPACE TO CHANGE DIFFICULTY", 1, (0, 0, 0))
    text5 = font2.render("CURRENT DIFFICULTY : " + stars[di], 1, (0, 0, 0))
    screen.blit(text1, (20, 520))	
    screen.blit(text4, (20, 540))
    screen.blit(text5, (20, 560))
    screen.blit(text2, (20, 580))
    screen.blit(text3, (20, 600))

def result():
	text1 = font1.render("FINISHED PRESS R or D", 1, (0, 0, 0))
	screen.blit(text1, (20, 570))
run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
while run:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            get_cord(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x+= 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y-= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y+= 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                flag2 = 1
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                grid =[
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0]
				]
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                generate()
            if event.key == pygame.K_o:
                rs = 0
                error = 0
                flag2 = 0
                browseFiles()
            if event.key == pygame.K_SPACE:
                if di==4:
                    di = 0
                else:
                    di+= 1

    if flag2 == 1:
        submit()
        flag2 = 0
    if val != 0:		
        draw_val(val)
        if valid(grid, int(x), int(y), val)== True:
            grid[int(x)][int(y)]= val
            flag1 = 0
        else:
            grid[int(x)][int(y)]= 0
            raise_error2()
        val = 0
	
    if error == 1:
        raise_error1()
    if rs == 1:
        result()
    draw()
    if flag1 == 1:
        draw_box()	
    instruction()

    pygame.display.update()

pygame.quit()
