import json
import numpy as np
import cv2

class Texture:
   __instance = None
   @staticmethod
   def getInstance():
      """ Static access method. """
      if Texture.__instance == None:
         Texture()
      return Texture.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if Texture.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Texture.__instance = self
         self.textures = {}
         self.upload_textures("description/textures.json")
   def upload_textures(self, file):
      with open(file, "r") as read_file:
         data = json.load(read_file)
      for k, value in data.items():
         img = cv2.imread(value, cv2.IMREAD_COLOR)
         if not(img is None):
            self.textures[k] = img
   def get_texture(self, texture_id):
       texture = self.textures.get(texture_id)
       if texture is None:
          print("Error, texture file ", texture_id, " not found")
          return None
       else:
          return texture

