
# reality_quest.py
# 현실 퀘스트 (Reality Quest) - 객체 탐지 모델 단독 버전
#
# [중요] 실행 전 필수 라이브러리를 설치해야 합니다.
# pip install transformers torch opencv-python Pillow
#
# [경고] 이 스크립트는 처음 실행 시 약 250MB의 AI 모델을 다운로드합니다.

import cv2
import torch
from transformers import pipeline
from PIL import Image
import time

# --- 게임 설정 ---
# 찾아야 할 사물 목록 (Object Detection 모델이 인식할 수 있는 영어 단어)
# 예: 'cup', 'book', 'keyboard', 'mouse', 'bottle', 'person', 'chair', 'laptop'
QUEST_ITEMS = ["cup", "book", "keyboard", "bottle"]

# 인식 정확도 임계값 (0.0 ~ 1.0)
CONFIDENCE_THRESHOLD = 0.9

def initialize_game():
    """
    게임에 필요한 AI 모델과 웹캠을 초기화합니다.
    """
    print("현실 퀘스트에 오신 것을 환영합니다!")
    print("="*40)
    
    # 1. AI 객체 탐지 모델 로딩
    print("  - 객체 탐지 AI 모델을 로딩합니다...")
    print("    (처음 실행 시 모델을 다운로드합니다.)")
    try:
        # GPU 사용 가능하면 GPU로, 아니면 CPU로 설정
        device = 0 if torch.cuda.is_available() else -1
        object_detector = pipeline("object-detection", model="facebook/detr-resnet-50", device=device)
        print("  > AI 모델 로딩 완료!")
    except Exception as e:
        print(f"  > AI 모델 로딩 실패: {e}")
        print("    스크립트를 종료합니다.")
        return None, None

    # 2. 웹캠 로딩
    print("  - 웹캠을 초기화합니다...")
    cap = cv2.VideoCapture(0) # 0번 카메라(기본 웹캠)
    if not cap.isOpened():
        print("  > 웹캠을 열 수 없습니다. 카메라가 연결되어 있는지 확인하세요.")
        return object_detector, None
    print("  > 웹캠 로딩 완료!")
    
    print("="*40)
    print("게임을 시작합니다! 화면에 표시되는 사물을 찾아 웹캠에 보여주세요.")
    print("게임을 종료하려면 'q' 키를 누르세요.")
    
    return object_detector, cap

def game_loop(object_detector, cap):
    """
    메인 게임 루프: 웹캠 영상을 처리하고 퀘스트를 진행합니다.
    """
    current_quest_index = 0
    quest_completed_time = 0

    while True:
        # 웹캠에서 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("웹캠에서 프레임을 읽어올 수 없습니다.")
            break

        # 현재 퀘스트 아이템
        quest_item = QUEST_ITEMS[current_quest_index]

        # AI 모델 입력을 위해 프레임 변환 (OpenCV BGR -> PIL RGB)
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # 객체 탐지 수행
        outputs = object_detector(pil_image)

        found_object = False
        # 탐지된 객체들을 순회하며 퀘스트 아이템과 일치하는지 확인
        for output in outputs:
            score = output["score"]
            label = output["label"]
            box = output["box"]

            # 정확도가 임계값 이상인 경우에만 처리
            if score >= CONFIDENCE_THRESHOLD:
                # 객체 주변에 사각형 그리기
                xmin, ymin, xmax, ymax = box.values()
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                # 객체 이름과 정확도 표시
                text = f"{label}: {score:.2f}"
                cv2.putText(frame, text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # 퀘스트 아이템을 찾았는지 확인
                if label == quest_item:
                    found_object = True

        # 퀘스트 완료 처리
        if found_object:
            # 퀘스트 완료 메시지 표시
            cv2.putText(frame, f"'{quest_item}' 찾음! (성공)", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            # 다음 퀘스트로 넘어가기 전 2초 대기
            if quest_completed_time == 0:
                quest_completed_time = time.time()

            if time.time() - quest_completed_time > 2:
                current_quest_index += 1
                quest_completed_time = 0 # 타이머 리셋
                # 모든 퀘스트를 완료했는지 확인
                if current_quest_index >= len(QUEST_ITEMS):
                    break # 게임 루프 종료

        # 현재 퀘스트 목표 표시
        if current_quest_index < len(QUEST_ITEMS):
            quest_text = f"Find: {QUEST_ITEMS[current_quest_index]}"
            cv2.putText(frame, quest_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        
        # 화면에 영상 출력
        cv2.imshow("Reality Quest", frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 게임 종료 처리
    if current_quest_index >= len(QUEST_ITEMS):
        print("축하합니다! 모든 퀘스트를 완료했습니다!")
    else:
        print("게임을 종료합니다.")

    # 자원 해제
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detector, camera = initialize_game()
    if detector and camera:
        game_loop(detector, camera)
