from rastros import *

N_CAMP = 50

def distancia (a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))

def moves_from_point(point, visited_squares, state):
        alladjacent = [(point[0]+a, point[1]+b) for a in [-1,0,1] for b in [-1,0,1]]
        return [p for p in alladjacent
                if p not in state.blacks and p not in visited_squares and p !=point and p in state.fullboard]
                
######################

def forced_path42(state, player, goal, no_goal, p_moves):
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
                return -3 if state.to_move == player else 3
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 3 if state.to_move == player else -3
    return 0    
def fun_aval_42(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
    dist_white_goal = distancia(state.white, goal)
    dist_white_no_goal = distancia(state.white, no_goal)        
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    elif dist_white_goal <= 1:
        return 3        
    moves = state.moves()
    forced_path_res = forced_path42(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res        
    def result(sub_state, move):
        blacks = sub_state.blacks.copy()
        blacks.add(sub_state.white)
        return EstadoRastros(to_move=('N' if sub_state.to_move == 'S' else 'S'),white=move,blacks=blacks)     
    def retreat(sub_state):
        for move in sub_state.moves():
            if distancia(move, goal) >= distancia(sub_state.white, goal):
                    if not approach_win(result(sub_state, move)):
                        return True
        return False    
    def approach_win(sub_state):
        has_approach = False
        for move in sub_state.moves():
            if distancia(move, goal) < distancia(sub_state.white, goal):
                has_approach = True
                if (move != goal) and retreat(result(sub_state, move)):
                    return False
        return has_approach
    if dist_white_goal <= 2 and approach_win(state):
        return 3
    elif dist_white_no_goal <= 2:
        return -2    
    if dist_white_goal <= 2:
        return -2    
    no_goal_dists = dist_white_no_goal
    for black in state.blacks:
        no_goal_dists += distancia(black, no_goal)
    return 1 / (no_goal_dists / (len(state.blacks) + 1))  

jogador42 = Jogador("jogador42",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_42))


################################################################################################
### OUTRAS FUNÇÕES #############################################################################

raio425 = 2
grid425 = [(x,y) for x in range (-raio425,raio425+1) for y in range(-raio425,raio425+1)]
def fun_aval_425(state, player):        
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)    
    if state.white == goal:
        return 10
    elif state.white == no_goal:
        return -10
    elif len(state.moves()) == 0:
        return -9 if state.to_move == player else 10    
    sum_score_moves = 0    
    for point in grid425:
        p = (state.white[0] + point[0] , state.white[1] + point[1])
        if p[0] >= 1 and p[0] <= 8 and p[1] >= 1 and p[1] <= 8 and p not in state.blacks:            
            sum_score_moves += 1.0 / (2 ** distancia(p, goal))            
    return sum_score_moves
jogador425 = Jogador("jogador425",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_425))
    
def fun_aval_426(state, player):        
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
    
    if state.white == goal:
        return 10000
    elif state.white == no_goal:
        return -10000
    elif len(state.moves()) == 0:
        return -8000 if state.to_move == player else 8000
    
    goal_dist_score = 1 / distancia(state.white, goal)
    no_goal_dist_score = 1 / distancia(state.white, no_goal)
    
    turns = len(state.blacks)
    return (no_goal_dist_score * ((24 / turns)**3)) + (goal_dist_score * ((turns / 24)**3))
jogador426 = Jogador("jogador426",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_426))
    
def fun_aval_427(state, player):        
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)    
    if state.white == goal:
        return 10000
    elif state.white == no_goal:
        return -10000
    elif len(state.moves()) == 0:
        return -8000 if state.to_move == player else 8000    
    goal_dist_score = 1 / distancia(state.white, goal)
    no_goal_dist_score = 1 / distancia(state.white, no_goal)    
    turns = max(1, (len(state.blacks) - 5) )    
    if turns <= 15:
        return no_goal_dist_score    
    return goal_dist_score
jogador427 = Jogador("jogador427",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_427))
                  
def fun_aval_433(state, player):    
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
    p_moves = moves.copy()
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
                return -2 if state.to_move == player else 2.5
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 2 if state.to_move == player else -2.5            
    move_score = 0
    num_moves = 0
    for move in moves:
        for sub_move in moves_from_point(move,[state.white],state):
            move_score += distancia(move, goal) - distancia(sub_move,goal)
            num_moves += 1
    if num_moves == 0:
        return 0
    return move_score / num_moves
