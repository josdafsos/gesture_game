import cvButton as cb
import json
from copy import deepcopy
import random

class ButtonHandler:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ButtonHandler.__instance == None:
            ButtonHandler()
        return ButtonHandler.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if ButtonHandler.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ButtonHandler.__instance = self
            self.loaded_buttons = {}
            self.upload_buttons("description/buttons.json")

    def upload_buttons(self, file):
        with open(file, "r") as read_file:
            data = json.load(read_file)
        self.parse_button_data(data, "static_buttons")
        self.parse_button_data(data, "dynamic_buttons")

    def parse_button_data(self, data, b_type):
        for i in range(len(data[b_type])):
            x = data[b_type][i]["x"]
            y = data[b_type][i]["y"]
            button_id = str(data[b_type][i]["id"])
            shape = data[b_type][i]["shape"]

            attributes = {"empty": "empty"}
            uploaded_attributes = data[b_type][i].get("attributes")
            if not (uploaded_attributes is None):
                attributes = uploaded_attributes

            color = (120, 120, 120)
            uploaded_color = data[b_type][i].get("color")
            if not (uploaded_color is None):
                color = uploaded_color

            line_thickness = 1
            uploaded_line_thickness = data[b_type][i].get("line_thickness")
            if not (uploaded_line_thickness is None):
                line_thickness = uploaded_line_thickness

            if shape == "rectangle":
                width = data[b_type][i]["width"]
                height = data[b_type][i]["height"]
            else:
                width = data[b_type][i]["radius"]
                height = width
            if b_type == "static_buttons":
                button_type = "static"
                self.loaded_buttons[button_id] = cb.Button(x, y, button_type,
                                                           button_id, shape, color, line_thickness,
                                                           attributes, width, height)
            else:
                button_type = "dynamic"
                self.loaded_buttons[button_id] = cb.DynamicButton(x, y, button_type,
                                                           button_id, shape, color, line_thickness,
                                                           attributes, width, height)

    def get_new_button(self, button_id):
        return deepcopy(self.loaded_buttons[button_id])

    def spawn_in_random_place(self, button_id, spawn_area):
        # spawn area configuration min_x, min_y, max_x, max_y
        button = self.get_new_button(button_id)
        button.x = random.randint(spawn_area[0], spawn_area[2])
        button.y = random.randint(spawn_area[1], spawn_area[3])
        return button

    def spawn_random_from_list(self, button_id_list, amount):
        button_list = []
        for i in range(amount):
            button_list.append(self.get_new_button(
                button_id_list[random.randint(0, len(button_id_list)-1)]))
        return button_list

    def spawn_random_from_list_random_place(self, button_id_list, amount, spawn_area):
        button_list = []
        for i in range(amount):
            button_list.append(self.spawn_in_random_place(
                button_id_list[random.randint(0, len(button_id_list)-1)], spawn_area))
        return button_list






