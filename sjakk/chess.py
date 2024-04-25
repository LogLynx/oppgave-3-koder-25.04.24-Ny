import pygame
from pygame.locals import *
import random

from piece import Piece
from utils import Utils

import time

class Chess(object):
    def __init__(self, screen, pieces_src, square_coords, square_length):
        # skjermflate
        self.screen = screen
        # lag et klasseobjekt for å vise sjakkbrikker på brettet
        self.chess_pieces = Piece(pieces_src, cols=6, rows=2)
        # lagre koordinatene til sjakkbrettrutene
        self.board_locations = square_coords
# lengde på siden av et sjakkbrettfirkant
        self.square_length = square_length
        # ordbok for å holde styr på spillerens tur
        self.turn = {"black": 0,
                     "white": 0}

        # liste som inneholder mulige trekk for den valgte brikken
        self.moves = []
        #
        self.utils = Utils()

        # kartlegging av brikkenavn til indeks over liste som inneholder brikkekoordinater på spritesheet
        self.pieces = {
            "white_pawn":   5,
            "white_knight": 3,
            "white_bishop": 2,
            "white_rook":   4,
            "white_king":   0,
            "white_queen":  1,
            "black_pawn":   11,
            "black_knight": 9,
            "black_bishop": 8,
            "black_rook":   10,
            "black_king":   6,
            "black_queen":  7
        }

        # liste som inneholder fangede brikker
        self.captured = []
        
        self.winner = ""

        self.reset()
    
    def reset(self):
        # tømme trekklister
        self.moves = []

        # randomisere spillerens tur
        x = random.randint(0, 1)
        if(x == 1):
            self.turn["black"] = 1
        elif(x == 0):
            self.turn["white"] = 1

        # to dimensionell ordbok som inneholder detaljer om hver brettplassering
        # lagringsformat er [piece_name, current_selected, x_y_coordinate]
        self.piece_location = {}
        x = 0
        for i in range(97, 105):
            a = 8
            y = 0
            self.piece_location[chr(i)] = {}
            while a>0:
                # [piece name, currently selected, board coordinates]
                self.piece_location[chr(i)][a] = ["", False, [x,y]]
                a = a - 1
                y = y + 1
            x = x + 1

        # resetter hele bordet
        for i in range(97, 105):
            x = 8
            while x>0:
                if(x==8):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "black_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "black_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "black_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "black_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "black_king"
                elif(x==7):
                    self.piece_location[chr(i)][x][0] = "black_pawn"
                elif(x==2):
                    self.piece_location[chr(i)][x][0] = "white_pawn"
                elif(x==1):
                    if(chr(i)=='a' or chr(i)=='h'):
                        self.piece_location[chr(i)][x][0] = "white_rook"
                    elif(chr(i)=='b' or chr(i)=='g'):
                        self.piece_location[chr(i)][x][0] = "white_knight"
                    elif(chr(i)=='c' or chr(i)=='f'):
                        self.piece_location[chr(i)][x][0] = "white_bishop"
                    elif(chr(i)=='d'):
                        self.piece_location[chr(i)][x][0] = "white_queen"
                    elif(chr(i)=='e'):
                        self.piece_location[chr(i)][x][0] = "white_king"
                x = x - 1


    # 
    def play_turn(self):
        # hvit farge
        white_color = (255, 255, 255)
        # lager fonts for teksten
        small_font = pygame.font.SysFont("comicsansms", 20)
        # lager tekst for å bli vist på Main Menu
        if self.turn["black"]:
            turn_text = small_font.render("Turn: Black", True, white_color)
        elif self.turn["white"]:
            turn_text = small_font.render("Turn: White", True, white_color)
        
        # viser velkommen teskst
        self.screen.blit(turn_text, 
                      ((self.screen.get_width() - turn_text.get_width()) // 2,
                      10))
        
        # lar spiller med svart brikke få spille
        if(self.turn["black"]):
            self.move_piece("black")
        # lar spiller med hvit brikke få spille
        elif(self.turn["white"]):
            self.move_piece("white")

    # metode for å tegne brikker på sjakkbrettet
    def draw_pieces(self):
        transparent_green = (0,194,39,170)
        transparent_blue = (28,21,212,170)

        # lage en gjennomsiktig overflate
        surface = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface.fill(transparent_green)

        surface1 = pygame.Surface((self.square_length, self.square_length), pygame.SRCALPHA)
        surface1.fill(transparent_blue)

        # løkke for å endre bakgrunnsfargen til det valgte stykket
        for val in self.piece_location.values():
            for value in val.values() :
                # navnet på stykket på gjeldende plassering
                piece_name = value[0]
                # x, y koordinater for gjeldende stykke
                piece_coord_x, piece_coord_y = value[2]

                # endre bakgrunnsfargen på stykket hvis det er valgt
                if value[1] and len(value[0]) > 5:
                    # hvis den valgte brikken er en svart brikke
                    if value[0][:5] == "black":
                        self.screen.blit(surface, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface, self.board_locations[x_coord][y_coord])
                    # hvis den valgte brikken er en hvit brikke
                    elif value[0][:5] == "white":
                        self.screen.blit(surface1, self.board_locations[piece_coord_x][piece_coord_y])
                        if len(self.moves) > 0:
                            for move in self.moves:
                                x_coord = move[0]
                                y_coord = move[1]
                                if x_coord >= 0 and y_coord >= 0 and x_coord < 8 and y_coord < 8:
                                    self.screen.blit(surface1, self.board_locations[x_coord][y_coord])
        
        # trekke alle sjakkbrikkene
        for val in self.piece_location.values():
            for value in val.values() :
                # navnet på stykket på gjeldende plassering
                piece_name = value[0]
                # x, y koordinater for gjeldende stykke
                piece_coord_x, piece_coord_y = value[2]
                # sjekk om det er en brikke på torget
                if(len(value[0]) > 1):
                    # tegne brikke på brettet
                    self.chess_pieces.draw(self.screen, piece_name, 
                                            self.board_locations[piece_coord_x][piece_coord_y])


    # metode for å finne mulige trekk for den valgte brikken
    def possible_moves(self, piece_name, piece_coord):
        # liste for å lagre mulige trekk av den valgte brikken
        positions = []
        # finne de mulige stedene for å sette et stykke
        if len(piece_name) > 0:
            # få x, y kordiatene
            x_coord, y_coord = piece_coord
            # beregne trekk for biskopen
            if piece_name[6:] == "bishop":
                positions = self.diagonal_moves(positions, piece_name, piece_coord)
            
            # beregne trekk for bonde
            elif piece_name[6:] == "pawn":
                # konverter listeindeks til ordboknøkkel
                columnChar = chr(97 + x_coord)
                rowNo = 8 - y_coord

                # beregne trekk for hvit bonde
                if piece_name == "black_pawn":
                    if y_coord + 1 < 8:
                        # få rad foran svart bonde
                        rowNo = rowNo - 1
                        front_piece = self.piece_location[columnChar][rowNo][0]
                
                        # bønder kan ikke bevege seg når de blokkeres av en annen annen bonde
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord+1])
                            # svarte bønder kan flytte to posisjoner foran for første trekk
                            if y_coord < 2:
                                positions.append([x_coord, y_coord+2])

                        # EM PASSANT
                        # diagonalt til venstre
                        if x_coord - 1 >= 0 and y_coord + 1 < 8:
                            x = x_coord - 1
                            y = y_coord + 1
                            
                            # konverter listeindeks til ordboknøkkel
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                        # diagonalt til høyre
                        if x_coord + 1 < 8  and y_coord + 1 < 8:
                            x = x_coord + 1
                            y = y_coord + 1

                            # konverter listeindeks til ordboknøkkel
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "white"):
                                positions.append([x, y])
                        
                # beregne trekk for hvit bonde
                elif piece_name == "white_pawn":
                    if y_coord - 1 >= 0:
                        # få rad foran svart bonde
                        rowNo = rowNo + 1
                        front_piece = self.piece_location[columnChar][rowNo][0]

                        # bønder kan ikke bevege seg når de blokkeres av en annen annen bonde
                        if(front_piece[6:] != "pawn"):
                            positions.append([x_coord, y_coord-1])
                            # svarte bønder kan flytte to posisjoner foran for første trekk
                            if y_coord > 5:
                                positions.append([x_coord, y_coord-2])

                        # EM PASSANT
                        # diagonalt til venstre
                        if x_coord - 1 >= 0 and y_coord - 1 >= 0:
                            x = x_coord - 1
                            y = y_coord - 1
                            
                            # konverter listeindeks til ordboknøkkel
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])

                            
                        # diagonalt til høyre
                        if x_coord + 1 < 8  and y_coord - 1 >= 0:
                            x = x_coord + 1
                            y = y_coord - 1

                            # konverter listeindeks til ordboknøkkel
                            columnChar = chr(97 + x)
                            rowNo = 8 - y
                            to_capture = self.piece_location[columnChar][rowNo]

                            if(to_capture[0][:5] == "black"):
                                positions.append([x, y])


            # beregne trekk for tårn
            elif piece_name[6:] == "rook":
                # finne lineære trekk
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # beregne trekk for ridder
            elif piece_name[6:] == "knight":
                # venstre posisjoner
                if(x_coord - 2) >= 0:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-2, y_coord+1])
                # top posisjoner
                if(y_coord - 2) >= 0:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord-2])
                # høyre posisjoner
                if(x_coord + 2) < 8:
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+2, y_coord-1])
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+2, y_coord+1])
                # nederste posisjoner
                if(y_coord + 2) < 8:
                    if(x_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord+2])
                    if(x_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+2])

            # beregne bevegelser for konge
            elif piece_name[6:] == "king":
                if(y_coord - 1) >= 0:
                    # øverste plass
                    positions.append([x_coord, y_coord-1])

                if(y_coord + 1) < 8:
                    # nederste plass
                    positions.append([x_coord, y_coord+1])

                if(x_coord - 1) >= 0:
                    # venstre plass
                    positions.append([x_coord-1, y_coord])
                    # top venstre plass
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord-1, y_coord-1])
                    # nederste venstre plass
                    if(y_coord + 1) < 8:
                        positions.append([x_coord-1, y_coord+1])
                    
                if(x_coord + 1) < 8:
                    # høyre plass
                    positions.append([x_coord+1, y_coord])
                    # top høyre plass
                    if(y_coord - 1) >= 0:
                        positions.append([x_coord+1, y_coord-1])
                    # nederste høyre plass
                    if(y_coord + 1) < 8:
                        positions.append([x_coord+1, y_coord+1])
                
            # beregne bevegelser for dronning
            elif piece_name[6:] == "queen":
                # finne diagonale posisjoner
                positions = self.diagonal_moves(positions, piece_name, piece_coord)

                # finne lineære trekk
                positions = self.linear_moves(positions, piece_name, piece_coord)

            # liste over stillinger som skal fjernes
            to_remove = []

            # fjerne posisjoner som overlapper andre deler av gjeldende spiller
            for pos in positions:
                x, y = pos

                # konverter listeindeks til ordboknøkkel
                columnChar = chr(97 + x)
                rowNo = 8 - y

                # finn brikkene som skal fjernes
                des_piece_name = self.piece_location[columnChar][rowNo][0]
                if(des_piece_name[:5] == piece_name[:5]):
                    to_remove.append(pos)

            # fjerne posisjon fra posisjonslisten
            for i in to_remove:
                positions.remove(i)

        # returliste som inneholder mulige trekk for den valgte brikken
        return positions


    def move_piece(self, turn):
        # få koordinatene til ruten valgt på brettet
        square = self.get_selected_square()

        # hvis en firkant ble valgt
        if square:
            # få navnet på brikken på den valgte ruten
            piece_name = square[0]
            # fargen på brikken på den valgte ruten
            piece_color = piece_name[:5]
            # tavlekolonnekarakter
            columnChar = square[1]
            # bordradnummer
            rowNo = square[2]

            # få x, y koordinater
            x, y = self.piece_location[columnChar][rowNo][2]

            # hvis det er en brikke på den valgte ruten
            if(len(piece_name) > 0) and (piece_color == turn):
                # finne mulige trekk for stykket
                self.moves = self.possible_moves(piece_name, [x,y])

            # sjakkmatt mekanisme
            p = self.piece_location[columnChar][rowNo]

            for i in self.moves:
                if i == [x, y]:
                    if(p[0][:5] == turn) or len(p[0]) == 0:
                        self.validate_move([x,y])
                    else:
                        self.capture_piece(turn, [columnChar, rowNo], [x,y])

            # bare spilleren med tur får spille
            if(piece_color == turn):
                # endre markeringsflagg fra alle andre brikker
                for k in self.piece_location.keys():
                    for key in self.piece_location[k].keys():
                        self.piece_location[k][key][1] = False

                # endre markeringsflagget til det valgte stykket
                self.piece_location[columnChar][rowNo][1] = True
                
            
    def get_selected_square(self):
        # få forlatt arrangement
        left_click = self.utils.left_click_event()

        # hvis det er en musehendelse
        if left_click:
            # et musebegivenhet
            mouse_event = self.utils.get_mouse_event()

            for i in range(len(self.board_locations)):
                for j in range(len(self.board_locations)):
                    rect = pygame.Rect(self.board_locations[i][j][0], self.board_locations[i][j][1], 
                            self.square_length, self.square_length)
                    collision = rect.collidepoint(mouse_event[0], mouse_event[1])
                    if collision:
                        selected = [rect.x, rect.y]
                        # finn x, y koordinerer det valgte kvadratet
                        for k in range(len(self.board_locations)):
                            #
                            try:
                                l = None
                                l = self.board_locations[k].index(selected)
                                if l != None:
                                    #tilbakestill fargen på alle valgte stykker
                                    for val in self.piece_location.values():
                                        for value in val.values() :
                                            # [brikkenavn, valgt for øyeblikket, tavlekoordinater]
                                            if not value[1]:
                                                value[1] = False

                                    # få kolonnekarakter og radnummer på sjakkbrikken
                                    columnChar = chr(97 + k)
                                    rowNo = 8 - l
                                    # få navnet på 
                                    piece_name = self.piece_location[columnChar][rowNo][0]
                                    
                                    return [piece_name, columnChar, rowNo]
                            except:
                                pass
        else:
            return None


    def capture_piece(self, turn, chess_board_coord, piece_coord):
        # få x, y-koordinaten til destinasjonsstykket
        x, y = piece_coord

        # få sjakkbrettkoordinat
        columnChar, rowNo = chess_board_coord

        p = self.piece_location[columnChar][rowNo]
        
        if p[0] == "white_king":
            self.winner = "Black"
            print("Black wins")
        elif p[0] == "black_king":
            self.winner = "White"
            print("White wins")

        # legg det fangede stykket til listen
        self.captured.append(p)
        # flytte kildedelen til målet
        self.validate_move(piece_coord)


    def validate_move(self, destination):
        desColChar = chr(97 + destination[0])
        desRowNo = 8 - destination[1]

        for k in self.piece_location.keys():
            for key in self.piece_location[k].keys():
                board_piece = self.piece_location[k][key]

                if board_piece[1]:
                    # fjern valget av kilden
                    self.piece_location[k][key][1] = False
                    # få navnet på kilden
                    piece_name = self.piece_location[k][key][0]
                    # flytte kildedelen til destinasjonsdelen
                    self.piece_location[desColChar][desRowNo][0] = piece_name
                    
                    src_name = self.piece_location[k][key][0]
                    # fjern kilden fra sin nåværende posisjon
                    self.piece_location[k][key][0] = ""

                    # bytte tur
                    if(self.turn["black"]):
                        self.turn["black"] = 0
                        self.turn["white"] = 1
                    elif("white"):
                        self.turn["black"] = 1
                        self.turn["white"] = 0

                    src_location = k + str(key)
                    des_location = desColChar + str(desRowNo)
                    print("{} moved from {} to {}".format(src_name,  src_location, des_location))


    # hjelpefunksjon for å finne diagonale bevegelser
    def diagonal_moves(self, positions, piece_name, piece_coord):
        # tilbakestill x- og y-koordinatverdiene
        x, y = piece_coord
        # finn diagonale flekker øverst til venstre
        while(True):
            x = x - 1
            y = y - 1
            if(x < 0 or y < 0):
                break
            else:
                positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # tilbakestill x- og y-koordinatverdiene
        x, y = piece_coord
        # finn diagonale flekker nederst til høyre
        while(True):
            x = x + 1
            y = y + 1
            if(x > 7 or y > 7):
                break
            else:
                positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # tilbakestill x- og y-koordinatverdiene
        x, y = piece_coord
        # finn diagonale flekker nederst til venstre
        while(True):
            x = x - 1
            y = y + 1
            if (x < 0 or y > 7):
                break
            else:
                positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # tilbakestill x- og y-koordinatverdiene
        x, y = piece_coord
        # finn diagonale punkter øverst til høyre
        while(True):
            x = x + 1
            y = y - 1
            if(x > 7 or y < 0):
                break
            else:
                positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        return positions
    

    # hjelpefunksjon for å finne horisontale og vertikale bevegelser
    def linear_moves(self, positions, piece_name, piece_coord):
        # tilbakestill x, y koordinatverdi
        x, y = piece_coord
        # horisontal flyttes til venstre
        while(x > 0):
            x = x - 1
            positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break
                    

        # tilbakestill x, y koordinatverdi
        x, y = piece_coord
        # horisontal beveger seg til høyre
        while(x < 7):
            x = x + 1
            positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break    

        # tilbakestill x, y koordinatverdi
        x, y = piece_coord
        # vertikal beveger seg oppover
        while(y > 0):
            y = y - 1
            positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break

        # tilbakestill x, y koordinatverdi
        x, y = piece_coord
        # vertikal beveger seg nedover
        while(y < 7):
            y = y + 1
            positions.append([x,y])

            # konverter listeindeks til ordboknøkkel
            columnChar = chr(97 + x)
            rowNo = 8 - y
            p = self.piece_location[columnChar][rowNo]

            # slutte å finne mulige trekk hvis blokkert av en brikke
            if len(p[0]) > 0 and piece_name[:5] != p[:5]:
                break


        return positions