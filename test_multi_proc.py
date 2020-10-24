from rastros import *

N_CAMP = 602
raio = 2

grid = [(x,y) for x in range (-raio,raio+1) for y in range(-raio,raio+1)]

def fun_aval_42(state, player):        
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
        return -9 if state.to_move == player else 9
    
    sum_score_moves = 0
    
    for point in grid:
        p = (state.white[0] + point[0] , state.white[1] + point[1])
        if p[0] >= 1 and p[0] <= 8 and p[1] >= 1 and p[1] <= 8 and p not in state.blacks:            
            sum_score_moves += 1.0 / (2 ** distancia(p, goal))
            
    #print(sum_score_moves)
    return sum_score_moves
    

#########################################################################################################
### APAGAR NO FIM #######################################################################################
def pergunta_print(game, state):
    state.display()
    print("ultima pos: ", list(state.blacks)[-1])
    if len(state.blacks) <= 1:
        pergunta_print.tst = 0
    pergunta_print.tst = pergunta_print.tst + 1
    print(pergunta_print.tst)
    print("Jogadas possíveis: ", state.moves())
    return eval(input(state.to_move+", para onde quer jogar? "))
    
humano_print = Jogador("print1", pergunta_print)
basilio_test = Jogador("Basilio_test", lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=f_aval_basico))
#########################################################################################################
#########################################################################################################

jogador42 = Jogador("jogador42",
                  lambda game, state:
                  alphabeta_cutoff_search_new(state,game,depth_for_all,eval_fn=fun_aval_42))

#jg = jogaRastros11(basilio,test1)
#print(jg)


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

if __name__ == '__main__':
    n_faz_campeonato(N_CAMP, [jogador42, basilio], verbose = False)