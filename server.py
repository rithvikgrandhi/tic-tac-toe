import socket 
import pickle 


from tic_tac_toe import TicTacToe

HOST = '10.20.206.242' 
PORT = 5025      

 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)


client_socket, client_address = s.accept()
print(f"\nNow Connnected to {client_address}!")

player_x = TicTacToe("X")


rematch = True

while rematch == True:
     
    print(f"\n\n T I C - T A C - T O E ")

   
    while player_x.did_win("X") == False and player_x.did_win("O") == False and player_x.is_draw() == False:
       
        print(f"\n       Your turn!")
        player_x.draw_grid()
        player_coord = input(f"Enter coordinate: ")
        player_x.edit_square(player_coord)

        
        player_x.draw_grid()

        
        x_symbol_list = pickle.dumps(player_x.symbol_list)
        client_socket.send(x_symbol_list)

        
        if player_x.did_win("X") == True or player_x.is_draw() == True:
            break

        
        print(f"\nWaiting for other player...")
        o_symbol_list = client_socket.recv(1024)
        o_symbol_list = pickle.loads(o_symbol_list)
        player_x.update_symbol_list(o_symbol_list)

    
    if player_x.did_win("X") == True:
        print(f"Congrats, you won!")
       
        f = open("scores.txt", "a")
        f.write("client Lost\n")
        f.close()
   
        
    elif player_x.is_draw() == True:
        print(f"It's a draw!")
        f = open("scores.txt", "a")
        f.write("draw\n")
        f.close()  
    else:
        print(f"Sorry, the client won.")
        f = open("scores.txt", "a")
        f.write("client won\n")

        f.close()

     
    
   
    
    
    client_response = ""
    print(f"Waiting for client response...")
    client_response = client_socket.recv(1024)
    client_response = pickle.loads(client_response)

        
    if client_response == "N":
        print(f"\nThe client does not want a rematch.")
        rematch = False

    else:
        player_x.restart()

spacer = input(f"\nThank you for playing!\nPress enter to quit...\n")

client_socket.close()