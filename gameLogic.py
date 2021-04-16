import cvButton
import audioPlayer as ap
import buttonHandler as bh
import utils
import textureManager as tm

class Game:
    def __init__(self):

        self.buttons = []
        self.hand_buttons = []
        self.scene_act = 0

    def set_hands(self, hand_buttons):
        self.hand_buttons = hand_buttons

    def game_logic(self, img):

        self.scene_1(img)

        h, w, c = img.shape
        for button in self.buttons:
            for hand in self.hand_buttons:
                if button.collisionWithButtonDetect(hand):
                    # ap.AudioPlayer.getInstance().playSound("1")
                    # img = button.action(img)
                    pass
            button.dynamic_action(h, w)
            if button.is_destroyed:
                self.buttons.remove(button)

    def draw(self, img):
        for button in self.buttons:
            img = button.draw(img)
        for h in self.hand_buttons:
            img = h.draw(img)
        return img

    def scene_1(self, img):

        if self.scene_act == 0:
            self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("kich_head"))
            self.scene_act += 2
        if self.scene_act == 1:
            destroyable_buttons_cnt = 0
            for b in self.buttons:
                if b.is_destroyable():
                    destroyable_buttons_cnt += 1
            required_buttons = 50
            if destroyable_buttons_cnt < int(0.15 * required_buttons):
                h, w, c = img.shape
                spawn_area = (int(w * 0.1), int(h * 0.1),
                              int(w * 0.9), int(h * 0.9))
                # for i in range(required_buttons):
                #     #pass
                #     buttons.append(bh.ButtonHandler.getInstance().
                #                   spawn_in_random_place("test_destroyable_button", spawn_area))
                button_list = ["red_circle", "blue_circle", "green_rect", "star"]
                self.buttons.extend(bh.ButtonHandler.getInstance().
                               spawn_random_from_list_random_place(button_list,
                                                                   required_buttons, spawn_area))
