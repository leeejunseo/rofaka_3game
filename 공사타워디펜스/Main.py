# Scene.py에서 정의된 장면 클래스들(MainMenu, Game, Pause, GameOver 등)을 모두 불러옴
from Scene import *

# Lib.py에서 정의된 상수들(게임 상태 코드, 이벤트 코드), 색상, 좌표 변환 함수 등을 불러옴
from Lib import (
    STATE_MAIN_MENU,         # 게임 상태: 메인 메뉴
    STATE_PRE_WAVE,          # 게임 상태: 다음 웨이브 시작 전 준비 상태
    STATE_WAVE,              # 게임 상태: 웨이브 진행 중
    STATE_GAME_OVER,         # 게임 상태: 게임 오버 상태
    EVENT_STATE_CHANGED,     # 사용자 정의 이벤트: 게임 상태가 바뀌었음을 알림
    BACKGROUND_COLOUR,       # 화면 초기화에 사용될 배경색
    ENEMY_REACHED_END,       # 이벤트: 적이 끝 지점에 도달함
    ENEMY_KILLED,            # 이벤트: 적이 죽었음
    posToGridCoords,         # 화면 좌표를 격자 좌표로 변환하는 함수
    gridCoordToPos           # 격자 좌표를 화면 좌표로 변환하는 함수
)

# Pygame의 모든 모듈을 초기화함 (그래픽, 사운드 등 포함)
pygame.init()

# 배경음악 설정을 시도 (예외 처리를 통해 실패 시 오류 메시지를 출력함)
try:
    pygame.mixer.music.load("공군가.mp3")  # 공군가.mp3 파일을 배경음악으로 로드
    pygame.mixer.music.set_volume(0.5)     # 배경음악 볼륨을 50%로 설정
    pygame.mixer.music.play(-1)            # 배경음악을 무한 반복(-1)으로 재생 시작
except Exception as e:
    print("배경음악 로딩 실패:", e)        # 로딩 실패 시 예외 메시지 출력

# 디스플레이 정보(화면 너비, 높이 등) 객체를 가져옴
display_info = pygame.display.Info()

# 윈도우 창 상단 제목 설정 (한글 가능)
pygame.display.set_caption("공사타워티펜스")

# 게임 아이콘 설정 (작은 이미지, 창 상단 탭에 표시됨)
pygame.display.set_icon(pygame.image.load("assets/tower1.png"))

# 전체화면 여부 설정 (True면 전체화면, False면 창모드)
FULLSCREEN = True

# 화면 크기 및 디스플레이 모드 설정
if FULLSCREEN:
    SCREEN_SIZE = (display_info.current_w, display_info.current_h)  # 현재 모니터 해상도 사용
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)  # 전체화면으로 디스플레이 설정
else:
    SCREEN_SIZE = (1500, 1000)  # 창모드일 경우 고정된 해상도 사용
    screen = pygame.display.set_mode(SCREEN_SIZE)  # 창모드로 디스플레이 설정

# 게임에서 사용할 Scene 객체들 초기화
SCENE_MAIN_MENU = MainMenu(SCREEN_SIZE, screen)  # 메인 메뉴 화면 인스턴스 생성
SCENE_GAME = None                                # 게임 화면은 플레이 버튼 클릭 시 동적으로 생성
SCENE_PAUSE = Pause(SCREEN_SIZE, screen)         # 일시정지 화면 인스턴스 생성
SCENE_GAME_OVER = GameOver(SCREEN_SIZE, screen)  # 게임오버 화면 인스턴스 생성

# 게임 루프 제어 변수들 초기화
done = False                    # 게임 루프 종료 여부 (False이면 계속 실행)
current_state = STATE_MAIN_MENU  # 현재 게임 상태를 메인 메뉴로 설정
current_scene = SCENE_MAIN_MENU  # 현재 표시되는 Scene을 메인 메뉴로 설정
clock = pygame.time.Clock()    # 게임 루프의 FPS 제어용 시계 객체 생성

