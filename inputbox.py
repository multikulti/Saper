import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *



def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,16)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 200,
                    (screen.get_height() / 2) - 10,
                    400,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 201,
                    (screen.get_height() / 2) - 11,
                    402,22), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 200, (screen.get_height() / 2) - 8))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = ""
  display_box(screen, question + ": " + current_string)
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string+=(chr(inkey))
    display_box(screen, question + ": " + current_string)
  return str(current_string)
  print(str(current_string))

def main():
  screen = pygame.display.set_mode((320,240))
  print(ask(screen, "Name") + " was entered")

if __name__ == '__main__': main()