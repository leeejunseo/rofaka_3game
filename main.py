import pygame as pg  # Pygame 모듈을 pg라는 이름으로 import하여 게임 그래픽 및 사운드 기능을 사용
import subprocess     # 외부 파이썬 스크립트를 실행하기 위한 모듈 (ex. 다른 게임 실행)
import sys            # 시스템 종료 및 실행 경로 등 시스템 관련 기능 사용
import os             # 파일 경로 등 운영체제 관련 기능 사용

# 게임 실행 함수
def launch_game(script_path):
    folder = os.path.dirname(script_path)  # 실행할 게임 파일의 디렉터리 경로 추출
    pg.mixer.music.stop()  # 현재 재생 중인 배경음악을 중지
    subprocess.run([sys.executable, "main.py"], cwd=folder)  # 해당 폴더에서 main.py 실행
    pg.mixer.music.play(-1)  # 게임 종료 후 다시 배경음악 반복 재생

# 텍스트를 배경 박스와 그림자와 함께 화면에 출력하는 함수
def draw_text_boxed_shadow(surface, text, font, center_x, y, padding=10):
    text_surface = font.render(text, True, (255, 255, 255))  # 흰색 텍스트 surface 생성
    text_width, text_height = text_surface.get_size()  # 텍스트 크기 측정
    box_surface = pg.Surface((text_width + padding * 2, text_height + padding * 2), pg.SRCALPHA)  # 반투명 박스 surface 생성
    box_surface.fill((0, 0, 0, 160))  # 박스 배경을 반투명 검정으로 채움
    shadow = font.render(text, True, (0, 0, 0))  # 그림자용 텍스트 surface (검정)

    x = center_x - text_width // 2  # 텍스트의 x 위치 (중앙 정렬)
    box_x = center_x - (text_width + padding * 2) // 2  # 박스의 x 위치 (텍스트보다 약간 더 넓게)

    surface.blit(box_surface, (box_x, y - padding))  # 배경 박스를 먼저 출력
    surface.blit(shadow, (x + 2, y + 2))  # 그림자 텍스트 출력 (조금 오른쪽 아래)
    surface.blit(text_surface, (x, y))  # 실제 텍스트 출력

# 메인 메뉴 화면을 보여주는 함수
def main_menu():
    pg.init()  # pygame 초기화
    pg.mixer.init()  # 사운드 시스템 초기화

    info = pg.display.Info()  # 현재 디스플레이 정보 가져오기
    screen_width, screen_height = info.current_w, info.current_h  # 화면 해상도 설정
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # 전체화면 모드로 게임 화면 생성
    pg.display.set_caption("🎮 게임 선택 메뉴")  # 윈도우 타이틀 설정
    pg.mouse.set_visible(False)  # 마우스 커서를 숨김

    font = pg.font.Font("TmonMonsori.ttf.ttf", 60)  # 지정한 한글 폰트를 60pt로 설정
    clock = pg.time.Clock()  # 프레임 속도 제어용 시계 객체 생성

    # 배경 이미지 로드 및 해상도에 맞게 크기 조정
    bg_image = pg.image.load("menu_bg.png").convert()  # 배경 이미지 로드 (메뉴 배경)
    bg_image = pg.transform.scale(bg_image, (screen_width, screen_height))  # 화면 크기에 맞게 이미지 크기 조정

    # 배경음악 설정
    music_path = os.path.join(os.path.dirname(__file__), "헌시.mp3")  # 현재 파일 위치 기준으로 음악 경로 설정
    if os.path.exists(music_path):  # 음악 파일이 존재하면
        try:
            pg.mixer.music.load(music_path)  # 음악 파일 로드
            pg.mixer.music.set_volume(0.6)  # 볼륨 설정 (0.0 ~ 1.0)
            pg.mixer.music.play(-1)  # 무한 반복 재생
        except Exception as e:
            print("배경음악 로딩 실패:", e)  # 오류 발생 시 메시지 출력
    else:
        print("배경음악 파일을 찾을 수 없습니다.")  # 음악 파일이 없을 경우 메시지 출력

    # 메인 루프 (무한 반복)
    while True:
        screen.blit(bg_image, (0, 0))  # 배경 이미지 화면에 출력

        # 텍스트 메뉴 항목을 화면에 출력
        draw_text_boxed_shadow(screen, "게임 선택하기", font, screen_width // 2, screen_height // 6)
        draw_text_boxed_shadow(screen, "1. 저학년으로 플레이하기", font, screen_width // 2, screen_height // 3)
        draw_text_boxed_shadow(screen, "2. 고학년으로 플레이하기", font, screen_width // 2, screen_height // 3 + 70)
        draw_text_boxed_shadow(screen, "3. 조종사로 플레이하기", font, screen_width // 2, screen_height // 3 + 140)
        draw_text_boxed_shadow(screen, "ESC. 종료하기", font, screen_width // 2, screen_height - 100)

        # 이벤트 처리
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 윈도우 종료 버튼을 누르면
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:  # 키보드 입력이 있을 때
                if event.key == pg.K_1:  # 숫자 1 → 저학년 게임 실행
                    launch_game("탕탕_생도대/main.py")
                elif event.key == pg.K_2:  # 숫자 2 → 고학년 게임 실행
                    launch_game("공사타워디펜스/main.py")
                elif event.key == pg.K_3:  # 숫자 3 → 조종사 게임 실행
                    launch_game("War-Plane/main.py")
                elif event.key == pg.K_ESCAPE:  # ESC → 종료
                    pg.mixer.music.stop()  # 음악 정지
                    pg.quit()  # pygame 종료
                    sys.exit()  # 프로그램 종료

        pg.display.flip()  # 모든 요소를 화면에 렌더링 (화면 업데이트)
        clock.tick(60)  # 초당 최대 60프레임으로 제한

# 메인 함수 실행
if __name__ == "__main__":
    main_menu()  # 스크립트를 직접 실행할 경우 메인 메뉴부터 시작
