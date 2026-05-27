# [3D / (주)레드브릭] Melody Pang Pang (리듬 게임)

**현 상황 : 출시 완료 및 서비스 중** 

**Game Play Link :**

 https://redbrick.land/detail-play?pid=1ce4db26-b22d-42f9-bb63-072c23e7ab06

![스크린샷 2024-10-10 오후 6.54.09.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-10_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_6.54.09.png)

![스크린샷 2024-10-10 오후 6.56.16.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-10_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_6.56.16.png)

## 제작 환경

- 사용 기술 및 언어 : Redbrick + JavaScript
- 업무 기간 : 2024년 10월 21일 출시 (약 2주 동안 개발)
- 역할 : 디자이너와 협업 **1인 개발**

## 게임 개요

- **장르** : 리듬 게임
- **플랫폼** : PC, Mobile
- **플레이어 수**  : 1인 (싱글 플레이)
- **목표** :  타이밍에 맞게 리듬 노드를 눌러 높은 점수를 획득 (+ 높은 랭킹)

## 게임 배경

- **장소**  : 사이버 펑크 스테이지
- **특징** : 주변이 어두움. LED 라이트 존재

## 게임 메커니즘

1. 플레이 시간 : 20~30초
2. 시점 : 3인칭

## 점수 및 체력 시스템

- 기본 점수 시스템
    - Perfect : 20점
    - Cool : 10점
    - Miss : 0점
- 콤보 시스템
    - 최초 Perfect시 1콤보 생성
    - 연속 Perfect 혹은 Cool시 +1씩 오름
    - 20콤보부터 1.5배 점수 획득
    - 50콤보부터 2배 점수 획득
- 체력 시스템
    - 체력 100
    - 노드 하나 놓칠 때 마다 -10

## UI/UX

- 판정 노드와 리듬 노드 사이의 거리별 판정
    - 기본 조작 버튼을 눌렀을 때 나오는 배경 빛 기둥
    - 리듬 노드가 판정 사거리 안으로 들어왔을 때의 라이트 효과
    - 판정에 맞게 표시되는 UI (Perfect, Cool, Miss)
- 콤보 판정
    - 최초 Perfect 판정 시 부터 시작하는 콤보 UI
    - Miss 판정 시 콤보 초기화
    - 스코어 보드에 최고 콤보 수 기록
- 체력 판정
    - Miss 판정 시 체력 -10 감소
- 게임 종료 시
    - 음악이 끝난 후에 , 인게임 외에 쓰이는 배경음악을 다시 재생함.
        - 게임 시작 : 타이틀 음악
        - 게임 진행 : 게임용 음악
        - 게임 종료 후 점수 표시 : 타이틀 음악

## 개발하면서 신경 쓴 부분

- 재미 → 노래 박자의 정확한 타이밍에 맞춰 떨어지는가 → 180bpm 인 노래에 맞춰 박자를 쪼개고 노드를 넣음 → 게임 시작 기점이 아닌 노래 시작과 현재 플레이 중인 노래 기점으로 박자를 계산함 (컴퓨터의 사양을 고려한 해결책)
- 시각적 효과 → 리듬 게임 레퍼런스를 조사해서 유명한 게임들의 시각적 효과를 비슷하게 가져가 친근감과 익숙함을 주고자 함 → 점수 및 판정 글자 커지면서 나오는 효과 / 알맞은 터치 시 터지는 이펙트
- 긴장감 → 실패할 때마다 옆에 HP가 자연스럽게 줄어들고 카메라의 살짝 흔들림을 넣음 → 콤보 GUI 사라짐

## 배경 디자인

![screenshot_3840x1440_2024-09-27_10-10-46.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/screenshot_3840x1440_2024-09-27_10-10-46.png)

## GUI

- **How to Play**
    
    ![스크린샷 2024-10-10 오후 6.54.09.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-10_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_6.54.09%201.png)
    

- **인게임**
    
    ![스크린샷 2024-10-10 오후 6.56.16.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-10_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_6.56.16%201.png)
    

- 게임 종료 (체력 감소)
    
    ![스크린샷 2024-10-08 오후 4.32.39.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-08_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_4.32.39.png)
    

