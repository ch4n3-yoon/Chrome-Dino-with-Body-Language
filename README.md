# Playing Chrome Dino game with Body Language

## 프로젝트 목표 및 내용

최신 버전(2020.05.26. 기준)의 크롬에서는 네트워크 연결이 끊겼을 때 즐길 수 있는 게임보이풍의 간단한 게임이 존재한다. 이는 크롬 브라우저에 내장된 이스터에그로, 정식 명칭은 존재하지 않고 Chrome Dinosaur, Chrome T-Rex, Chrome Dino 등으로 불린다. 해당 게임은 스페이스바를 눌러 공룡이 점프하도록 할 수 있으며 장애물로는 선인장과 익룡이 등장하는데, 장애물을 만나면 공룡은 죽고 게임이 끝나게 된다. 별도의 설치가 필요없고, 간단하게 즐길 수 있기 때문에 많은 사람들의 사랑을 받고 있다.

![Chrome Dino Game](https://lh3.googleusercontent.com/I39p4qQ7NebJ9Q6CAGzjzTuFt7naS5dCd3Gh7yS9aivaGh4pZKwU5tNLfWSQoeoke1TfMtfy=w640-h400-e365) 
  
 이 프로젝트는 컴퓨터에 장착된 카메라 영상에서 플레이어의 동작을 인식해, 실제로 카메라 앞에서 사용자가 특정한 동작을 하면 T-Rex가 점프하도록 만든다. 이 프로젝트의 최종적인 목표는 아이들도 쉽게 플레이할 수 있고, 가족끼리 즐길 수 있으며, 아이들이 별 다른 도구 없이도 친구들과 재밌게 놀 수 있는 실내형 게임을 구축하는 것이다.

## 구현내용

### 4-1. Image Classification
 Image Classification에는 Teachable Machine으로 만든 예측모델을 사용하였다.
 
### 4-2. Tensorflow.js

 원래는 Python3의 opencv와 Python3의 tensorflow 모듈을 사용해서 개발하려 했으나, Teachable Machine에서 Tensorflow.js에서 사용하는 모델만 지원하는 이유로 Python3와 Javascript를 모두 사용하는 방식으로 바꾸었다. 찾아보니 `tfjs_converter` 라는 툴이 있었다. 이 도구를 사용하면 `Tensorflow.js`에서 사용하는 `models.json`과 `weights.bin` 파일을 사용하여 Python Keras에서 사용되는 `.h5` 파일로 변환할 수 있다. 하지만, 이 도구를 실행하여 반환된 모델을 사용하여 스크립트를 실행하면 계속 자잘한 오류가 생겨서, 안정성 문제로 Python3의 tensorflow 모듈 대신 Javascript의 tensorflow.js를 사용할 수 밖에 없었다.
 

### 4-3. Flask Web Server

 Flask Web Server 에서 적용되는 라우트는 `/game`, `/cam`, `/jump` 세 가지이다. 
 1. `/game`에 접속하면 Chrome T-Rex Game이 뜬다. T-Rex Game은 HTML + Javascript로 되어 있으며, Flask의 `render_template()` 함수를 이용하여 Response를 보낸다.
 2. `/cam`에 접속하면 `Tensorflow.js`를 사용한 예측 모델로 WebCam에서 감지한 이미지를 predict한 결과값을 볼 수 있다. 해당 페이지에서 사용자가 Jump 했다고 판단하면 `fetch()` 함수를 사용해서 `/jump`에 HTTP Request를 보낸다. 그런데 Jump라고 판단할 때마다 `/jump`에 request를 보내면 그 만큼의 Spacebar가 계속 눌려지는 것으로 판단되기 때문에 사용자가 원하지 않을 때 Jump를 수행할 수도 있다. 따라서 한 번 요청하면 0.5 간 요청하지 않도록 하는 코드를 추가했다.

 3. `/jump`에서는 `4-4. Win32API`와 연결되어 있다. 접속하는 순간 스페이스바의 Keyboard Signal을 보낸다.

 만약에 Flask로 Web server를 구동했다면 `app.run()`을 실행하고 나서 다음코드를 실행할 수 없다. `app.run()` 메소드는 HTTP Request를 기다리며 매번 루프를 돌기 때문에 다음 코드를 실행하거나 병렬적인 실행을 할 수 없다. 이러한 점을 해결하기 위해 Python3의 `threading` module을 사용하였다. 해당 모듈을 사용하면 스레드를 통해 코드를 병렬적으로 처리할 수 있기 때문에 Python에서 Flask로 웹서버도 구동하면서 이와 별개의 코드를 함께 돌릴 수 있게 된다.

### 4-4. Win32API

3번 항목은 Python에서도 WinAPI 등, Binary resource를 사용하고 싶을 때 보통 ctypes module을 사용한다. ctypes module은 파이썬용 외부 함수 라이브러리로서, 해당 module을 이용하면 파이썬에서 DLL 또는 공유 라이브러리에 있는 함수를 사용할 수 있다. 이 프로젝트에서는 user32.dll의 [SendInput](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput) 함수를 사용하면 스페이스바의 keyboard signal을 구현할 수 있다.


### 4-5. Chrome T-Rex Game

크롬에 내장되어 있는 T-Rex game은 `chrome://dino`로 접속하면 플레이할 수 있다. 하지만 이미지 처리 및 분석 과정에 약간의 시차가 있기 때문에 정상적으로 게임을 진행하기 힘든 점이 생겨서 난이도 조절을 위해 오픈소스로 된 Chrome T-Rex Game 을 가져와서 난이도 조절을 하였다. 난이도 하향을 적용한 부분은 `MAX_OBSTACLE_LENGTH`와 `Obstacle.getGap()`, `INIITAL_JUMP_VELOCITY`와 `DROP_VELOCITY`이다.

- `MAX_OBSTACLE_LENGTH` : 원래의 게임에서는 장애물이 3개가 곂쳐져 나오는 경우가 있었는데, 해당 프로젝트 게임에서는 사용자가 타이밍을 맞추기 힘들어하는 점을 고려하여 MAX_OBSTACLE_LENGTH를 2로 조정했다.
- `Obstacle.getGap()` : 이 메소드는 장애물이 생성되기 전 장애물 간의 거리를 구하는 코드의 집합이다. 여기에서 장애물 간의 거리를 증폭하여 사용자가 더 쉽게 게임을 할 수 있도록 수정했다. 
- `INIITAL_JUMP_VELOCITY`, `DROP_VELOCITY` : 두 변수는 각각 Dinosaur가 점프할 때의 초기속도와 떨어질 때의 중력가속도라고 생각하면 되는데, 이 값을 적절히 조정하여 Dinosaur이 더 높게 점프하고 더 천천히 착지하는 것으로 난이도를 조정했다.


### 4-6. Python Selenium

 제작한 Flask Web Server에서 `/game`에 접속하면 `Chrome T-Rex Game` 화면을 출력하고 `/cam` 에 접속하면 `Tensorflow.js + WebCam` 화면이 출력된다. 이를 사용자가 브라우저에서 직접 접속하면 매우 번거롭기 때문에 Python Selenium을 이용하여, Python 스크립트를 실행하면 `http://URL/game` 과 `http://URL/cam` 화면을 동시에 띄어주도록 하였다.

## 구현 결과

[\*] github : https://github.com/ch4n3-yoon/Chrome-Dino-with-Body-Language <br>
[\*] 구현 영상 : https://www.youtube.com/watch?v=UOAHIvQxxNA

## author
 경희대학교 컴퓨터공학과 20학번 윤석찬<br>
 Seok-chan Yoon, Department of Computer Science and Engineering, Kyunghee University
