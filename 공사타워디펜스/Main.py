# 필요한 모듈과 클래스 불러오기
from Scene import *
from Lib import (
    STATE_MAIN_MENU,
    STATE_PRE_WAVE,
    STATE_WAVE,
    STATE_GAME_OVER,
    EVENT_STATE_CHANGED,
    BACKGROUND_COLOUR,
    ENEMY_REACHED_END,
    ENEMY_KILLED,
    posToGridCoords,
    gridCoordToPos
)

# Pygame 초기화
pygame.init()

try:
    pygame.mixer.music.load("공군가.mp3")  # 또는 "assets/공군가.mp3"
    pygame.mixer.music.set_volume(0.5)     # 볼륨 (0.0 ~ 1.0)
    pygame.mixer.music.play(-1)            # 무한 반복 재생
except Exception as e:
    print("배경음악 로딩 실패:", e)

display_info = pygame.display.Info()  # 현재 디스플레이 정보 가져오기
pygame.display.set_caption("공사타워티펜스")  # 창 제목 설정
pygame.display.set_icon(pygame.image.load("assets/tower1.png"))  # 아이콘 설정
FULLSCREEN = True  # 전체 화면 여부 설정

# 화면 크기 및 디스플레이 설정
if FULLSCREEN:
    SCREEN_SIZE = (display_info.current_w, display_info.current_h)  # 현재 화면 해상도 가져오기
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)  # 전체 화면으로 설정
else:
    SCREEN_SIZE = (1500, 1000)  # 창 모드일 경우 해상도 수동 설정
    screen = pygame.display.set_mode(SCREEN_SIZE)  # 창 모드로 설정

# 게임 장면(Scene) 초기화
SCENE_MAIN_MENU = MainMenu(SCREEN_SIZE, screen)  # 메인 메뉴 장면
SCENE_GAME = None  # 게임 장면은 플레이 버튼 클릭 시 생성됨
SCENE_PAUSE = Pause(SCREEN_SIZE, screen)  # 일시정지 장면
SCENE_GAME_OVER = GameOver(SCREEN_SIZE, screen)  # 게임 오버 장면

# 게임 상태 변수들
done = False  # 게임 루프 종료 여부
current_state = STATE_MAIN_MENU  # 현재 게임 상태 (메인 메뉴 상태로 시작)
current_scene = SCENE_MAIN_MENU  # 현재 표시 중인 장면
clock = pygame.time.Clock()  # 프레임 조절용 시계 객체

