import cv2
"""
В этом фале реализрванн 
видеоо детектор 
который подаёт необходимый сигнал 
при пободании в кадр железной шайбы
"""
how_obj = 0
cord_xy = []
picture = cv2.VideoCapture(0)
while picture.isOpened():
    ret, frame = picture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    borders = cv2.Canny(gray, 130, 230, 4)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(borders, cv2.MORPH_CLOSE, kernel)
    cv2.line(frame, (650, 240), (0, 240), (0, 255, 0), 4)
    width, height, safdasf = frame.shape
    cv2.circle(frame, (int(height / 2), int(height / 2) - 80), 10, (0, 0, 255), -1)
    conturs, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in conturs:
        if 196 < len(cnt) < 430:
            moments = cv2.moments(cnt, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']
            if dArea > 10:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                print(y)
                if 240 <= x <= 300 and len(cord_xy) == 0:
                    print(y)
                    cord_xy.append(x)
                    cord_xy.append(y)
                    break

                cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
                circle = cv2.fitEllipse(cnt)
                cv2.ellipse(frame, circle, (0, 0, 255), 2)
                cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)

    cv2.imshow('frame', borders)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
picture.release()
