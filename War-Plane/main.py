import pygame, random, math
from pygame.locals import *
import pygame_menu

# Main Menu
def mainmenu():
  pygame.init()
  
  try:
    pygame.mixer.music.load("탑건.mp3")  # 경로가 다르면 "audio/탑건.mp3"처럼 수정
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # -1은 무한 반복
  except Exception as e:
      print("음악 재생 오류:", e)
  
  info = pygame.display.Info()
  screenWidth, screenHeight = info.current_w, info.current_h
  surface = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
  pygame.display.set_caption("War Plane")

  # Starts the game
  def start_the_game():
    main()
    pass

  # Menu Theme
  mytheme = pygame_menu.Theme(
    background_color=(0, 0, 0, 0),
    title_background_color=(0, 0, 0),
    widget_padding=25,
    title_font="fonts/TmonMonsori.ttf.ttf",
    widget_font="fonts/TmonMonsori.ttf.ttf",
    widget_background_color=(0, 0, 0),
    title_font_size=64,
    title_offset=(0, 7.5),
    title_font_antialias=True,
    widget_font_antialias=True,
    widget_margin=(0, 10),
    widget_font_size=32,
  )

  # Menu background image
  bg = pygame_menu.baseimage.BaseImage(
  image_path="backgrounds/camo.png",
  drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
  mytheme.background_color = bg

  # Menu title and buttons
  menu = pygame_menu.Menu('탑건 스쿨', screenWidth, screenHeight, theme=mytheme)
  menu.add.button('플레이', start_the_game)
  menu.add.button('끄기',
                  pygame_menu.events.EXIT,
                  selection_color=(150, 10, 0))

  # Adds the menu to the screen
  menu.mainloop(surface)



# Main game loop
def main():
  # Defines values for width and height of the screen
  # 화면 해상도 자동으로 설정
  info = pygame.display.Info()
  screenWidth, screenHeight = info.current_w, info.current_h


  # Clock for the game, used to set the FPS
  clock = pygame.time.Clock()

  # Player class
  class Player(pygame.sprite.Sprite):
    width = 96
    height = 96
    x = (screenWidth - width) / 2
    y = (screenHeight - 2 * height)

    def __init__(self):
      super(Player, self).__init__()
      self.surf = pygame.transform.smoothscale(
        pygame.image.load('sprites/playerplane.png').convert_alpha(),
        (self.width, self.height))
      self.mask = pygame.mask.from_surface(self.surf)
      self.rect = self.surf.get_rect()
      self.rect.x = self.x
      self.rect.y = self.y
      self.speed = 3

    # Player controls
    def update(self):
      keys = pygame.key.get_pressed()
      if keys[K_UP] or keys[K_w]:
        self.rect.move_ip(0, -self.speed)
      if keys[K_DOWN] or keys[K_s]:
        self.rect.move_ip(0, self.speed)
      if keys[K_LEFT] or keys[K_a]:
        self.rect.move_ip(-self.speed, 0)
      if keys[K_RIGHT] or keys[K_d]:
        self.rect.move_ip(self.speed, 0)
      # Prevents player from moving outside the screen
      if self.rect.left < 0:
        self.rect.left = 0
      if self.rect.bottom > screenHeight:
        self.rect.bottom = screenHeight
      if self.rect.top < 0:
        self.rect.top = 0
      if self.rect.right > screenWidth:
        self.rect.right = screenWidth
      self.speed = 3 + score / 20

  # Enemy class
  class Enemy(pygame.sprite.Sprite):
    width = 96
    height = 96

    def __init__(self):
      super(Enemy, self).__init__()
      self.surf = pygame.transform.flip(
        pygame.transform.smoothscale(
          pygame.image.load('sprites/enemyplane.png').convert_alpha(),
          (self.width, self.height)), False, True)
      self.mask = pygame.mask.from_surface(self.surf)
      self.x = random.randint(self.width, screenWidth - self.width)
      self.y = random.randint(0 - screenHeight, 0)
      self.rect = self.surf.get_rect(center=(self.x, self.y))
      self.speed = 2

    def update(self):
      # Enemy movement
      self.rect.move_ip(0, self.speed)
      # Enemy is deleted when it goes past the bottom of the screen
      if self.rect.top > screenHeight:
        self.kill()
      # Speed increases by 0.1 with every point
      self.speed = 2 + (score / 10)

  # Bullet class
  class Bullet(pygame.sprite.Sprite):

    def __init__(self):
      super(Bullet, self).__init__()
      width = 32
      height = 32
      self.speed = -5
      self.surf = pygame.transform.smoothscale(
        pygame.image.load('sprites/bullet.png').convert_alpha(),
        (width, height))
      self.mask = pygame.mask.from_surface(self.surf)
      self.rect = self.surf.get_rect()
      self.rect.x = player.rect.x + player.rect.width / 2 - self.rect.width / 2
      self.rect.y = player.rect.top

    def update(self):
      # If bullet goes past the top of the screen, it gets deleted
      if self.rect.bottom < 0:
        self.kill()

  # Enemy Bullet subclass of Bullet
  class EnemyBullet(Bullet):

    def __init__(self):
      super(EnemyBullet, self).__init__()
      width = 32
      height = 32
      self.speed = 4
      self.surf = pygame.transform.smoothscale(
        pygame.image.load('sprites/enemybullet.png').convert_alpha(),
        (width, height))
      self.mask = pygame.mask.from_surface(self.surf)
      self.rect = self.surf.get_rect()
      self.rect.x = enemy.rect.x + enemy.rect.width / 2 - enemy.rect.width / 2
      self.rect.y = enemy.rect.top

    def update(self):
      # If bullet goes past the bottom of the screen, it gets deleted
      if self.rect.top > screenHeight:
        self.kill()
      # Speed increases by 0.1 with every point
      self.speed = 4 + (score / 10)

  # Sets score to 0
  score = 0

  # Starts Pygame
  pygame.init()

  # Screen Resolution
  screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

  # Game title
  pygame.display.set_caption('War Plane')

  # Adds sprites to classes and groups
  player = Player()
  enemy = Enemy()
  enemies = pygame.sprite.Group()
  bullets = pygame.sprite.Group()
  enemybullets = pygame.sprite.Group()
  all_sprites = pygame.sprite.Group()
  all_sprites.add(player)
  all_sprites.add(enemy)
  enemies.add(enemy)

  # Timer that sets when the ADDENEMY event is able to be called so too many enemies won't be created at once
  ADDENEMY = pygame.USEREVENT + 1
  pygame.time.set_timer(ADDENEMY, 1000)

  # Timer that sets when the ENEMYBULLETFIRE event is able to be called so too many enemy bullets won't be created at once
  ENEMYBULLETFIRE = pygame.USEREVENT + 2
  pygame.time.set_timer(ENEMYBULLETFIRE, 5000)

  # Background Image and turns the background into tiles to make it able to scroll
  bg = pygame.transform.smoothscale(
    pygame.image.load("backgrounds/sand.png").convert_alpha(),
    (screenWidth, screenHeight))
  scroll = 0
  tiles = math.ceil(screenHeight / bg.get_height()) + 1

  # Pause Menu
  pausetheme = pygame_menu.Theme(
    background_color=(0, 0, 0, 0),
    title_background_color=(0, 0, 0),
    widget_padding=25,
    title_font="fonts/Farenheight.ttf",
    widget_font="fonts/Farenheight.ttf",
    widget_background_color=(0, 0, 0),
    title_font_size=64,
    title_offset=(0, 7.5),
    title_font_antialias=True,
    widget_font_antialias=True,
    widget_margin=(0, 10),
    widget_font_size=32,
  )

  pause_menu = pygame_menu.Menu('Paused', 640, 480, theme=pausetheme)
  pause_menu.add.button("Continue", pygame_menu.events.BACK)
  pause_menu.add.button('Quit',
                        pygame_menu.events.EXIT,
                        selection_color=(150, 10, 0))

  # Define the paused function
  def paused():
    # Pause the game
    clock = pygame.time.Clock()
    paused = True

    while paused:
      # Tick the clock
      clock.tick(60)  # 60 FPS

      # Pause music
      pygame.mixer.music.pause()

      # Handle events
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          paused = False

      # Show the pause menu
      result = pause_menu.mainloop(screen)
      if result == pygame_menu.events.BACK:
        paused = False
      elif result == pygame_menu.events.EXIT:
        pygame.quit()
        exit()

  # When the game is running or has ended
  running = True
  end = False
  while running:
    # Sets FPS to 60
    clock.tick(60)

    # Vertical scrolling background
    i = 0
    while (i < tiles):
      screen.blit(bg, (0, -(bg.get_height() * i + scroll)))
      i = i + 1
    # Scrolling speed that increases by 0.05 with every point
    scroll = scroll - (1 + score / 20)
    if abs(scroll) > bg.get_height():
      scroll = 0

    # Handle events
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        # Pause the game and show the pause menu
        paused()

      # If Game Over, it will stop creating enemies and bullets
      if end == False:
        # Creates new enemies
        if event.type == ADDENEMY:
          new_enemy = Enemy()
          enemies.add(new_enemy)
          all_sprites.add(new_enemy)

        # Enemy bullet firing
        for new_enemy in enemies:
          if event.type == ENEMYBULLETFIRE:
            enemybullet = EnemyBullet()
            enemybullets.add(enemybullet)
            all_sprites.add(enemybullet)
            enemybullet.rect.x = new_enemy.rect.centerx - enemybullet.rect.width / 2
            enemybullet.rect.y = new_enemy.rect.bottom

        # Bullet controls
        if event.type == pygame.KEYDOWN:
          if event.key == K_SPACE:
            # Creates new bullets
            new_bullet = Bullet()
            bullets.add(new_bullet)
            all_sprites.add(new_bullet)

    # Bullet movement
    for new_bullet in bullets:
      new_bullet.rect.move_ip(0, new_bullet.speed)

    for enemybullet in enemybullets:
      enemybullet.rect.move_ip(0, enemybullet.speed)

    # Updates sprites
    player.update()
    enemies.update()
    bullets.update()
    enemybullets.update()

    # Adds sprites to the game
    for entity in all_sprites:
      screen.blit(entity.surf, entity.rect)

    # Collision detection for the player colliding with an enemy
    if pygame.sprite.spritecollideany(player, enemies,
                                      pygame.sprite.collide_mask):
      # Kills both the player and enemy and goes to the Game Over screen
      player.kill()
      enemy.kill()
      end = True

    # Collision detection for bullets hitting enemies, both the bullet and enemy get deleted
    if pygame.sprite.groupcollide(bullets, enemies, True, True,
                                  pygame.sprite.collide_mask):
      # Adds 1 point to the score whenever an enemy is killed
      score = score + 1

    # Collision detection for enemy bullets hitting the player, both sprites get deleted
    if pygame.sprite.spritecollideany(player, enemybullets,
                                      pygame.sprite.collide_mask):
      player.kill()
      enemybullet.kill()
      end = True

    # Collision detection for player and enemy bullets hitting each other, they both get deleted
    if pygame.sprite.groupcollide(bullets, enemybullets, True, True,
                                  pygame.sprite.collide_mask):
      new_bullet.kill()
      enemybullet.kill()

    # Display score in-game which updates every time an enemy is killed
    defaultfont = "fonts/AmericanCaptain.otf"
    font = pygame.font.Font(defaultfont, 32)
    scoretext = font.render("Score: " + str(score), 1, (0, 0, 0))
    screen.blit(scoretext, (4, 4))

    # Game Over screen which is displayed when the player dies
    if end == True:
      # Kills all sprites on the screen
      for entity in all_sprites:
        entity.kill()
      # Displays the background image to hide the score text, enemies and stops scrolling
      screen.blit(bg, (0, 0))
      # Defines the font size for each text
      gameoverFont = pygame.font.Font(defaultfont, 64)
      scoreFont = pygame.font.Font(defaultfont, 48)
      restartFont = pygame.font.Font(defaultfont, 32)
      gameover = gameoverFont.render("!!!GROUNDING!!!", 1, (255, 0, 0))
      # Shows the total score
      endscore = scoreFont.render("Score: " + str(score), 1, (255, 0, 0))
      restart = restartFont.render("Press Enter to Restart", 1, (255, 0, 0))
      # Text is displayed to the screen
      screen.blit(gameover, (screenWidth / 4, screenHeight / 4))
      screen.blit(endscore, (screenWidth / 4, screenHeight / 2.5))
      screen.blit(restart, (screenWidth / 4, screenHeight / 1.5))
      # Game restarts when the Enter key is pressed
      if event.type == pygame.KEYDOWN:
        if event.key == K_RETURN:
          main()

    # Updates the display
    pygame.display.update()


# Starts the game's main menu
mainmenu()