import pygame
import json
from shapely.geometry import shape
import sys

# ------------------------------
# Fonctions utilitaires
# ------------------------------

def latlon_to_pixel(lat, lon, width, height, margin=50):
    lon_min, lon_max = -5.2, 9.8
    lat_min, lat_max = 41.0, 51.3
    x = margin + (lon - lon_min) / (lon_max - lon_min) * (width - 2 * margin)
    y = margin + (lat_max - lat) / (lat_max - lat_min) * (height - 2 * margin)
    return int(x), int(y)

def load_france_polygon(path="data/france.geojson"):
    """Charge le polygone de la France métropolitaine à partir d’un fichier GeoJSON."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    polygons = []
    for feature in data["features"]:
        geom = shape(feature["geometry"])
        if geom.geom_type == "Polygon":
            polygons.append(list(geom.exterior.coords))
        elif geom.geom_type == "MultiPolygon":
            for poly in geom.geoms:
                polygons.append(list(poly.exterior.coords))
    return polygons

def draw_france(screen, polygons, width, height):
    for poly in polygons:
        pts = [latlon_to_pixel(lat, lon, width, height) for lon, lat in poly]
        pygame.draw.polygon(screen, (240, 240, 200), pts)
        pygame.draw.lines(screen, (100, 100, 100), True, pts, 1)

def draw_path(screen, cities, path, color=(0, 0, 255)):
    coords = [latlon_to_pixel(cities[i]["Latitude"], cities[i]["Longitude"], screen.get_width(), screen.get_height() - 60) for i in path]
    coords.append(coords[0])
    for i in range(len(coords) - 1):
        pygame.draw.line(screen, color, coords[i], coords[i + 1], 2)
    for i, city in enumerate(coords[:-1]):
        pygame.draw.circle(screen, (255, 0, 0), city, 5)
        font = pygame.font.SysFont(None, 18)
        text = font.render(cities[path[i]]["Ville"], True, (0, 0, 0))
        screen.blit(text, (city[0] + 4, city[1] - 4))

# ------------------------------
# Classe principale
# ------------------------------

class TSPVisualizer:
    def __init__(self, cities, path_christofides, path_genetic,
                 dist_c, dist_g, exec_c, exec_g, geojson_path="data/france.geojson"):
        pygame.init()
        self.cities = cities
        self.path_c = path_christofides
        self.path_g = path_genetic
        self.dist_c = dist_c
        self.dist_g = dist_g
        self.exec_c = exec_c
        self.exec_g = exec_g
        self.active_path = None
        self.polygons = load_france_polygon(geojson_path)

        # Fenêtre
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        # self.width, self.height = 800, 550
        # self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Voyageur de Commerce")
        self.clock = pygame.time.Clock()

        self.buttons = {
            "Christofides": pygame.Rect(50, self.height - 50, 150, 30),
            "Génétique": pygame.Rect(250, self.height - 50, 150, 30),
            "Comparaison": pygame.Rect(450, self.height - 50, 150, 30),
            "Quitter": pygame.Rect(650, self.height - 50, 150, 30)
        }

    def draw_buttons(self):
        font = pygame.font.SysFont(None, 24)
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (220, 220, 220), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            text = font.render(name, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_info_box(self):
        """Affiche les informations en bas à droite."""
        box_width = 340
        box_height = 220
        x = self.width - box_width - 10
        y = self.height - box_height - 10

        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        s.fill((40, 40, 40, 200))
        self.screen.blit(s, (x, y))

        font = pygame.font.Font(None, 24)
        title_font = pygame.font.Font(None, 28)

        title = title_font.render("Infos algorithme", True, (255, 255, 255))
        self.screen.blit(title, (x + 10, y + 10))

        if self.active_path == "christofides":
            lines = [
                f"Distance totale : {self.dist_c:.2f} km",
                f"Temps d'exécution : {self.exec_c:.3f} s",
            ]
            path = self.path_c
        elif self.active_path == "genetic":
            lines = [
                f"Distance totale : {self.dist_g:.2f} km",
                f"Temps d'exécution : {self.exec_g:.3f} s",
            ]
            path = self.path_g
        elif self.active_path == "compare":
            lines = [
                f"Christofides (bleu) : {self.dist_c:.2f} km ({self.exec_c:.3f} s)",
                f"Génétique (orange) : {self.dist_g:.2f} km ({self.exec_g:.3f} s)"
            ]
            path = self.path_c
        else:
            lines = ["Aucun algorithme sélectionné."]
            path = []

        # Écriture des infos
        for i, line in enumerate(lines):
            txt = font.render(line, True, (255, 255, 255))
            self.screen.blit(txt, (x + 10, y + 50 + i * 25))

    def run(self):
        running = True
        while running:
            self.screen.fill((173, 216, 230))
            draw_france(self.screen, self.polygons, self.width, self.height - 60)

            # Tracés selon le mode actif
            if self.active_path == "christofides":
                draw_path(self.screen, self.cities, self.path_c, color=(0, 100, 255))
            elif self.active_path == "genetic":
                draw_path(self.screen, self.cities, self.path_g, color=(255, 120, 0))
            elif self.active_path == "compare":
                draw_path(self.screen, self.cities, self.path_c, color=(0, 100, 255))
                draw_path(self.screen, self.cities, self.path_g, color=(255, 120, 0))

            self.draw_info_box()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for name, rect in self.buttons.items():
                        if rect.collidepoint(x, y):
                            if name == "Christofides":
                                self.active_path = "christofides"
                            elif name == "Génétique":
                                self.active_path = "genetic"
                            elif name == "Comparaison":
                                self.active_path = "compare"
                            elif name == "Quitter":
                                running = False

        pygame.quit()
        sys.exit()
