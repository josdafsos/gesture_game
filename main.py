import cv2
import handDetection as Hd
import cvButton
import time
import audioPlayer as ap
import buttonHandler as bh

FINGER_RADIUS = 7

def main():
    bh.ButtonHandler.getInstance()
    #bh.ButtonHandler.getInstance().get_new_button("1")
    hand_detector = Hd.handDetector()
    ap.AudioPlayer.getInstance()
    cap = cv2.VideoCapture(0)

    buttons = []
    for i in range(8):
        button = cvButton.Button(40 + i * 80, 100, 1, i, "rectangle")
        buttons.append(button)
    timeNew = time.time()
    timeOld = 0
    make_check = True

    buttons.append(bh.ButtonHandler.getInstance().get_new_button("2"))
    buttons.append(bh.ButtonHandler.getInstance().get_new_button("2"))
    buttons.append(bh.ButtonHandler.getInstance().get_new_button("example_button"))


    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands = hand_detector.findHands(img)

        point_fingers = []
        ring_fingers = []
        for hand in hands:
            finger = (hand[8][1], hand[8][2])
            point_fingers.append(finger)
            ring_finger = (hand[16][1], hand[16][2])
            ring_fingers.append(ring_finger)
        #print(point_fingers)
        if make_check:
            h, w, c = img.shape
            for button in buttons:
                for finger in point_fingers:
                    if button.collisionDetect(finger, FINGER_RADIUS, FINGER_RADIUS):
                        img = button.action(img)
                        ap.AudioPlayer.getInstance().playSound(str(button.id))
                        make_check = False
                        break
                for finger in ring_fingers:
                    if not(button.is_triggered):
                        if button.collisionDetect(finger, FINGER_RADIUS, FINGER_RADIUS):
                            img = button.action(img)
                            #ap.AudioPlayer.getInstance().playSound(str(button.id + 8))
                            make_check = False
                            break
                button.dynamic_action(h, w)

        timeNew = time.time()
        if timeNew - timeOld > 0.05:
            timeOld = time.time()
            make_check = True

        ##### Drawing ######

        img = hand_detector.drawHands(img)
        for button in buttons:
            img = button.draw(img)

        for i in point_fingers:
           img = cv2.circle(img, i, FINGER_RADIUS, (50, 255, 50), -1)
        for i in ring_fingers:
           img = cv2.circle(img, i, FINGER_RADIUS, (50, 50, 250), -1)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
