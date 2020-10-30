from rastros import *

N_CAMP = 20

def distancia (a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def moves_from_point(point, visited_squares, state):
        alladjacent = [(point[0]+a, point[1]+b) for a in [-1,0,1] for b in [-1,0,1]]
        return [p for p in alladjacent
                if p not in state.blacks and p not in visited_squares and p !=point and p in state.fullboard]
                
def distancia_42 (a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def moves_from_point_42(point, visited_squares, state):
        alladjacent = [(point[0]+a, point[1]+b) for a in [-1,0,1] for b in [-1,0,1]]
        return [p for p in alladjacent
                if p not in state.blacks and p not in visited_squares and p !=point and p in state.fullboard]
                
######################



#jogador42 = Jogador("jogador42",
 #                 lambda game, state:
  #                alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_42))


################################################################################################
### OUTRAS FUNÇÕES #############################################################################
                  
def near_goal_situation_win36(state, player, goal):    
    return (distancia(state.white, goal) <= 2
            and (distancia(state.white, goal) <= 1 
                 or (player == "S" 
                     and (7,1) not in state.blacks and (7,2) not in state.blacks and (8,2) not in state.blacks
                     and (state.white == (6,3) or (6,3) in state.blacks) 
                     and (((state.white == (6,1) or (6,1) in state.blacks) and (state.white == (8,3) or (8,3) in state.blacks))                   
                         or ((state.white == (6,2) or (6,2) in state.blacks) and (state.white == (7,3) or (7,3) in state.blacks)))
                    )    
                 or (player == "N" 
                     and (1,7) not in state.blacks and (2,7) not in state.blacks and (2,8) not in state.blacks
                     and (state.white == (3,6) or (3,6) in state.blacks) 
                     and (((state.white == (1,6) or (1,6) in state.blacks) and (state.white == (3,8) or (3,8) in state.blacks))                   
                         or ((state.white == (2,6) or (2,6) in state.blacks) and (state.white == (3,7) or (3,7) in state.blacks))))
                 )
            )
def forced_path36(state, player, goal, no_goal, p_moves):
    if len(p_moves) < 2:
        visited_squares = set()
        visited_squares.add(state.white) 
        from_point = None
        while len(p_moves) == 1:
            from_point = p_moves[0]
            p_moves = moves_from_point(from_point,visited_squares,state)
            visited_squares.add(from_point)        
        if len(p_moves) == 0:
            if from_point == goal:
                return 3
            elif from_point == no_goal:
                return -3
            elif (len(visited_squares) - 1) % 2 == 0:
                return -2 if state.to_move == player else 3
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 2 if state.to_move == player else -3
    return 0
def general_eval36(moves, state, goal):
    move_score = 0
    num_moves = 0
    for move in moves:        
        for sub_move in moves_from_point(move,[state.white],state):
            s_score = distancia(move, goal) - distancia(sub_move,goal)
            move_score += s_score
            num_moves += 1
    if num_moves == 0:
        return 3
    return (move_score / num_moves)    
def fun_aval_436(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)        
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    if distancia(state.white, no_goal) <= 2:
        return -1.5        
    return general_eval36(moves, state, goal)
jogador436 = Jogador("jogador436",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_436))
                  
def fun_aval_4362(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)        
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    if distancia(state.white, no_goal) <= 1:
        return -1.5        
    return general_eval36(moves, state, goal)
jogador4362 = Jogador("jogador4362",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4362))
                  
def fun_aval_4363(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)        
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    return general_eval36(moves, state, goal)
jogador4363 = Jogador("jogador4363",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4363))

def test_forced_path_42(state, player, goal, no_goal, moves):
    def forced_path(move, p_moves):
        if len(p_moves) < 2:
            visited_squares = set()
            visited_squares.add(state.white)
            visited_squares.add(move)
            from_point = None
            while len(p_moves) == 1:
                from_point = p_moves[0]
                p_moves = moves_from_point_42(from_point,visited_squares,state)
                visited_squares.add(from_point)        
            if len(p_moves) == 0:
                if from_point == goal:
                    return 1
                elif from_point == no_goal:
                    return -1
                elif (len(visited_squares) - 1) % 2 == 0:
                    return -1 if state.to_move == player else 1
                elif (len(visited_squares) - 1) % 2 == 1:                
                    return 1 if state.to_move == player else -1
        return 0    
    has_zero = False
    for move in moves:
        forced_path_res = forced_path(move, moves_from_point_42(move,[state.white], state))
        if forced_path_res == 3:
            return 1
        elif forced_path_res == 0:
            has_zero = True
    if not has_zero:
        return -1 if state.to_move == player else 1
    return 0
def test_near_goal_certain_win_42(state, goal):
    def result(sub_state, move):
        blacks = sub_state.blacks.copy()
        blacks.add(sub_state.white)
        return EstadoRastros(to_move=('N' if sub_state.to_move == 'S' else 'S'),white=move,blacks=blacks)            
    def retreat(sub_state):
        for move in sub_state.moves():
            if distancia_42(move, goal) >= distancia_42(sub_state.white, goal):
                    if not approach_win(result(sub_state, move)):
                        return True
        return False    
    def approach_win(sub_state):
        has_approach = False
        for move in sub_state.moves():
            if distancia_42(move, goal) < distancia_42(sub_state.white, goal):
                has_approach = True
                if (move != goal) and retreat(result(sub_state, move)):
                    return False
        return has_approach    
    return approach_win(state)

def fun_aval_439(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3        
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 2:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador439 = Jogador("jogador439",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439))
                  
def fun_aval_4391(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3        
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4391 = Jogador("jogador4391",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4391))
                  
