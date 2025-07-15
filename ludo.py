from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import time
from random import randint,choices

class Ludo:
    def __init__(self, root,six_side_block,five_side_block,four_side_block,three_side_block,two_side_block,one_side_block):
        self.window = root
        #canvas (game board)
        self.cvs = Canvas(self.window, bg="#4d4dff", width=800, height=630)  ##4d4dff
        self.cvs.pack()                                                        #fill=BOTH,expand=1

        #containers to store data 
        #it stores references to each player's 4 coins 
        self.red_coins = []
        self.green_coins = []
        self.yellow_coins = []
        self.blue_coins = []
        #reference to their number labels
        self.red_number_label = []
        self.green_number_label = []
        self.yellow_number_label = []
        self.sky_blue_number_label = []

        self.block_value_predict = []
        self.total_people_play = []

        # Ludo block all side image store
        self.block_number_side = [one_side_block, two_side_block, three_side_block, four_side_block, five_side_block, six_side_block]

        # Use for store specific position of all coins
        self.red_coord_store = [-1, -1, -1, -1]     #-1 means its inside home
        self.green_coord_store = [-1, -1, -1, -1]
        self.yellow_coord_store = [-1, -1, -1, -1]
        self.sky_blue_coord_store = [-1, -1, -1, -1]

        self.red_coin_position = [-1, -1, -1, -1]
        self.green_coin_position = [-1, -1, -1, -1]
        self.yellow_coin_position = [-1, -1, -1, -1]
        self.sky_blue_coin_position = [-1, -1, -1, -1]

        # Number to room to be traverse by specific color coin, store in that variable
        self.move_red_counter = 0
        self.move_green_counter = 0
        self.move_yellow_counter = 0
        self.move_sky_blue_counter = 0

        self.take_permission = 0
        self.six_with_overlap = 0

        self.red_store_active = 0
        self.sky_blue_store_active = 0
        self.yellow_store_active = 0
        self.green_store_active = 0

        self.six_counter = 0
        self.current_player_index = -1

        # Some variables initializes with None
        self.right_star = None
        self.down_star = None
        self.left_star = None
        self.up_star = None

        # By default some function call
        self.board_set_up()

        self.instruction_btn_red()
        self.instruction_btn_sky_blue()
        self.instruction_btn_yellow()
        self.instruction_btn_green()

        self.take_initial_control()


    def board_set_up(self):
        # Cover Box made
        self.cvs.create_rectangle(100, 15, 100 + (40 * 15), 15 + (40 * 15), width=6, fill="white")  #width for thickness of the border 
          #-Because the Ludo board is of 15x15 grid, and each block is 40 pixels wide

        # main home boxes
        self.cvs.create_rectangle(100, 15, 100+(40*6), 15+240, width=3, fill="pink")
        self.cvs.create_rectangle(100, (15+240)+(40*3), 100+240, (15+240)+(40*3)+(40*6), width=3, fill="#29d0ed")
        self.cvs.create_rectangle(340+(40*3), 15, 340+(40*3)+(40*6), 15+240, width=3, fill="#33F433")
        self.cvs.create_rectangle(340+(40*3), (15+240)+(40*3), 340+(40*3)+(40*6), (15+240)+(40*3)+(40*6), width=3, fill="yellow")

        # Left 3 box(In white region)
        self.cvs.create_rectangle(100, (15+240), 100+240, (15+240)+40, width=3)
        self.cvs.create_rectangle(100+40, (15 + 240)+40, 100 + 240, (15 + 240) + 80, width=3, fill="#FF8080")
        self.cvs.create_rectangle(100, (15 + 240)+80, 100 + 240, (15 + 240) + 80+40, width=3)

        # right 3 box(In white region)
        self.cvs.create_rectangle(100+240, 15, 100 + 240+40, 15 + (40*6), width=3)
        self.cvs.create_rectangle(100+240+40, 15+40, 100+240+80, 15 + (40*6), width=3, fill="#00FF00")
        self.cvs.create_rectangle(100+240+80, 15, 100 + 240+80+40, 15 + (40*6), width=3)

        # up 3 box(In white region)
        self.cvs.create_rectangle(340+(40*3), 15+240, 340+(40*3)+(40*6), 15+240+40, width=3)
        self.cvs.create_rectangle(340+(40*3), 15+240+40, 340+(40*3)+(40*6)-40, 15+240+80, width=3, fill="yellow")
        self.cvs.create_rectangle(340+(40*3), 15+240+80, 340+(40*3)+(40*6), 15+240+120, width=3)

        # down 3 box(In white region)
        self.cvs.create_rectangle(100, (15 + 240)+(40*3), 100 + 240+40, (15 + 240)+(40*3)+(40*6), width=3)
        self.cvs.create_rectangle(100+240+40, (15 + 240)+(40*3), 100 + 240+40+40, (15 + 240)+(40*3)+(40*6)-40, width=3, fill="#04d9ff")
        self.cvs.create_rectangle(100 + 240+40+40, (15 + 240)+(40*3), 100 + 240+40+40+40, (15 + 240)+(40*3)+(40*6), width=3)

        # All left separation line
        start_x = 100 + 40
        start_y = 15 + 240
        end_x = 100 + 40
        end_y = 15 + 240 + (40 * 3)
        for i in range(5):
            self.cvs.create_line(start_x, start_y, end_x, end_y, width=3)
            start_x+=40
            end_x+= 40

        # All right separation line
        start_x = 100+240+(40*3)+40
        start_y = 15 + 240
        end_x = 100+240+(40*3)+40
        end_y = 15 + 240 + (40 * 3)
        for _ in range(5):
            self.cvs.create_line(start_x, start_y, end_x, end_y, width=3)
            start_x += 40
            end_x += 40

        # All up separation done
        start_x = 100+240
        start_y = 15+40
        end_x = 100+240+(40*3)
        end_y = 15+40
        for _ in range(5):
            self.cvs.create_line(start_x, start_y, end_x, end_y, width=3)
            start_y += 40
            end_y += 40

        # All down separation done
        start_x = 100 + 240
        start_y = 15 + (40*6)+(40*3)+40
        end_x = 100 + 240 + (40 * 3)
        end_y = 15 + (40*6)+(40*3)+40
        for _ in range(5):
            self.cvs.create_line(start_x, start_y, end_x, end_y, width=3)
            start_y += 40
            end_y += 40

        # Square box- white region
        self.cvs.create_rectangle(100+20, 15+20, 100 + 220, 15+200, width=3, fill="white")  #15+40+40+40+100-20
        self.cvs.create_rectangle(340+(40*3)+20, 15 +20, 340+(40*3)+220, 15+200, width=3, fill="white")
        self.cvs.create_rectangle(100+20, 15+240+(4*40), 100 +220, 595, width=3, fill="white")
        self.cvs.create_rectangle(340+(40*3)+20, 15+240+(4*40), 340+(40*3)+220, 595, width=3, fill="white")


        # red main squares
        self.cvs.create_rectangle(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red")
        self.cvs.create_rectangle(100+40+120, 15 + 40, 100+40+160, 15 + 40 + 40, width=3, fill="red")
        self.cvs.create_rectangle(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3, fill="red")
        self.cvs.create_rectangle(100 + 40 + 60 + 60, 15 + 40+100, 100 + 40 + 60 + 40 +60, 15 + 40 + 40+100, width=3, fill="red")


        # green main squares
        self.cvs.create_rectangle(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="#00FF00")
        self.cvs.create_rectangle(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="#00FF00")
        self.cvs.create_rectangle(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="#00FF00")
        self.cvs.create_rectangle(340+(40*3)+40+ 60 + 40+20, 15 + 40 + 100, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40 + 100, width=3, fill="#00FF00")


        # blue main squares
        self.cvs.create_rectangle(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="#04d9ff")
        self.cvs.create_rectangle(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#04d9ff")
        self.cvs.create_rectangle(100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="#04d9ff")
        self.cvs.create_rectangle(100 + 40 + 60 + 40+20, 340+80+60+40+15, 100 + 40 + 60 + 40 + 40+20, 340+80+60+40+40+15, width=3, fill="#04d9ff")


        # yellow main squares
        self.cvs.create_rectangle(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="yellow")
        self.cvs.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="yellow")
        self.cvs.create_rectangle(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="yellow")
        self.cvs.create_rectangle(340 + (40 * 3) + 40 + 60 + 40+20, 340+80+60+40+15,340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+60+40+40+15, width=3, fill="yellow")

        #start positions
        self.cvs.create_rectangle(100+240,340+(40*5)-5,100+240+40,340+(40*6)-5,fill="#04d9ff",width=3)
        self.cvs.create_rectangle(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="red", width=3)
        self.cvs.create_rectangle(100 + (40*8), 15 + 40, 100 +(40*9), 15 + 40+ 40, fill="#00FF00", width=3)
        self.cvs.create_rectangle(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="yellow", width=3)

        # Traingle in middle
        self.cvs.create_polygon(100+240, 15+240, 100+240+60, 15+240+60, 100+240, 15+240+(40*3), width=3,fill="red",outline="black")
        self.cvs.create_polygon(100 + 240+(40*3), 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240+(40*3), 15 + 240 + (40 * 3), width=3, fill="yellow",outline="black")
        self.cvs.create_polygon(100 + 240, 15 + 240, 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240, width=3, fill="#00FF00",outline="black")
        self.cvs.create_polygon(100 + 240, 15 + 240+(40*3), 100 + 240 + 60, 15 + 240 + 60, 100 + 240 + (40 * 3), 15 + 240+(40*3), width=3, fill="#04d9ff",outline="black")


        #coins for red
        red_1_coin = self.cvs.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red", outline="black")
        red_2_coin = self.cvs.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="red", outline="black")
        red_3_coin = self.cvs.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="red", outline="black")
        red_4_coin = self.cvs.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3,fill="red", outline="black")
        self.red_coins.append(red_1_coin)
        self.red_coins.append(red_2_coin)
        self.red_coins.append(red_3_coin)
        self.red_coins.append(red_4_coin)

        # Make coin under number label for red left up block
        red_1_label = Label(self.cvs, text="1", font=("Arial", 15, "bold"), bg="red", fg="black")
        red_1_label.place(x=100 + 40 + 10, y=15 + 40 + 5)
        red_2_label = Label(self.cvs, text="2", font=("Arial", 15, "bold"), bg="red", fg="black")
        red_2_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 5)
        red_3_label = Label(self.cvs, text="3", font=("Arial", 15, "bold"), bg="red", fg="black")
        red_3_label.place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
        red_4_label = Label(self.cvs, text="4", font=("Arial", 15, "bold"), bg="red", fg="black")
        red_4_label.place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)
        self.red_number_label.append(red_1_label)
        self.red_number_label.append(red_2_label)
        self.red_number_label.append(red_3_label)
        self.red_number_label.append(red_4_label)

        # Make coin for green right up block
        green_1_coin = self.cvs.create_oval(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="#00FF00", outline="black")
        green_2_coin = self.cvs.create_oval(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="#00FF00", outline="black")
        green_3_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 15 + 40 + 100, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 15 + 40 + 40 + 100, width=3, fill="#00FF00", outline="black")
        green_4_coin = self.cvs.create_oval(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="#00FF00", outline="black")
        self.green_coins.append(green_1_coin)
        self.green_coins.append(green_2_coin)
        self.green_coins.append(green_3_coin)
        self.green_coins.append(green_4_coin)

        # Make coin under number label for green right up block
        green_1_label = Label(self.cvs, text="1", font=("Arial", 15, "bold"), bg="#00FF00", fg="black")
        green_1_label.place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 5)
        green_2_label = Label(self.cvs, text="2", font=("Arial", 15, "bold"), bg="#00FF00", fg="black")
        green_2_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 5)
        green_3_label = Label(self.cvs, text="3", font=("Arial", 15, "bold"), bg="#00FF00", fg="black")
        green_3_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 100 + 5)
        green_4_label = Label(self.cvs, text="4", font=("Arial", 15, "bold"), bg="#00FF00", fg="black")
        green_4_label.place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 100 + 5)
        self.green_number_label.append(green_1_label)
        self.green_number_label.append(green_2_label)
        self.green_number_label.append(green_3_label)
        self.green_number_label.append(green_4_label)

        # Make coin for sky_blue left down block
        sky_blue_1_coin = self.cvs.create_oval(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="#04d9ff", outline="black")
        sky_blue_2_coin = self.cvs.create_oval(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#04d9ff", outline="black")
        sky_blue_3_coin = self.cvs.create_oval(100 + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 100 + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#04d9ff", outline="black")
        sky_blue_4_coin = self.cvs.create_oval( 100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="#04d9ff", outline="black")
        self.blue_coins.append(sky_blue_1_coin)
        self.blue_coins.append(sky_blue_2_coin)
        self.blue_coins.append(sky_blue_3_coin)
        self.blue_coins.append(sky_blue_4_coin)

        # Make coin under number label for sky_blue left down block
        sky_blue_1_label = Label(self.cvs, text="1", font=("Arial", 15, "bold"), bg="#04d9ff", fg="black")
        sky_blue_1_label.place(x=100 + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        sky_blue_2_label = Label(self.cvs, text="2", font=("Arial", 15, "bold"), bg="#04d9ff", fg="black")
        sky_blue_2_label.place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        sky_blue_3_label = Label(self.cvs, text="3", font=("Arial", 15, "bold"), bg="#04d9ff", fg="black")
        sky_blue_3_label.place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
        sky_blue_4_label = Label(self.cvs, text="4", font=("Arial", 15, "bold"), bg="#04d9ff", fg="black")
        sky_blue_4_label.place(x=100 + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
        self.sky_blue_number_label.append(sky_blue_1_label)
        self.sky_blue_number_label.append(sky_blue_2_label)
        self.sky_blue_number_label.append(sky_blue_3_label)
        self.sky_blue_number_label.append(sky_blue_4_label)

        # Make coin for yellow right down block
        yellow_1_coin = self.cvs.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="yellow", outline="black")
        yellow_2_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="yellow", outline="black")
        yellow_3_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="yellow", outline="black")
        yellow_4_coin = self.cvs.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="yellow", outline="black")
        self.yellow_coins.append(yellow_1_coin)
        self.yellow_coins.append(yellow_2_coin)
        self.yellow_coins.append(yellow_3_coin)
        self.yellow_coins.append(yellow_4_coin)

        # Make coin under number label for yellow right down block
        yellow_1_label = Label(self.cvs, text="1", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        yellow_1_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        yellow_2_label = Label(self.cvs, text="2", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        yellow_2_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 10)
        yellow_3_label = Label(self.cvs, text="3", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        yellow_3_label.place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        yellow_4_label = Label(self.cvs, text="4", font=("Arial", 15, "bold"), bg="yellow", fg="black")
        yellow_4_label.place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)
        self.yellow_number_label.append(yellow_1_label)
        self.yellow_number_label.append(yellow_2_label)
        self.yellow_number_label.append(yellow_3_label)
        self.yellow_number_label.append(yellow_4_label)


        # Make star safe zone

        #right star
        self.cvs.create_polygon(600,257,600+5,257+15,600+15,257+15,600+8,257+20,600+15,257+25,600+5,257+25,600,257+25+10,600-5,257+25,600-16,257+25,600-8,257+15+5,600-15,257+15,600-5,257+15,width=3,fill="blue")
        # Up star
        self.cvs.create_polygon(360, 95, 360+5, 95+15, 360+15, 95+15, 360+8, 95+20, 360+15, 95+25, 360+5, 95+25, 360, 95+25+10, 360-5, 95+25, 360-16, 95+25, 360-8, 95+15+5, 360-15, 95+15, 360-5, 95+15, width=3, fill="blue")
        # Left star
        self.cvs.create_polygon(200, 337, 200+5, 337+15, 200+15, 337+15, 200+8, 337+20, 200+15, 337+25, 200+5, 337+25, 200, 337+25+10, 200-5, 337+25, 200-16, 337+25, 200-8, 337+15+5, 200-15, 337+15, 200-5, 337+15, width=3, fill="blue")
        # Down star
        self.cvs.create_polygon(440, 497,440 + 5,497 + 15,440 + 15, 497 + 15,440 + 8, 497 + 20,440 + 15, 497 + 25, 440 + 5, 497 + 25,440, 497 + 25 + 10,440 - 5, 497 + 25, 440 - 16, 497 + 25,440 - 8, 497 + 15 + 5,440 - 15, 497 + 15,440 - 5, 497 + 15, width=3, fill="blue")

  # Total number of players: Control take at first
    def take_initial_control(self):
        for i in range(4):
            self.block_value_predict[i][1]['state'] = DISABLED

        # Make other window to control take
        top = Toplevel()
        top.geometry("600x150")
        top.maxsize(600,150)
        top.minsize(600,150)
        top.config(bg="orange")
        top.iconbitmap("Images/ludo_icon.ico")

        head = Label(top,text="-:Total number of players:- ",font=("Arial",25,"bold","italic"),bg="orange",fg="chocolate")
        head.place(x=70,y=30)
        take_entry = Entry(top,font=("Arial",18,"bold","italic"),relief=SUNKEN,bd=7,width=12)                             #relief for the 3D effect and bd= border width
        take_entry.place(x=150,y=80)
        take_entry.focus()


        def filtering():# Total player input value filtering
            if 4>= int(take_entry.get())>1:
                for pi in range(int(take_entry.get())):
                    self.total_people_play.append(pi)
                print("total people playing: ",self.total_people_play)
                self.start_next_turn()
                top.destroy()
            else:
                messagebox.showerror("Input Error", "Please input number of players between 2 and 4")

        submit_btn = Button(top,text="Submit",bg="black",fg="#00FF00",font=("Arial",13,"bold"),relief=RAISED,bd=8,command=filtering)
        submit_btn.place(x=350,y=80)
        top.mainloop()
    

    # Player Turn Manager
    def start_next_turn(self): # it starts the next player’s turn
        if  self.current_player_index != -1:    # current_player_index - tracking which player’s turn it is
            self.block_value_predict[self.total_people_play[self.current_player_index]][1]['state'] = DISABLED
        if  self.current_player_index == len(self.total_people_play)-1:
            self.current_player_index = -1

        self.current_player_index+=1
        self.block_value_predict[self.total_people_play[self.current_player_index]][1]['state'] = NORMAL

    # Get block value after prediction based on probability
    def make_prediction(self,color_indicator):
        try:
            if color_indicator == "red":
                block_value_predict = self.block_value_predict[0]
                permanent_block_number = self.move_red_counter =choices([1,2,3,4, 5, 6], weights=[2,1,3,1, 2, 4])[0]

            elif color_indicator == "sky_blue":
                block_value_predict = self.block_value_predict[1]
                permanent_block_number = self.move_sky_blue_counter = choices([1,2,3,4, 5, 6], weights=[2,1,3,1, 2, 4])[0]

            elif color_indicator == "yellow":
                block_value_predict = self.block_value_predict[2]
                permanent_block_number = self.move_yellow_counter = choices([1,2,3,4, 5, 6], weights=[2,1,3,1, 2, 4])[0]

            else:
                block_value_predict = self.block_value_predict[3]
                permanent_block_number = self.move_green_counter = choices([1,2,3,4, 5, 6], weights=[2,1,3,1, 2, 4])[0]


                block_value_predict[1]['state'] = DISABLED   
#  block_value_predict = [
#     dice_image_label,     # [0]
#     predict_button,       # [1]
#     entry_box,            # [2]
#     give_button           # [3]
# ]
        # self.block_value_predict[0] = red instruction information
        # self.block_value_predict[1] = sky_blue instruction information
        # self.block_value_predict[2] = yellow instruction information
        # self.block_value_predict[3] = green instruction information

        # self.block_value_predict[something][1] = Predict btn
        # self.block_value_predict[something][3] = Give btn
            # animation of coin floating
            temp_counter = 15
            while temp_counter>0:
                move_counter = randint(1, 6)
                block_value_predict[0]['image'] = self.block_number_side[move_counter - 1]
                self.window.update()
                time.sleep(0.1)
                temp_counter-=1

            print("Prediction result: ", permanent_block_number)

            # Permanent predicted value containing image set
            block_value_predict[0]['image'] = self.block_number_side[permanent_block_number-1]
            self.instructional_btn_customization_based_on_current_situation(color_indicator,permanent_block_number,block_value_predict)
        except:
            print("something went wrong!")

    def instructional_btn_customization_based_on_current_situation(self,color_indicator,permanent_block_number,block_value_predict):
        if color_indicator == "red":
            temp_coin_position = self.red_coin_position
        elif color_indicator == "green":
            temp_coin_position = self.green_coin_position
        elif color_indicator == "yellow":
            temp_coin_position = self.yellow_coin_position
        else:
            temp_coin_position = self.sky_blue_coin_position
        #sub conditions
        all_in = 1
        for i in range(4):
            if temp_coin_position[i] == -1:
                all_in = 1
            else:
                all_in = 0
                break

        if  permanent_block_number == 6:
            self.six_counter += 1
        else:
            self.six_counter = 0
        #main conditon
        if ((all_in == 1 and permanent_block_number == 6) or (all_in==0) and self.six_counter<3) : 
            permission = 1
            if color_indicator == "red":
                temp = self.red_coord_store
            elif color_indicator == "green":
                temp = self.green_coord_store
            elif color_indicator == "yellow":
                temp = self.yellow_coord_store
            else:
                temp = self.sky_blue_coord_store

            if  permanent_block_number<6:
                if self.six_with_overlap == 1: #got 6 + killed oponent on the same move
                    self.current_player_index-=1 #gives another chance to the same player
                    self.six_with_overlap=0
                for i in range(4):
                    if  temp[i] == -1:
                        permission=0
                    elif temp[i]>100:
                        if  temp[i]+permanent_block_number<=106:
                            permission=1
                            break
                        else:
                            permission=0
                    else:
                        permission=1
                        break
            else:
                for i in range(4):
                    if  temp[i]>100:
                        if  temp[i] + permanent_block_number <= 106:
                            permission = 1
                            break
                        else:
                            permission = 0
                    else:
                        permission = 1
                        break
            if permission == 0:
                self.start_next_turn()
            else:
                block_value_predict[3]['state'] = NORMAL# Give btn activation
                block_value_predict[1]['state'] = DISABLED# Predict btn deactivation

        else:
            block_value_predict[1]['state'] = NORMAL# Predict btn activation
            if self.six_with_overlap == 1:
                self.current_player_index -= 1
                self.six_with_overlap = 0
            self.start_next_turn()
        #one more chance if got 6
        if  permanent_block_number == 6 and self.six_counter<3 and block_value_predict[3]['state'] == NORMAL:  
            self.current_player_index-=1
        else:
            self.six_counter=0

    #predict , give and entry field
    def instruction_btn_red(self): 
        block_predict_red = Label(self.cvs,image=self.block_number_side[0])
        block_predict_red.place(x=45,y=15)
        predict_red = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Predict", font=("Arial", 8, "bold"), command=lambda: self.make_prediction("red"))
        predict_red.place(x=37, y=15 + 40) 
        entry_take_red = Entry(self.cvs,bg="white",fg="blue",font=("Arial",25,"bold","italic"),width=2,relief=SUNKEN,bd=5)
        entry_take_red.place(x=40,y=15+80) 
        final_move = Button(self.cvs,bg="black",fg="#00FF00",relief=RAISED,bd=5,text="Give",font=("Arial",8,"bold"),command=lambda: self.main_controller("red",entry_take_red.get()),state=DISABLED)
        final_move.place(x=42,y=15+140)
        Label(self.cvs,text="Player 1",bg="#4d4dff",fg="gold",font=("Arial",15,"bold")).place(x=15,y=15+140+40)
        self.store_instructional_btn(block_predict_red,predict_red,entry_take_red,final_move)

    def instruction_btn_sky_blue(self):
        block_predict_sky_blue = Label(self.cvs, image=self.block_number_side[0])
        block_predict_sky_blue.place(x=45, y=15+(40*6+40*3)+10)
        predict_sky_blue = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Predict",font=("Arial", 8, "bold"), command=lambda: self.make_prediction("sky_blue"))
        predict_sky_blue.place(x=37, y=15+(40*6+40*3)+40 + 10)
        entry_take_sky_blue = Entry(self.cvs, bg="white", fg="blue", font=("Arial", 25, "bold", "italic"), width=2,relief=SUNKEN, bd=5)
        entry_take_sky_blue.place(x=40, y=15+(40*6+40*3)+40 + 50)
        final_move = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Give", font=("Arial", 8, "bold"),command=lambda: self.main_controller("sky_blue",entry_take_sky_blue.get()),state=DISABLED)
        final_move.place(x=42, y=15+(40*6+40*3)+40 + 110)
        Label(self.cvs, text="Player 2", bg="#4d4dff", fg="gold", font=("Arial", 15, "bold")).place(x=15,y=15+(40*6+40*3)+40 + 110+ 40)
        self.store_instructional_btn(block_predict_sky_blue, predict_sky_blue, entry_take_sky_blue, final_move)

    def instruction_btn_yellow(self):
        block_predict_yellow = Label(self.cvs, image=self.block_number_side[0])
        block_predict_yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 10)+10, y=15 + (40 * 6 + 40 * 3) + 10)
        predict_yellow = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Predict",font=("Arial", 8, "bold"), command=lambda: self.make_prediction("yellow"))
        predict_yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+10, y=15 + (40 * 6 + 40 * 3) + 40 + 10)
        entry_take_yellow = Entry(self.cvs, bg="white", fg="blue", font=("Arial", 25, "bold", "italic"),width=2, relief=SUNKEN, bd=5)
        entry_take_yellow.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+13, y=15 + (40 * 6 + 40 * 3) + 40 + 50)
        final_move = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Give",font=("Arial", 8, "bold"),command=lambda: self.main_controller("yellow",entry_take_yellow.get()),state=DISABLED)
        final_move.place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 2)+17, y=15 + (40 * 6 + 40 * 3) + 40 + 110)
        Label(self.cvs, text="Player 3", bg="#4d4dff", fg="gold", font=("Arial", 15, "bold")).place(x=100 + (40 * 6 + 40 * 3 + 40 * 6 + 3),y=15 + (40 * 6 + 40 * 3) + 40 + 110 + 40)
        self.store_instructional_btn(block_predict_yellow, predict_yellow, entry_take_yellow, final_move)

    def instruction_btn_green(self):
        block_predict_green = Label(self.cvs, image=self.block_number_side[0])
        block_predict_green.place(x=100+(40*6+40*3+40*6+10)+10, y=15)
        predict_green = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Predict", font=("Arial", 8, "bold"), command=lambda: self.make_prediction("green"))
        predict_green.place(x=100+(40*6+40*3+40*6+2)+10, y=15 + 40)
        entry_take_green = Entry(self.cvs, bg="white", fg="blue", font=("Arial", 25, "bold", "italic"), width=2, relief=SUNKEN, bd=5)
        entry_take_green.place(x=100+(40*6+40*3+40*6+2)+13, y=15 + 80)
        final_move = Button(self.cvs, bg="black", fg="#00FF00", relief=RAISED, bd=5, text="Give",font=("Arial", 8, "bold"),command=lambda: self.main_controller("green",entry_take_green.get()),state=DISABLED)
        final_move.place(x=100+(40*6+40*3+40*6+2)+17, y=15 + 140)
        Label(self.cvs, text="Player 4", bg="#4d4dff", fg="gold", font=("Arial", 15, "bold")).place(x=100+(40*6+40*3+40*6+3), y=15 + 140+40)
        self.store_instructional_btn(block_predict_green, predict_green, entry_take_green, final_move)

    def store_instructional_btn(self, block_indicator, predictor, entry_controller, give_finally):
        temp = []
        temp.append(block_indicator)
        temp.append(predictor)
        temp.append(entry_controller)
        temp.append(give_finally)
        self.block_value_predict.append(temp)
        # self.block_value_predict[0] = red instruction information
        # self.block_value_predict[1] = sky_blue instruction information
        # self.block_value_predict[2] = yellow instruction information
        # self.block_value_predict[3] = green instruction information

        # self.block_value_predict[something][1] = Predict btn
        # self.block_value_predict[something][3] = Give btn


    def red_circle_start_position(self, coin_number):
        self.cvs.delete(self.red_coins[int(coin_number)-1])
        self.red_coins[int(coin_number)-1] = self.cvs.create_oval(100 + 40, 15+(40*6), 100 +40 + 40, 15+(40*6)+40, fill="red", width=3, outline="black")

        self.red_number_label[int(coin_number)-1].place_forget()
        red_start_label_x = 100 + 40 + 10
        red_start_label_y = 15 + (40 * 6) + 5
        self.red_number_label[int(coin_number)-1].place(x=red_start_label_x, y=red_start_label_y)

        self.red_coin_position[int(coin_number)-1] = 1
        self.window.update()
        time.sleep(0.2)


    def green_circle_start_position(self,coin_number):
        self.cvs.delete(self.green_coins[int(coin_number)-1])
        self.green_coins[int(coin_number)-1] = self.cvs.create_oval(100 + (40*8), 15 + 40, 100 +(40*9), 15 + 40+ 40, fill="#00FF00", width=3)

        self.green_number_label[int(coin_number)-1].place_forget()
        green_start_label_x = 100 + (40*8) + 10
        green_start_label_y = 15 + 40 + 5
        self.green_number_label[int(coin_number)-1].place(x=green_start_label_x, y=green_start_label_y)

        self.green_coin_position[int(coin_number)-1] = 14
        self.window.update()
        time.sleep(0.2)


    def yellow_circle_start_position(self,coin_number):
        self.cvs.delete(self.yellow_coins[int(coin_number)-1])
        self.yellow_coins[int(coin_number)-1] = self.cvs.create_oval(100 + (40 * 6)+(40*3)+(40*4), 15 + (40*8), 100 + (40 * 6)+(40*3)+(40*5), 15 + (40*9), fill="yellow", width=3)

        self.yellow_number_label[int(coin_number)-1].place_forget()
        yellow_start_label_x = 100 + (40 * 6)+(40*3)+(40*4) + 10
        yellow_start_label_y = 15 + (40*8) + 5
        self.yellow_number_label[int(coin_number) - 1].place(x=yellow_start_label_x, y=yellow_start_label_y)

        self.yellow_coin_position[int(coin_number) - 1] = 27
        self.window.update()
        time.sleep(0.2)


    def sky_blue_circle_start_position(self,coin_number):
        self.cvs.delete(self.blue_coins[int(coin_number)-1])
        self.blue_coins[int(coin_number)-1] = self.cvs.create_oval(100+240,340+(40*5)-5,100+240+40,340+(40*6)-5,fill="#04d9ff",width=3)

        self.sky_blue_number_label[int(coin_number)-1].place_forget()
        sky_blue_start_label_x = 100+240 + 10
        sky_blue_start_label_y = 340+(40*5)-5 + 5
        self.sky_blue_number_label[int(coin_number) - 1].place(x=sky_blue_start_label_x, y=sky_blue_start_label_y)

        self.sky_blue_coin_position[int(coin_number) - 1] = 40
        self.window.update()
        time.sleep(0.2)


    def main_controller(self, color_coin, coin_number):                                                                   #controls the predict and give button
        try:
            if not (4>=int(coin_number)>=1):
                messagebox.showerror("Wrong input number","Please input the coin number between 1 to 4")
                return
        except:
            pass
            
        if  color_coin == "red":
            self.block_value_predict[0][3]['state'] = DISABLED   #disable give after clicked onces

        
            if self.red_coin_position[int(coin_number)-1] == -1 and self.move_red_counter == 6:
                self.red_circle_start_position(coin_number)
                self.red_coord_store[int(coin_number) - 1] = 1

            elif self.red_coin_position[int(coin_number)-1] > -1:
                take_coord = self.cvs.coords(self.red_coins[int(coin_number)-1])
                red_start_label_x = take_coord[0] + 10
                red_start_label_y = take_coord[1] + 5
                self.red_number_label[int(coin_number) - 1].place(x=red_start_label_x, y=red_start_label_y)

                if self.red_coin_position[int(coin_number)-1]+self.move_red_counter<=106:                                             #red_coin holds the shapes(oval)
                   self.red_coin_position[int(coin_number)-1] = self.motion_of_coin(self.red_coin_position[int(coin_number) - 1],self.red_coins[int(coin_number)-1],self.red_number_label[int(coin_number)-1],red_start_label_x,red_start_label_y,"red",self.move_red_counter)
                else:
                   messagebox.showerror("Not possible","Sorry, not permitted")
                   self.block_value_predict[0][3]['state'] = NORMAL
                   return

                if not self.red_coin_position[int(coin_number)-1]==22 or self.red_coin_position[int(coin_number)-1]==9 or self.red_coin_position[int(coin_number)-1]==48 or self.red_coin_position[int(coin_number)-1]==35 or self.red_coin_position[int(coin_number)-1]==14 or self.red_coin_position[int(coin_number)-1]==27 or self.red_coin_position[int(coin_number)-1]==40:
                    if self.red_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.red_coin_position[int(coin_number)-1],color_coin, self.move_red_counter)

                self.red_coord_store[int(coin_number)-1] = self.red_coin_position[int(coin_number)-1]

            else:
                messagebox.showerror("Wrong choice","Sorry, Your coin in not permitted to travel")
                self.block_value_predict[0][3]['state'] = NORMAL
                return

            self.block_value_predict[0][1]['state'] = NORMAL


        elif color_coin == "green":
            self.block_value_predict[3][3]['state'] = DISABLED

            if self.green_coin_position[int(coin_number) - 1] == -1 and self.move_green_counter == 6:
                self.green_circle_start_position(coin_number)
                self.green_coord_store[int(coin_number) - 1] = 14

            elif self.green_coin_position[int(coin_number) - 1] > -1:
                take_coord = self.cvs.coords(self.green_coins[int(coin_number) - 1])
                green_start_label_x = take_coord[0] + 10
                green_start_label_y = take_coord[1] + 5
                self.green_number_label[int(coin_number) - 1].place(x=green_start_label_x, y=green_start_label_y)


                if  self.green_coin_position[int(coin_number) - 1] + self.move_green_counter <= 106:
                    self.green_coin_position[int(coin_number) - 1] = self.motion_of_coin(self.green_coin_position[int(coin_number) - 1], self.green_coins[int(coin_number) - 1], self.green_number_label[int(coin_number) - 1], green_start_label_x, green_start_label_y, "green", self.move_green_counter)
                else:
                   messagebox.showerror("Not possible","No path available")
                   self.block_value_predict[3][3]['state'] = NORMAL
                   return


                if  self.green_coin_position[int(coin_number)-1]==22 or self.green_coin_position[int(coin_number)-1]==9 or self.green_coin_position[int(coin_number)-1]==48 or self.green_coin_position[int(coin_number)-1]==35 or self.green_coin_position[int(coin_number)-1]==1 or self.green_coin_position[int(coin_number)-1]==27 or self.green_coin_position[int(coin_number)-1]==40:
                    pass
                else:
                    if self.green_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.green_coin_position[int(coin_number) - 1],color_coin, self.move_green_counter)

                self.green_coord_store[int(coin_number) - 1] = self.green_coin_position[int(coin_number) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.block_value_predict[3][3]['state'] = NORMAL
                return

            self.block_value_predict[3][1]['state'] = NORMAL


        elif color_coin == "yellow":
            self.block_value_predict[2][3]['state'] = DISABLED

            if self.yellow_coin_position[int(coin_number) - 1] == -1 and self.move_yellow_counter == 6:
                self.yellow_circle_start_position(coin_number)
                self.yellow_coord_store[int(coin_number) - 1] = 27

            elif self.yellow_coin_position[int(coin_number) - 1] > -1:
                take_coord = self.cvs.coords(self.yellow_coins[int(coin_number) - 1])
                yellow_start_label_x = take_coord[0] + 10
                yellow_start_label_y = take_coord[1] + 5
                self.yellow_number_label[int(coin_number) - 1].place(x=yellow_start_label_x, y=yellow_start_label_y)

                if  self.yellow_coin_position[int(coin_number) - 1] + self.move_yellow_counter <= 106:
                    self.yellow_coin_position[int(coin_number) - 1] = self.motion_of_coin(self.yellow_coin_position[int(coin_number) - 1], self.yellow_coins[int(coin_number) - 1], self.yellow_number_label[int(coin_number) - 1], yellow_start_label_x, yellow_start_label_y, "yellow", self.move_yellow_counter)
                else:
                   messagebox.showerror("Not possible","No path available")
                   self.block_value_predict[2][3]['state'] = NORMAL
                   return

                if  self.yellow_coin_position[int(coin_number)-1]==22 or self.yellow_coin_position[int(coin_number)-1]==9 or self.yellow_coin_position[int(coin_number)-1]==48 or self.yellow_coin_position[int(coin_number)-1]==35 or self.yellow_coin_position[int(coin_number)-1]==1 or self.yellow_coin_position[int(coin_number)-1]==14 or self.yellow_coin_position[int(coin_number)-1]==40:
                    pass
                else:
                    if self.yellow_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.yellow_coin_position[int(coin_number) - 1],color_coin, self.move_yellow_counter)

                self.yellow_coord_store[int(coin_number) - 1] = self.yellow_coin_position[int(coin_number) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.block_value_predict[2][3]['state'] = NORMAL
                return

            self.block_value_predict[2][1]['state'] = NORMAL


        elif color_coin == "sky_blue":
            self.block_value_predict[1][3]['state'] = DISABLED
            
            if self.sky_blue_coin_position[int(coin_number) - 1] == -1 and self.move_sky_blue_counter == 6:
                self.sky_blue_circle_start_position(coin_number)
                self.sky_blue_coord_store[int(coin_number) - 1] = 40

            elif self.sky_blue_coin_position[int(coin_number) - 1] > -1:
                take_coord = self.cvs.coords(self.blue_coins[int(coin_number) - 1])
                sky_blue_start_label_x = take_coord[0] + 10
                sky_blue_start_label_y = take_coord[1] + 5
                self.sky_blue_number_label[int(coin_number) - 1].place(x=sky_blue_start_label_x, y=sky_blue_start_label_y)

                if  self.sky_blue_coin_position[int(coin_number) - 1] + self.move_sky_blue_counter <= 106:
                    self.sky_blue_coin_position[int(coin_number) - 1] = self.motion_of_coin(self.sky_blue_coin_position[int(coin_number) - 1], self.blue_coins[int(coin_number) - 1], self.sky_blue_number_label[int(coin_number) - 1], sky_blue_start_label_x, sky_blue_start_label_y, "sky_blue", self.move_sky_blue_counter)
                else:
                   messagebox.showerror("Not possible","No path available")
                   self.block_value_predict[1][3]['state'] = NORMAL
                   return

                if  self.sky_blue_coin_position[int(coin_number)-1]==22 or self.sky_blue_coin_position[int(coin_number)-1]==9 or self.sky_blue_coin_position[int(coin_number)-1]==48 or self.sky_blue_coin_position[int(coin_number)-1]==35 or self.sky_blue_coin_position[int(coin_number)-1]==1 or self.sky_blue_coin_position[int(coin_number)-1]==14 or self.sky_blue_coin_position[int(coin_number)-1]==27:
                    pass
                else:
                    if self.sky_blue_coin_position[int(coin_number) - 1] < 100:
                        self.coord_overlap(self.sky_blue_coin_position[int(coin_number) - 1],color_coin, self.move_sky_blue_counter) #only 1-6

                self.sky_blue_coord_store[int(coin_number) - 1] = self.sky_blue_coin_position[int(coin_number) - 1]

            else:
                messagebox.showerror("Wrong choice", "Sorry, Your coin in not permitted to travel")
                self.block_value_predict[1][3]['state'] = NORMAL
                return

            self.block_value_predict[1][1]['state'] = NORMAL

        print("reds",self.red_coord_store)
        print("green",self.green_coord_store)
        print("yellows",self.yellow_coord_store)
        print("blues",self.sky_blue_coord_store)

        permission_granted_to_proceed = True

        if  color_coin == "red" and self.red_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)
        elif  color_coin == "green" and self.green_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)
        elif  color_coin == "yellow" and self.yellow_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)
        elif  color_coin == "sky_blue" and self.sky_blue_coin_position[int(coin_number)-1] == 106:
            permission_granted_to_proceed = self.check_winner_and_runner(color_coin)

        if permission_granted_to_proceed:# if that is False, Game is over and not proceed more
            self.start_next_turn()

 #counter_coin - current position of coin
 #specific_coin- the canvas obj(oval)
 #number_label- number shown on top of coin
 #path_counter - dice value. ie- no. of steps to move

    def motion_of_coin(self,counter_coin,specific_coin,number_label,number_label_x ,number_label_y,color_coin,path_counter): #animates the coin one block at a time, updating both the coin's position and its number label.
        number_label.place(x=number_label_x,y=number_label_y)
        while True:
            if path_counter == 0:
                break
            elif (counter_coin == 51 and color_coin == "red") or (counter_coin==12 and color_coin == "green") or (counter_coin == 25 and color_coin == "yellow") or (counter_coin == 38 and color_coin == "sky_blue") or counter_coin>=100:
                if counter_coin<100:
                    counter_coin=100
                counter_coin = self.under_room_traversal_control(specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin, color_coin)

                if  counter_coin == 106:
                    messagebox.showinfo("Destination reached","Congrats! You now at the destination")
                    if path_counter == 6:
                        self.six_with_overlap = 1
                    else:
                        self.current_player_index -= 1
                break

            counter_coin += 1
            path_counter -=1
            number_label.place_forget()

            print("counter coin:",counter_coin)

            if counter_coin<=5:
                self.cvs.move(specific_coin, 40, 0)
                number_label_x+=40
            elif counter_coin == 6:
                self.cvs.move(specific_coin, 40, -40)
                number_label_x += 40
                number_label_y-=40
            elif 6< counter_coin <=11:
                self.cvs.move(specific_coin, 0, -40)
                number_label_y -= 40
            elif counter_coin <=13:
                self.cvs.move(specific_coin, 40, 0)
                number_label_x += 40
            elif counter_coin <=18:
                self.cvs.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin == 19:
                self.cvs.move(specific_coin, 40, 40)
                number_label_x += 40
                number_label_y += 40
            elif counter_coin <=24:
                self.cvs.move(specific_coin, 40, 0)
                number_label_x += 40
            elif counter_coin <=26:
                self.cvs.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin <=31:
                self.cvs.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif counter_coin == 32:
                self.cvs.move(specific_coin, -40, 40)
                number_label_x -= 40
                number_label_y += 40
            elif counter_coin <= 37:
                self.cvs.move(specific_coin, 0, 40)
                number_label_y += 40
            elif counter_coin <= 39:
                self.cvs.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif counter_coin <= 44:
                self.cvs.move(specific_coin, 0, -40)
                number_label_y -= 40
            elif counter_coin == 45:
                self.cvs.move(specific_coin, -40, -40)
                number_label_x -= 40
                number_label_y -= 40
            elif counter_coin <= 50:
                self.cvs.move(specific_coin, -40, 0)
                number_label_x -= 40
            elif 50< counter_coin <=52:
                self.cvs.move(specific_coin, 0, -40)
                number_label_y -= 40
            elif counter_coin == 53:
                self.cvs.move(specific_coin, 40, 0)
                number_label_x += 40
                counter_coin = 1

            number_label.place_forget()
            number_label.place(x=number_label_x, y=number_label_y)

            self.window.update()
            time.sleep(0.2)

        return counter_coin

    # For same position, previous coin deleted and set to the room
    def coord_overlap(self, counter_coin, color_coin, path_to_traverse_before_overlap):
        if  color_coin!="red":
            for take_player_num in range(len(self.red_coord_store)):
                if  self.red_coord_store[take_player_num] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap=1
                    else:
                        self.current_player_index-=1

                    self.cvs.delete(self.red_coins[take_player_num])
                    self.red_number_label[take_player_num].place_forget()
                    self.red_coin_position[take_player_num] = -1
                    self.red_coord_store[take_player_num] = -1

                    if take_player_num == 0:
                       remade_coin = self.cvs.create_oval(100+40, 15+40, 100+40+40, 15+40+40, width=3, fill="red", outline="black")
                       self.red_number_label[take_player_num].place(x=100 + 40 + 10, y=15 + 40 + 5)
                    elif take_player_num == 1:
                        remade_coin = self.cvs.create_oval(100+40+60+60, 15 + 40, 100+40+60+60+40, 15 + 40 + 40, width=3, fill="red", outline="black")
                        self.red_number_label[take_player_num].place(x=100 + 40 + 60 +60 + 10, y=15 + 40 + 5)
                    elif take_player_num == 2:
                        remade_coin = self.cvs.create_oval(100 + 40 + 60 + 60, 15 + 40 + 100, 100 + 40 + 60 + 60 + 40, 15 + 40 + 40 + 100, width=3, fill="red", outline="black")
                        self.red_number_label[take_player_num].place(x=100 + 40 + 60 + 60 + 10, y=15 + 40 + 100 + 5)
                    else:
                        remade_coin = self.cvs.create_oval(100 + 40, 15 + 40+100, 100 + 40 + 40, 15 + 40 + 40+100, width=3,fill="red", outline="black")
                        self.red_number_label[take_player_num].place(x=100 + 40 + 10, y=15 + 40 + 100 + 5)

                    self.red_coins[take_player_num]=remade_coin

        if  color_coin != "green":
            for take_player_num in range(len(self.green_coord_store)):
                if  self.green_coord_store[take_player_num] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap = 1
                    else:
                        self.current_player_index-=1    

                    self.cvs.delete(self.green_coins[take_player_num])
                    self.green_number_label[take_player_num].place_forget()
                    self.green_coin_position[take_player_num] = -1
                    self.green_coord_store[take_player_num] = -1

                    if take_player_num == 0:
                        remade_coin = self.cvs.create_oval(340+(40*3)+40, 15 + 40, 340+(40*3)+40 + 40, 15 + 40 + 40, width=3, fill="#00FF00", outline="black")
                        self.green_number_label[take_player_num].place(x=340 + (40 * 3) + 40 + 10, y=15 + 40 + 5)
                    elif take_player_num == 1:
                        remade_coin = self.cvs.create_oval(340+(40*3)+40+ 60 + 40+20, 15 + 40, 340+(40*3)+40 + 60 + 40 + 40+20, 15 + 40 + 40, width=3, fill="#00FF00", outline="black")
                        self.green_number_label[take_player_num].place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 5)
                    elif take_player_num == 2:
                        remade_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 15 + 40 + 100, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 15 + 40 + 40 + 100, width=3, fill="#00FF00", outline="black")
                        self.green_number_label[take_player_num].place(x=340 + (40 * 3) + 40 + 40 + 60 + 30, y=15 + 40 + 100 + 5)
                    else:
                        remade_coin = self.cvs.create_oval(340+(40*3)+40, 15 + 40 + 100, 340+(40*3)+40 + 40, 15 + 40 + 40 + 100, width=3, fill="#00FF00", outline="black")
                        self.green_number_label[take_player_num].place(x=340+(40*3) + 40 + 10, y=15 + 40 + 100 + 5)

                    self.green_coins[take_player_num] = remade_coin


        if  color_coin != "yellow":
            for take_player_num in range(len(self.yellow_coord_store)):
                if  self.yellow_coord_store[take_player_num] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap = 1
                    else:
                        self.current_player_index -= 1

                    self.cvs.delete(self.yellow_coins[take_player_num])
                    self.yellow_number_label[take_player_num].place_forget()
                    self.yellow_coin_position[take_player_num] = -1
                    self.yellow_coord_store[take_player_num] = -1

                    if take_player_num == 0:
                        remade_coin = self.cvs.create_oval(340 + (40 * 3) + 40, 340+80+15, 340 + (40 * 3) + 40 + 40, 340+80+40+15, width=3, fill="yellow", outline="black")
                        self.yellow_number_label[take_player_num].place(x=340+(40*3) + 40 + 10, y=30 + (40*6)+(40*3)+40+10)
                    elif take_player_num == 1:
                        remade_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340+80+15, 340 + (40 * 3) + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="yellow", outline="black")
                        self.yellow_number_label[take_player_num].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+10)
                    elif take_player_num == 2:
                        remade_coin = self.cvs.create_oval(340 + (40 * 3) + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 340 + (40 * 3) + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="yellow", outline="black")
                        self.yellow_number_label[take_player_num].place(x=340+(40*3)+ 40 + 40+ 60 + 30, y=30 + (40*6)+(40*3)+40+100+10)
                    else:
                        remade_coin = self.cvs.create_oval(340 + (40 * 3) + 40, 340+80+60+40+15, 340 + (40 * 3) + 40 + 40,340+80+60+40+40+15, width=3, fill="yellow", outline="black")
                        self.yellow_number_label[take_player_num].place(x=340 + (40 * 3) + 40 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 100 + 10)

                    self.yellow_coins[take_player_num] = remade_coin

        if  color_coin != "sky_blue":
            for take_player_num in range(len(self.sky_blue_coord_store)):
                if  self.sky_blue_coord_store[take_player_num] == counter_coin:
                    if path_to_traverse_before_overlap == 6:
                        self.six_with_overlap = 1
                    else:
                        self.current_player_index -= 1

                    self.cvs.delete(self.blue_coins[take_player_num])
                    self.sky_blue_number_label[take_player_num].place_forget()
                    self.sky_blue_coin_position[take_player_num] = -1
                    self.sky_blue_coord_store[take_player_num]=-1

                    if take_player_num == 0:
                        remade_coin = self.cvs.create_oval(100 + 40, 340+80+15, 100 + 40 + 40, 340+80+40+15, width=3, fill="#04d9ff", outline="black")
                        self.sky_blue_number_label[take_player_num].place(x=100+40+10, y=30 + (40*6)+(40*3)+40+10)
                    elif take_player_num == 1:
                        remade_coin = self.cvs.create_oval(100 + 40 + 60 + 40+20, 340+80+15, 100 + 40 + 60 + 40 + 40+20, 340+80+40+15, width=3, fill="#04d9ff", outline="black")
                        self.sky_blue_number_label[take_player_num].place(x=100 + 40 + 60 +60 + 10, y=30 + (40*6)+(40*3)+40+10)
                    elif take_player_num == 2:
                        remade_coin = self.cvs.create_oval(100 + 40 + 60 + 40 + 20, 340 + 80 + 60 + 40 + 15, 100 + 40 + 60 + 40 + 40 + 20, 340 + 80 + 60 + 40 + 40 + 15, width=3, fill="#04d9ff", outline="black")
                        self.sky_blue_number_label[take_player_num].place(x=100 + 40 + 60 + 60 + 10, y=30 + (40 * 6) + (40 * 3) + 40 + 60 + 40 + 10)
                    else:
                        remade_coin = self.cvs.create_oval( 100 + 40, 340+80+60+40+15, 100 + 40 + 40, 340+80+60+40+40+15, width=3, fill="#04d9ff", outline="black")
                        self.sky_blue_number_label[take_player_num].place(x=100+40+10, y=30 + (40*6)+(40*3)+40+60+40+10)

                    self.blue_coins[take_player_num] = remade_coin


    def under_room_traversal_control(self,specific_coin,number_label,number_label_x,number_label_y,path_counter,counter_coin,color_coin):
        if color_coin == "red" and counter_coin >= 100:
            if int(counter_coin)+int(path_counter)<=106:
               counter_coin = self.room_red_traversal(specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin)

        elif color_coin == "green" and counter_coin >= 100:
            if  int(counter_coin) + int(path_counter) <= 106:
                counter_coin = self.room_green_traversal(specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin)

        elif color_coin == "yellow" and counter_coin >= 100:
            if  int(counter_coin) + int(path_counter) <= 106:
                counter_coin = self.room_yellow_traversal(specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin)

        elif color_coin == "sky_blue" and counter_coin >= 100:
            if  int(counter_coin) + int(path_counter) <= 106:
                counter_coin = self.room_sky_blue_traversal(specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin)

        return counter_coin


    def room_red_traversal(self, specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin):
        while path_counter>0:
            counter_coin += 1
            path_counter -= 1
            self.cvs.move(specific_coin, 40, 0)
            number_label_x+=40
            number_label.place(x=number_label_x,y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def room_green_traversal(self, specific_coin, number_label, number_label_x, number_label_y, path_counter, counter_coin):
        while path_counter > 0:
            counter_coin += 1
            path_counter -= 1
            self.cvs.move(specific_coin, 0, 40)
            number_label_y += 40
            number_label.place(x=number_label_x, y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def room_yellow_traversal(self, specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin):
        while path_counter > 0:
            counter_coin += 1
            path_counter -= 1
            self.cvs.move(specific_coin, -40, 0)
            number_label_x -= 40
            number_label.place(x=number_label_x, y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def room_sky_blue_traversal(self, specific_coin, number_label, number_label_x, number_label_y,path_counter,counter_coin):
        while path_counter > 0:
            counter_coin += 1
            path_counter -= 1
            self.cvs.move(specific_coin, 0, -40)
            number_label_y -= 40
            number_label.place(x=number_label_x, y=number_label_y)
            self.window.update()
            time.sleep(0.2)
        return counter_coin

    def check_winner_and_runner(self,color_coin):
        destination_reached = 0 # Check for all specific color coins
        if color_coin == "red":
            temp_store = self.red_coord_store
            temp_delete = 0# Player index
        elif color_coin == "green":
            temp_store = self.green_coord_store
            temp_delete = 3# Player index
        elif color_coin == "yellow":
            temp_store = self.yellow_coord_store
            temp_delete = 2# Player index
        else:
            temp_store = self.sky_blue_coord_store
            temp_delete = 1# Player index

        for take in temp_store:
            if take == 106:
                destination_reached = 1
            else:
                destination_reached = 0
                break

        if  destination_reached == 1:# If all coins reached to the destination, winner and runner check
            self.take_permission += 1
            if self.take_permission == 1:# Winner check
                messagebox.showinfo("Winner","Congrats! You are the winner")
            elif self.take_permission == 2:# 1st runner check
                messagebox.showinfo("Winner", "Wow! You are 1st runner")
            elif self.take_permission == 3:# 2nd runner check
                messagebox.showinfo("Winner", "Wow! You are 2nd runner")

            self.block_value_predict[temp_delete][1]['state'] = DISABLED
            self.total_people_play.remove(temp_delete)

            if len(self.total_people_play) == 1:
                messagebox.showinfo("Game Over","Good bye!!!!")
                self.block_value_predict[0][1]['state'] = DISABLED
                return False
            else:
                self.current_player_index-=1
        else:
            print("Winner not decided")

        return True




window = Tk()
window.geometry("800x630")
window.maxsize(800,630)
window.minsize(800,630)
window.title("LUDO WITH ADI")
window.iconbitmap("Images/ludo_icon.ico")
block_six_side = ImageTk.PhotoImage(Image.open("Images/6_block.png").resize((33, 33)))
block_five_side = ImageTk.PhotoImage(Image.open("Images/5_block.png").resize((33, 33)))
block_four_side = ImageTk.PhotoImage(Image.open("Images/4_block.png").resize((33, 33)))
block_three_side = ImageTk.PhotoImage(Image.open("Images/3_block.png").resize((33, 33)))
block_two_side = ImageTk.PhotoImage(Image.open("Images/2_block.png").resize((33, 33)))
block_one_side = ImageTk.PhotoImage(Image.open("Images/1_block.png").resize((33, 33)))
Ludo(window,block_six_side,block_five_side,block_four_side,block_three_side,block_two_side,block_one_side)
window.mainloop()