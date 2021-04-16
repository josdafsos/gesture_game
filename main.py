import cv2
import handDetection as Hd
import cvButton
import time
import audioPlayer as ap
import buttonHandler as bh
import utils
import textureManager as tm
import gameLogic

FINGER_RADIUS = 7
LOGIC_DELAY = 0.001
FPS_DELAY = 0.005
#WIN_HEIGHT = 720
#WIN_WIDTH = 900

buttons = []
hand_buttons = []
# to check which subact in each scene is happening
scene_act = 0



def main():
    # TODO two finger connect to cause wave
    # TODO scene class with health bar and other staff, check if hands on the screen
    # TODO lambda for upload attributes

    bh.ButtonHandler.getInstance()
    tm.Texture.getInstance()
    hand_detector = Hd.handDetector()
    ap.AudioPlayer.getInstance()
    game = gameLogic.Game()
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

        #scene_1(img)

        hand_buttons.clear()
        for hand in hands:
            hand_buttons.extend(utils.get_button_from_hand(hand))
        game.set_hands(hand_buttons)

        if logic_timer_1 - logic_timer_2 > LOGIC_DELAY:
            game.game_logic(img)
            logic_timer_2 = time.time()
        else:
            #time.sleep(0.001)
            logic_timer_1 = time.time()

        ##### Drawing ######
        if fps_timer_1 - fps_timer_2 > FPS_DELAY:
            img = hand_detector.drawHands(img)
            img = game.draw(img)
            cv2.imshow("Image", img)
            fps_timer_2 = time.time()
        else:
            #time.sleep(0.001)
            fps_timer_1 = time.time()


        cv2.waitKey(1)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

