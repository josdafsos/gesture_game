import cvButton
import audioPlayer as ap
import buttonHandler as bh
import utils
import textureManager as tm
import cv2

class Game:
    # TODO hp function + drawing

    def __init__(self, win_width, win_height):

        self.buttons = []
        self.hand_buttons = []
        self.scene_act = 0
        self.scene_list = [self.intro_scene, self.scene_1, self.intro_scene]
        self.current_scene = 0
        self.win_width = win_width
        self.win_height = win_height
        self.kill_counter = 0
        self.hp = -1
        self.max_hp = 10
        self.game_status = "game"

    def set_hands(self, hand_buttons):
        self.hand_buttons = hand_buttons

    def game_logic(self, img):

        h, w, c = img.shape
        for button in self.buttons:
            for hand in self.hand_buttons:
                if button.collisionWithButtonDetect(hand):
                    # ap.AudioPlayer.getInstance().playSound("1")
                    # img = button.action(img)
                    pass
            button.dynamic_action(h, w)
        if self.game_status == "game":
            img = self.scene_list[self.current_scene](img)
        elif self.game_status == "loose":
            img = self.loose_scene(img)

        for button in self.buttons:
            if button.is_destroyed:
                self.buttons.remove(button)
        for hand in self.hand_buttons:
            if hand.is_destroyed:
                self.hp -= 1
        return img

    def next_scene(self):
        self.restart_scene_parameters()
        self.current_scene += 1

    def restart_scene_parameters(self):
        self.scene_act = 0
        self.kill_counter = 0
        self.buttons.clear()
        self.hp = -1

    def draw(self, img):
        if self.hp > 0:
            startPoint = (self.win_width - self.hp * 20, 0)
            endPoint = (self.win_width, 40)
            img = cv2.rectangle(img, startPoint, endPoint, (80, 80, 230), -1)
            img = cv2.putText(img, "HP", ((self.win_width - self.hp * 12), 25),
                              cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 120, 120), 2)
        for button in self.buttons:
            img = button.draw(img)
        for h in self.hand_buttons:
            img = h.draw(img)
        return img

    def scene_1(self, img):

        # if self.scene_act == 0:
        #     self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("kich_head_random"))
        #     self.scene_act += 2
        if self.scene_act == 0:
            self.hp = self.max_hp
            self.scene_act += 1
        elif self.scene_act == 1:
            if self.hp <= 0:
                self.defeat()
                return img

            destroyable_buttons_cnt = 0
            for b in self.buttons:
                if b.is_destroyable():
                    destroyable_buttons_cnt += 1
            required_buttons = 15
            if destroyable_buttons_cnt < int(0.15 * required_buttons):

                spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                              int(self.win_width * 0.9), int(self.win_height * 0.9))
                button_list = ["kich_naked_random", "kich_head"]
                self.buttons.extend(bh.ButtonHandler.getInstance().
                               spawn_random_from_list_random_place(button_list,
                                                                   required_buttons, spawn_area))
            for b in self.buttons:
                if b.id == "kich_naked_random" and b.is_destroyed:
                    self.kill_counter += 1
            if self.kill_counter > 30:
                self.next_scene()
                ap.AudioPlayer.getInstance().play_random_from_list(["success_nakroem"])
            hint = "Kill %s naked Kich'es using fists" % (30)
            img = cv2.putText(img, hint, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
            hint = "Kich'es killed %s" % (self.kill_counter)
            img = cv2.putText(img, hint, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
            hint = "Avoid fisting Kich heads"
            img = cv2.putText(img, hint, (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
            hint = "Destroy Kich heads with palms"
            img = cv2.putText(img, hint, (10, 110), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
        return img

    def defeat(self):
        self.restart_scene_parameters()
        self.game_status = "loose"
        ap.AudioPlayer.getInstance().play_random_from_list(["end_driver_stop"])


    def intro_scene(self, img):
        img = tm.Texture.getInstance().get_resized_texture("intro", self.win_width,
                                                           self.win_height)
        if self.scene_act == 0:
            #self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.scene_act += 1

        if len(self.buttons) == 0:
            self.next_scene()
            ap.AudioPlayer.getInstance()\
                .play_random_from_list(["start_black_ass", "start_mexican"])
        cv2.putText(img, 'Use your hands to control', (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Keep at least one hand on the screen', (10, 45), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Press "start" to continue', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)

        return img

    def loose_scene(self, img):
        img = tm.Texture.getInstance().get_resized_texture("intro", self.win_width,
                                                           self.win_height)
        if self.scene_act == 0:
            #self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.scene_act += 1

        if len(self.buttons) == 0:
            self.restart_scene_parameters()
            self.game_status = "game"
        cv2.putText(img, 'You lost', (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Next time be more careful with KICH', (10, 45), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Press "start" to try once again', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)

        return img