# 메인 게임 루프 시작 (done이 True가 될 때까지 반복)
while not done:
    screen.fill(BACKGROUND_COLOUR)  # 화면 전체를 배경색으로 채워 초기화

    current_scene.update()  # 현재 Scene의 업데이트 로직 실행 (애니메이션, 버튼 상태 등)

    # 현재 Scene을 화면에 렌더링 (화면 surface에 그림 출력)
    current_scene.render(screen=screen, current_state=current_state, SCENE_GAME=SCENE_GAME)

    # pygame에서 발생한 이벤트들을 순회하며 처리
    for event in pygame.event.get():
        # 창 닫기 버튼 클릭 시
        if event.type == pygame.QUIT:
            done = True  # 게임 루프 종료

        # 키보드 키 뗐을 때
        elif event.type == pygame.KEYUP:
            # ESC 키를 누르면 게임 종료 이벤트 발생
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        # 게임 상태 변경 이벤트가 발생했을 경우
        elif event.type == EVENT_STATE_CHANGED:
            # 웨이브 준비 상태로 전환된 경우
            if event.next_state == STATE_PRE_WAVE:
                if current_state == STATE_WAVE:  # 웨이브에서 전환된 경우
                    current_state = STATE_PRE_WAVE
                    SCENE_GAME.next_wave_button.background_colour = BUTTON_COLOUR
                    SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                else:  # 게임을 새로 시작하는 경우
                    SCENE_GAME = Game(SCREEN_SIZE, screen)
                    current_scene = SCENE_GAME
                    current_state = STATE_PRE_WAVE

            # 웨이브 진행 상태로 전환된 경우
            elif event.next_state == STATE_WAVE:
                if current_state == STATE_PAUSED:  # 일시정지 해제
                    current_state = STATE_WAVE
                    SCENE_GAME.pause_button.background_colour = BUTTON_COLOUR
                    current_scene = SCENE_GAME
                else:  # 웨이브 새로 시작
                    current_state = STATE_WAVE
                    SCENE_GAME.wave_handler.start_wave()
                    SCENE_GAME.next_wave_button.background_colour = BUTTON_DISABLED_COLOUR
                    SCENE_GAME.enemies_alive = SCENE_GAME.wave_handler.current_wave.enemies
                    SCENE_GAME.enemy_count_display.text = "남은 메추리 : " + str(SCENE_GAME.enemies_alive)
                    SCENE_GAME.pause_button.background_colour = BUTTON_COLOUR
                    SCENE_GAME.wave_display.text = "현재 웨이브: " + str(SCENE_GAME.wave_handler.current_wave_number)

            # 일시정지 상태로 전환된 경우
            elif event.next_state == STATE_PAUSED:
                current_state = STATE_PAUSED
                SCENE_GAME.pause_button.background_colour = BUTTON_DISABLED_COLOUR
                current_scene = SCENE_PAUSE

            # 메인 메뉴로 돌아가는 경우
            elif event.next_state == STATE_MAIN_MENU:
                current_state = STATE_MAIN_MENU
                current_scene = SCENE_MAIN_MENU

            # 게임 오버 상태로 전환된 경우
            elif event.next_state == STATE_GAME_OVER:
                current_state = STATE_GAME_OVER
                current_scene = SCENE_GAME_OVER
                SCENE_GAME_OVER.survival_message.text = "최종 웨이브 : " + str(SCENE_GAME.wave_handler.current_wave_number)

        # 메인 메뉴 Scene에서의 마우스 클릭 이벤트 처리
        if current_scene == SCENE_MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 마우스 왼쪽 버튼 클릭
                    if SCENE_MAIN_MENU.play_button.contains(event.pos):  # 플레이 버튼 클릭 시
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))
                    elif SCENE_MAIN_MENU.quit_button.contains(event.pos):  # 종료 버튼 클릭 시
                        pygame.event.post(pygame.event.Event(pygame.QUIT))

        # 게임 오버 Scene에서의 마우스 클릭 이벤트 처리
        elif current_scene == SCENE_GAME_OVER:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if SCENE_GAME_OVER.main_menu_button.contains(event.pos):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_MAIN_MENU))

        # 일시정지 Scene에서의 마우스 클릭 이벤트 처리
        if current_scene == SCENE_PAUSE:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if SCENE_PAUSE.resume_button.contains(adjustCoordsByOffset(event.pos, SCENE_GAME.offset)):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))
                    elif SCENE_PAUSE.quit_button.contains(adjustCoordsByOffset(event.pos, SCENE_GAME.offset)):
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_MAIN_MENU))

        # 실제 게임 Scene에서의 마우스 및 키보드 이벤트 처리
        elif current_scene == SCENE_GAME:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 왼쪽 클릭
                    if SCENE_GAME.next_wave_button.contains(event.pos) and current_state == STATE_PRE_WAVE:
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))
                    elif SCENE_GAME.pause_button.contains(event.pos) and current_state == STATE_WAVE:
                        pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PAUSED))
                    elif SCENE_GAME.shop.button_pressed(adjustCoordsByOffset(event.pos, SCENE_GAME.shop.image.get_abs_offset())) != -1:
                        SCENE_GAME.selected_tower = SCENE_GAME.shop.button_pressed(adjustCoordsByOffset(event.pos, SCENE_GAME.shop.image.get_abs_offset()))
                    else:
                        mouse_pos = adjustCoordsByOffset(event.pos, SCENE_GAME.offset)
                        if not SCENE_GAME.path.contains(mouse_pos):
                            if 0 < mouse_pos[0] < SCENE_GAME.path.rect.width and 0 < mouse_pos[1] < SCENE_GAME.path.rect.height:
                                tower = createTower(
                                    gridCoordToPos(posToGridCoords(mouse_pos, GRID_SIZE), GRID_SIZE),
                                    SCENE_GAME.selected_tower,
                                    SCENE_GAME.tower_models,
                                    SCENE_GAME.path,
                                    SCENE_GAME.towers
                                )
                                if tower is not None and tower.model.value <= SCENE_GAME.money:
                                    SCENE_GAME.towers.add(tower)
                                    SCENE_GAME.money -= tower.model.value
                elif event.button == 3:  # 오른쪽 클릭 (타워 삭제)
                    mouse_pos = adjustCoordsByOffset(event.pos, SCENE_GAME.offset)
                    for tower in SCENE_GAME.towers.sprites():
                        if tower.rect.collidepoint(mouse_pos):
                            tower.kill()
                            SCENE_GAME.money += tower.model.value // 2

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    SCENE_GAME.selected_tower = 0
                elif event.key == pygame.K_2:
                    SCENE_GAME.selected_tower = 1
                elif event.key == pygame.K_SPACE and current_state == STATE_PRE_WAVE:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_WAVE))

            elif event.type == ENEMY_KILLED:
                SCENE_GAME.enemies_alive -= 1
                SCENE_GAME.enemy_count_display.text = "남은 메추리 : " + str(SCENE_GAME.enemies_alive)
                SCENE_GAME.money += event.enemy.value
                event.enemy.kill()
                SCENE_GAME.effects.add(SpriteSheet(event.enemy.rect.center, 'assets/explosion.png'))
                if SCENE_GAME.enemies_alive <= 0:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_PRE_WAVE))

            elif event.type == ENEMY_REACHED_END:
                SCENE_GAME.lives += 1
                SCENE_GAME.lives_display.text = "탈출한 메추리 : " + str(SCENE_GAME.lives)
                if SCENE_GAME.lives == 10:
                    pygame.event.post(pygame.event.Event(EVENT_STATE_CHANGED, next_state=STATE_GAME_OVER))
                else:
                    event.enemy.current_waypoint = 1
                    event.enemy.rect.center = gridCoordToPos(SCENE_GAME.path.waypoints[0], GRID_SIZE)
                    event.enemy.distance_travelled = 0

    # 모든 그려진 요소를 화면에 출력 (화면 업데이트)
    pygame.display.flip()

    # 프레임 속도를 초당 60으로 고정
    clock.tick(60)
