import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game - 3 Levels")

WHITE = (240,240,240)
BLACK = (30,30,30)
BLUE = (50,150,255)
RED = (255,80,80)
GREEN = (0,200,0)
PURPLE = (150,0,150)  # enemy color

font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 60)

levels = [9, 13, 17]
current_level = 0

def generate_maze(n):
    maze = [[1]*n for _ in range(n)]

    def dfs(x, y):
        maze[x][y] = 0
        dirs = [(0,2),(2,0),(-2,0),(0,-2)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0<=nx<n and 0<=ny<n and maze[nx][ny]==1:
                maze[x+dx//2][y+dy//2] = 0
                dfs(nx, ny)

    dfs(0,0)
    return maze

def setup_level():
    global maze, CELL, player, goal, start_time, win, enemies

    n = levels[current_level]
    if n % 2 == 0:
        n += 1

    maze = generate_maze(n)
    CELL = WIDTH // n
    player = [0,0]
    goal = [n-1, n-1]
    start_time = time.time()
    win = False

    # 🧟 Enemies setup
    enemies = []
    for _ in range(current_level + 1):
        while True:
            x = random.randint(0, n-1)
            y = random.randint(0, n-1)
            if maze[x][y] == 0 and [x,y] != player and [x,y] != goal:
                enemies.append([x,y])
                break

setup_level()

def draw():
    screen.fill(WHITE)

    # Maze
    for i in range(len(maze)):
        for j in range(len(maze)):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, BLACK,
                    (j*CELL, i*CELL, CELL, CELL), border_radius=6)

    # Player
    pygame.draw.circle(screen, BLUE,
        (player[1]*CELL + CELL//2, player[0]*CELL + CELL//2), CELL//3)

    # Goal
    pygame.draw.circle(screen, RED,
        (goal[1]*CELL + CELL//2, goal[0]*CELL + CELL//2), CELL//3)

    # 🧟 Enemies draw
    for ex, ey in enemies:
        pygame.draw.circle(screen, PURPLE,
            (ey*CELL + CELL//2, ex*CELL + CELL//2), CELL//3)

    elapsed = int(time.time() - start_time)
    score = max(0, 1000 - elapsed*10)

    t1 = font.render(f"Level: {current_level+1}", True, BLACK)
    t2 = font.render(f"Time: {elapsed}s", True, BLACK)
    t3 = font.render(f"Score: {score}", True, BLACK)

    screen.blit(t1, (10, 600))
    screen.blit(t2, (200, 600))
    screen.blit(t3, (380, 600))

    if win:
        msg = big_font.render("LEVEL COMPLETE!", True, GREEN)
        screen.blit(msg, (100, 250))

        if current_level < 2:
            msg2 = font.render("Press N for Next Level", True, BLACK)
        else:
            msg2 = font.render("Game Completed 🎉", True, BLACK)

        screen.blit(msg2, (150, 320))

    pygame.display.update()

running = True

while running:
    pygame.time.delay(120)  # thoda slow for enemies

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Next level
            if win and event.key == pygame.K_n:
                if current_level < 2:
                    current_level += 1
                    setup_level()

            if not win:
                x, y = player

                if event.key == pygame.K_UP:
                    nx, ny = x-1, y
                elif event.key == pygame.K_DOWN:
                    nx, ny = x+1, y
                elif event.key == pygame.K_LEFT:
                    nx, ny = x, y-1
                elif event.key == pygame.K_RIGHT:
                    nx, ny = x, y+1
                else:
                    continue

                if 0<=nx<len(maze) and 0<=ny<len(maze) and maze[nx][ny]==0:
                    player = [nx, ny]

    # 🧟 Enemy movement
    for i in range(len(enemies)):
        ex, ey = enemies[i]

        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = ex + dx, ey + dy
            if 0<=nx<len(maze) and 0<=ny<len(maze) and maze[nx][ny]==0:
                enemies[i] = [nx, ny]
                break

    # 💥 Collision (enemy hit)
    for ex, ey in enemies:
        if player == [ex, ey]:
            setup_level()  # restart level

    # 🏆 Win check
    if player == goal:
        win = True

    draw()

pygame.quit()