- 게임 종료(노래 종료)
    
    ![스크린샷 2024-10-08 오후 4.33.31.png](%5B3D%20(%EC%A3%BC)%EB%A0%88%EB%93%9C%EB%B8%8C%EB%A6%AD%5D%20Melody%20Pang%20Pang%20(%EB%A6%AC%EB%93%AC%20%EA%B2%8C%EC%9E%84)/%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA_2024-10-08_%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE_4.33.31.png)
    

## 주요 개발 코드 설명

- **노드 생성 코드**
    - 사용자마다 노래 시작 타이밍이 달라서 게임 버튼 클릭한 기준이 아닌 노래 재생하여 노래 재생 시간을 기준으로 노드를 생성하고 내려오게 생성함.
    - 일정 y 축 이하로 내려갔고 사용자가 클릭하지 못한 노드라면 Miss 판단
    - 추가적으로, 판정을 쉽게 하기 위해 생성 순서대로 각 노드 별로 고유의 숫자 번호 부여
    
    ```jsx
    const boxSpeed = 5; // 박스 하락 속도
    //const boxSpeed = 3; 
    const leadTime = 2;  // 비트 타이밍보다 미리 생성할 시간 (초)
    const trigger_y = 0;
    const startBeatTimes = 3.37;
    const trigger_x = [-2, -1.2, -0.4, 0.4];
    const timeAdjustment = 0.5;
    
    function calBoxPosition(time, speed, targetY, trigger_x, index) {
        let trigger_index = 0;
        // 시작 위치를 계산: initialY = targetY + (speed * time)
        const initialY = targetY + (speed * time);
        const initialX = trigger_x[index % 4];
        const initialZ = 66;
        
        return {x: initialX, y: initialY, z: initialZ};
    }
    
    function Update(dt) {
        if (music.isPlaying) {
            const playTime = music.context.currentTime - music._startedAt;
    
            // beatTimes에 따라 미리 박스를 생성
            beatTimes.forEach((beatTime, index) => {
                // 현재 재생 시간(playTime)이 beatTime - leadTime에 도달했을 때 박스 생성
                if (playTime >= (beatTime + timeAdjustment - leadTime) && !downBoxes[index] && beatNodePattern[currentNodePatternNum] != null) {
                    let newBoxes = [];
                    beatNodePattern[currentNodePatternNum].forEach((num, index) => {
                        if(num === 1){
                            let newBox = null;
                            if(index === 1 || index === 3){
                                if(index === 1) newBox = upNode.clone(); 
                                else newBox = rightNode.clone(); 
                            }else{
                                if(index === 0) newBox = leftNode.clone(); 
                                else  newBox = downNode.clone(); 
                            }
                            const initialY = calBoxPosition(playTime, boxSpeed, trigger_y, trigger_x, index).y; // 시작 Y값
                            newBox.position.set(trigger_x[index % 4], initialY, 66); // X, Y, Z 설정
                            newBox.isClick = false;
                            newBox.index = currentNodeNum;
                            WORLD.add(newBox); // 씬에 박스 추가
                            newBoxes.push(newBox);
                            beatBoxes.push(newBox);
                            
                            currentNodeNum++;
                            console.log(currentNodeNum);
                        }
                    });
                    downBoxes[index] = newBoxes; // 생성한 박스를 downBoxes 배열에 저장
                    currentNodePatternNum++;
                }
            });
    
            // 박스의 위치를 업데이트
            downBoxes.forEach((boxes) => {
                if (boxes) {
                    boxes.forEach((box) => {
                        box.position.y -= boxSpeed * dt; // 박스 하락
                        if (box.position.y <= trigger_y) {
                            if(box.isClick === false) {
                                console.log(`drop Miss ${box.index} box`);
                                gameGUI.clickNode(false, false, true);
                                box.isClick = true;
                                lastClickBox = box.index;
                                currentCombo = 0;
                                gameGUI.settingComboUI(currentCombo);
                                missDamge();
                            }
                            
                            box.position.y = trigger_y; // 최소 Y값 설정
                        }
                    });
                }
            });
    
            //console.log('현재 재생 위치:', playTime.toFixed(2));
        }else{
            if(currentGameState === "GAME_START"){
                GameEnd(true);
            }
        }
    }
    ```
    