def fun_aval_4392(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3        
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 2:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4392 = Jogador("jogador4392",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4392))
                  
def fun_aval_4393(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 2:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4393 = Jogador("jogador4393",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4393))
                  
def fun_aval_4394(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3        
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4394 = Jogador("jogador4394",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4394))
                  
def fun_aval_4395(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4395 = Jogador("jogador4395",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4395))
                  
def fun_aval_4396(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5     
    return general_eval36(moves, state, goal)
jogador4396 = Jogador("jogador4396",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4396))
                  
def fun_aval_4397(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if dist_white_goal <= 3 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4397 = Jogador("jogador4397",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4397))
                  
def fun_aval_4398(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if dist_white_goal <= 3 and test_near_goal_certain_win_42(state, goal):
        return 2.5    
    return general_eval36(moves, state, goal)
jogador4398 = Jogador("jogador4398",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4398))
                  
def fun_aval_4399(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    if len(state.moves()) == 0:
        return -3 if state.to_move == player else 3
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador4399 = Jogador("jogador4399",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_4399))
                  
def fun_aval_43999(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    if len(state.moves()) == 0:
        return -3 if state.to_move == player else 3
    if near_goal_situation_win36(state, player, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador43999 = Jogador("jogador43999",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_43999))
                  
def fun_aval_439990(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    if len(state.moves()) == 0:
        return -3 if state.to_move == player else 3
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador439990 = Jogador("jogador439990",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439990))
                  
def fun_aval_439991(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    forced_path_res = forced_path36(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res 
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval36(moves, state, goal)
jogador439991 = Jogador("jogador439991",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439991))
                  
def general_eval361(moves, state, goal):
    move_score = 0
    num_moves = 0
    seen = set()
    seen.add(state.white)
    for move in moves:
        for sub_move in moves_from_point(move,seen,state):
            s_score = distancia(move, goal) - distancia(sub_move,goal)
            move_score += s_score
            num_moves += 1
        seen.add(move)
    if num_moves == 0:
        return 3
    return (move_score / num_moves)
def fun_aval_439992(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    if len(moves) == 0:
        return -3 if state.to_move == player else 3
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval361(moves, state, goal)
jogador439992 = Jogador("jogador439992",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439992))
                  
def fun_aval_439993(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3        
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval361(moves, state, goal)
jogador439993 = Jogador("jogador439993",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439993))
                  
def fun_aval_439994(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()    
    forced_path = test_forced_path_42(state, player, goal, no_goal, moves)
    if forced_path == 1:
        return 3
    elif forced_path == -1:
        return -3
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval361(moves, state, goal)
jogador439994 = Jogador("jogador439994",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439994))
                  
def fun_aval_439995(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)               
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    dist_white_goal = distancia_42(state.white, goal)
    if dist_white_goal <= 1:
        return 3           
    moves = state.moves()
    if len(moves) == 0:
        return -3 if state.to_move == player else 3     
    if dist_white_goal <= 2 and test_near_goal_certain_win_42(state, goal):
        return 2.5
    if distancia_42(state.white, no_goal) <= 1:
        return -1.5          
    return general_eval361(moves, state, goal)
jogador439995 = Jogador("jogador439995",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439995))
                  
#########################################################################################################


import multiprocessing
import dill
import sys
dill.settings['recurse'] = True
def run_dill_encoded(payload):
    fun, args = dill.loads(payload)
    return fun(*args)
    
def noprint_faz_campeonato(nc,listaJogadores,nsec,verbose):
    print(str(nc + 1) + " ", end='')    
    campeonato = jogaRastrosNN(listaJogadores, listaJogadores, nsec)
    if verbose:
        print("\nZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
        print("CAMPEONATO " + str(nc + 1))
        for jogo in campeonato:
            mostraJogo(jogo[2][0], verbose = True)
        print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    resultado_jogos = [(a,b,n) for (a,b,(x,n)) in campeonato]
    tabela = dict([(jog.nome, 0) for jog in listaJogadores])
    for jogo in resultado_jogos:
        if jogo[2] == 1:
            tabela[jogo[0]] += 1
        else:
            tabela[jogo[1]] += 1
    classificacao = list(tabela.items())
    classificacao.sort(key=lambda p: -p[1])
    sys.stdout.flush()
    return classificacao
    
def n_faz_campeonato(num_campeonatos, listaJogadores, nsec=5, verbose = False):
    print("Progresso com " + str(num_campeonatos) + " campeonatos: ", end='')
    sys.stdout.flush()
    pool = multiprocessing.Pool(processes=4)
    classificacao_list = []
    for nc in range(num_campeonatos):
        classificacao = pool.apply_async(run_dill_encoded,(dill.dumps((noprint_faz_campeonato,(nc,listaJogadores,nsec,verbose))),))
        classificacao_list.append(classificacao)
    pool.close()
    pool.join()
    jogador_vitorias = {}
    for classificacao in classificacao_list:
        classificacao = classificacao.get()
        for jog in classificacao:
            jogador_vitorias[jog[0]] = jogador_vitorias.get(jog[0],0) + jog[1] 
    
    print("\nJOGADOR", "VITÓRIAS")
    for jogador in jogador_vitorias:
        print('{:11}'.format(jogador), '{:>4}'.format(jogador_vitorias[jogador]))

basilio_test = Jogador("Basilio_test", lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=f_aval_basico))
        
lista_campeonato = [basilio, jogador4362, jogador4395, jogador439990, jogador439992, jogador439993, jogador439994, jogador439995]
                    
if __name__ == '__main__':
    n_faz_campeonato(N_CAMP, lista_campeonato, verbose = False)