jogador433 = Jogador("jogador433",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_433))            
                  
def near_goal_situation_win36(state, player, goal):    
    return (distancia(state.white, goal) <= 2 and state.to_move == player
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
        return 0    
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
    elif distancia(state.white, no_goal) <= 2:
        return -1.5        
    return general_eval36(moves, state, goal)
jogador436 = Jogador("jogador436",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_436))
                  
def near_goal_situation_win37(state, player, goal):    
    return (distancia(state.white, goal) <= 2 and state.to_move == player
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
def forced_path37(state, player, goal, no_goal, p_moves):
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
def general_eval37(moves, state, goal):
    move_avg = -infinity
    for move in moves:
        mm_score = 0
        mm_num = 1
        for sub_move in moves_from_point(move,[state.white],state):
            s_score = distancia(move, goal) - distancia(sub_move,goal)
            mm_score += s_score
            mm_num += 1
        move_avg = max(move_avg, (mm_score / mm_num))
    return move_avg     
def fun_aval_437(state, player):    
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
    forced_path_res = forced_path37(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res           
    if near_goal_situation_win37(state, player, goal):
        return 2.5  
    elif distancia(state.white, no_goal) <= 2:
        return -1.5      
    return general_eval37(moves, state, goal)
jogador437 = Jogador("jogador437",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_437))
                  
def near_goal_situation_win38(state, player, goal):    
    return (distancia(state.white, goal) <= 2 and state.to_move == player
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
def forced_path38(state, player, goal, no_goal, p_moves):
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
def fun_aval_438(state, player):    
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
    forced_path_res = forced_path38(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res
    if near_goal_situation_win38(state, player, goal):
        return 2.5
    elif distancia(state.white, no_goal) <= 2:
        return -1.5   
    if distancia(state.white, goal) <= 3:
        return -1    
    return 1 / distancia(state.white, no_goal)
jogador438 = Jogador("jogador438",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_438))
                  
def forced_path39(state, player, goal, no_goal, p_moves):
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
                return -3 if state.to_move == player else 3
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 3 if state.to_move == player else -3
    return 0    
def fun_aval_439(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
    dist_white_goal = distancia(state.white, goal)
    dist_white_no_goal = distancia(state.white, no_goal)        
    if state.white == goal:
        return 3    
    elif state.white == no_goal:
        return -3    
    elif dist_white_goal <= 1:
        return 3        
    moves = state.moves()
    forced_path_res = forced_path39(state, player, goal, no_goal, moves)
    if forced_path_res != 0:
        return forced_path_res        
    def result(sub_state, move):
        blacks = sub_state.blacks.copy()
        blacks.add(sub_state.white)
        return EstadoRastros(to_move=('N' if sub_state.to_move == 'S' else 'S'),white=move,blacks=blacks)     
    def retreat(sub_state):
        for move in sub_state.moves():
            if distancia(move, goal) >= distancia(sub_state.white, goal):
                    if not approach_win(result(sub_state, move)):
                        return True
        return False    
    def approach_win(sub_state):
        has_approach = False
        for move in sub_state.moves():
            if distancia(move, goal) < distancia(sub_state.white, goal):
                has_approach = True
                if (move != goal) and retreat(result(sub_state, move)):
                    return False
        return has_approach
    if dist_white_goal <= 3 and approach_win(state):
        return 3
    elif dist_white_no_goal <= 2:
        return -2    
    if dist_white_goal <= 3:
        return -2    
    no_goal_dists = dist_white_no_goal
    for black in state.blacks:
        no_goal_dists += distancia(black, no_goal)
    return 1 / (no_goal_dists / (len(state.blacks) + 1))    
jogador439 = Jogador("jogador439",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_439))
                  
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
    pool = multiprocessing.Pool(processes=5)
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
        
lista_campeonato = [jogador42, basilio, jogador425, jogador426, jogador427, 
                    jogador433, jogador436, jogador437, jogador438, jogador439]
                    
if __name__ == '__main__':
    n_faz_campeonato(N_CAMP, lista_campeonato, verbose = False)