# 메인 루프
while not done:
    # 화면 전체 지우기 (배경 색으로 초기화)
    screen.fill(BACKGROUND_COLOUR)

    # 현재 Scene 업데이트
    current_scene.update()

    # 현재 Scene 렌더링
    current_scene.render(screen=screen, current_state=current_state, SCENE_GAME=SCENE_GAME)

    # 이벤트 처리
    for event in pygame.event.get():
        # 모든 Scene에 적용되는 전역 이벤트
        if event.type == pygame.QUIT:
            done = True  # 창 닫기 시 게임 종료
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # ESC 키로 게임 종료
        elif event.type == EVENT_STATE_CHANGED:
            # 웨이브 준비 상태로 전환
            if event.next_state == STATE_PRE_WAVE:
                if current_state == STATE_WAVE:
                    # 웨이브가 끝났을 때
                    current_state = STATE_PRE_WAVE
                    SCENE_GAME.next_wave_button.background_colour = BUTTON_COLOUR
                    SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                else:
                    # 새 게임 시작
                    SCENE_GAME = Game(SCREEN_SIZE, screen)  # Game 인스턴스 생성
                    current_scene = SCENE_GAME
                    current_state = STATE_PRE_WAVE

            # 웨이브 시작 상태로 전환
            elif event.next_state == STATE_WAVE:
                if current_state == STATE_PAUSED:
                    # 일시정지 해제
                    current_state = STATE_WAVE
                    SCENE_GAME.pause_button.background_colour = BUTTON_COLOUR
                    current_scene = SCENE_GAME
                else:
                    # 웨이브 시작
                    current_state = STATE_WAVE
                    SCENE_GAME.wave_handler.start_wave()
                    SCENE_GAME.next_wave_button.background_colour = BUTTON_DISABLED_COLOUR
                    SCENE_GAME.enemies_alive = SCENE_GAME.wave_handler.current_wave.enemies
                    SCENE_GAME.enemy_count_display.text = "남은 메추리 : " + str(SCENE_GAME.enemies_alive)
                    SCENE_GAME.pause_button.background_colour = BUTTON_COLOUR
                    SCENE_GAME.wave_display.text = "현재 웨이브: " + str(SCENE_GAME.wave_handler.current_wave_number)

            # 일시정지 상태로 전환
            elif event.next_state == STATE_PAUSED:
                current_state = STATE_PAUSED
                SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                current_scene = SCENE_PAUSE

            # 메인 메뉴로 돌아가기
            elif event.next_state == STATE_MAIN_MENU:
                current_state = STATE_MAIN_MENU
                current_scene = SCENE_MAIN_MENU

            # 게임 오버 상태로 전환
            elif event.next_state == STATE_GAME_OVER:
                current_state = STATE_GAME_OVER
                current_scene = SCENE_GAME_OVER
                SCENE_GAME_OVER.survival_message.text = "최종 웨이브 : " + str(SCENE_GAME.wave_handler.current_wave_number)

        # 메인 메뉴 Scene에서 발생하는 이벤트 처리
        if current_scene == SCENE_MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 클릭
                    if SCENE_MAIN_MENU.play_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))  # 게임 시작
                    elif SCENE_MAIN_MENU.quit_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(pygame.QUIT))  # 게임 종료

        # 게임 오버 Scene에서 발생하는 이벤트 처리
        elif current_scene == SCENE_GAME_OVER:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if SCENE_GAME_OVER.main_menu_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_MAIN_MENU))  # 메인 메뉴로

        # 일시정지 Scene에서 발생하는 이벤트 처리
        if current_scene == SCENE_PAUSE:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if SCENE_PAUSE.resume_button.contains(adjustCoordsByOffset(event.pos, SCENE_GAME.offset)):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))  # 재개
                    elif SCENE_PAUSE.quit_button.contains(adjustCoordsByOffset(event.pos, SCENE_GAME.offset)):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_MAIN_MENU))  # 메인 메뉴로

        # 실제 게임 Scene에서 발생하는 이벤트 처리
        elif current_scene == SCENE_GAME:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 클릭
                    # 툴바 버튼 클릭 확인
                    if SCENE_GAME.next_wave_button.contains(event.pos):
                        if current_state == STATE_PRE_WAVE:
                            pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))
                    elif SCENE_GAME.pause_button.contains(event.pos):
                        if current_state == STATE_WAVE:
                            pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PAUSED))
                    # 상점 버튼 클릭
                    elif SCENE_GAME.shop.button_pressed(adjustCoordsByOffset(event.pos, SCENE_GAME.shop.image.get_abs_offset())) != -1:
                        SCENE_GAME.selected_tower = SCENE_GAME.shop.button_pressed(adjustCoordsByOffset(event.pos, SCENE_GAME.shop.image.get_abs_offset()))
                    else:
                        # 타워 설치
                        mouse_pos = adjustCoordsByOffset(event.pos, SCENE_GAME.offset)
                        if not SCENE_GAME.path.contains(mouse_pos):
                            if 0 < mouse_pos[0] < SCENE_GAME.path.rect.width and 0 < mouse_pos[1] < SCENE_GAME.path.rect.height:
                                tower = createTower(gridCoordToPos(posToGridCoords(mouse_pos, GRID_SIZE), GRID_SIZE),
                                                    SCENE_GAME.selected_tower,
                                                    SCENE_GAME.tower_models,
                                                    SCENE_GAME.path,
                                                    SCENE_GAME.towers)
                                if tower is not None and tower.model.value <= SCENE_GAME.money:
                                    SCENE_GAME.towers.add(tower)
                                    SCENE_GAME.money -= tower.model.value
                elif event.button == 3:  # 오른쪽 클릭 → 설치한 타워 제거
                    mouse_pos = adjustCoordsByOffset(event.pos, SCENE_GAME.offset)
                    for tower in SCENE_GAME.towers.sprites():
                        if tower.rect.collidepoint(mouse_pos):
                            tower.kill()
                            SCENE_GAME.money += tower.model.value // 2  # 절반 가격 환급

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    SCENE_GAME.selected_tower = 0
                elif event.key == pygame.K_2:
                    SCENE_GAME.selected_tower = 1
                elif event.key == pygame.K_SPACE:
                    if current_state == STATE_PRE_WAVE:
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))  # 스페이스바로 웨이브 시작

            # 적 처치 이벤트 처리
            elif event.type == ENEMY_KILLED:
                SCENE_GAME.enemies_alive -= 1
                SCENE_GAME.enemy_count_display.text = "남은 메추리 : " + str(SCENE_GAME.enemies_alive)
                SCENE_GAME.money += event.enemy.value  # 보상 금액 획득
                event.enemy.kill()
                SCENE_GAME.effects.add(SpriteSheet(event.enemy.rect.center, 'assets/explosion.png'))  # 폭발 이펙트
                if SCENE_GAME.enemies_alive <= 0:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))  # 웨이브 종료

            # 적이 맵 끝에 도달했을 때
            elif event.type == ENEMY_REACHED_END:
                SCENE_GAME.lives += 1
                SCENE_GAME.lives_display.text = "탈출한 메추리 : " + str(SCENE_GAME.lives)
                if SCENE_GAME.lives <= 0:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_GAME_OVER))  # 게임 오버
                else:
                    # 적을 처음 시작 지점으로 되돌림
                    event.enemy.current_waypoint = 1
                    event.enemy.rect.center = gridCoordToPos(SCENE_GAME.path.waypoints[0], GRID_SIZE)
                    event.enemy.distance_travelled = 0

    # Display frame
    pygame.display.flip()

    # Keep frame rate constant
    clock.tick(60)