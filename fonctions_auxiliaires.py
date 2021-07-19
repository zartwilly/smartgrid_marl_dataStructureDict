#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 18:05:40 2021

@author: willy
"""

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