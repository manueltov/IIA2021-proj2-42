from rastros import *

N_CAMP = 2

def distancia (a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))
    
def moves_from_point(point, visited_squares, state):
        alladjacent = [(point[0]+a, point[1]+b) for a in [-1,0,1] for b in [-1,0,1]]
        return [p for p in alladjacent
                if p not in state.blacks and p not in visited_squares and p !=point and p in state.fullboard]

def fun_aval_42(state, player):    
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
                return -2 if state.to_move == player else 2
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 2 if state.to_move == player else -2
            
    move_score = 0
    num_moves = 0
    for move in moves:
        for sub_move in moves_from_point(move,[state.white],state):
            move_score += distancia(move, goal) - distancia(sub_move,goal)
            num_moves += 1
    if num_moves == 0:
        return 0
    return move_score / num_moves


jogador42 = Jogador("jogador42",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_42))


################################################################################################
### OUTRAS FUNÇÕES #############################################################################

def fun_aval_421(state, player):
    win_or_loss = state.compute_utility(player)
    if win_or_loss != 0:
        return win_or_loss * 300000
    else:
        goal = (8, 1) if player == "S" else (1, 8)
        sum_dist_actions = 0
        for move in state.moves():
            sum_dist_actions += 7 - distancia(move, goal)
        sum_dist_actions += 7 - (distancia(state.white, goal) * 2)
        return sum_dist_actions ** 3
jogador421 = Jogador("jogador421",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_421))

def fun_aval_422(state, player):
    win_or_loss = state.compute_utility(player)
    if win_or_loss != 0:
        return win_or_loss * 5000
    else:
        goal = (8, 1) if player == "S" else (1, 8)
        sum_dist_actions = 0
        for move in state.moves():
            dist_move_goal = distancia(move, goal)
            dist_white_goal = distancia(state.white, goal)
            if (dist_move_goal >= dist_white_goal):
                sum_dist_actions -= dist_move_goal
            else:
                sum_dist_actions += dist_move_goal
                
        return sum_dist_actions ** 2
jogador422 = Jogador("jogador422",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_422))
        
def fun_aval_423(state, player):        
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)    
    
    if state.white == goal:
        return 6.0
    elif state.white == no_goal:
        return -12.0
    elif len(state.moves()) == 0:
        return -12.0 if state.to_move == player else 6.0
           
    score_white_goal = 1.0 / (3 ** distancia(state.white, goal))
    sum_score_moves = 0
    for move in state.moves():
        score_move_goal = 1.0 / (3 ** distancia(move, goal))
        sum_score_moves += score_move_goal
        
    return (sum_score_moves * 1.0) + (score_white_goal * 3.0)
jogador423 = Jogador("jogador423",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_423))
    
def fun_aval_424(state, player):        
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
    for move in state.moves():
        score_move_goal = 1.0 / (2 ** distancia(move, goal))
        sum_score_moves += score_move_goal
    
    return sum_score_moves
jogador424 = Jogador("jogador424",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_424))

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
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_425))
    
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
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_426))
    
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
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_427))
                 
raio428 = 2
grid428 = [(x,y) for x in range (-raio428,raio428+1) for y in range(-raio428,raio428+1)]
def fun_aval_428(state, player):
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
    
    for point in grid428:
        p = (state.white[0] + point[0] , state.white[1] + point[1])
        if p == goal:
            return 1 / distancia(state.white, goal)
        elif p == no_goal:
            return -1 / distancia(state.white, no_goal)
        
    return 1 / (raio428 ** distancia(state.white, goal))
jogador428 = Jogador("jogador428",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_428))

raio429 = 3
grid429 = [(x,y) for x in range (-raio429,raio429+1) for y in range(-raio429,raio429+1)]
def fun_aval_429(state, player):
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
    
    for point in grid429:
        p = (state.white[0] + point[0] , state.white[1] + point[1])
        if p == goal:
            return 1 / distancia(state.white, goal)
        elif p == no_goal:
            return -1 / distancia(state.white, no_goal)
        
    return 1 / (raio429 ** distancia(state.white, goal))
jogador429 = Jogador("jogador429",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_429))
                  
def fun_aval_430(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
    
    if state.white == goal:
        return 3
    elif state.white == no_goal:
        return -3
    elif len(state.moves()) == 0:
        return -2 if state.to_move == player else 2
    elif distancia(state.white, goal) <= 3:
        return 1.5
    
    return 1 / distancia(state.white, goal)
jogador430 = Jogador("jogador430",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_430))
                  
def fun_aval_431(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
        
    if state.white == goal:
        return 3
    elif state.white == no_goal:
        return -3
    
    p_moves = state.moves()
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
                return -2 if state.to_move == player else 2
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 2 if state.to_move == player else -2
        
    if distancia(state.white, goal) <= 3:
        return (1 / distancia(state.white, goal)) + 1
    if distancia(state.white, no_goal) <= 3:
        return (1 / distancia(state.white, goal)) - 1
    
    return 1 / distancia(state.white, goal)
jogador431 = Jogador("jogador431",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_431))

def fun_aval_432(state, player):    
    goal = (8, 1)
    no_goal = (1, 8)
    if player == "N":
        goal = (1, 8)
        no_goal = (8, 1)
        
    if state.white == goal:
        return 3
    elif state.white == no_goal:
        return -3
    
    p_moves = state.moves()
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
                return -2 if state.to_move == player else 2
            elif (len(visited_squares) - 1) % 2 == 1:                
                return 2 if state.to_move == player else -2
        
    if distancia(state.white, goal) <= 3:
        return 1
    if distancia(state.white, no_goal) <= 3:
        return -1
    
    return 1 / distancia(state.white, goal)
jogador432 = Jogador("jogador432",
                  lambda game, state:
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=fun_aval_432))
    
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
    
def n_faz_campeonato(num_campeonatos, listaJogadores, nsec=10, verbose = False):
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
                  alphabeta_cutoff_search(state,game,depth_for_all,eval_fn=f_aval_basico))
        
lista_campeonato = [jogador42, jogador421, jogador422, jogador423, 
                    jogador424, jogador425, jogador426, jogador427, 
                    jogador428,jogador429,jogador430,jogador431,jogador432,
                    basilio_test]
                    
if __name__ == '__main__':
    n_faz_campeonato(N_CAMP, lista_campeonato, verbose = False)