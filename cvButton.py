import cv2
import math

class Button:
    def __init__(self, x, y, button_type, id, shape, width=50, height=80):
        # Note: width is also used as a radius in case of circular shape
        self.x = x
        self.y = y
        self.shape = shape
        self.width = width
        self.height = height
        self.button_type = button_type
        self.id = id
        self.is_triggered = False

    def draw(self, img):
        if self.shape == "rectangle":
            startPoint = (self.x - self.width//2, self.y - self.height//2)
            endPoint = (self.x + self.width//2, self.y + self.height//2)
            img = cv2.rectangle(img, startPoint, endPoint, (120, 100, 0), 2)
        else:
            img = cv2.circle(img,(self.x,self.y),self.width,(40,200,120),-1)
        return img
    def collisionDetect(self, coords, obj_width, obj_height):
        self.is_triggered = self.x - self.width//2 < coords[0] < self.x + self.width//2 and \
            self.y - self.height//2 < coords[1] < self.y + self.height//2
        return self.is_triggered
    def isTriggered(self):
        return self.is_triggered
    def unTrigger(self):
        self.is_triggered = False
    def action(self, img):
        return cv2.circle(img,(self.x,self.y),5,(255,0,0),-1)

    def dynamic_action(self, top_y, right_x):
        # action that happens every cycle
        pass


class DynamicButton(Button):

    def __init__(self, x, y, button_type, id, shape, width=50, height=80):
        super().__init__(x, y, button_type, id, shape, width, height)
        self.max_speed = 300
        self.y_acceleration = 1
        self.x_speed = 0
        self.y_speed = 0

    def collisionDetect(self, coords, obj_width, obj_height):
        #right now assume that everything is circle
        #TODO add collision with other object types
        d = math.hypot(self.x-coords[0],self.y-coords[1])
        if(d < self.width + obj_width):
            self.is_triggered = True
            delta = self.width + obj_width - d
            self.x_speed = int(delta * (self.y - coords[1])*0.8 - self.x_speed * 0.2)
            self.y_speed = int(delta * (self.x - coords[0])*0.8 - self.y_speed * 0.2)
        else:
            self.is_triggered = False
        return self.is_triggered

    def dynamic_action(self, top_y, right_x):
        self.y_speed += self.y_acceleration
        if self.x_speed ** 2 + self.y_speed ** 2 > self.max_speed:
            #dividor_y = self.y_speed * math.fabs(self.y_speed) // (self.x_speed**2 + self.y_speed**2)
            #dividor_x = self.x_speed * math.fabs(self.x_speed) // (self.x_speed**2 + self.y_speed**2)
            #self.y_speed = int(dividor_y * self.max_speed * 0.9)
            #self.x_speed = int(dividor_x * self.max_speed * 0.9)
            self.y_speed = int(0.8*self.y_speed)
            self.x_speed = int(0.8 * self.x_speed)
            #print("dividor y = ", dividor_y)
            #print("y speed = ", self.y_speed)
            #print("x speed = ", self.x_speed)

        self.x += self.x_speed
        self.y += self.y_speed

        # window border detection
        if self.x-self.width//2 < 0 or self.x+self.width//2 > right_x:
            self.x_speed *= -1
            self.x += self.x_speed
            self.x_speed = int(self.x_speed*0.9)
        if self.y-self.height//2 < 0 or self.y+self.height//2 > top_y:
            self.y_speed *= -1
            self.y += self.y_speed
            self.y_speed = int(self.y_speed*0.9)

