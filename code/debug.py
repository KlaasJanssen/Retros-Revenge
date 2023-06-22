import pygame

def debug(text, x = 10, y = 10):
    display_surface = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)
    text_surf = font.render(str(text), True, "White")
    text_rect = text_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, "black", text_rect)
    display_surface.blit(text_surf, text_rect)