- **노드 판정 코드**
    - 클릭 시 어떤 노드인지 확인 후 가까운 노드를 찾는 코드
    - 클릭 했을 때, 마지막에 친 노드 번호를 기점으로 앞의 노드 4개, 뒤의 노드 4개 검사 → 모든 노드를 검사하면 과 부화가 오기 때문에 , 또한 각 X 위치 값을 통해서 어떤 기준 노드에 해당해서 친 건지 확인 → 일정 거리 값(적어도 판정할 수 있는) 이하에 있는 제일 가까운 노드를 가져와서 기준 노드와 거리값을 통해서 perfect, cool, miss 로 판정
    
    ```jsx
    function CheckDownBoxes(keyNum){
        let compareBox = null;
        let compareX = 0; 
        let findNearBox = null;
        let nearDistance = 10000000;
        
        switch(keyNum){
            case "Left":
                compareBox = leftBox.position;
                compareX = trigger_x[0];
                break;
            case "Up":
                compareBox = upBox.position;
                compareX = trigger_x[1];
                break;
            case "Down":
                compareBox = downBox.position;
                compareX = trigger_x[2];
                break;
            case "Right":
                compareBox = rightBox.position;
                compareX = trigger_x[3];
                break;
            default:
                break;
        }
        
        for(let i=-4; i<4; i++){
            if(lastClickBox + i >= 0 && beatBoxes[lastClickBox + i]){
                let box = beatBoxes[lastClickBox + i];
                if(box.position.x === compareX && box.isClick === false){
                    let distanceY = box.position.y - compareBox.y;
                    distanceY = Math.abs(distanceY);
                    if(distanceY < nearDistance){
                        findNearBox = box;
                        nearDistance = distanceY;
                    }
                }
            }
        }
        
        if(findNearBox != null){
            findNearBox.isClick = true;
            lastClickBox = findNearBox.index;
            if(nearDistance <= 0.2){
                //console.log(`Perfect ${nearDistance}`);
                console.log(`Perfect ${findNearBox.index} box`);
                
                currentCombo++;
                gameGUI.settingComboUI(currentCombo);
                
                let comboScore = 20;
                if(currentCombo >= 50) comboScore *= 2;
                else if(currentCombo >= 20) comboScore *= 1.5;
                
                gameGUI.clickNode(true, false, false);
                gameGUI.settingScoreUI(comboScore);
                
                playLightBox(keyNum);
                
            }else if(nearDistance <= 0.5){
                //console.log(`Cool ${nearDistance}`);
                console.log(`Cool ${findNearBox.index} box`);
                
                currentCombo++;
                gameGUI.settingComboUI(currentCombo);
                
                let comboScore = 10;
                if(currentCombo >= 50) comboScore *= 2;
                else if(currentCombo >= 20) comboScore *= 1.5;
                
                gameGUI.clickNode(false, true, false);
                gameGUI.settingScoreUI(comboScore);
                
            }else if(nearDistance <= 1){
                //console.log(`Miss ${nearDistance}`);
                console.log(`Miss ${findNearBox.index} box ${nearDistance}`);
                gameGUI.clickNode(false, false, true);
                gameGUI.settingScoreUI(0);
                currentCombo = 0;
                gameGUI.settingComboUI(currentCombo);
                missDamge();
            }      
        }
    }
    ```
    
- **GUI 애니메이션 코드**
    - 판정, 콤보 GUI 에게 이펙터 같은 효과를 주기 위해서 tween 을 사용해 애니메이션 제작
    
    ```jsx
    clickNode(isPerfect, isCool, isMiss){
            this.perfectUI.hide();
            this.coolUI.hide();
            this.missUI.hide();
            
            let currentJudeUI = null;
            
            if(isPerfect){
                this.perfectUI.show();
                currentJudeUI = this.perfectUI;
            }
            else if(isCool){
                this.coolUI.show();
                currentJudeUI = this.coolUI;
            }
            else if(isMiss){
                this.missUI.show();
                currentJudeUI = this.missUI;
            }
            
            const start = { x: 20 }; 
            const end = { x: 25 }; 
            
            const tween = new TWEEN.Tween(start)
            .to(end, 200) 
            .onUpdate((obj) => { 
                currentJudeUI.size.x.value = start.x;
            })
            .easing(TWEEN.Easing.Quartic.InOut) 
            .start();
        }
    ```