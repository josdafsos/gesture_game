import simpleaudio as sa
import json

class AudioPlayer:
   __instance = None
   @staticmethod
   def getInstance():
      """ Static access method. """
      if AudioPlayer.__instance == None:
         AudioPlayer()
      return AudioPlayer.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if AudioPlayer.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         AudioPlayer.__instance = self
         self.wave_obj_list = {}
         self.upload_sounds("sounds.json")
   def upload_sounds(self, file):
      with open(file, "r") as read_file:
         data = json.load(read_file)
      for k, value in data.items():
         wave_obj = sa.WaveObject.from_wave_file(value)
         self.wave_obj_list[k] = wave_obj
   def playSound(self, soundId):

      #TODO a lot of lags are comming when music is played. Fix it
       obj_to_play = self.wave_obj_list.get(soundId)
       if obj_to_play is None:
          print("Error, sound file ", soundId, " not found")
       else:
          obj_to_play.play()
