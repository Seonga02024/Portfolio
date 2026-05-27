# reality_quest_ui.py
# 현실 퀘스트 (Reality Quest) - 최종 수정본

import cv2
import torch
from transformers import pipeline
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import os

# --- 게임 설정 ---
QUEST_ITEMS = ["cup", "cell phone", "remote", "backpack"]
CONFIDENCE_THRESHOLD = 0.95
QUEST_TIME_LIMIT = 30

# --- UI 설정 ---
WIN_WIDTH, WIN_HEIGHT = 480, 800
CAM_SIZE = 200
CAM_X_OFFSET = (WIN_WIDTH - CAM_SIZE) // 2

# --- 게임 상태 정의 ---
STATE_TITLE = 0
STATE_STORY = 1
STATE_PRE_GAMEPLAY = 2
STATE_GAMEPLAY = 3
STATE_GAMEOVER = 4

# --- 한글 폰트 설정 ---
FONT_PATH = "C:/Windows/Fonts/malgun.ttf"
if not os.path.exists(FONT_PATH):
    print(f"경고: 폰트 파일을 찾을 수 없습니다 ({FONT_PATH}). 한글이 깨질 수 있습니다.")
    FONT_PATH = None

def draw_korean_text(img, text, pos, font_size, color):
    """Pillow를 사용하여 OpenCV 이미지에 한글을 그리는 함수"""
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size) if FONT_PATH else ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    draw_pos = (pos[0] - text_width // 2, pos[1] - text_height // 2)

    draw.text(draw_pos, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def draw_multiline_korean_text(img, text, start_pos, font_size, color):
    """여러 줄의 한글 텍스트를 중앙 정렬하여 그리는 함수"""
    y = start_pos[1]
    for line in text.split('\n'):
        img = draw_korean_text(img, line, (start_pos[0], y), font_size, color)
        y += font_size + 15
    return img

def draw_multiline_korean_text_typing(img, text, start_pos, font_size, color, chars_to_draw):
    """여러 줄의 한글 텍스트를 타이핑 효과와 함께 중앙 정렬하여 그리는 함수"""
    y = start_pos[1]
    chars_drawn = 0
    full_text = ""
    for line in text.split('\n'):
        full_text += line + "\n"

    text_to_draw = full_text[:chars_to_draw]

    for i, line in enumerate(text_to_draw.split('\n')):
        img = draw_korean_text(img, line, (start_pos[0], y + i * (font_size + 15)), font_size, color)
    return img


def draw_vertical_korean_text(img, text, start_pos, font_size, color, padding):
    """세로로 한 글자씩 한글을 그리는 함수"""
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size) if FONT_PATH else ImageFont.load_default()
    except IOError:
        font = ImageFont.load_default()

    y = start_pos[1]
    for char in text:
        text_bbox = draw.textbbox((0, 0), char, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        draw_x = start_pos[0] - text_width // 2
        
        draw.text((draw_x, y), char, font=font, fill=color)
        y += font_size + padding

    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def imread_korean(path, flags=cv2.IMREAD_COLOR):
    """한글 경로의 이미지를 읽는 함수"""
    try:
        n = np.fromfile(path, np.uint8)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

def apply_transparency(img):
    white_canvas = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255
    return cv2.addWeighted(img, 0.3, white_canvas, 0.7, 0)

def initialize_game():
    print("현실 퀘스트에 오신 것을 환영합니다!")
    print("="*40)
    print("  - AI 모델 및 웹캠을 초기화합니다...")
    try:
        device = 0 if torch.cuda.is_available() else -1
        object_detector = pipeline("object-detection", model="facebook/detr-resnet-50", device=device)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("  > 웹캠을 열 수 없습니다.")
            return None, None
        print("  > 초기화 완료!")
        return object_detector, cap
    except Exception as e:
        print(f"  > 초기화 실패: {e}")
        return None, None

mouse_clicked = False
def on_mouse_click(event, x, y, flags, param):
    """마우스 클릭 이벤트를 처리하는 콜백 함수"""
    global mouse_clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_clicked = True

def main():
    detector, camera = initialize_game()
    if not (detector and camera):
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # --- 이미지 로드 (수정: IMREAD_COLOR 추가) ---
    teacher_img_path = os.path.join(script_dir, "teacher.png")
    teacher_img = imread_korean(teacher_img_path, cv2.IMREAD_COLOR)
    if teacher_img is None:
        print(f"경고: 스승 이미지를 찾을 수 없습니다 ({teacher_img_path}).")
        teacher_img = np.ones((CAM_SIZE, CAM_SIZE, 3), dtype=np.uint8) * 50
    else:
        teacher_img = cv2.resize(teacher_img, (CAM_SIZE, CAM_SIZE))
        
    bg_img_path = os.path.join(script_dir, "backImg1.png")
    bg_img = imread_korean(bg_img_path, cv2.IMREAD_COLOR)
    if bg_img is None:
        print(f"경고: 배경 이미지 1을 찾을 수 없습니다 ({bg_img_path}). 흰색 배경으로 대체합니다.")
        final_bg_texture = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255
        final_bg_texture = apply_transparency(final_bg_texture)
    else:
        bg_img = cv2.resize(bg_img, (WIN_WIDTH, WIN_HEIGHT))
        final_bg_texture = apply_transparency(bg_img)

    bg_img_path2 = os.path.join(script_dir, "backImg2.png")
    bg_img2 = imread_korean(bg_img_path2, cv2.IMREAD_COLOR)
    if bg_img2 is not None:
        bg_img2 = cv2.resize(bg_img2, (WIN_WIDTH, WIN_HEIGHT))
        bg_img2 = apply_transparency(bg_img2)
    else:
        print(f"경고: 배경 이미지 2를 찾을 수 없습니다 ({bg_img_path2}). 흰색 배경으로 대체합니다.")
        bg_img2 = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255
        bg_img2 = apply_transparency(bg_img2)

    bg_img_path3 = os.path.join(script_dir, "backImg3.png")
    original_bg_img3 = imread_korean(bg_img_path3, cv2.IMREAD_COLOR)
    if original_bg_img3 is not None:
        original_bg_img3 = cv2.resize(original_bg_img3, (WIN_WIDTH, WIN_HEIGHT))
        transparent_bg_img3 = apply_transparency(original_bg_img3)
    else:
        print(f"경고: 배경 이미지 3을 찾을 수 없습니다 ({bg_img_path3}). 흰색 배경으로 대체합니다.")
        original_bg_img3 = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255
        transparent_bg_img3 = apply_transparency(original_bg_img3)

    result_img_path1 = os.path.join(script_dir, "result1.png")
    result_img1 = imread_korean(result_img_path1, cv2.IMREAD_COLOR)
    if result_img1 is not None:
        result_img1 = cv2.resize(result_img1, (WIN_WIDTH, WIN_HEIGHT))
    else:
        print(f"경고: 결과 이미지 1을 찾을 수 없습니다 ({result_img_path1}). 흰색 배경으로 대체합니다.")
        result_img1 = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255

    result_img_path2 = os.path.join(script_dir, "result2.png")
    result_img2 = imread_korean(result_img_path2, cv2.IMREAD_COLOR)
    if result_img2 is not None:
        result_img2 = cv2.resize(result_img2, (WIN_WIDTH, WIN_HEIGHT))
    else:
        print(f"경고: 결과 이미지 2를 찾을 수 없습니다 ({result_img_path2}). 흰색 배경으로 대체합니다.")
        result_img2 = np.ones((WIN_HEIGHT, WIN_WIDTH, 3), dtype=np.uint8) * 255
    
    # --- 여기까지 ---

    cv2.namedWindow("Reality Quest")
    cv2.setMouseCallback("Reality Quest", on_mouse_click)

    game_state = STATE_TITLE
    current_quest_index = 0
    quest_completed_time = 0
    last_detected_object = ""
    quest_start_time = 0
    pre_gameplay_flow = 0
    dialogue_start_time = 0
    person_first_detected_at = 0
    time_remaining = QUEST_TIME_LIMIT

    # Typing effect variables
    story_text_chars = 0
    story_text_last_update = 0
    pre_game_text_chars = 0
    pre_game_text_last_update = 0
    game_over_text_chars = 0
    game_over_text_last_update = 0
    typing_speed = 0.05  # seconds per character

    while True:
        global mouse_clicked

        if game_state == STATE_TITLE:
            background = final_bg_texture.copy()
            background = draw_vertical_korean_text(background, "현실 퀘스트", (60, 80), 50, (0,0,0), 10)
            background = draw_korean_text(background, "아무 곳이나 클릭하여 시작하세요", (WIN_WIDTH//2, 700), 25, (50,50,50))
            cv2.imshow("Reality Quest", background)
            if mouse_clicked:
                game_state = STATE_STORY
                story_text_last_update = time.time()
                mouse_clicked = False
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        elif game_state == STATE_STORY:
            background = bg_img2.copy()
            story_text = """당신은 차원 여행 마법사의 제자입니다.\n\n원래 세계로 돌아가기 위해서는\n이 현실에 당신을 묶어두는\n특정 '사물'들을 찾아야만 합니다.\n\n스승님의 목소리가 당신을 안내할 것입니다."""
            
            if time.time() - story_text_last_update > typing_speed:
                if story_text_chars < len(story_text):
                    story_text_chars += 1
                    story_text_last_update = time.time()

            background = draw_multiline_korean_text_typing(background, story_text, (WIN_WIDTH//2, 280), 22, (0,0,0), story_text_chars)
            
            if story_text_chars >= len(story_text):
                background = draw_korean_text(background, "아무 곳이나 클릭하여 계속하세요", (WIN_WIDTH//2, 550), 25, (50,50,50))
            
            cv2.imshow("Reality Quest", background)
            if mouse_clicked and story_text_chars >= len(story_text):
                game_state = STATE_PRE_GAMEPLAY
                mouse_clicked = False
            elif mouse_clicked:
                story_text_chars = len(story_text)


            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        elif game_state == STATE_PRE_GAMEPLAY:
            background = original_bg_img3.copy()
            IMG_Y = 50
            TEXT_Y = IMG_Y + CAM_SIZE + 30
            CAM_Y = 520

            ret, frame = camera.read()
            if not ret: break

            h, w, _ = frame.shape
            crop_size = min(h, w)
            start_x = (w - crop_size) // 2
            start_y = (h - crop_size) // 2
            cam_view = cv2.resize(frame[start_y:start_y+crop_size, start_x:start_x+crop_size], (CAM_SIZE, CAM_SIZE))

            background[IMG_Y:IMG_Y+CAM_SIZE, CAM_X_OFFSET:CAM_X_OFFSET+CAM_SIZE] = teacher_img
            background[CAM_Y:CAM_Y+CAM_SIZE, CAM_X_OFFSET:CAM_X_OFFSET+CAM_SIZE] = cam_view

            if pre_gameplay_flow == 0:
                background = draw_korean_text(background, "제자야... 무사히 잘 있는 거 맞느냐?", (WIN_WIDTH//2, TEXT_Y), 22, (255,255,255))
                background = draw_korean_text(background, "나한테 얼굴을 보여보거라", (WIN_WIDTH//2, TEXT_Y + 30), 22, (255,255,255))
                
                pil_image = Image.fromarray(cv2.cvtColor(cam_view, cv2.COLOR_BGR2RGB))
                outputs = detector(pil_image)
                person_found = False
                for output in outputs:
                    if output["label"] == "person" and output["score"] > CONFIDENCE_THRESHOLD:
                        person_found = True
                        if person_first_detected_at == 0:
                            person_first_detected_at = time.time()
                        elif time.time() - person_first_detected_at > 1.0:
                            pre_gameplay_flow = 1
                            mouse_clicked = False
                        break
                if not person_found:
                    person_first_detected_at = 0

            elif pre_gameplay_flow == 1:
                background = draw_korean_text(background, "확인되었구나. 클릭하여 계속하거라.", (WIN_WIDTH//2, TEXT_Y), 22, (255,255,255))
                if mouse_clicked:
                    pre_gameplay_flow = 2
                    pre_game_text_last_update = time.time()
                    mouse_clicked = False
            elif pre_gameplay_flow == 2:
                story_text = """내가 확인해보니 총 4가지의 물건을\n찾아야 하는 것 같구나...\n내가 오래 힘을 유지할 수가 없어\n빠르게 해내야할 것 같구나...\n만약 다 찾지 못한다면\n너는 다시 이 곳에 돌아올 수 없단다\n명심하렴...!"""
                
                if time.time() - pre_game_text_last_update > typing_speed:
                    if pre_game_text_chars < len(story_text):
                        pre_game_text_chars += 1
                        pre_game_text_last_update = time.time()

                background = draw_multiline_korean_text_typing(background, story_text, (WIN_WIDTH//2, TEXT_Y - 20), 20, (255,255,255), pre_game_text_chars)
                
                if pre_game_text_chars >= len(story_text) and time.time() - pre_game_text_last_update > 2:
                    game_state = STATE_GAMEPLAY
                    quest_start_time = time.time()

            cv2.imshow("Reality Quest", background)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        elif game_state == STATE_GAMEPLAY:
            background = original_bg_img3.copy()
            IMG_Y = 50
            QUEST_TEXT_Y = IMG_Y + CAM_SIZE + 75
            TIME_TEXT_Y = QUEST_TEXT_Y + 60
            DETECT_TEXT_Y = TIME_TEXT_Y + 60
            CAM_Y = DETECT_TEXT_Y + 75

            time_elapsed = time.time() - quest_start_time
            time_remaining = QUEST_TIME_LIMIT - time_elapsed
            if time_remaining < 0:
                time_remaining = 0
                game_state = STATE_GAMEOVER
                game_over_text_last_update = time.time()
                mouse_clicked = False
            
            if game_state == STATE_GAMEOVER:
                continue

            ret, frame = camera.read()
            if not ret: break

            h, w, _ = frame.shape
            crop_size = min(h, w)
            start_x = (w - crop_size) // 2
            start_y = (h - crop_size) // 2
            cam_view = cv2.resize(frame[start_y:start_y+crop_size, start_x:start_x+crop_size], (CAM_SIZE, CAM_SIZE))

            pil_image = Image.fromarray(cv2.cvtColor(cam_view, cv2.COLOR_BGR2RGB))
            outputs = detector(pil_image)

            found_quest_object = False
            highest_confidence_object = ""
            highest_confidence = 0

            for output in outputs:
                score, label, box = output["score"], output["label"], output["box"]
                if score > highest_confidence: highest_confidence, highest_confidence_object = score, label
                if score >= CONFIDENCE_THRESHOLD:
                    xmin, ymin, xmax, ymax = box.values()
                    cv2.rectangle(cam_view, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                    cv2.putText(cam_view, f"{label}: {score:.2f}", (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    if label == QUEST_ITEMS[current_quest_index]: found_quest_object = True
            
            last_detected_object = highest_confidence_object if highest_confidence > 0.5 else ""
            
            background[IMG_Y:IMG_Y+CAM_SIZE, CAM_X_OFFSET:CAM_X_OFFSET+CAM_SIZE] = teacher_img
            
            quest_item = QUEST_ITEMS[current_quest_index]
            background = draw_korean_text(background, f"요구하는 물체: {quest_item}", (WIN_WIDTH//2, QUEST_TEXT_Y), 25, (255, 255, 255))
            if time_remaining > 10:
                timer_color = (0, 255, 0)  # Green
            elif time_remaining > 5:
                timer_color = (0, 255, 255)  # Yellow
            else:
                timer_color = (0, 0, 255)  # Red
            background = draw_korean_text(background, f"제한 시간: {int(time_remaining)}초", (WIN_WIDTH//2, TIME_TEXT_Y), 25, timer_color)
            background = draw_korean_text(background, f"인식된 물체: {last_detected_object}", (WIN_WIDTH//2, DETECT_TEXT_Y), 25, (255, 255, 255))
            
            background[CAM_Y:CAM_Y+CAM_SIZE, CAM_X_OFFSET:CAM_X_OFFSET+CAM_SIZE] = cam_view

            if found_quest_object:
                background = draw_korean_text(background, f"'{quest_item}' 찾음! (성공)", (WIN_WIDTH//2, CAM_Y + CAM_SIZE // 2), 40, (0, 0, 255))
                if quest_completed_time == 0: quest_completed_time = time.time()
                if time.time() - quest_completed_time > 2:
                    current_quest_index += 1
                    quest_completed_time = 0
                    quest_start_time = time.time()
                    if current_quest_index >= len(QUEST_ITEMS): 
                        game_state = STATE_GAMEOVER
                        game_over_text_last_update = time.time()


            cv2.imshow("Reality Quest", background)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        elif game_state == STATE_GAMEOVER:
            success_story = """당신은 당신을 묶어두는 모든 물건을\n찾아서 해체했습니다.\n\n하지만 불행하게도\n당신에게는 다른 차원을 \n건너갈 수 있는 마력이 남아있지 않았고\n당신의 스승님도 힘을 다 써버렸습니다.\n\n결국에 이 차원에 남게 된 당신은\n본래의 차원을 그리워 하며\n살아가게 됩니다.\n\n-끝-"""

            failure_story = """당신은 당신을 묶어두는 모든 물건을\n찾아서 해체하지 못했고\n당신의 스승님은 힘을 다 써버려서\n연락이 끊기고 말았습니다.\n\n결국에 이 차원에 남게 된 당신은\n본래의 차원을 그리워 하며\n살아가게 됩니다.\n\n-끝-"""

            if current_quest_index >= len(QUEST_ITEMS):
                background = apply_transparency(result_img1.copy())
                end_text = success_story
            else:
                background = apply_transparency(result_img2.copy())
                end_text = failure_story

            if time.time() - game_over_text_last_update > typing_speed:
                if game_over_text_chars < len(end_text):
                    game_over_text_chars += 1
                    game_over_text_last_update = time.time()

            background = draw_multiline_korean_text_typing(background, end_text, (WIN_WIDTH//2, 300), 22, (0,0,0), game_over_text_chars)
            
            if game_over_text_chars >= len(end_text):
                background = draw_korean_text(background, "아무 곳이나 클릭하여 종료하세요", (WIN_WIDTH//2, 750), 25, (50,50,50))
            
            cv2.imshow("Reality Quest", background)
            if mouse_clicked and game_over_text_chars >= len(end_text):
                break
            elif mouse_clicked:
                game_over_text_chars = len(end_text)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    print("게임을 종료합니다.")
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
