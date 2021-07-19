#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 18:05:40 2021

@author: willy
"""
import os

import generation_data_scenarios as geneData

#------------------------------------------------------------------------------
#                       definition of constantes
#------------------------------------------------------------------------------
N_DECIMALS = 2
NB_REPEAT_K_MAX = 4
STOP_LEARNING_PROBA = 0.90


STATES = ["Deficit", "Self", "Surplus"]

STATE1_STRATS = ("CONS+", "CONS-")                                             # strategies possibles pour l'etat 1 de a_i
STATE2_STRATS = ("DIS", "CONS-")                                               # strategies possibles pour l'etat 2 de a_i
STATE3_STRATS = ("DIS", "PROD")                                                # strategies possibles pour l'etat 3 de a_i

INDEX_ATTRS = {"Ci":0, "Pi":1, "Si_init":2, "Si":3, "Si_max":4, "gamma_i":5, 
               "prod_i":6, "cons_i":7, "r_i":8, "state_i":9, "mode_i":10,
               "Profili":11, "Casei":12, "R_i_old":13, "Si_old":14, 
               "balanced_pl_i": 15, "formule":16, "Si_minus":17, "Si_plus":18, 
               "u_i": 19, "bg_i": 20, "S1_p_i_j_k": 21, "S2_p_i_j_k": 22, 
               "playing_players":23, "setX":24, 
               "ben_i":25, "cst_i":26, "Vi":27}

RACINE_PLAYER = "player"
RACINE_TPERIOD = "t"

###############################################################################
#                       fonctions transverses: debut       
###############################################################################
def fct_positive(sum_list1, sum_list2):
    """
    sum_list1 : sum of items in the list1
    sum_list2 : sum of items in the list2
    
    difference between sum of list1 et sum of list2 such as :
         diff = 0 if sum_list1 - sum_list2 <= 0
         diff = sum_list1 - sum_list2 if sum_list1 - sum_list2 > 0

        diff = 0 if sum_list1 - sum_list2 <= 0 else sum_list1 - sum_list2
    Returns
    -------
    return 0 or sum_list1 - sum_list2
    
    """
    
    # boolean = sum_list1 - sum_list2 > 0
    # diff = boolean * (sum_list1 - sum_list2)
    diff = 0 if sum_list1 - sum_list2 <= 0 else sum_list1 - sum_list2
    return diff

# _____________________________________________________________________________
#           compute q_minus, q_plus, pi_EPO_minus, pi_EPO_plus : debut
# _____________________________________________________________________________
def compute_phi_minus(q_minus=0, beta=1, prix_achat=30):
    return prix_achat * pow(q_minus, beta)

def compute_phi_plus(q_plus=0, alpha=1, prix_vente=10):
    return prix_vente * pow(q_plus, alpha)

def compute_q_pi_EPO_4_all_t(dico_T_players, 
                             prix_achat=30, prix_vente=10, beta=1, alpha=1):
    """
    compute the variables q_minus_t, q_plus_t, pi_EPO_minus_t, pi_EPO_plus_t.
    each variable is a list of T items. 
    example q_minus = [q_minus_t]_{0<t<T-1}, q_plus = [q_plus_t]_{0<t<T-1}
            pi_EPO_minus = [pi_EPO_minus_t]_{0<t<T-1},
            pi_EPO_plus = [pi_EPO_plus_t]_{0<t<T-1}

    Parameters
    ----------
    dico_T_players : dict
        {"t0":dico_players_t0, "t1":dico_players_t1, "t2":dico_players_t2, ...}  
            with dico_players_t0 = {"pl_0":dico_pl0, pl_1":dico_pl1, ... }
                dico_pl0 = {"Pi":[], "Ci":[], "Si":[], "Si_max":[], ....}
                
    prix_achat: prix d'achat de l électricité de SG a EPO
    prix_vente: prix de vente de l électricité de SG a EPO
                
    Returns
    -------
    dico_q_pi_EPO_T : dict
        {"q_minus": [q_minus_t]_{0<t<T-1}, 
         "q_plus" : [q_plus_t]_{0<t<T-1}
         "pi_EPO_minus": [pi_EPO_minus_t]_{0<t<T-1},
         "pi_EPO_plus": [pi_EPO_plus_t]_{0<t<T-1}}
        }

    """
    q_minus, q_plus = list(), list()
    pi_EPO_minus, pi_EPO_plus = list(), list()
    
    for t, dico_players_t in dico_T_players.items():
        q_minus_t, q_plus_t = 0, 0
        for player_name, dico_plX in dico_players_t.items():
            diffpos_Ci_Pi = fct_aux.fct_positive(sum_list1=dico_plX["Ci"], 
                                                 sum_list2=dico_plX["Pi"])
            diffpos_Pi_Ci = fct_aux.fct_positive(sum_list1=dico_plX["Pi"], 
                                                 sum_list2=dico_plX["Ci"])
            diffpos_Pi_Ci_Simax_Si = fct_aux.fct_positive(
                                        sum_list1=dico_plX["Pi"], 
                                        sum_list2=dico_plX["Ci"] \
                                                    + dico_plX["Si_max"] \
                                                    - dico_plX["Si_init"])
            diffpos_Ci_Pi_Si = fct_aux.fct_positive(
                                        sum_list1=dico_plX["Ci"], 
                                        sum_list2=dico_plX["Pi"] \
                                                    + dico_plX["Si_init"])
            
            diffpos_CiPi_PiCiSimaxSi = fct_aux.fct_positive(
                                        sum_list1=diffpos_Ci_Pi, 
                                        sum_list2=diffpos_Pi_Ci_Simax_Si)
            diffpos_PiCi_CiPiSi = fct_aux.fct_positive(
                                        sum_list1=diffpos_Pi_Ci, 
                                        sum_list2=diffpos_Ci_Pi_Si)
            
            q_minus_plX, q_plus_plX = None, None
            q_minus_plX = diffpos_CiPi_PiCiSimaxSi
            q_plus_plX = diffpos_PiCi_CiPiSi
            
            q_minus_t += q_minus_plX
            q_plus_t += q_plus_plX
        
        # compute pi_EPO_{minus,plus}_t
        phi_EPO_minus_t =  compute_phi_minus(q_minus=q_minus_t, beta=beta, 
                                           prix_achat=prix_achat)
        phi_EPO_plus_t =  compute_phi_plus(q_plus=q_plus_t, alpha=alpha, 
                                         prix_vente=prix_vente)
        pi_EPO_minus_t = round(phi_EPO_minus_t/q_minus_t, fct_aux.NB_REPEAT_K_MAX) \
                            if q_minus_t != 0 else 0
        pi_EPO_plus_t = round(phi_EPO_plus_t/q_plus_t, fct_aux.NB_REPEAT_K_MAX) \
                            if q_plus_t != 0 else 0
        # save q_{plus,minus}_t, pi_EPO_{minus,plus}_t
        q_minus.append(q_minus_t)
        q_plus.append(q_plus_t)
        pi_EPO_minus.append(pi_EPO_minus_t)
        pi_EPO_plus.append(pi_EPO_plus_t)
        
    dico_q_pi_EPO_T = dict()
    dico_q_pi_EPO_T = {"q_minus": q_minus, "q_plus" : q_plus,
                       "pi_EPO_minus": pi_EPO_minus, "pi_EPO_plus": pi_EPO_plus}
    
    return dico_q_pi_EPO_T

# _____________________________________________________________________________
#           compute q_minus, q_plus, pi_EPO_minus, pi_EPO_plus : fin
# _____________________________________________________________________________

# _____________________________________________________________________________
#           generate data for tests : debut
# _____________________________________________________________________________
def generate_dico_T_players_4_test_scenario1(setA_m_players=2000, setB1_m_players=3000, 
                                  setB2_m_players=3000, setC_m_players=4000,
                                  t_periods=5, 
                                  path_2_save=os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"]),
                                  used_instances=False):
    
    
    scen1_pr = 0.6
    scen1_dico_setA = {"Pi":(0,0+1), "Ci":(10,10+1), "Si":(3,3+1),"Si_max":(20,20+1)}
    scen1_dico_setC = {"Pi":(20,20+1), "Ci":(10,10+1), "Si":(10,10+1),"Si_max":(20,20+1)}
    prob_A_A = scen1_pr; prob_A_C = 1-scen1_pr;
    prob_C_A = 1-scen1_pr; prob_C_C = scen1_pr;
    scenario1 = [(prob_A_A, prob_A_C), 
                (prob_C_A, prob_C_C)]
    scenario_name = "scenario1"
    
    dico_T_players = geneData.get_or_create_PiCiSi_players_scenario1instances(
                        setA_m_players=setA_m_players, dico_setA=scen1_dico_setA,
                        setC_m_players=setC_m_players, dico_setC=scen1_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario1, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
    
    return dico_T_players

def generate_dico_T_players_4_test_scenario2(setA_m_players=2000, setB1_m_players=3000, 
                                  setB2_m_players=3000, setC_m_players=4000,
                                  t_periods=5, 
                                  path_2_save=os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"]),
                                  used_instances=False):
    
    
    scen2_pr = 0.6
    scen2_dico_setA = {"Pi":(2,4+1), "Ci":(10,10+1), "Si":(3,3+1),"Si_max":(6,6+1)}
    scen2_dico_setB1 = {"Pi":(8,12+1), "Ci":(10,10+1), "Si":(4,4+1),"Si_max":(6,6+1)}
    scen2_dico_setB2 = {"Pi":(18,22+1), "Ci":(22,22+1), "Si":(10,10+1),"Si_max":(15,15+1)}
    scen2_dico_setC = {"Pi":(26,26+1), "Ci":(20,20+1), "Si":(10,10+1),"Si_max":(15,15+1)}
    prob_A_A = scen2_pr; prob_A_B1 = 1-scen2_pr; prob_A_B2 = 0.0; prob_A_C = 0.0;
    prob_B1_A = scen2_pr; prob_B1_B1 = 1-scen2_pr; prob_B1_B2 = 0.0; prob_B1_C = 0.0;
    prob_B2_A = 0.0; prob_B2_B1 = 0.0; prob_B2_B2 = 1-scen2_pr; prob_B2_C = scen2_pr;
    prob_C_A = 0.0; prob_C_B1 = 0.0; prob_C_B2 = 1-scen2_pr; prob_C_C = scen2_pr 
    scenario2 = [(prob_A_A, prob_A_B1, prob_A_B2, prob_A_C), 
                 (prob_B1_A, prob_B1_B1, prob_B1_B2, prob_B1_C),
                 (prob_B2_A, prob_B2_B1, prob_B2_B2, prob_B2_C),
                 (prob_C_A, prob_C_B1, prob_C_B2, prob_C_C)]
    scenario_name = "scenario2"
    
    
    dico_T_players = geneData.get_or_create_PiCiSi_players_scenario23instances(
                        setA_m_players=setA_m_players, dico_setA=scen2_dico_setA,
                        setB1_m_players=setB1_m_players, dico_setB1=scen2_dico_setB1,
                        setB2_m_players=setB2_m_players, dico_setB2=scen2_dico_setB2,
                        setC_m_players=setC_m_players, dico_setC=scen2_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario2, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
    
    return dico_T_players

def generate_dico_T_players_4_test_scenario3(setA_m_players=2000, setB1_m_players=3000, 
                                  setB2_m_players=3000, setC_m_players=4000,
                                  t_periods=5, 
                                  path_2_save=os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"]),
                                  used_instances=False):
    
    scen3_pr = 0.8
    scen3_dico_setA = {"Pi":(2,4+1), "Ci":(10,10+1), "Si":(3,3+1),"Si_max":(6,6+1)}
    scen3_dico_setB1 = {"Pi":(8,12+1), "Ci":(12,12+1), "Si":(4,4+1),"Si_max":(6,6+1)}
    scen3_dico_setB2 = {"Pi":(18,22+1), "Ci":(22,22+1), "Si":(10,10+1),"Si_max":(15,15+1)}
    scen3_dico_setC = {"Pi":(26,26+1), "Ci":(20,20+1), "Si":(10,10+1),"Si_max":(15,15+1)}
    prob_A_A = scen3_pr; prob_A_B1 = 1-scen3_pr; prob_A_B2 = 0.0; prob_A_C = 0.0;
    prob_B1_A = scen3_pr; prob_B1_B1 = 1-scen3_pr; prob_B1_B2 = 0.0; prob_B1_C = 0.0;
    prob_B2_A = 0.0; prob_B2_B1 = 0.0; prob_B2_B2 = 1-scen3_pr; prob_B2_C = scen3_pr;
    prob_C_A = 0.0; prob_C_B1 = 0.0; prob_C_B2 = 1-scen3_pr; prob_C_C = scen3_pr
    scenario3 = [(prob_A_A, prob_A_B1, prob_A_B2, prob_A_C), 
                 (prob_B1_A, prob_B1_B1, prob_B1_B2, prob_B1_C),
                 (prob_B2_A, prob_B2_B1, prob_B2_B2, prob_B2_C),
                 (prob_C_A, prob_C_B1, prob_C_B2, prob_C_C)]
    scenario_name = "scenario3"
    
    dico_T_players = geneData.get_or_create_PiCiSi_players_scenario23instances(
                        setA_m_players=setA_m_players, dico_setA=scen3_dico_setA,
                        setB1_m_players=setB1_m_players, dico_setB1=scen3_dico_setB1,
                        setB2_m_players=setB2_m_players, dico_setB2=scen3_dico_setB2,
                        setC_m_players=setC_m_players, dico_setC=scen3_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario3, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
    
    return dico_T_players
# _____________________________________________________________________________
#           generate data for tests : fin
# _____________________________________________________________________________