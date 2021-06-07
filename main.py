from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from os import listdir, system, remove
from os.path import isfile, join
import random

class Slice:
  def __init__(self, original_video):
    self.original_video = original_video
    self.initial_video = None
    self.ending_video = None

  def cut(self):
      ffmpeg_extract_subclip(self.original_video , self.start_time, self.end_time, targetname=self.slice_video_name)

  def export(self):
    if self.initial_video is None and self.ending_video is None:
      self.cut()
    else:
      clip_list = []
      min_height = 99999
      min_width = 99999
      #video inicial
      if self.initial_video is not None:
        clip_initial_video = VideoFileClip(self.initial_video).set_fps(60)
        clip_list.append(clip_initial_video)
        min_width = clip_initial_video.size[0] if clip_initial_video.size[0] < min_width else min_width
        min_height = clip_initial_video.size[1] if clip_initial_video.size[1] < min_height else min_height
      #video cortado
      clip_sliced_video = VideoFileClip(self.original_video).subclip(self.start_time, self.end_time).set_fps(60)
      clip_list.append(clip_sliced_video)
      min_width = clip_sliced_video.size[0] if clip_sliced_video.size[0] < min_width else min_width
      min_height = clip_sliced_video.size[1] if clip_sliced_video.size[1] < min_height else min_height
      #video final
      if self.ending_video is not None:
        clip_ending_video = VideoFileClip(self.ending_video).set_fps(60)
        clip_list.append(clip_ending_video)
        min_width = clip_ending_video.size[0] if clip_ending_video.size[0] < min_width else min_width
        min_height = clip_ending_video.size[1] if clip_ending_video.size[1] < min_height else min_height
      #redimensionando videos para tamanho do menor video
      for i in range(0,len(clip_list)): 
        clip_list[i] = clip_list[i].resize(height=min_height, width=min_width)
      #gerando video
      final_clip = concatenate_videoclips(clip_list, method='compose')
      final_clip.write_videofile(self.slice_video_name, logger='bar', temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")

def cut():
  initial_video = ""
  ending_video = ""
  original_video = input('Nome do arquivo a ser cortado: ')
  slices_count = int(input('Quantidade de partes a serem cortadas: '))
  initial_video = input('Nome do video de a ser concatenado no inicio (pressione Enter caso vazio): ')
  ending_video = input('Nome do video de a ser concatenado no fim (pressione Enter caso vazio): ')

  slice_list = []
  for slice in range(0, slices_count):
    print("==========================================")
    print("==> Corte #" + str(slice))
    slice_video_name = input('Nome do arquivo novo: ')
    start_time = input('Inicio do corte (em segundos): ')
    end_time = input('Fim do corte (em segundos): ')
    current_slice = Slice(original_video)
    current_slice.id = slice
    current_slice.start_time = int(start_time)
    current_slice.end_time = int(end_time)
    current_slice.slice_video_name = slice_video_name
    #video inicial
    if len(initial_video) > 0:
      current_slice.initial_video = initial_video
    #video final
    if len(ending_video) > 0:
      current_slice.ending_video = ending_video
    slice_list.append(current_slice)

  print("==========================================")
  print("Processando...")

  for slice in slice_list:
    slice.export()
    print("Gerado corte #" + str(slice.id) + " - " + slice.slice_video_name)

if __name__ == '__main__':
  cut()
  print("Finalizado!")
  input("Pressione Enter para finalizar")
