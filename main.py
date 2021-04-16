import cv2
import handDetection as Hd
import cvButton
import time
import audioPlayer as ap
import buttonHandler as bh
import utils
import textureManager as tm

FINGER_RADIUS = 7
LOGIC_DELAY = 0.001
FPS_DELAY = 0.005
#WIN_HEIGHT = 720
#WIN_WIDTH = 900

buttons = []
hand_buttons = []
# to check which subact in each scene is happening
scene_act = 0

def scene_1(img):

    global scene_act
    global buttons
    global hand_buttons

    if scene_act == 0:
        #pass
        # for i in range(8):
        #     button = cvButton.Button(40 + i * 80, 100, 1, i, "rectangle", {})
        #     buttons.append(button)

        # buttons.append(bh.ButtonHandler.getInstance().get_new_button("2"))
        # buttons.append(bh.ButtonHandler.getInstance().get_new_button("example_button"))
        buttons.append(bh.ButtonHandler.getInstance().get_new_button("kich_head"))

        scene_act += 2

    if scene_act == 1:
        destroyable_buttons_cnt = 0
        for b in buttons:
            if b.is_destroyable():
                destroyable_buttons_cnt += 1
        required_buttons = 50
        if destroyable_buttons_cnt < int(0.15*required_buttons):
            h, w, c = img.shape
            spawn_area = (int(w*0.1), int(h*0.1),
                          int(w*0.9), int(h*0.9))
            # for i in range(required_buttons):
            #     #pass
            #     buttons.append(bh.ButtonHandler.getInstance().
            #                   spawn_in_random_place("test_destroyable_button", spawn_area))
            button_list = ["red_circle", "blue_circle", "green_rect", "star"]
            buttons.extend(bh.ButtonHandler.getInstance().
                           spawn_random_from_list_random_place(button_list,
                                                               required_buttons, spawn_area))


def main():
    # TODO two finger connect to cause wave
    # TODO scene class with health bar and other staff, check if hands on the screen
    # TODO lambda for upload attributes

    bh.ButtonHandler.getInstance()
    tm.Texture.getInstance()
    #bh.ButtonHandler.getInstance().get_new_button("1")
    hand_detector = Hd.handDetector()
    ap.AudioPlayer.getInstance()
    cap = cv2.VideoCapture(0)
    # screen cannot be extended for values higher than camera provides
    # cap.set(3, WIN_WIDTH)
    # cap.set(4, WIN_HEIGHT)
    # timers to fix fps with respect to time
    fps_timer_1 = time.time()
    fps_timer_2 = 0
    # timers to fix game logic with respect to time
    logic_timer_1 = time.time()
    logic_timer_2 = 0



    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands = hand_detector.findHands(img)

        scene_1(img)

        hand_buttons.clear()
        for hand in hands:
            hand_buttons.extend(utils.get_button_from_hand(hand))
            print(utils.get_hand_type(hand))

        if logic_timer_1 - logic_timer_2 > LOGIC_DELAY:
            h, w, c = img.shape

            for button in buttons:
                for hand in hand_buttons:
                    if button.collisionWithButtonDetect(hand):
                        #ap.AudioPlayer.getInstance().playSound("1")
                        #img = button.action(img)
                        pass

                button.dynamic_action(h, w)
                if button.is_destroyed:
                    buttons.remove(button)

            logic_timer_2 = time.time()
        else:
            #time.sleep(0.001)
            logic_timer_1 = time.time()

        ##### Drawing ######

        if fps_timer_1 - fps_timer_2 > FPS_DELAY:
            img = hand_detector.drawHands(img)
            for button in buttons:
                img = button.draw(img)

            for h in hand_buttons:
                img = h.draw(img)

            cv2.imshow("Image", img)
            fps_timer_2 = time.time()
        else:
            #time.sleep(0.001)
            fps_timer_1 = time.time()


        cv2.waitKey(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

