import pygame
import random
import sys
import sqlite3

# ゲーム画面のサイズ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
score = 0

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 画面の状態を表す定数
TITLE_SCREEN = 0
PLAY_SCREEN = 1
RANKING_SCREEN = 2
POSE_SCREEN = 3

def draw_text(siz, txt, col, bg, x, y): #画面上のテキスト表示関数
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def draw_button(bg, col_r, button, w, siz, txt, col_f): #画面上のボタン表示関数
    pygame.draw.rect(bg, col_r, button, width=w, border_radius=10)
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col_f)
    w = button[0] + button[2]/2 - sur.get_width()/2
    h = button[1] + button[3]/2 - sur.get_height()/2
    bg.blit(sur, [w, h])
    
def save_score(score): #スコアの保存
    with open("scores.txt", "a") as file:
        file.write(str(score) + "\n")
        
def save_name(name): #ユーザー名の保存
    with open("scores.txt", "a") as file:
        file.write(str(name) + "\n")
#sqliteを使うことで簡単にスコアとそれに紐づいたユーザ名が管理できると思われる
 
def show_ranking():
    scores = []  # ランキングを格納するリスト
    with open("scores.txt", "r") as file:
        for line in file:
            score_value = int(line.strip())  # 別の変数にスコアを保存
            scores.append(score_value)

    scores.sort(reverse=True)  # スコアを降順にソート

    for i, score_value in enumerate(scores[:10], 1):
        return f"{i}. {score_value}"

