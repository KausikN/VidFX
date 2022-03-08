import cv2
import requests
import numpy as np
import imutils

# url = "http://192.168.0.102:8080/shot.jpg"
url = "http://195.77.185.114:8081/oneshotimage1"
while True:
    img_resp = requests.get(url).content
    print(type(img_resp))
    img_arr = np.array(bytearray(img_resp), dtype=np.uint8)
    print(img_arr.shape)
    # img = cv2.imdecode(img_arr, -1)
    img = cv2.imdecode(img_arr, 0)
    print(img)
    img = imutils.resize(img, width=1000, height=1800)
    cv2.imshow("Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()