import cv2
import math
import textureManager as tm
import random

class Button:
    def __init__(self, x, y, button_type, id, shape, color, line_thickness,
                 attributes, width=50, height=80):
        # Note: width is also used as a radius in case of circular shape
        self.x = x
        self.y = y
        self.shape = shape
        self.width = width
        self.height = height
        self.button_type = button_type
        self.id = id
        self.is_triggered = False
        self.is_destroyed = False
        self.attributes = attributes
        self.color = color
        self.line_thickness = line_thickness

    def draw(self, img):
        texture_id = self.attributes.get("texture")
        if not (texture_id is None):
            img = self.merge_images(img, texture_id)
        elif self.shape == "rectangle":
            startPoint = (self.x - self.width//2, self.y - self.height//2)
            endPoint = (self.x + self.width//2, self.y + self.height//2)
            img = cv2.rectangle(img, startPoint, endPoint, self.color, self.line_thickness)
        else:
            img = cv2.circle(img,(self.x,self.y),self.width,self.color,self.line_thickness)
        return img
    def collisionDetect(self, coords, obj_width, obj_height):
        self.is_triggered = self.x - self.width//2 < coords[0] < self.x + self.width//2 and \
            self.y - self.height//2 < coords[1] < self.y + self.height//2
        return self.is_triggered
    def collisionWithButtonDetect(self, button):
    #Note, circle - rect collision works as rect -rect collision
        if self.getShape() == "circle":
            if button.getShape() == "circle":
                self.is_triggered = self.circleCircleCollisionDetect(button)
            elif button.getShape() == "rectangle":
                self.is_triggered = self.rectRectCollisionDetect(button)
        elif self.getShape() == "rectangle":
            self.is_triggered = self.rectRectCollisionDetect(button)
        if self.is_triggered:
            self.on_collision_action(button)
        if self.is_triggered:
            self.check_destroy_by_button(button)
            button.check_destroy_by_button(self)
        return self.is_triggered

    def circleCircleCollisionDetect(self, button):
        return math.hypot(self.x-button.x, self.y-button.y) <= self.width + button.width
    def rectRectCollisionDetect(self, button):
        return math.fabs(self.x - button.x) < self.width/2 + button.width/2 and \
                math.fabs(self.y - button.y) < self.height/2 + button.height/2

    def isTriggered(self):
        return self.is_triggered
    def unTrigger(self):
        self.is_triggered = False
    def action(self, img):
        return cv2.circle(img,(self.x,self.y),5,(255,0,0),-1)

    def dynamic_action(self, top_y, right_x):
        if not (self.attributes is None):
            self.check_life_time()

    def set_coords(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    def set_button_type(self, button_type):
        self.button_type = button_type
    def getShape(self):
        return self.shape

    def on_collision_action(self, button):
        pass

    def check_destroy_by_button(self, button):

        destroyable_by = self.attributes.get("destroyable_by")
        if not (destroyable_by is None):
            for d in destroyable_by:
                if d == button.id:
                    self.is_destroyed = True

    def is_destroyable(self):
        return not (self.attributes.get("destroyable_by") is None)

    def merge_images(self, img, texture_id):
        #texture = tm.Texture.getInstance()\
        #    .get_resized_texture(texture_id, self.width, self.height)
        texture = self.attributes.get("texture")
        img_height = img.shape[0]
        img_width = img.shape[1]
        texture_height = texture.shape[0]
        texture_width = texture.shape[1]
        min_x = max(0, self.x - texture_width // 2)
        min_y = max(0, self.y - texture_height // 2)
        max_x = min(img_width-1, self.x + texture_width // 2)
        max_y = min(img_height-1, self.y + texture_height // 2)
        transp_color = (0, 0, 0)

        #print("min x: ", min_x, " min y: ", min_y, " max x: ", max_x, " max y: ", max_y)
        for i in range(0, texture_width):
            for j in range(0, texture_height):
                if min_x + i < max_x and j + min_y < max_y:
                    if tuple(texture[j, i, :]) != transp_color:
                        img[min_y+j, min_x+i, :] = texture[j, i, :]
        return img

    def check_life_time(self):
        if not (self.attributes.get("life_time") is None):
            life_time = self.attributes.get("life_time")
            if type(life_time) is list:
                min_time, max_time = self.attributes.get("life_time")
                self.attributes["life_time"] = random.randint(min_time, max_time)
            else:
                self.attributes["life_time"] = life_time - 1
                if life_time <= 0:
                    self.is_destroyed = True

    def check_spawn_on_death(self):
        spawn_buttons_id = []
        if not (self.attributes.get("spawn_on_death") is None):
            spawn_buttons_id = self.attributes.get("spawn_on_death")
        return spawn_buttons_id

class DynamicButton(Button):

    def __init__(self, x, y, button_type, id, shape, color, line_thickness,
                 attributes, width=50, height=80):
        super().__init__(x, y, button_type, id, shape, color, line_thickness,
                         attributes, width, height)
        self.max_speed = 300
        self.y_acceleration = 1
        self.x_speed = 0
        self.y_speed = 0
        self.get_initial_velocity()

    def get_initial_velocity(self):
        if not (self.attributes.get("start_vel_x") is None):
            x_vel = self.attributes.get("start_vel_x")
            if str(x_vel) == "random":
                self.x_speed = random.randint(-int(math.sqrt(self.max_speed)),
                                              int(math.sqrt(self.max_speed)))
            else:
                self.x_speed = int(x_vel * int(math.sqrt(self.max_speed)))
        if not (self.attributes.get("start_vel_y") is None):
            y_vel = self.attributes.get("start_vel_y")
            if str(y_vel) == "random":
                self.y_speed = random.randint(-int(math.sqrt(self.max_speed)),
                                              int(math.sqrt(self.max_speed)))
            else:
                self.y_speed = int(y_vel * int(math.sqrt(self.max_speed)))

    def on_collision_action(self, button):
        if self.attributes.get("collision_bounce") is None:
            delta = self.width + button.width\
                    - math.hypot(self.x-button.x, self.y-button.y)
            self.x_speed = int(delta * (self.y - button.y)*0.8 - self.x_speed * 0.2)
            self.y_speed = int(delta * (self.x - button.x)*0.8 - self.y_speed * 0.2)

    def get_gravitic_acc(self):
        graviti_acc = 0
        if not (self.attributes.get("gravity") is None):
            graviti_acc = self.attributes.get("gravity")
        return graviti_acc

    def get_damping(self):
        damping = 0.9
        if not (self.attributes.get("damping") is None):
            damping = self.attributes.get("damping")
        return damping

    def dynamic_action(self, top_y, right_x):
        #self.y_speed += self.y_acceleration
        self.y_speed += self.get_gravitic_acc()
        if self.x_speed ** 2 + self.y_speed ** 2 > self.max_speed:
            self.y_speed = int(0.8*self.y_speed)
            self.x_speed = int(0.8 * self.x_speed)

        self.x += self.x_speed
        self.y += self.y_speed

        # window border detection
        if self.attributes.get("no_border") is None:
            if self.x-self.width//2 < 0 or self.x+self.width//2 > right_x:
                self.x_speed *= -1
                self.x += self.x_speed
                self.x_speed = int(self.x_speed*self.get_damping())
            if self.y-self.height//2 < 0 or self.y+self.height//2 > top_y:
                self.y_speed *= -1
                self.y += self.y_speed
                self.y_speed = int(self.y_speed*self.get_damping())

        self.check_life_time()
