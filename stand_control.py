import cv2
import serial
import time
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

ser = serial.Serial('COM9', 9600) # 시리얼 포트를 연결합니다.

data_array = []
word_array = []
while True:
    if ser.in_waiting > 0:
        data = ser.read().decode('utf-8')
        data_array.append(data)  # 데이터를 배열에 추가

        # 새로운 데이터가 입력되면 이전 데이터 출력하지 않음
        if len(data_array) == 8:
            word = ''.join(data_array)
            word = word[1:] + word[0]  # 0번 인덱스를 맨 뒤로 보냄
            word_array.append(word)  # word를 배열에 추가
            print(word)

            if len(word_array) == 2:
                n1_str = word_array[1][1:4]
                n2_str = word_array[1][5:8]
                want_guri = int(n1_str)
                want_loc = int(n2_str)
                print("원하는 거리 : ", want_guri)
                print("원하는 높이 : ", want_loc)
                break

            data_array = []  # 배열 초기화


#동기화 한 식
D = -9.5 * want_guri +550

print(D)

want_line1 = want_loc - D//2
want_line2 = want_loc + D//2 #y값


start_time = time.time()
frame_count = 0

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("Video frame size: {} x {}".format(frame_width, frame_height))

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    image_height, image_width, _ = image.shape
    if not success:
      print("웹캠을 찾을 수 없습니다.")
      # 비디오 파일의 경우 'continue'를 사용하시고, 웹캠에 경우에는 'break'를 사용하세요.
      continue
   # 보기 편하기 위해 이미지를 좌우를 반전하고, BGR 이미지를 RGB로 변환합니다.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
   # 성능을 향상시키려면 이미지를 작성 여부를 False으로 설정하세요.
    image.flags.writeable = False
    results = face_detection.process(image)

    cv2.line(image, (0, round(want_line1)), (640, round(want_line1)), (0, 255, 0), 2)
    cv2.line(image, (0, round(want_line2)), (640, round(want_line2)), (0, 255, 0), 2)

    # 영상에 얼굴 감지 주석 그리기 기본값 : True.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection)
        height, ctr_point = mp_drawing.draw_detection(image, detection)
        height = height * frame_height #미디어파이프와 cv2 픽셀값 동기화

        print("현재 위치: ", ctr_point,"\n")
        print("현재 거리(크기): ",height, "\n")
        print("\n")

        d_error = 40 #거리 오차
        if(height > D+d_error):
          text = "Move further away "
          ser.write('a'.encode()) #뒤로 가기
          time.sleep(0.6)
          print("a")
        elif (height >= D-d_error and height <= D+d_error):
          text = "Right"
        elif (height < D-d_error) :
          text = "Get closer"
          ser.write('b'.encode())  # 앞으로 가기
          time.sleep(0.6)
          print("b")

        if(ctr_point[1] < want_line1): #얼굴이 line1 위에 있다 -> 화면을 올린다
          text2 = "laptop up"
          ser.write('d'.encode())  # 위로 올리기
          time.sleep(0.6)
          print("d")
        elif(ctr_point[1] > want_line2): #얼굴이 line2보다 아래에 있다 -> 화면을 내린다.
          text2 = "laptop down"
          ser.write('c'.encode())  # 아래로 내리기
          time.sleep(0.6)
          print("c")
        else:
          text2 ="right"

        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        cv2.putText(image, text2, (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        # image = apply_face_blur(image, results.detections)

    cv2.imshow('MediaPipe Face Detection', image)

    frame_count += 1

    if cv2.waitKey(5) & 0xFF == 27:
      break

    if time.time() - start_time >= 1:
        print("FPS:", frame_count)
        frame_count = 0
        start_time = time.time()