def main():
    pygame.init()
    pygame.display.set_caption("Game with Transition Screens")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    global playing
    previous_score = 0

    # タイトル画面のボタン
    title_buttons = [
        pygame.Rect(115, 360, 120, 40),
        pygame.Rect(175, 430, 120, 40),
        pygame.Rect(245, 500, 120, 40)
    ]
    title_button_texts = ["Play", "Ranking", "Quit"]
    
    #　プレイ画面のボタン
    play_buttons = [
        pygame.Rect(100, 500, 120, 40)
    ]
    play_button_text = ["pose"]
    
    
    # ポーズ画面のボタン
    pose_buttons = [
        pygame.Rect(115, 360, 120, 40),
        pygame.Rect(300, 360, 120, 40)
    ]
    pose_button_text = ["continue", "done"]

    # ランキング画面のボタン
    ranking_buttons = [
        pygame.Rect(115, 500, 120, 40)
    ]
    ranking_button_texts = ["Back to Title"]


    game_state = TITLE_SCREEN
    playing = True
    paused = False
    flag = 0
    while True: #ゲーム全体のwhile
        for event in pygame.event.get(): #画面遷移
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == TITLE_SCREEN:
                    for i, button in enumerate(title_buttons):
                        if button.collidepoint(event.pos):
                            if i == 0:
                                game_state = PLAY_SCREEN
                            elif i == 1:
                                game_state = RANKING_SCREEN
                            elif i == 2:
                                pygame.quit()
                                sys.exit()
                            break
                elif game_state == RANKING_SCREEN:
                    show_ranking()
                    for i, button in enumerate(ranking_buttons):
                        if button.collidepoint(event.pos):
                            game_state = TITLE_SCREEN
                            break
                elif game_state == POSE_SCREEN:
                    for i, button in enumerate(pose_buttons):
                        if button.collidepoint(event.pos):
                            if i == 0:
                                paused = False
                                #playing = True
                                flag = 1
                                game_state = PLAY_SCREEN
                            elif i == 1:
                                #playing = False
                                paused = False
                                game_state = TITLE_SCREEN
                                previous_score = 0
                            break
                        
                elif game_state == PLAY_SCREEN:
                    if paused: ###not paused
                        for i, button in enumerate(play_buttons):
                            if button.collidepoint(event.pos):
                                if i == 0:  # ポーズボタンが押された場合
                                    paused = True
                                    playing = False
                                    previous_score = score
                                    game_state = POSE_SCREEN
                                break
                        
        if game_state == TITLE_SCREEN: #タイトル画面
            # タイトル画面の描画
            screen.fill((0,0,0))
            draw_text(75, "Star Shoot", (255,255,255), screen, 200, 100)
            for i, button in enumerate(title_buttons):
                draw_button(screen, (255,255,255), button, 0, 24, title_button_texts[i], (0,0,0))
       
        elif game_state == PLAY_SCREEN: #プレイ中表示、実行されるもの
                # プレイ画面の描画
                screen.fill((0,0,0))
                if flag == 1:
                    score = previous_score
                else:
                    score = 0
                # ポーズ画面を描画します
                screen.fill(BLACK)
                draw_text(50, "Pause", WHITE, screen, 250, 100)
                pygame.display.flip()
                clock.tick(15)
                POWERUP_APPEAR_INTERVAL = 5000

                # 色
                #WHITE = (255, 255, 255)
                #BLACK = (0, 0, 0)
                #global BLACK, WHITE
                font_name = pygame.font.match_font('arial')

                # スコア表示用の関数
                def draw_score(surface, text, size, x, y):
                    font = pygame.font.Font(font_name, size)
                    text_surface = font.render(text, True, WHITE)
                    text_rect = text_surface.get_rect()
                    text_rect.midtop = (x, y)
                    surface.blit(text_surface, text_rect)

                # プレイヤーのクラス
                class Player(pygame.sprite.Sprite):
                    def __init__(self):
                        super().__init__()
                        self.image = pygame.image.load("dog.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.centerx = SCREEN_WIDTH // 2
                        self.rect.bottom = SCREEN_HEIGHT - 10
                        self.speed = 5

                    def update(self):
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT]:
                            self.rect.x -= self.speed
                        if keys[pygame.K_RIGHT]:
                            self.rect.x += self.speed
                        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
                        

                    def shoot(self):
                        bullet = Bullet(self.rect.centerx, self.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    
                    def shoot2(self):
                        bullet = Bullet2(self.rect.centerx, self.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        
                    def shoot3(self):
                        bullet = Bullet3(self.rect.centerx, self.rect.top)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                    
                    def power_up(self): #Power Up後の処理
                        self.powered_up = True
                        self.speed += 2 #スピード処理
                       
                        
                    def game_over(self):
                        global playing
                        playing = False
                        print("hit")
                        print(playing)
                            
                # 敵のクラス
                class Enemy(pygame.sprite.Sprite):
                    def __init__(self):
                        super().__init__()
                        self.image = pygame.image.load("cat.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                        self.rect.y =  0   #-40, -30
                        self.speed = random.randint(1, 3)
                        self.shoot_delay = random.randint(3000, 5000)
                        self.last_shot = pygame.time.get_ticks()

                    def update(self):
                        self.rect.x += self.speed
                        if self.rect.left < 0 or self.rect.right > 800:
                            self.speed *= -1
                        now = pygame.time.get_ticks()
                        if now - self.last_shot > self.shoot_delay:
                            self.last_shot = now
                            self.shoot()    
                        
                        if self.rect.top > SCREEN_HEIGHT:
                            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                            self.rect.y = random.randint(-100, -40)
                            self.speed = random.randint(1, 3)
                    
                    def shoot(self):
                        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        
                # 強敵のクラス
                class Enemy2(pygame.sprite.Sprite):
                    def __init__(self):
                        super().__init__()
                        self.image = pygame.image.load("cat.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                        self.rect.y =  0   #-40, -30
                        self.speed = random.randint(10, 20)
                        self.shoot_delay = random.randint(3000, 5000)
                        self.last_shot = pygame.time.get_ticks()

                    def update(self):
                        self.rect.x += self.speed
                        if self.rect.left < 0 or self.rect.right > 800:
                            self.speed *= -1
                        now = pygame.time.get_ticks()
                        if now - self.last_shot > self.shoot_delay:
                            self.last_shot = now
                            self.shoot()    
                        
                        if self.rect.top > SCREEN_HEIGHT:
                            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                            self.rect.y = random.randint(-100, -40)
                            self.speed = random.randint(10, 20)
                        
                    
                    def shoot(self):
                        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
                        all_sprites.add(bullet)
                        bullets.add(bullet)

                # 弾のクラス
                class Bullet(pygame.sprite.Sprite):
                    def __init__(self, x, y):
                        super().__init__()
                        self.image = pygame.image.load("bullet.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        if player.speed < 9:
                            self.rect.centerx = x
                        else:
                            self.rect.centerx = x - 20
                        self.rect.bottom = y
                        self.speed = 8

                    def update(self):
                        self.rect.y -= self.speed
                        if self.rect.bottom < 0:
                            self.kill()
                            
                        
                        if pygame.sprite.spritecollide(self, powerups, False): #プレイヤーの弾とパワーアップアイテムの当たり判定
                            for powerup in powerups:
                                if powerup.state == "horizontal":
                                    powerup.state = "vertical"
                            self.kill()
                                    
                # 敵の弾のクラス
                class EnemyBullet(pygame.sprite.Sprite):
                    def __init__(self, x, y, *groups):
                        super().__init__(*groups)
                        self.image = pygame.Surface((10, 20))
                        self.image.fill((255, 0, 0))
                        self.rect = self.image.get_rect()
                        self.rect.centerx = x
                        self.rect.top = y
                        self.speed = 2
                        self.score = self.speed

                    def update(self):
                        self.rect.y += self.speed
                        if self.rect.top > SCREEN_HEIGHT:
                            self.kill()
                        if pygame.sprite.collide_rect(self, player): #敵の弾とプレイヤーの当たり判定
                            player.game_over()    
                            #print(playing)     
                            
                # 進化弾のクラス
                class Bullet2(pygame.sprite.Sprite):
                    def __init__(self, x, y):
                        super().__init__()
                        self.image = pygame.image.load("bullet.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.centerx = x
                        self.rect.bottom = y
                        self.speed = 20
                        
                    def update(self):
                        self.rect.y -= self.speed
                        if self.rect.bottom < 0:
                            self.kill()
                            
                        if pygame.sprite.spritecollide(self, powerups, False): #プレイヤーの弾とパワーアップアイテムの当たり判定
                                for powerup in powerups:
                                    if powerup.state == "horizontal":
                                        powerup.state = "vertical"
                                self.kill()
                    
                # 超進化弾クラス        
                class Bullet3(pygame.sprite.Sprite):
                    def __init__(self, x, y):
                        super().__init__()
                        self.image = pygame.image.load("bullet.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.centerx = x + 30
                        self.rect.bottom = y
                        self.speed = 8
                        
                    def update(self):
                        self.rect.y -= self.speed
                        if self.rect.bottom < 0:
                            self.kill()
                        if pygame.sprite.spritecollide(self, powerups, False): #プレイヤーの弾とパワーアップアイテムの当たり判定
                                for powerup in powerups:
                                    if powerup.state == "horizontal":
                                        powerup.state = "vertical"
                                self.kill()

                # パワーアップアイテムのクラス
                class PowerUpItem(pygame.sprite.Sprite):
                    def __init__(self):
                        super().__init__()
                        self.image = pygame.image.load("born.png").convert_alpha()
                        self.rect = self.image.get_rect()
                        self.rect.x = random.choice([0, SCREEN_WIDTH - self.rect.width])
                        self.rect.y = random.randint(50, 150)
                        self.speed = random.randint(1, 3)
                        self.state = "horizontal"  # パワーアップアイテムの初期状態（横移動）

                    def update(self):
                        if self.state == "horizontal":
                            self.rect.x += self.speed
                        elif self.state == "vertical":
                            self.rect.y += self.speed
                        if pygame.sprite.collide_rect(self, player): #パワーアップアイテムとプレイヤーの当たり判定
                            self.kill()
                            player.power_up()

                        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                            self.rect.x = random.choice([0, SCREEN_WIDTH - self.rect.width])
                            self.rect.y = random.randint(50, 150)
                            self.speed = random.randint(1, 3)
                            self.state = "horizontal"


                # ゲームの初期化
                pygame.init()
                screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                clock = pygame.time.Clock()
                all_sprites = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                #enemies2 = pygame.sprite.Group()
                bullets = pygame.sprite.Group()
                enemy_bullets = pygame.sprite.Group()
                powerups = pygame.sprite.Group()
                player = Player()
                all_sprites.add(player)

                if paused == False:
                    playing = True
                else:
                    game_state == POSE_SCREEN
                    previous_score = score
                enemy_timer = pygame.time.get_ticks()
                enemy_bullet_timer = pygame.time.get_ticks()
                powerup_timer = pygame.time.get_ticks()
                # ゲームループ
                while playing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            playing = False
                        elif event.type == pygame.KEYDOWN:
                            if player.speed == 5:
                                if event.key == pygame.K_SPACE:
                                    player.shoot()
                            elif player.speed == 7:
                                if event.key == pygame.K_SPACE:
                                    #player.shoot()
                                    player.shoot2()
                            else:
                                if event.key == pygame.K_SPACE:
                                    player.shoot()
                                    #player.shoot2()
                                    player.shoot3()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for i, button in enumerate(play_buttons):
                                if button.collidepoint(pygame.mouse.get_pos()):
                                    if i == 0:  # ポーズボタンが押された場合
                                        playing = False
                                        paused = True
                                        game_state = POSE_SCREEN
                                    break
                                    
                    # 敵の出現             
                    now = pygame.time.get_ticks()
                    if now - enemy_timer > random.randint(2000, 5000):
                        enemy = Enemy()
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                        enemy_timer = now
                        
                    # 強敵の出現             
                    now = pygame.time.get_ticks()
                    if now - enemy_timer > random.randint(2000, 5000):
                        enemy = Enemy2()
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                        enemy_timer = now
                        
                    # 敵の弾の発射
                    if now - enemy_bullet_timer > random.randint(1000, 1500):
                        for enemy in enemies:
                            enemy.shoot()
                        enemy_bullet_timer = now
                            
                    # アイテムの出現
                    if now - powerup_timer > POWERUP_APPEAR_INTERVAL:
                            powerup = PowerUpItem()
                            all_sprites.add(powerup)
                            powerups.add(powerup)
                            powerup_timer = now
                                        
                    # プレイヤーの弾と敵の当たり判定
                    for bullet in bullets:
                            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
                            for enemy in enemy_hit_list:
                                bullet.kill()
                                score += abs(enemy.speed) 
                                previous_score = score
                                    
                    all_sprites.update()
                    screen.fill(BLACK)
                    all_sprites.draw(screen)
                        
                    # スコア表示
                    draw_score(screen, "Score: " + str(score), 24, SCREEN_WIDTH // 2, 10)
                    # ポーズボタンの描画
                    for i, button in enumerate(play_buttons):
                        draw_button(screen, WHITE, button, 0, 24, play_button_text[i], BLACK)
                    pygame.display.flip()
                    clock.tick(60)
                    if playing == False and paused == False:
                        print("Game Over")
                        # ゲームオーバー後の処理
                        screen.fill(BLACK)
                        draw_score(screen, "Game Over", 75, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        pygame.display.flip()
                        pygame.time.delay(2000)  # 2秒間待機
                        previous_score = 0
                        save_score(score)
                        #save_name(input())
                        game_state = TITLE_SCREEN
                        all_sprites.empty()
                        enemies.empty()
                        bullets.empty()
                        enemy_bullets.empty()
                        powerups.empty()
                        break

        elif game_state == RANKING_SCREEN: #ランキング画面の描写
            screen.fill(BLACK)
            draw_text(50, "Ranking", WHITE, screen, 200, 100)

            # ランキングの取得 正規版
            scores = []  # ランキングを格納するリスト
            with open("scores.txt", "r") as file:
                for line in file:
                    score_value = int(line.strip())  # 別の変数にスコアを保存
                    scores.append(score_value)

            scores.sort(reverse=True)  # スコアを降順にソート
            
            # ランキングの表示
            y_position = 200
            for i, score_value in enumerate(scores[:10], 1):
                draw_text(30, f"{i}. {score_value}", WHITE, screen, 300, y_position)
                y_position += 40

            for i, button in enumerate(ranking_buttons):
                draw_button(screen, WHITE, button, 0, 24, ranking_button_texts[i], BLACK)

            pygame.display.flip()
            clock.tick(15)
            
        elif game_state == POSE_SCREEN: #ポーズスクリーンの描写
            screen.fill(BLACK)
            draw_text(50, "Pose", WHITE, screen, 200, 100)
            draw_text(30, f"Score: {previous_score}", WHITE, screen, 300, 250)
            for i, button in enumerate(pose_buttons):
                draw_button(screen, WHITE, button, 0, 24, pose_button_text[i], BLACK)

        pygame.display.flip()
        clock.tick(15)

if __name__ == "__main__":
    main()
