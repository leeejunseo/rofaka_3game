import pygame, random, math
from pygame.locals import *
import pygame_menu


# Add at the beginning of main()
score = 0
has_bx = False
invincible = False
slow_mode = False
invincible_timer = 0
slow_timer = 0


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


# 엔딩 크래딧 화면
def show_ending_credits(screen, screenWidth, screenHeight, final_score):
    import pygame

    credits = [
    "", "", "🎉 생도대 마블 제작팀 🎉", "",
    "===== 제작진 =====", "",
    "이준서 조장", "· 전체 코드 및 시스템 설계", "· 게임 구조 및 기능 개발", "",
    "권순수 조원", "· 그림 만들기", "· 사운드 만들기", "",
    "===== 핵심 기능 =====", "",
    "· 총알 구현", "· boss 구현", "· 아이템 시스템", "· boss 총알 구현", "",
    "===== 기술 요소 =====", "",
    "· 애니메이션 구현 ", "· UI 꾸미기 재밌네요", "",
    "===== 테스트 =====", "", "· 이준서, 권순수", "· 재미있었습니다.", "",
    "🏆 감사합니다! 🏆",
    "플레이해주셔서 진심으로 감사합니다.", "좋은 하루 되세요! 공사 화이팅!", "시스템 프로그래밍 최고!", "",
    "ESC 키를 누르면 메인 메뉴로 돌아갑니다", "", "", ""
    ]


    def load_font(path, size):
        try:
            return pygame.font.Font(path, size)
        except:
            return pygame.font.Font(None, size)

    font_path = "fonts/TmonMonsori.ttf.ttf"
    title_font = load_font(font_path, 48)
    credit_font = load_font(font_path, 32)
    small_font = load_font(font_path, 24)

    scroll_y = screenHeight
    scroll_speed = 2

    try:
        bg = pygame.transform.smoothscale(
            pygame.image.load("backgrounds/sand.png").convert_alpha(),
            (screenWidth, screenHeight))
    except:
        bg = pygame.Surface((screenWidth, screenHeight))
        bg.fill((0, 0, 0))

    clock = pygame.time.Clock()
    category_titles = {
    "===== 제작진 =====",
    "===== 핵심 기능 =====",
    "===== 기술 요소 =====",
    "===== 테스트 및 피드백 ====="
    }
    title_lines = {"🎉 게임 종료 한다! 🎉", "🏆 감사합니다! 🏆"}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_SPACE:
                    scroll_speed = 6
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                scroll_speed = 2

        screen.blit(bg, (0, 0))
        overlay = pygame.Surface((screenWidth, screenHeight))
        overlay.fill((0, 0, 0)); overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))

        current_y = scroll_y
        for line in credits:
            if -100 < current_y < screenHeight + 100:
                if line in title_lines:
                    font, color = title_font, (255, 215, 0)
                elif line == "===== 인터페이스 제작 가이드 =====":
                    font, color = credit_font, (255, 255, 255)
                elif line in category_titles:
                    font, color = credit_font, (255, 255, 0)
                elif line == "ESC 키를 누르면 메인 메뉴로 돌아가기":
                    font, color = small_font, (200, 200, 200)
                elif line.strip():
                    font, color = credit_font, (255, 255, 255)
                else:
                    current_y += 60
                    continue

                text_surface = font.render(line, True, color)
                text_rect = text_surface.get_rect(center=(screenWidth // 2, current_y))
                screen.blit(text_surface, text_rect)

            current_y += 60

        scroll_y -= scroll_speed
        if scroll_y < -len(credits) * 60:
            scroll_y = screenHeight

        pygame.display.flip()
        clock.tick(60)

# Main game loop
def main():
  
  # Defines values for width and height of the screen
  # 화면 해상도 자동으로 설정
  info = pygame.display.Info()
  screenWidth, screenHeight = info.current_w, info.current_h
  global score, has_bx, invincible, slow_mode, invincible_timer, slow_timer
  
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
      self.speed = (1.5 if slow_mode else 3) + min(score / 20, 2)  # 최대 속도 제한


  # Boss class
  class Boss(pygame.sprite.Sprite):
    width = 384
    height = 192

    def __init__(self):
      super(Boss, self).__init__()
      try:
        self.surf = pygame.transform.smoothscale(
          pygame.image.load('sprites/boss.png').convert_alpha(),
          (self.width, self.height))
      except pygame.error:
        # 보스 이미지 없을 때 빨간색 사각형
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 0, 0))
      
      self.mask = pygame.mask.from_surface(self.surf)
      self.rect = self.surf.get_rect()
      self.rect.x = screenWidth // 2 - self.width // 2
      self.rect.y = -self.height
      self.speed = 1
      self.health = 50
      self.max_health = 50
      self.direction = 1  # 좌우 이동 방향
      self.attack_timer = 0
      self.last_attack_time = 0

    def update(self):
      # 보스 등장 애니메이션
      if self.rect.y < 50:
        self.rect.move_ip(0, self.speed)
      else:
        # 좌우로 이동
        self.rect.move_ip(self.direction * 2, 0)
        if self.rect.left <= 0 or self.rect.right >= screenWidth:
          self.direction *= -1
      
      # 화면 밖으로 나가지 않도록
      if self.rect.left < 0:
        self.rect.left = 0
      if self.rect.right > screenWidth:
        self.rect.right = screenWidth

    def take_damage(self):
      self.health -= 1
      if self.health <= 0:
        self.kill()
        return True
      return False

    def get_health_ratio(self):
      return self.health / self.max_health
 
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
      # Speed increases by 0.1 with every point (but limited)
      self.speed = 2 + min(score / 10, 3)  # 최대 속도 제한

  # Airforce Item
  class AirforceItem(pygame.sprite.Sprite):
      def __init__(self, kind, image_path, effect_fn):
          super().__init__()
          self.kind = kind
          try:
              self.surf = pygame.transform.smoothscale(
                  pygame.image.load(image_path).convert_alpha(), (64, 64))
          except pygame.error:
              # 이미지 로드 실패 시 기본 색상 사각형 생성
              self.surf = pygame.Surface((64, 64))
              if kind == 'bx':
                  self.surf.fill((0, 255, 0))  # 녹색
              elif kind == '공끝삼':
                  self.surf.fill((255, 255, 0))  # 노란색
              elif kind == '생활강화':
                  self.surf.fill((0, 0, 255))  # 파란색
          
          self.mask = pygame.mask.from_surface(self.surf)
          self.rect = self.surf.get_rect(
              center=(random.randint(100, screenWidth - 100), -50))
          self.effect_fn = effect_fn
          self.speed = 2

      def update(self):
          self.rect.move_ip(0, self.speed)
          if self.rect.top > screenHeight:
              self.kill()
            
  def grant_bx():
    global has_bx
    has_bx = True
    print("BX 아이템 획득!")  # 디버깅용

  def grant_invincibility():
    global invincible, invincible_timer
    invincible = True
    invincible_timer = pygame.time.get_ticks()
    print("무적 아이템(공끝삼) 획득!")

  def apply_slow():
      global slow_mode, slow_timer
      slow_mode = True
      slow_timer = pygame.time.get_ticks()
      print("슬로우 아이템 획득!")  # 디버깅용


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

  # Boss Bullet class
  class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x=0, direction_y=1, bullet_type='normal'):
      super(BossBullet, self).__init__()
      width = 24
      height = 24
      self.bullet_type = bullet_type
      
      try:
        if bullet_type == 'spread':
          self.surf = pygame.transform.smoothscale(
            pygame.image.load('sprites/bossbullet_spread.png').convert_alpha(),
            (width, height))
        elif bullet_type == 'laser':
          self.surf = pygame.transform.smoothscale(
            pygame.image.load('sprites/bossbullet_laser.png').convert_alpha(),
            (width, height))
        else:
          self.surf = pygame.transform.smoothscale(
            pygame.image.load('sprites/bossbullet.png').convert_alpha(),
            (width, height))
      except pygame.error:
        # 이미지 없을 때 색상으로 구분
        self.surf = pygame.Surface((width, height))
        if bullet_type == 'spread':
          self.surf.fill((255, 165, 0))  # 주황색
        elif bullet_type == 'laser':
          self.surf.fill((255, 0, 255))  # 마젠타
        else:
          self.surf.fill((255, 0, 0))  # 빨간색
      
      self.mask = pygame.mask.from_surface(self.surf)
      self.rect = self.surf.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.direction_x = direction_x
      self.direction_y = direction_y
      self.speed = 3

    def update(self):
      self.rect.move_ip(self.direction_x * self.speed, self.direction_y * self.speed)
      if (self.rect.top > screenHeight or self.rect.bottom < 0 or 
          self.rect.left > screenWidth or self.rect.right < 0):
        self.kill()
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
      # Speed increases by 0.1 with every point (but limited)
      self.speed = 4 + min(score / 10, 3)  # 최대 속도 제한

  # Sets score to 0
  score = 0
  boss_spawned = False
  boss_defeated = False
  game_cleared = False  # 게임 클리어 상태 추가

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
  bossbullets = pygame.sprite.Group()
  items = pygame.sprite.Group()  # 아이템 그룹을 먼저 생성
  bosses = pygame.sprite.Group()
  all_sprites = pygame.sprite.Group()
  all_sprites.add(player)
  all_sprites.add(enemy)
  enemies.add(enemy)

  # Timer that sets when the ADDENEMY event is able to be called so too many enemies won't be created at once
  ADDENEMY = pygame.USEREVENT + 1
  pygame.time.set_timer(ADDENEMY, 1000)

  ADDITEM = pygame.USEREVENT + 3
  pygame.time.set_timer(ADDITEM, 3000)  # 3초마다 등장 (테스트용으로 짧게)

  BOSSBULLETFIRE = pygame.USEREVENT + 4
  pygame.time.set_timer(BOSSBULLETFIRE, 1500)  # 보스 총알 발사

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

    # 게임 클리어 체크
    if game_cleared:
      # 엔딩 크래딧 실행
      show_ending_credits(screen, screenWidth, screenHeight, score)
      # 크래딧 종료 후 메인 메뉴로 돌아가기
      mainmenu()
      return

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
      if end == False and not game_cleared:
        # 보스 스폰 체크 (점수 15점에서 보스 등장)
        if score >= 15 and not boss_spawned and not boss_defeated:
          boss = Boss()
          bosses.add(boss)
          all_sprites.add(boss)
          boss_spawned = True
          print("보스 등장!")
          
          # 보스 등장 시 일반 적 생성 중단
          pygame.time.set_timer(ADDENEMY, 0)
          pygame.time.set_timer(ENEMYBULLETFIRE, 0)

        # Creates new enemies (보스가 없을 때만)
        if event.type == ADDENEMY and not boss_spawned:
          new_enemy = Enemy()
          enemies.add(new_enemy)
          all_sprites.add(new_enemy)

        # 아이템 생성
        if event.type == ADDITEM and not game_cleared:
            kind = random.choice(['bx', '공끝삼', '생활강화'])
            image_dict = {
                'bx': 'backgrounds/bx.png',
                '공끝삼': 'backgrounds/gong3.png',
                '생활강화': 'backgrounds/lifeup.png'
            }
            effect_dict = {
                'bx': grant_bx,
                '공끝삼': grant_invincibility,
                '생활강화': apply_slow
            }
            item = AirforceItem(kind, image_dict[kind], effect_dict[kind])
            items.add(item)
            all_sprites.add(item)
            print(f"아이템 생성: {kind}")  # 디버깅용

        # 보스 총알 발사
        if event.type == BOSSBULLETFIRE and boss_spawned and not game_cleared:
          for boss in bosses:
            current_time = pygame.time.get_ticks()
            
            # 다양한 공격 패턴
            attack_pattern = random.choice(['normal', 'spread', 'laser'])
            
            if attack_pattern == 'normal':
              # 플레이어 방향으로 직선 공격
              bossbullet = BossBullet(
                boss.rect.centerx, boss.rect.bottom, 
                0, 1, 'normal'
              )
              bossbullets.add(bossbullet)
              all_sprites.add(bossbullet)
              
            elif attack_pattern == 'spread':
              # 부채꼴 공격
              for i in range(-2, 3):
                bossbullet = BossBullet(
                  boss.rect.centerx, boss.rect.bottom,
                  i * 0.5, 1, 'spread'
                )
                bossbullets.add(bossbullet)
                all_sprites.add(bossbullet)
                
            elif attack_pattern == 'laser':
              # 레이저 공격 (빠른 직선)
              bossbullet = BossBullet(
                boss.rect.centerx, boss.rect.bottom,
                0, 2, 'laser'
              )
              bossbullets.add(bossbullet)
              all_sprites.add(bossbullet)

        # Enemy bullet firing (보스가 없을 때만)
        if not boss_spawned and not game_cleared:
          for new_enemy in enemies:
            if event.type == ENEMYBULLETFIRE:
              enemybullet = EnemyBullet()
              enemybullets.add(enemybullet)
              all_sprites.add(enemybullet)
              enemybullet.rect.x = new_enemy.rect.centerx - enemybullet.rect.width / 2
              enemybullet.rect.y = new_enemy.rect.bottom

        # Bullet controls
        if event.type == pygame.KEYDOWN and not game_cleared:
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
    if not game_cleared:
      player.update()
      # 아이템 충돌 체크
      collected_items = pygame.sprite.spritecollide(player, items, True, pygame.sprite.collide_mask)
      for item in collected_items:
          print(f"아이템 충돌: {item.kind}")  # 디버깅용
          item.effect_fn()  # 아이템 효과 적용
          # BX 아이템은 점수를 주지 않음 (무적이 보상이므로)
          if item.kind != 'bx':
              score += 1  # 다른 아이템 획득 시에만 점수 증가

      # 무적 상태 해제 체크 (BX나 공끝삼 아이템으로 인한 무적)
      if invincible and pygame.time.get_ticks() - invincible_timer > 3000:  # 3초 무적
          invincible = False
          # BX 아이템 효과도 함께 해제되도록 수정
          if has_bx:
              has_bx = False
              print("BX 무적 해제!")
          else:
              print("무적 해제!")

      # 슬로우 모드 해제 체크
      if slow_mode and pygame.time.get_ticks() - slow_timer > 5000:  # 5초 슬로우
          slow_mode = False
          print("슬로우 해제!")

      # 적 업데이트
      for enemy in enemies:
          enemy.update()

      # 보스 업데이트
      for boss in bosses:
          boss.update()

      # 총알 업데이트
      for bullet in bullets:
          bullet.update()

      for enemybullet in enemybullets:
          enemybullet.update()

      for bossbullet in bossbullets:
          bossbullet.update()

      # 아이템 업데이트
      for item in items:
          item.update()

        # ✅ 충돌 처리 (무적 상태가 아닐 때만)
        
    # ✅ 충돌 처리 (무적 상태가 아닐 때만)
    if not invincible and not game_cleared:
        # 적과 플레이어 충돌
        player_hit = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask)
        if player_hit:
            if has_bx:
                has_bx = False
                print("BX 방어 발동!")
                # BX 방어 발동 후 짧은 무적 시간 부여 (선택사항)
                invincible = True
                invincible_timer = pygame.time.get_ticks()
            else:
                end = True

        # 적 총알과 플레이어 충돌
        player_hit_by_bullet = pygame.sprite.spritecollide(player, enemybullets, False, pygame.sprite.collide_mask)
        if player_hit_by_bullet:
            if has_bx:
                has_bx = False
                print("BX 방어 발동!")
                # 충돌한 총알들을 제거
                for bullet in player_hit_by_bullet:
                    bullet.kill()
                # BX 방어 발동 후 짧은 무적 시간 부여 (선택사항)
                invincible = True
                invincible_timer = pygame.time.get_ticks()
            else:
                end = True

        # 보스 총알과 플레이어 충돌
        player_hit_by_boss_bullet = pygame.sprite.spritecollide(player, bossbullets, False, pygame.sprite.collide_mask)
        if player_hit_by_boss_bullet:
            if has_bx:
                has_bx = False
                print("BX 방어 발동!")
                # 충돌한 총알들을 제거
                for bullet in player_hit_by_boss_bullet:
                    bullet.kill()
                # BX 방어 발동 후 짧은 무적 시간 부여 (선택사항)
                invincible = True
                invincible_timer = pygame.time.get_ticks()
            else:
                end = True

        # 보스와 플레이어 충돌
        player_hit_by_boss = pygame.sprite.spritecollide(player, bosses, False, pygame.sprite.collide_mask)
        if player_hit_by_boss:
            if has_bx:
                has_bx = False
                print("BX 방어 발동!")
                # BX 방어 발동 후 짧은 무적 시간 부여 (선택사항)
                invincible = True
                invincible_timer = pygame.time.get_ticks()
            else:
                end = True
    # 플레이어 총알과 적 충돌
    if not game_cleared:
      for bullet in bullets:
        enemy_hit = pygame.sprite.spritecollide(bullet, enemies, True, pygame.sprite.collide_mask)
        if enemy_hit:
          bullet.kill()
          score += 1

        # 보스와 총알 충돌
        boss_hit = pygame.sprite.spritecollide(bullet, bosses, False, pygame.sprite.collide_mask)
        if boss_hit:
          bullet.kill()
          for boss in boss_hit:
            if boss.take_damage():
              print("보스 처치!")
              boss_defeated = True
              game_cleared = True
              score += 10  # 보스 처치 보너스 점수
              # 보스 총알 발사 타이머 중지
              pygame.time.set_timer(BOSSBULLETFIRE, 0)
        # 💥 플레이어 총알과 적 총알 충돌
      pygame.sprite.groupcollide(bullets, enemybullets, True, True, collided=pygame.sprite.collide_mask)
      pygame.sprite.groupcollide(bullets, bossbullets, True, True, collided=pygame.sprite.collide_mask)
    # 무적 상태일 때 플레이어 깜빡임 효과
    if invincible and not game_cleared:
      # 깜빡임 효과를 위한 시간 기반 표시/숨김
      if (pygame.time.get_ticks() // 100) % 2 == 0:
        screen.blit(player.surf, player.rect)
    else:
      # 일반 상태에서 플레이어 표시
      if not game_cleared:
        screen.blit(player.surf, player.rect)

    # 다른 스프라이트들 그리기
    for enemy in enemies:
      screen.blit(enemy.surf, enemy.rect)

    for boss in bosses:
      screen.blit(boss.surf, boss.rect)
      
      # 보스 체력바 그리기
      if boss_spawned and not boss_defeated:
        health_bar_width = 300
        health_bar_height = 20
        health_bar_x = screenWidth // 2 - health_bar_width // 2
        health_bar_y = 30
        
        # 체력바 배경 (빨간색)
        pygame.draw.rect(screen, (255, 0, 0), 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # 체력바 (녹색)
        current_health_width = int(health_bar_width * boss.get_health_ratio())
        pygame.draw.rect(screen, (0, 255, 0), 
                        (health_bar_x, health_bar_y, current_health_width, health_bar_height))
        
        # 체력바 테두리
        pygame.draw.rect(screen, (255, 255, 255), 
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)

    for bullet in bullets:
      screen.blit(bullet.surf, bullet.rect)

    for enemybullet in enemybullets:
      screen.blit(enemybullet.surf, enemybullet.rect)

    for bossbullet in bossbullets:
      screen.blit(bossbullet.surf, bossbullet.rect)

    for item in items:
      screen.blit(item.surf, item.rect)

    # 점수 표시
    try:
      font = pygame.font.Font("fonts/AmericanCaptain.otf", 36)
    except:
      font = pygame.font.Font(None, 36)
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # 아이템 상태 표시
    status_y = 60
    if has_bx:
        bx_text = font.render("BX Ready (1회 방어)", True, (0, 255, 0))
        screen.blit(bx_text, (10, status_y))
        status_y += 30

    if invincible:
        remaining_time = 3000 - (pygame.time.get_ticks() - invincible_timer)
        if remaining_time > 0:
            inv_text = font.render(f"Invincible: {remaining_time // 1000 + 1}s", True, (255, 255, 0))
            screen.blit(inv_text, (10, status_y))
            status_y += 30



    if slow_mode:
      remaining_time = 5000 - (pygame.time.get_ticks() - slow_timer)
      if remaining_time > 0:
        slow_text = font.render(f"Slow Mode: {remaining_time//1000 + 1}s", True, (0, 0, 255))
        screen.blit(slow_text, (10, status_y))

    # Game Over 화면
    if end:
      try:
        game_over_font = pygame.font.Font("fonts/AmericanCaptain.otf", 64)
        restart_font = pygame.font.Font("fonts/AmericanCaptain.otf", 32)
      except:
        game_over_font = pygame.font.Font(None, 64)
        restart_font = pygame.font.Font(None, 32)

      game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
      final_score_text = restart_font.render(f"Final Score: {score}", True, (255, 255, 255))
      restart_text = restart_font.render("Press R to restart or ESC to quit", True, (255, 255, 255))

      # 텍스트 중앙 정렬
      game_over_rect = game_over_text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 50))
      final_score_rect = final_score_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
      restart_rect = restart_text.get_rect(center=(screenWidth // 2, screenHeight // 2 + 50))

      screen.blit(game_over_text, game_over_rect)
      screen.blit(final_score_text, final_score_rect)
      screen.blit(restart_text, restart_rect)

      # 재시작 또는 종료 키 입력 처리
      keys = pygame.key.get_pressed()
      if keys[pygame.K_r]:
        # 게임 재시작
        main()
        return
      elif keys[pygame.K_ESCAPE]:
        # 메인 메뉴로 돌아가기
        mainmenu()
        return

    # 화면 업데이트
    pygame.display.flip()

  # 게임 루프 종료 시 정리
  pygame.quit()

# 게임 시작
if __name__ == "__main__":
  mainmenu()