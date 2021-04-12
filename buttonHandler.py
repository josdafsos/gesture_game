import cvButton as cb
import json
from copy import deepcopy

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
            if shape == "rectangle":
                width = data[b_type][i]["width"]
                height = data[b_type][i]["height"]
            else:
                width = data[b_type][i]["radius"]
                height = width
            if b_type == "static_buttons":
                button_type = "static"
                self.loaded_buttons[button_id] = cb.Button(x, y, button_type,
                                                           button_id, shape,
                                                           width, height)
            else:
                button_type = "dynamic"
                self.loaded_buttons[button_id] = cb.DynamicButton(x, y, button_type,
                                                           button_id, shape,
                                                           width, height)

    def get_new_button(self, button_id):
        return deepcopy(self.loaded_buttons[button_id])

    def create_static_button(self, button_dict):
        pass


