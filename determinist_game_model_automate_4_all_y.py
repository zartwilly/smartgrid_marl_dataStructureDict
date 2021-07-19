#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 18:05:46 2021

@author: willy
"""

import os
import time

import numpy as np
import pandas as pd
import smartgrids_players as players
import fonctions_auxiliaires as fct_aux

from pathlib import Path
from datetime import datetime

###############################################################################
#                   definition  des fonctions annexes
#
###############################################################################


###############################################################################
#                   main function of DETERMINIST         
###############################################################################
def determinist_balanced_player_game():
    pass


###############################################################################
#                   definition  des unittests
#
###############################################################################
def test_determinist_balanced_player_game():
    
    setA_m_players = 200 #2000, 
    setB1_m_players = 300 #3000, 
    setB2_m_players = 300 #3000, 
    setC_m_players = 400 #4000 
    t_periods = 5
    path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    used_instances = False
    
    beta = 1; alpha = 1
    prix_achat = 30; prix_vente = 10 
    
    
    rd = np.random.randint(low=0, high=3)
    scenario_name = ["scenario1", "scenario2", "scenario3"][rd]
    
    dico_T_players = None
    if scenario_name == "scenario1":
        print("Play with SCENARIO1 data")
        dico_T_players = fct_aux.generate_dico_T_players_4_test_scenario1(
                                setA_m_players=setA_m_players, 
                                setB1_m_players=setB1_m_players, 
                                setB2_m_players=setB2_m_players, 
                                setC_m_players=setC_m_players,
                                t_periods=t_periods, 
                                path_2_save=path_2_save,
                                used_instances=used_instances)
    elif scenario_name == "scenario2":
        print("Play with SCENARIO2 data")
        dico_T_players = fct_aux.generate_dico_T_players_4_test_scenario2(
                            setA_m_players=setA_m_players, 
                            setB1_m_players=setB1_m_players, 
                            setB2_m_players=setB2_m_players, 
                            setC_m_players=setC_m_players,
                            t_periods=t_periods, 
                            path_2_save=path_2_save,
                            used_instances=used_instances)
    elif scenario_name == "scenario3":
        print("Play with SCENARIO3 data")
        dico_T_players = fct_aux.generate_dico_T_players_4_test_scenario3(
                            setA_m_players=setA_m_players, 
                            setB1_m_players=setB1_m_players, 
                            setB2_m_players=setB2_m_players, 
                            setC_m_players=setC_m_players,
                            t_periods=t_periods, 
                            path_2_save=path_2_save,
                            used_instances=used_instances)
        
    dico_q_pi_EPO_T = fct_aux.compute_q_pi_EPO_4_all_t(
                            dico_T_players=dico_T_players, 
                             prix_achat=prix_achat, prix_vente=prix_vente, 
                             beta=beta, alpha=alpha)
    print("dico_q_pi_EPO_T={}".format(dico_q_pi_EPO_T))

###############################################################################
#                   Execution
#
###############################################################################
if __name__ == "__main__":
    ti = time.time()
    test_determinist_balanced_player_game()
    
    print("runtime = {}".format(time.time() - ti))