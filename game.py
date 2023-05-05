import pygame
import math
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

FONT = pygame.font.SysFont("arial", 20)
FONT_POINT = pygame.font.SysFont("arial", 40)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
tick = 30

class Ball():
    
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.xFac = -10
        self.yFac = 10
        self.radius = radius
        self.ball = pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.xFac
        self.y += self.yFac
        
        if self.y <= self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.yFac *= -1
            
        if self.x <= self.radius:
            return "left_wall"
        
        if  self.x >= SCREEN_WIDTH - self.radius:
            return "right_wall"
    
    def hit(self):
        self.xFac *= -1
        
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        
    def draw(self):
        self.ball = pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)
        
    def get_ball(self):
        return self.ball

class Player():
    
    def __init__(self, x, y, width, height):
        self.player_rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((x,y), (width, height)))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.score = 0
        
    def move(self, dy):
        if self.player_rect.top + dy >= 0 and self.player_rect.bottom + dy <= SCREEN_HEIGHT:
            self.y += dy
    
    def draw(self):
        self.player_rect = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((self.x,self.y), (self.width, self.height)))
    
    def get_score(self):
        return self.score
    
    def point(self):
        self.score += 1
    
    def get_rect(self):
        return self.player_rect
        

def draw_window(listPlayers, ball):
    screen.fill((0,0,0))
    listPlayers[0].draw()
    listPlayers[1].draw()
    ball.draw()
    
    text = FONT.render("Player 1: " + str(listPlayers[0].get_score()), 1, (255, 255, 255))
    screen.blit(text, (100, 0))
    
    text = FONT.render("Player 2: " + str(listPlayers[1].get_score()), 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 200, 0))
    
    pygame.display.update()

def point_screen(listPlayers, winner):
    text1 = FONT_POINT.render("", 1, (255, 255, 255))
    if winner == listPlayers[0]:
        text1 = FONT_POINT.render("Player 1 won", 1, (255, 255, 255))
        
    if winner == listPlayers[1]:
        text1 = FONT_POINT.render("Player 2 won", 1, (255, 255, 255))
        
    text_rect1 = text1.get_rect(center = (SCREEN_WIDTH // 2, 200))
    
    text2 = FONT.render("Press SPACE to play again", 1, (255, 255, 255))
    text_rect2 = text2.get_rect(center = (SCREEN_WIDTH // 2, 300))  
        
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    
    pygame.display.update()

def handle_moves(listPlayers, ball):
    key = pygame.key.get_pressed()
    if key[pygame.K_s]:
        listPlayers[0].move(10)
    if key[pygame.K_w]:
        listPlayers[0].move(-10)
        
    if key[pygame.K_DOWN]:
        listPlayers[1].move(10)
    if key[pygame.K_UP]:
        listPlayers[1].move(-10)
    
    for player in listPlayers:    
        if pygame.Rect.colliderect(ball.get_ball(), player.get_rect()):
            ball.hit()
    
    wall_hit = ball.move()
    if wall_hit == "left_wall":
        listPlayers[1].point()
        return listPlayers[1]
        
    elif wall_hit == "right_wall":
        listPlayers[0].point()
        return listPlayers[0]

def main():
    running = True
    player1 = Player(0,0, 30, 200)
    player2 = Player(SCREEN_WIDTH - 30, 0, 30, 200)
    listPlayers = [player1, player2]
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 20)
    game_status = "game"
    winner = None
    while running:
        clock.tick(tick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if game_status == "game":
            winner = handle_moves(listPlayers, ball)
            if winner != None:
                game_status = "point"
        
        if game_status == "point":
            point_screen(listPlayers, winner)
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                winner = None
                ball.reset()
                game_status = "game"
            
        draw_window(listPlayers, ball)
    
    
    pygame.quit()

if __name__ == "__main__":
    main()