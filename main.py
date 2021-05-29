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

  def export(self):
    if self.initial_video is None and self.ending_video is None:
      # apenas corte
      ffmpeg_extract_subclip(self.original_video , self.start_time, self.end_time, targetname=self.slice_video_name)
    else:
      clip_list = []
      #video inicial
      if self.initial_video is not None:
        clip_initial_video = VideoFileClip(self.initial_video).set_fps(60)
        clip_list.append(clip_initial_video)
      #video cortado
      clip_sliced_video = VideoFileClip(self.original_video).subclip(self.start_time, self.end_time).set_fps(60)
      clip_list.append(clip_sliced_video)
      print(clip_sliced_video.size)
      #video final
      if self.ending_video is not None:
        clip_ending_video = VideoFileClip(self.ending_video).set_fps(60)
        clip_list.append(clip_ending_video)
      #redimensionando videos
      #TODO https://zulko.github.io/moviepy/ref/videofx/moviepy.video.fx.all.resize.html?highlight=resize#moviepy.video.fx.all.resize
      #gerando video
      final_clip = concatenate_videoclips(clip_list, method='compose')
      final_clip.write_videofile(self.slice_video_name)

def cut():
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
    if initial_video is not None:
      current_slice.initial_video = initial_video
    #video final
    if ending_video is not None:
      current_slice.ending_video = ending_video
    slice_list.append(current_slice)

  print("==========================================")
  print("Iniciando processamento")
  print("==========================================")

  for slice in slice_list:
    print("Processando corte #" + str(slice.id) + " - " + slice.slice_video_name + "...", end = '')
    slice.export()

  print("Finalizado!")
  system("pause")

if __name__ == '__main__':
  cut()