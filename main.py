import pygame
import time
import random
import os
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Rocks')

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))
spaceship_img = pygame.image.load(os.path.join("assets", "player.png"))
enemy_img = pygame.image.load(os.path.join("assets", "enemy.png"))
bullet_img = pygame.image.load(os.path.join("assets", "bullet.png"))
bullet_img = pygame.transform.scale(bullet_img, (20, 40))
ufo_img = pygame.image.load(os.path.join("assets", "ufo.png"))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 30
STAR_HEIGHT = 20
STAR_VEL = 3
BULLET_VEL = 10

FONT = pygame.font.SysFont("comicsans", 30)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = bullet_img

    def draw(self, window):
        # print("bullet.draw called")
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= BULLET_VEL

    def collide(self, stars, ufos):
        for star in stars:
            if pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height()).colliderect(star):
                stars.remove(star)
                return True
        for ufo in ufos:
            if pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height()).colliderect(ufo):
                ufos.remove(ufo)
                return True

        return False


def draw(player, elapsed_time, stars, ufos, bullets):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, 'white')
    WIN.blit(time_text, (10, 10))

    # pygame.draw.rect(WIN, "red", player)
    WIN.blit(spaceship_img, (player.x, player.y))

    for star in stars:
        # WIN.blit(ufo_img, (star.x, star.y))
        WIN.blit(enemy_img, (star.x, star.y))
        # pygame.draw.rect(WIN, 'white', star)
    
    for ufo in ufos:
        WIN.blit(ufo_img, (ufo.x, ufo.y))

    for bullet in bullets:
        bullet.draw(WIN)

    pygame.display.update()



def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    bullets = []
    stars = []
    ufos = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT - random.randint(1, 500), STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            for _ in range(1):
                ufo_x = random.randint(0, WIDTH - STAR_WIDTH-5)
                ufo = pygame.Rect(ufo_x, -STAR_HEIGHT - random.randint(1, 500), STAR_WIDTH, STAR_HEIGHT)
                ufos.append(ufo)

            star_add_increment = max(200, star_add_increment - 50) 
            star_count = 0
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_x = player.x + player.width / 2 - bullet_img.get_width() / 2
                    bullet_y = player.y - bullet_img.get_height()
                    bullet = Bullet(bullet_x, bullet_y)
                    bullets.append(bullet)
                    print(bullet)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_UP] and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + player.height <= HEIGHT:
            player.y += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        for ufo in ufos[:]:
            ufo.y += STAR_VEL
            if ufo.y > HEIGHT:
                ufos.remove(ufo)
            elif ufo.y + ufo.height >= player.y and ufo.colliderect(player):
                ufos.remove(ufo)
                hit = True
                break
        
        
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)
            elif bullet.collide(stars, ufos):
                bullets.remove(bullet)

        if hit:
            lost_text = FONT.render("You Lose!", 1, 'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_width()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars, ufos, bullets)
        # pygame.time.delay(5)

    pygame.quit()

if __name__ == "__main__":
    main()