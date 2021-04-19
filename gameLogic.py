import cvButton
import audioPlayer as ap
import buttonHandler as bh
import utils
import textureManager as tm
import cv2
import time
import random
from copy import deepcopy

class Game:

    def __init__(self, win_width, win_height):
        # TODO harder level with basketball and damaging objects
        self.buttons = []
        self.hand_buttons = []
        self.special_buttons = []
        self.scene_act = 0
        self.scene_list = [self.scene_tutorial, self.scene_1,
                           self.scene_2, self.boss_fight]
        self.descritpion_list = [self.description_1, self.description_2,
                                 self.description_3, self.description_4]
        self.current_scene = -1 # by default -1, 2 - boss
        self.win_width = win_width
        self.win_height = win_height
        self.kill_counter = 0
        self.hp = -1
        self.max_hp = 10
        self.game_status = "menu"
        self.timer_1 = 0
        self.timer_2 = 0

        self.difficulty = 1

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
            for s in self.special_buttons:
                if button.collisionWithButtonDetect(s):
                    pass
            button.dynamic_action(h, w)
        if self.game_status == "game":
            img = self.scene_list[self.current_scene](img)
        elif self.game_status == "loose":
            img = self.loose_scene(img)
        elif self.game_status == "menu":
            img = self.menu_scene(img)
        elif self.game_status == "victory":
            img = self.victory_screen(img)

        for button in self.buttons:
            if button.is_destroyed:
                for to_spawn in button.check_spawn_on_death():
                    new_button = bh.ButtonHandler.getInstance()\
                        .get_new_button(to_spawn)
                    new_button.x = button.x + random.randint(-button.width//2,
                                                             button.width//2)
                    new_button.y = button.y + random.randint(-button.height//2,
                                                             button.height//2)
                    self.buttons.append(new_button)
                self.buttons.remove(button)
        for hand in self.hand_buttons:
            if hand.is_destroyed:
                self.hp -= 1
        for s in self.special_buttons:
            s.dynamic_action(h, w)
            if s.is_destroyed:
                self.special_buttons.remove(s)
        return img

    def next_scene(self):
        self.restart_scene_parameters()
        if self.game_status == "game":
            self.game_status = "menu"
        else:
            self.game_status = "game"
            self.current_scene += 1

    def restart_scene_parameters(self):
        self.scene_act = 0
        self.kill_counter = 0
        self.buttons.clear()
        self.special_buttons.clear()
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
        for s in self.special_buttons:
            img = s.draw(img)
        return img

    def scene_tutorial(self, img):

        if self.scene_act == 0:
            self.scene_act += 1
            self.special_buttons.append(bh.ButtonHandler.getInstance().get_new_button("basket"))
            spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                          int(self.win_width * 0.9), int(self.win_height * 0.9))
            top_spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                          int(self.win_width * 0.9), int(self.win_height * 0.3))
            bottom_spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.7),
                          int(self.win_width * 0.9), int(self.win_height * 0.9))
            if self.difficulty == 0:
                balls_to_spawn = 1 # by default = 5
            else:
                balls_to_spawn = 5
            self.buttons.extend(bh.ButtonHandler.getInstance().
                                spawn_random_from_list_random_place(["blue_basket_ball"],
                                                                    balls_to_spawn + 1,
                                                                    spawn_area))
            self.buttons.extend(bh.ButtonHandler.getInstance().
                                spawn_random_from_list_random_place(["red_basket_ball_inversed"],
                                                                    balls_to_spawn,
                                                                    top_spawn_area))
            self.buttons.extend(bh.ButtonHandler.getInstance().
                                spawn_random_from_list_random_place(["red_basket_ball"],
                                                                    balls_to_spawn,
                                                                    bottom_spawn_area))
        else:
            if len(self.buttons) <= 0:
                self.next_scene()

        text = ["let's start from something simple", "Destroy blue balls using fists",
                "put other balls into the basket"]
        self.draw_corner_text(img, text)


        return img

    def scene_1(self, img):

        if self.scene_act == 0:
            self.hp = self.max_hp
            self.scene_act += 1
        elif self.scene_act == 1:
            if self.hp <= 0:
                self.defeat()
                return img
            destroyable_buttons_cnt = 0
            for b in self.buttons:
                if b.is_destroyable(): destroyable_buttons_cnt += 1
            required_buttons = 10
            if destroyable_buttons_cnt < int(0.3 * required_buttons):
                spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                              int(self.win_width * 0.9), int(self.win_height * 0.9))
                button_list = ["kich_naked_random", "kich_head"]
                self.buttons.extend(bh.ButtonHandler.getInstance().
                               spawn_random_from_list_random_place(button_list,
                                                                   required_buttons, spawn_area))
            for b in self.buttons:
                if b.id == "kich_naked_random" and b.is_destroyed: self.kill_counter += 1
            if self.difficulty == 0:
                units_to_kill = 5
            else:
                units_to_kill = 19
            if self.kill_counter >= units_to_kill:
                self.next_scene()
                ap.AudioPlayer.getInstance().play_random_from_list(["success_nakroem"])
                return img
            hint = "Collect %s naked Kich'es using fists" % (units_to_kill - self.kill_counter)
            img = cv2.putText(img, hint, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
            hint = "Avoid fisting Kich heads"
            img = cv2.putText(img, hint, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
            hint = "Clear Kich heads with palms"
            img = cv2.putText(img, hint, (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                              0.7, (255, 255, 255), 2)
        return img

    def scene_2(self, img):

        if self.scene_act == 0:
            self.hp = self.max_hp
            self.scene_act += 1
            self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("touch_here"))

        elif self.scene_act == 1:
            if len(self.buttons) == 0:
                self.scene_act += 1
                self.timer_2 = time.time()
            text_list = ["Keep at least one hand on the screen",
                         "Or you will lose HP!",
                         "Try to survive for as long as possible",
                         "Don't touch anything, except for this button"]
            self.draw_corner_text(img, text_list)
        elif self.scene_act == 2:
            spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                          int(self.win_width * 0.9), int(self.win_height * 0.9))

            # self.buttons.extend(bh.ButtonHandler.getInstance()
            #                     .spawn_behind_scene("misha_chaser", 5,
            #                                         "random", (self.win_width, self.win_height)))
            # self.buttons.extend(bh.ButtonHandler.getInstance()
            #                     .spawn_behind_scene("red_ball_chaser", 5,
            #                                         "random", (self.win_width, self.win_height)))
            self.buttons.extend(bh.ButtonHandler.getInstance().
                                spawn_random_from_list_random_place(["misha_chaser"],
                                                                    3, spawn_area))
            self.buttons.extend(bh.ButtonHandler.getInstance().
                                spawn_random_from_list_random_place(["red_ball_chaser"],
                                                                    3, spawn_area))
            self.scene_act += 1
        elif self.scene_act == 3:
            if len(self.hand_buttons) == 0:
                self.timer_1 = time.time()
                if self.timer_1 - self.timer_2 > 0.5:
                    self.timer_2 = time.time()
                    self.hp -= 1
            if len(self.buttons) == 0:
                self.next_scene()
                return img

            text_list = ["Keep at least one hand on the screen",
                         "Avoid them!",
                         "Switch between palm and fist!"]
            for h in self.hand_buttons:
                chasing_speed = 7
                repelling_speed = -1
                if h.id == "fist_hand":
                    for b in self.buttons:
                        if b.id == "red_ball_chaser":
                            if b.x > h.x:
                                b.x_speed -= chasing_speed
                            if b.x < h.x:
                                b.x_speed += chasing_speed
                            if b.y > h.y:
                                b.y_speed -= chasing_speed
                            if b.y < h.y:
                                b.y_speed += chasing_speed
                        if b.id == "misha_chaser":
                            chasing_speed = 3
                            if b.x > h.x:
                                b.x_speed -= repelling_speed
                            if b.x < h.x:
                                b.x_speed += repelling_speed
                            if b.y > h.y:
                                b.y_speed -= repelling_speed
                            if b.y < h.y:
                                b.y_speed += repelling_speed
                if h.id == "palm_ring_f":
                    for b in self.buttons:
                        if b.id == "misha_chaser":
                            if b.x > h.x:
                                b.x_speed -= chasing_speed
                            if b.x < h.x:
                                b.x_speed += chasing_speed
                            if b.y > h.y:
                                b.y_speed -= chasing_speed
                            if b.y < h.y:
                                b.y_speed += chasing_speed
                        if b.id == "red_ball_chaser":
                            chasing_speed = 3
                            if b.x > h.x:
                                b.x_speed -= repelling_speed
                            if b.x < h.x:
                                b.x_speed += repelling_speed
                            if b.y > h.y:
                                b.y_speed -= repelling_speed
                            if b.y < h.y:
                                b.y_speed += repelling_speed

            enemies_alive = len(list(filter(lambda x: x.id =='misha_chaser'
                                                      or x.id =='red_ball_chaser',
                                            self.buttons)))
            hint = "Enemies alive %s" % enemies_alive
            cv2.putText(img, hint, (int(self.win_width * 0.45), int(self.win_height * 0.3)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (20, 20, 255), 3)
            self.draw_corner_text(img, text_list)

        if self.hp <= 0:
            self.defeat()
            return img

        return img

    def defeat(self):
        self.restart_scene_parameters()
        self.game_status = "loose"
        ap.AudioPlayer.getInstance()\
            .play_random_from_list(["end_driver_stop", "end_Kich_VseStop",
                                    "end_panna_poslashe", "end_panna_ti"])

    def menu_scene(self, img):
        img = tm.Texture.getInstance().get_resized_texture("intro", self.win_width,
                                                            self.win_height)
        if self.scene_act == 0:
            self.buttons.append(bh.ButtonHandler.getInstance()
                                .get_new_button("start"))
            self.scene_act += 1
        elif self.scene_act == 1:
            if len(self.buttons) == 0:
                self.buttons.append(bh.ButtonHandler.getInstance()
                                    .get_new_button("start_for_sure"))
                self.scene_act += 1
        else:
            if len(self.buttons) == 0:
                self.next_scene()
                #self.restart_scene_parameters()
                #self.game_status = "game"
                ap.AudioPlayer.getInstance()\
                    .play_random_from_list(["start_black_ass", "start_mexican",
                                            "start_panna_budes"])
                return img

        img = self.descritpion_list[self.current_scene+1](img)

        return img

    def loose_scene(self, img):
        if self.current_scene < 2:
            img = tm.Texture.getInstance().get_resized_texture("game_over", self.win_width,
                                                               self.win_height)

            cv2.putText(img, 'You lost', (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
            cv2.putText(img, 'Next time be more careful with KICH', (10, 45), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
            cv2.putText(img, 'Press "start" to try once again', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)
        else:
            img = tm.Texture.getInstance().get_resized_texture("lose_boss", self.win_width,
                                                               self.win_height)

        if self.scene_act == 0:
            #self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.buttons.append(bh.ButtonHandler.getInstance().get_new_button("start"))
            self.scene_act += 1
        if self.scene_act == 1:
            if len(self.buttons) == 0:
                self.restart_scene_parameters()
                self.game_status = "game"

        return img
    def description_1(self, img):
        cv2.putText(img, 'Use your hands to control', (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Keep at least one hand on the screen', (10, 45), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        cv2.putText(img, 'Press "start" to continue', (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)
        hint = "Round %s" % (self.current_scene + 2)
        cv2.putText(img, hint, (int(self.win_width*0.45), int(self.win_height*0.3)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (20, 20, 255), 3)
        return img
    def description_2(self, img):
        text = ["Good job, the first round is done", "But KICH needs your help",
                "And it is just a beginning..."]
        self.draw_corner_text(img, text)
        hint = "Round %s" % (self.current_scene + 2)
        cv2.putText(img, hint, (int(self.win_width*0.45), int(self.win_height*0.3)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (20, 20, 255), 3)
        return img
    def description_3(self, img):
        text = ["Okay, okay!", "KICH seems to be stronger than we though", "You must continue!"]
        self.draw_corner_text(img, text)
        hint = "Round %s" % (self.current_scene + 2)
        cv2.putText(img, hint, (int(self.win_width*0.45), int(self.win_height*0.3)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (20, 20, 255), 3)
        return img
    def description_4(self, img):
        text = ["Wait! do you hear that?",
                "Evil Grisha is coming",
                "Hurry up we have to save KICH"]
        self.draw_corner_text(img, text)
        hint = "Round %s" % (self.current_scene + 2)
        cv2.putText(img, hint, (int(self.win_width*0.45), int(self.win_height*0.3)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (20, 20, 255), 3)
        return img
    def draw_corner_text(self, img, text_list):
        for i in range(0, len(text_list)):
            cv2.putText(img, text_list[i], (10, 20 + 25*i), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)

    def boss_fight(self, img):
        # stage one throw balls into grisha, panna heads fly
        # stage two protect kich, grisha is moving towards him
        # stage three battle with grisha, his is on the bottom throwing something into
        # player, player must destroy panna - guards, spawning in front

        #### stage 1

        if self.scene_act == 0:
            self.boss_1_act_1(img)
            self.scene_act += 1
        elif self.scene_act == 1:
            if len(self.buttons) == 0:
                ap.AudioPlayer.getInstance().play_random_from_list(["grisha_1"])
                self.scene_act += 1
            text = ["Grisha with his faithful", "guards wants to attack KICH",
                    "Stop him at any cost!",
                    "Shoot from you hands"]
            self.draw_corner_text(img, text)
        elif self.scene_act == 2:
            if len(self.special_buttons) == 0:
                self.scene_act += 1
                ap.AudioPlayer.getInstance().play_random_from_list(["panna_krutoi_1"])
                touch_here = bh.ButtonHandler.getInstance().get_new_button("touch_here")
                self.buttons.clear()
                touch_here.x = int(0.6 * self.win_width)
                touch_here.y = int(0.2 * self.win_height)
                self.buttons.append(touch_here)
            img = self.boss_1_act_2(img)
        elif self.scene_act == 3:
            if len(self.buttons) == 0:
                self.scene_act += 1
                ap.AudioPlayer.getInstance().play_random_from_list(["grisha_2"])
                self.special_buttons.append(bh.ButtonHandler
                                    .getInstance().get_new_button("grisha_boss_1_2"))
                self.buttons.append(bh.ButtonHandler
                                    .getInstance().get_new_button("kich_boss_1_2"))
                text = ["Grisha has started transformation!",
                        "His is chasing KICH to make him trap",
                        "Push KICH away from Grisha"]
                self.draw_corner_text(img, text)
        elif self.scene_act == 4:
            img = self.boss_1_act_3(img)

        elif self.scene_act == 5:
            if len(self.buttons) == 0:
                ap.AudioPlayer.getInstance().play_random_from_list(["grisha_3"])
                self.scene_act += 1
            text = ["Grisha is attracting Vlads", "to turn into supreme Shluha",
                    "and get KICH!",
                    "Last push, SHOOT!"]
            self.draw_corner_text(img, text)
        elif self.scene_act == 6:
            grisha = bh.ButtonHandler.getInstance().get_new_button("grisha_boss_1_3")
            grisha.x = self.win_width//2
            self.special_buttons.append(grisha)

            self.scene_act += 1
        elif self.scene_act == 7:
            img = self.boss_1_act_4(img)

        return img

    def boss_1_act_1(self, img):
        self.hp = int(1.2 * self.max_hp)
        grisha = bh.ButtonHandler.getInstance().get_new_button("grisha_1")
        self.special_buttons.append(grisha)
        vlad = bh.ButtonHandler.getInstance().get_new_button("panna_guard")
        vlad.x = grisha.x + grisha.width
        vlad.y = grisha.y
        self.special_buttons.append(deepcopy(vlad))
        vlad.x = grisha.x
        vlad.y = grisha.y - int(grisha.height * 0.7)
        self.special_buttons.append(deepcopy(vlad))
        vlad.x = grisha.x + grisha.width
        vlad.y = grisha.y - int(grisha.height * 0.7)
        self.special_buttons.append(deepcopy(vlad))

        touch_here = bh.ButtonHandler.getInstance().get_new_button("touch_here")
        touch_here.x = int(0.6 * self.win_width)
        touch_here.y = int(0.3 * self.win_height)
        self.buttons.append(touch_here)

    def boss_1_act_2(self, img):
        # if random.randint(0, 6) <= 1:
        #     bullet = bh.ButtonHandler.getInstance()\
        #         .spawn_behind_scene( "blue_circle_bullet", 1,
        #                              "left", (self.win_width, self.win_height))[0]
        #     bullet.y = random.randint(0, int(self.win_height * 0.45))
        #     self.buttons.append(bullet)
        chasing_speed = 2
        for hand in self.hand_buttons:
            if hand.id == "fist_hand" and random.randint(0, 7) <= 1:
                bullet = bh.ButtonHandler \
                    .getInstance().get_new_button("yellow_finger_bullet")
                bullet.x = hand.x - int(hand.width * 1.1)
                bullet.y = hand.y - hand.height // 2
                self.buttons.append(bullet)
            elif hand.id == "palm_index_f" and random.randint(0, 7) <= 1:
                bullet = bh.ButtonHandler \
                    .getInstance().get_new_button("blue_finger_bullet")
                bullet.y = hand.y - int(hand.height * 0.8)
                bullet.x = hand.x
                self.buttons.append(bullet)
            for b in self.buttons:
                if b.id == "grisha_panna_bullet":
                    if b.x > hand.x:
                        b.x_speed -= chasing_speed
                    if b.x < hand.x:
                        b.x_speed += chasing_speed
                    if b.y > hand.y:
                        b.y_speed -= chasing_speed
                    if b.y < hand.y:
                        b.y_speed += chasing_speed
        if self.hp <= 0:
            self.defeat()
            return img

        for s in self.special_buttons:
            if s.id == "panna_guard":
                if random.randint(0, 80) <= 1:
                    ap.AudioPlayer.getInstance()\
                        .play_random_from_list(["panna_ne_popadaui_1"])
                if s.is_destroyed:
                    ap.AudioPlayer.getInstance().play_random_from_list(["panna_tvar_1"])
            if random.randint(0, 31) <= 1:
                bullet = bh.ButtonHandler \
                    .getInstance().get_new_button("grisha_panna_bullet")
                bullet.y = s.y
                bullet.x = s.x
                self.buttons.append(bullet)

        text = ["Shoot at them!",
                "Palm - shoot blue bullets",
                "Fist - shoot yellow bullets"]
        self.draw_corner_text(img, text)

        return img

    def boss_1_act_3(self, img):
        text = ["Grisha has started transformation!",
                "His is chasing KICH to make him trap",
                "Push KICH away from Grisha"]
        self.draw_corner_text(img, text)
        chasing_speed = 1
        for k in self.buttons:
            if k.id == "kich_boss_1_2":
                for g in self.special_buttons:
                    if g.id == "grisha_boss_1_2":
                        if g.x > k.x:
                            g.x_speed -= chasing_speed
                        if g.x < k.x:
                            g.x_speed += chasing_speed
                        if g.y > k.y:
                            g.y_speed -= chasing_speed
                        if g.y < k.y:
                            g.y_speed += chasing_speed
                if k.is_destroyed:
                    self.hp -= 1
                    spawn_area = (int(self.win_width * 0.1), int(self.win_height * 0.1),
                                  int(self.win_width * 0.9), int(self.win_height * 0.9))
                    self.buttons.extend(bh.ButtonHandler.getInstance().
                                        spawn_random_from_list_random_place(["kich_boss_1_2"],
                                                                            1, spawn_area))

                    ap.AudioPlayer.getInstance().play_random_from_list(["grisha_catch_2"])

        if self.hp <= 0:
            self.defeat()
            return img
        if len(self.special_buttons) == 0:
            self.scene_act += 1
            self.buttons.clear()
            self.special_buttons.clear()
            self.hp = self.max_hp
            ap.AudioPlayer.getInstance().play_random_from_list(["grisha_fail_2"])
            touch_here = bh.ButtonHandler.getInstance().get_new_button("touch_here")
            touch_here.x = int(0.6 * self.win_width)
            touch_here.y = int(0.8 * self.win_height)
            self.buttons.append(touch_here)

        return img

    def boss_1_act_4(self, img):
        if random.randint(0, 12) <= 1:
            direction = random.randint(0, 3)
            panna = bh.ButtonHandler.getInstance()\
                .get_new_button("panna_3")
            panna.x = self.win_width // 2
            panna.y = self.win_height + panna.height
            if direction == 0:
                panna.x = -int(0.1*self.win_width)
                panna.y = self.win_height // 2
            elif direction == 1:
                panna.x = int(1.1*self.win_width)
                panna.y = self.win_height // 2
            self.buttons.append(panna)
        chasing_speed = 3
        for k in self.special_buttons:
            if k.id == "grisha_boss_1_3":
                for g in self.buttons:
                    if g.id == "panna_3":
                        if g.x > k.x:
                            g.x_speed -= chasing_speed
                        if g.x < k.x:
                            g.x_speed += chasing_speed
                        if g.y > k.y:
                            g.y_speed -= chasing_speed
                        if g.y < k.y:
                            g.y_speed += chasing_speed
        if random.randint(0, 22) <= 1:
            bullet = bh.ButtonHandler \
                .getInstance().get_new_button("grisha_panna_bullet")
            bullet.y = int(0.1*self.win_height)
            bullet.x = self.win_width//2
            self.buttons.append(bullet)
        for hand in self.hand_buttons:
            if random.randint(0, 7) <= 1:
                bullet = bh.ButtonHandler \
                    .getInstance().get_new_button("boss_3_finger_bullet")
                bullet.x = hand.x
                bullet.y = hand.y - hand.height // 2
                self.buttons.append(bullet)
            for b in self.buttons:
                if b.id == "grisha_panna_bullet":
                    if b.x > hand.x:
                        b.x_speed -= chasing_speed
                    if b.x < hand.x:
                        b.x_speed += chasing_speed
                    if b.y > hand.y:
                        b.y_speed -= chasing_speed
                    if b.y < hand.y:
                        b.y_speed += chasing_speed

        if self.hp <= 0:
            self.defeat()
            return img

        if len(self.special_buttons) == 0:
            self.restart_scene_parameters()
            self.game_status = "victory"
            ap.AudioPlayer.getInstance().play_random_from_list(["grisha_fail_3"])

        text = ["Grisha has started transformation!",
                "His is chasing KICH to make him trap",
                "Push KICH away from Grisha"]
        self.draw_corner_text(img, text)

        return img


    def victory_screen(self, img):
        img = tm.Texture.getInstance().get_resized_texture("victory", self.win_width,
                                                            self.win_height)
        text_list = ["You have made it!", "KICH is saved",
                     "But be sure that eveil Grisha", "and other guys will return..."]
        for i in range(0, len(text_list)):
            cv2.putText(img, text_list[i],
                        (int(self.win_width*0.5), 20 + 25*i),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 255), 2)

        return img

