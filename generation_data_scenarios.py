
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 08:45:14 2021

@author: willy
"""

import os
import sys
import time
import math
import json
import string
import random
import numpy as np
import pandas as pd
import itertools as it
import fonctions_auxiliaires as fct_aux

from datetime import datetime
from pathlib import Path


#------------------------------------------------------------------------------
#                       definition of constantes
#------------------------------------------------------------------------------
SET_ABC = ["setA", "setB", "setC"]
SET_AB1B2C = ["setA", "setB1",  "setB2", "setC"]

RACINE_FILENAME_JSON_PLAYERS = "dico_Tperiods{}_Mplayers_setA_{}_setB_{}_setC_{}_{}.json"
RACINE_SCEN1_FILENAME_JSON_PLAYERS = "dico_T{}_Mplayers_setA_{}_setC_{}_{}.json"
RACINE_SCEN23_FILENAME_JSON_PLAYERS = "dico_T{}_Mplayers_setA_{}_setB1_{}_setB2_{}_setC_{}_{}.json"


#------------------------------------------------------------------------------
#           definitions of functions
#------------------------------------------------------------------------------


###############################################################################
#            generate Pi, Ci by scenario_50Instances --> debut
###############################################################################
def get_set_players(id_pl_i, setA_id_players, setB_id_players, setC_id_players):
    """
    get the set of player with index id_pl_i
    setA_id_players, setB_id_players, setC_id_players: set
    """
    setX_pl_i = None
    if id_pl_i in setA_id_players:
        setX_pl_i = SET_ABC[0]                                                  # setA
    elif id_pl_i in setB_id_players:
        setX_pl_i = SET_ABC[1]                                                  # setB
    elif id_pl_i in setC_id_players:
        setX_pl_i = SET_ABC[2]                                                  # setC
    return setX_pl_i
    
def generate_PiCiSi_scenario50instances(setA_m_players, dico_setA,
                                        setB_m_players, dico_setB,
                                        setC_m_players, dico_setC,
                                        t_periods=1, 
                                        scenario=None, 
                                        scenario_name="scenario50instances"):
    """
    generate Pi, Si, Ci of M players for one period t

    Parameters
    ----------
    setA_m_players : int
        DESCRIPTION. number of players in the set A
    dico_setA : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setA = {"Pi":(5,10+1), "Ci":(15,15+1), "Si":(0,0+1),"Si_max":(20,20+1)}
    setB_m_players : int
        DESCRIPTION. number of players in the set B
    dico_setB : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setB = {"Pi_inf_prob":(5,8+1), "Ci_inf_prob":(10,10+1), 
                                 "Pi_sup_prob":(21,30+1), "Ci_sup_prob":(31,31+1), 
                                 "Si_inf_prob":(6,6+1),"Si_max_inf_prob":(20,20+1),
                                 "Si_sup_prob":(8,8+1),"Si_max_sup_prob":(20,20+1)}
    setC_m_players : int
        DESCRIPTION. number of players in the set C
    dico_setC : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setC = {"Pi":(21,30+1), "Ci":(20,20+1), "Si":(8,8+1),"Si_max":(20,20+1)}
    t_periods : int
        DESCRIPTION. number of periods. here t_periods = 1
    scenario : TYPE, optional
        DESCRIPTION. The default is None.
    scenario_name : TYPE, optional
        DESCRIPTION. The default is "scenario50instances".

    Returns
    -------
    dico_T_players: dict
    for example:
        {"t0":dico_players_t0}  
        with dico_players_t0 = {"pl_0":dico_pl0, pl_1":dico_pl1, ... }
            dico_pl0 = {"Pi":[], "Ci":[], "Si":[], "Si_max":[], ....}

    """
    
    # ____ generation of sub set of players in set1 and set2 : debut _________
    m_players = setA_m_players + setB_m_players + setC_m_players
    id_players = range(0, m_players)
    
    setA_id_players = list(np.random.choice(list(id_players), 
                                            size=setA_m_players, 
                                            replace=False))
    remain_players = list(set(id_players) - set(setA_id_players))
    setB_id_players = list(np.random.choice(list(remain_players), 
                                            size=setB_m_players, 
                                            replace=False))
    remain_players = list(set(id_players) 
                          - set(setA_id_players) 
                          - set(setB_id_players))
    setC_id_players = list(np.random.choice(list(remain_players), 
                                            size=setC_m_players, 
                                            replace=False))
    remain_players = list(set(id_players) 
                          - set(setA_id_players) 
                          - set(setB_id_players)
                          - set(setC_id_players))
    
    print("Remain_players: {} -> OK ".format(remain_players)) \
        if len(remain_players) == 0 \
        else print("Remain_players: {} -> NOK ".format(remain_players))
    print("generation players par setA, setB, setC = OK") \
        if len(set(setA_id_players)
                   .intersection(
                       set(setB_id_players)
                       .intersection(
                           set(setC_id_players)
                           )
                       )
                ) == 0 \
        else print("generation players par setA, setB, setC = NOK")
    # ____ generation of sub set of players in setA, setB and setC : fin   ____
    
    
    dico_T_players = dict()
    
    for t in range(0, t_periods):
        dico_players_t = dict()
        for id_pl_i in range(0, m_players):
            Pi, Ci, Si, Si_max, setX_pl_i = None, None, None, None, None
            prob = np.random.random(size=1)[0]
            if id_pl_i in setA_id_players:
                setX_pl_i = SET_ABC[0]                                          # setA = Deficit
                Pi = np.random.randint(low=dico_setA["Pi"][0], 
                                       high=dico_setA["Pi"][1])
                Ci = np.random.randint(low=dico_setA["Ci"][0], 
                                       high=dico_setA["Ci"][1])
                Si = np.random.randint(low=dico_setA["Si"][0], 
                                       high=dico_setA["Si"][1])
                Si_max = np.random.randint(low=dico_setA["Si_max"][0], 
                                           high=dico_setA["Si_max"][1])
            elif id_pl_i in setB_id_players and prob < 1/2:
                setX_pl_i = SET_ABC[1]                                          # setB = Self
                Pi = np.random.randint(low=dico_setB["Pi_inf_prob"][0], 
                                       high=dico_setB["Pi_inf_prob"][1])
                Ci = np.random.randint(low=dico_setB["Ci_inf_prob"][0], 
                                       high=dico_setB["Ci_inf_prob"][1])
                Si = np.random.randint(low=dico_setB["Si_inf_prob"][0], 
                                       high=dico_setB["Si_inf_prob"][1])
                Si_max = np.random.randint(low=dico_setB["Si_max_inf_prob"][0], 
                                           high=dico_setB["Si_max_inf_prob"][1])
            elif id_pl_i in setB_id_players and prob >= 1/2:
                setX_pl_i = SET_ABC[1]                                          # setB = Self
                Pi = np.random.randint(low=dico_setB["Pi_sup_prob"][0], 
                                       high=dico_setB["Pi_sup_prob"][1])
                Ci = np.random.randint(low=dico_setB["Ci_sup_prob"][0], 
                                       high=dico_setB["Ci_sup_prob"][1])
                Si = np.random.randint(low=dico_setB["Si_sup_prob"][0], 
                                       high=dico_setB["Si_sup_prob"][1])
                Si_max = np.random.randint(low=dico_setB["Si_max_sup_prob"][0], 
                                           high=dico_setB["Si_max_sup_prob"][1])
            elif id_pl_i in setC_id_players:
                setX_pl_i = SET_ABC[2]                                          # setC = Surplus
                Pi = np.random.randint(low=dico_setC["Pi"][0], 
                                       high=dico_setC["Pi"][1])
                Ci = np.random.randint(low=dico_setC["Ci"][0], 
                                       high=dico_setC["Ci"][1])
                Si = np.random.randint(low=dico_setC["Si"][0], 
                                       high=dico_setC["Si"][1])
                Si_max = np.random.randint(low=dico_setC["Si_max"][0], 
                                           high=dico_setC["Si_max"][1]) 
                
            # update arrays cells with variables
            col_vals = [("Pi",Pi), ("Ci",Ci), 
                        ("Si_init",Si), ("Si",Si), ("Si_max",Si_max), 
                        ("mode_i",""), ("state_i",""), ("setX", setX_pl_i)]
            dico_player_i = dict()
            for col in fct_aux.INDEX_ATTRS.keys():
                if col in ["Pi", "Ci", "Si_init", "Si", "Si_max", 
                           "setX"]:
                    val = [col_val[1] for col_val in col_vals if col_val[0] == col]
                    if col in ["Si", "setX"]:
                        dico_player_i[col] = val
                    else:
                        dico_player_i[col] = val[0]
                else:
                    dico_player_i[col] = []
                
            dico_players_t[fct_aux.RACINE_PLAYER+str(id_pl_i)] = dico_player_i    
       
        dico_T_players[fct_aux.ACINE_TPERIOD+str(t)] = dico_players_t
        
    return dico_T_players
        
def get_or_create_PiCiSi_players_scenario50instances(setA_m_players, dico_setA,
                                        setB_m_players, dico_setB,
                                        setC_m_players, dico_setC,
                                        t_periods=1, 
                                        scenario=None, 
                                        scenario_name="scenario50instances",
                                        path_2_save="", 
                                        used_instances=False):
    """
    get json dico_T_players and convert to dictionnary 
    if it exists 
    else create dico_T_players.
    
    Parameters
    ----------
    setA_m_players : integer
        DESCRIPTION.
        Number of players having their states belonging to setA.
    dico_setA : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setA = {"Pi":(5,10+1), "Ci":(15,15+1), "Si":(0,0+1),"Si_max":(20,20+1)}
    setB_m_players : integer
        DESCRIPTION.
        Number of players having their states belonging to setB.
    dico_setB : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setB = {"Pi_inf_prob":(5,8+1), "Ci_inf_prob":(10,10+1), 
                                 "Pi_sup_prob":(21,30+1), "Ci_sup_prob":(31,31+1), 
                                 "Si_inf_prob":(6,6+1),"Si_max_inf_prob":(20,20+1),
                                 "Si_sup_prob":(8,8+1),"Si_max_sup_prob":(20,20+1)}
    setC_m_players : integer
        DESCRIPTION.
        Number of players having their states belonging to setC.
    dico_setC : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setC = {"Pi":(21,30+1), "Ci":(20,20+1), "Si":(8,8+1),"Si_max":(20,20+1)}
    t_periods : integer
        DESCRIPTION.
        Number of periods in the game
    scenario : list of tuple. 
                each tuple is the moving transition from one state to the other sates
        DESCRIPTION
        contains the transition probability of each state
        exple  [(prob_A_A, prob_A_B, prob_A_C), (prob_B_A, prob_B_B, prob_B_C),
                (prob_C_A, prob_C_B, prob_C_C)]
                with prob_A_A = 0.7; prob_A_B = 0.3; prob_A_C = 0.0,
                     prob_B_A = 0.3; prob_B_B = 0.4; prob_B_C = 0.3,
                     prob_C_A = 0.1; prob_C_B = 0.2; prob_C_C = 0.7; 
                and 
                prob_A_A : float [0,1] - moving transition probability from A to A

    path_to_arr_pl_M_T : string
        DESCRIPTION.
        path to save/get array arr_pl_M_T
        example: tests/AUTOMATE_INSTANCES_GAMES/\
                    arr_pl_M_T_players_set1_{m_players_set1}_set2_{m_players_set2}\
                        _periods_{t_periods}.npy
    used_instances : boolean
        DESCRIPTION.

    """
    
    dico_T_players = None;
    "dico_T{}_Mplayers_setA_{}_setB_{}_setC_{}_{}.json"
    filename_json = RACINE_FILENAME_JSON_PLAYERS.format(t_periods, 
                        setA_m_players, setB_m_players, setC_m_players, 
                        scenario_name)
    
    if path_2_save == "" :
        path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    Path(path_2_save).mkdir(parents=True, exist_ok=True)
    path_2_json_T_players = os.path.join(*[path_2_save, filename_json])
    
    if os.path.exists(path_2_json_T_players):
        # read dico_T_players from file
        if used_instances:
            # Read dico_T_players from file:
            dico_T_players = json.load( open( path_2_json_T_players ) )
            print("READ dico INSTANCE GENERATED")
            
        else:
            # create dico_T_players when used_instances = False
            dico_T_players =\
                generate_PiCiSi_scenario50instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setB_m_players=setB_m_players, dico_setB=dico_setB,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
            # convert dict to json then save : Serialize data into file:
            json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
            
            print("CREATE dict INSTANCE used_instance={}".format(used_instances))
    else:
        # create dico_T_players
        dico_T_players =\
                generate_PiCiSi_scenario50instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setB_m_players=setB_m_players, dico_setB=dico_setB,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
        # convert dict to json then save : Serialize data into file:
        json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
          
        print("NO PREVIOUS dict INSTANCE GENERATED: CREATE NOW !!!")
        
    return dico_T_players
    
def boolean_PiCiSi(dico_setX, Pi, Ci, Si, Si_init, setX):
    """
    test if 
    bool_Pi : Pi is between dico_setX["Pi"][0] and dico_setX["Pi"][1] and return True else false
    bool_Ci : Pi is between dico_setX["Ci"][0] and dico_setX["Ci"][1] and return True else false
    bool_Si : Pi is between dico_setX["Si"][0] and dico_setX["Si"][1] and return True else false
    """
    bool_Pi, bool_Ci, bool_Si, bool_Si_init = False, False, False, False
    if setX in [SET_ABC[0], SET_ABC[2], SET_AB1B2C[1], SET_AB1B2C[2]]:
        if Pi >= dico_setX["Pi"][0] and Pi <= dico_setX["Pi"][1]:
            bool_Pi = True
        if Ci >= dico_setX["Ci"][0] and Ci <= dico_setX["Ci"][1]:
            bool_Ci = True
        if Si >= dico_setX["Si"][0] and Si <= dico_setX["Si"][1]:
            bool_Si = True
        if Si == Si_init :
            bool_Si_init = True
    else:
        if (Pi >= dico_setX["Pi_inf_prob"][0] and Pi <= dico_setX["Pi_inf_prob"][1]) \
           or (Pi >= dico_setX["Pi_sup_prob"][0] and Pi <= dico_setX["Pi_sup_prob"][1]) :
            bool_Pi = True
        if (Ci >= dico_setX["Ci_inf_prob"][0] and Ci <= dico_setX["Ci_inf_prob"][1]) \
           or (Ci >= dico_setX["Ci_sup_prob"][0] and Ci <= dico_setX["Ci_sup_prob"][1]) :
            bool_Ci = True
        if (Si >= dico_setX["Si_inf_prob"][0] and Si <= dico_setX["Si_inf_prob"][1]) \
           or (Si >= dico_setX["Si_sup_prob"][0] and Si <= dico_setX["Si_sup_prob"][1]) :
            bool_Si = True
        if Si == Si_init :
            bool_Si_init = True
    return bool_Pi, bool_Ci, bool_Si, bool_Si_init
    
def checkout_dico_T_players(dico_T_players, dico_setA, dico_setB, dico_setC):
    """
    check out if values of variables are corrects ie values are inside 
    defined intervals on dico_setX
    """
    for t, dico_players in dico_T_players.items():
        cpt_t_Pi, cpt_t_Ci, cpt_t_Si, cpt_t_Si_init = 0, 0, 0, 0
        cpt_players = 0
        for player_name, player_i in dico_players.items():
            cpt_players += 1
            bool_Pi, bool_Ci, bool_Si, bool_Si_init = None, None, None, None
            setX = player_i["setX"][0]
            if setX == SET_ABC[0]:                                             # setA
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setA,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init,
                                     setX=setX)
            elif setX == SET_ABC[1]:                                           # setB
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setB,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init, 
                                     setX=setX)
            elif setX == SET_ABC[2]:                                           # setC
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setC,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init, 
                                     setX=setX)
            
            cpt_t_Pi += 1 if bool_Pi == True else 0
            cpt_t_Ci += 1 if bool_Ci == True else 0
            cpt_t_Si += 1 if bool_Si == True else 0
            cpt_t_Si_init += 1 if bool_Si_init == True else 0
            
        print("{} - correct: %Pi={}, %Ci={}, %Si={}, %Si_int={}".format( t,
              round(cpt_t_Pi/cpt_players, 2), round(cpt_t_Ci/cpt_players, 2), 
              round(cpt_t_Si/cpt_players, 2), round(cpt_t_Si_init/cpt_players, 2), 
                ))

###############################################################################
#            generate Pi, Ci by scenario_50Instances --> fin
###############################################################################

###############################################################################
#            generate Pi, Ci by scenarios 1 --> debut
###############################################################################
def generate_PiCiSi_scenario1instances(setA_m_players, dico_setA,
                                       setC_m_players, dico_setC,
                                       t_periods, 
                                       scenario, scenario_name):
    """
    generate Pi, Si, Ci of M players for multi periods on scenario 1

    Parameters
    ----------
    setA_m_players : int
        DESCRIPTION. number of players in the set A
    dico_setA : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setA = {"Pi":(5,10+1), "Ci":(15,15+1), "Si":(0,0+1),"Si_max":(20,20+1)}
    setC_m_players : int
        DESCRIPTION. number of players in the set C
    dico_setC : dict
        DESCRIPTION. contains the interval of values for each variable. 
        for example dico_setC = {"Pi":(21,30+1), "Ci":(20,20+1), "Si":(8,8+1),"Si_max":(20,20+1)}
    t_periods : int
        DESCRIPTION. number of periods. here t_periods = 1
    scenario : TYPE, optional
        DESCRIPTION. The default is None.
    scenario_name : TYPE, optional
        DESCRIPTION. The default is "scenario50instances".

    Returns
    -------
    dico_T_players: dict
    for example:
        {"t0":dico_players_t0, "t1":dico_players_t1, "t2":dico_players_t2, ...}  
        with dico_players_t0 = {"pl_0":dico_pl0, pl_1":dico_pl1, ... }
            dico_pl0 = {"Pi":[], "Ci":[], "Si":[], "Si_max":[], ....}

    """
    # ____ generation of sub set of players in setA and setC : debut   ____
    m_players = setA_m_players + setC_m_players
    id_players = range(0, m_players)
    
    setA_id_players = list(np.random.choice(list(id_players), 
                                            size=setA_m_players, 
                                            replace=False))
    remain_players = list(set(id_players) - set(setA_id_players))
    setC_id_players = list(np.random.choice(list(remain_players), 
                                            size=setC_m_players, 
                                            replace=False))
    remain_players = list(set(id_players) 
                          - set(setA_id_players) 
                          - set(setC_id_players))
    
    print("Remain_players: {} -> OK ".format(remain_players)) \
        if len(remain_players) == 0 \
        else print("Remain_players: {} -> NOK ".format(remain_players))
    print("generation players par setA, setC = OK") \
        if len(set(setA_id_players)
                   .intersection(
                       set(setC_id_players)
                       )
                ) == 0 \
        else print("generation players par setA, setC = NOK")
    # ____ generation of sub set of players in setA and setC : fin   ____
    
    dico_T_players = dict()
    
    for t in range(0, t_periods):
        dico_players_t = dict()
        for id_pl_i in range(0, m_players):
            Pi, Ci, Si, Si_max, setX_pl_i = None, None, None, None, None
            if id_pl_i in setA_id_players:
                setX_pl_i = SET_ABC[0]                                          # setA = Deficit
                Pi = np.random.randint(low=dico_setA["Pi"][0], 
                                       high=dico_setA["Pi"][1])
                Ci = np.random.randint(low=dico_setA["Ci"][0], 
                                       high=dico_setA["Ci"][1])
                Si = np.random.randint(low=dico_setA["Si"][0], 
                                       high=dico_setA["Si"][1])
                Si_max = np.random.randint(low=dico_setA["Si_max"][0], 
                                           high=dico_setA["Si_max"][1])
            elif id_pl_i in setC_id_players:
                setX_pl_i = SET_ABC[2]                                          # setC = Surplus
                Pi = np.random.randint(low=dico_setC["Pi"][0], 
                                       high=dico_setC["Pi"][1])
                Ci = np.random.randint(low=dico_setC["Ci"][0], 
                                       high=dico_setC["Ci"][1])
                Si = np.random.randint(low=dico_setC["Si"][0], 
                                       high=dico_setC["Si"][1])
                Si_max = np.random.randint(low=dico_setC["Si_max"][0], 
                                           high=dico_setC["Si_max"][1])
            
            # update arrays cells with variables
            col_vals = [("Pi",Pi), ("Ci",Ci), 
                        ("Si_init",Si), ("Si",Si), ("Si_max",Si_max), 
                        ("mode_i",""), ("state_i",""), ("setX", setX_pl_i)]
            dico_player_i = dict()
            for col in fct_aux.INDEX_ATTRS.keys():
                if col in ["Pi", "Ci", "Si_init", "Si", "Si_max", 
                           "setX"]:
                    val = [col_val[1] for col_val in col_vals if col_val[0] == col]
                    if col in ["Si", "setX"]:
                        dico_player_i[col] = val
                    else:
                        dico_player_i[col] = val[0]
                else:
                    dico_player_i[col] = []
                
            dico_players_t[fct_aux.RACINE_PLAYER+str(id_pl_i)] = dico_player_i    
       
        dico_T_players[fct_aux.RACINE_TPERIOD+str(t)] = dico_players_t
        
    return dico_T_players
            
               
def get_or_create_PiCiSi_players_scenario1instances(setA_m_players, dico_setA,
                                                    setC_m_players, dico_setC,
                                                    t_periods, 
                                                    scenario, scenario_name,
                                                    path_2_save, used_instances):
    dico_T_players = None;
    "dico_T{}_Mplayers_setA_{}_setC_{}_{}.json"
    filename_json = RACINE_SCEN1_FILENAME_JSON_PLAYERS.format(t_periods, 
                        setA_m_players, setC_m_players, scenario_name)
    
    if path_2_save == "" :
        path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    Path(path_2_save).mkdir(parents=True, exist_ok=True)
    path_2_json_T_players = os.path.join(*[path_2_save, filename_json])
    
    if os.path.exists(path_2_json_T_players):
        # read dico_T_players from file
        if used_instances:
            # Read dico_T_players from file:
            dico_T_players = json.load( open( path_2_json_T_players ) )
            print("READ dico INSTANCE GENERATED")
            
        else:
            # create dico_T_players when used_instances = False
            dico_T_players =\
                generate_PiCiSi_scenario1instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
            # convert dict to json then save : Serialize data into file:
            json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
            
            print("CREATE dict INSTANCE used_instance={}".format(used_instances))
    else:
        # create dico_T_players
        dico_T_players =\
                generate_PiCiSi_scenario1instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
        # convert dict to json then save : Serialize data into file:
        json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
          
        print("NO PREVIOUS dict INSTANCE GENERATED: CREATE NOW !!!")
        
    return dico_T_players
    
def checkout_dico_T_players_scenario123(dico_T_players, 
                                        scenario_name,
                                        dico_setA, 
                                        dico_setB1, dico_setB2, 
                                        dico_setC):
    """
    check out if values of variables are corrects ie values are inside 
    defined intervals on dico_setX
    """
    for t, dico_players in dico_T_players.items():
        cpt_t_Pi, cpt_t_Ci, cpt_t_Si, cpt_t_Si_init = 0, 0, 0, 0
        cpt_players = 0
        for player_name, player_i in dico_players.items():
            cpt_players += 1
            Pi, Ci, Si, Si_init = None, None, None, None
            bool_Pi, bool_Ci, bool_Si, bool_Si_init = None, None, None, None
            setX = player_i["setX"][0]
            if setX == SET_AB1B2C[0]:                                          # setA
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setA,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init,
                                     setX=setX)
            elif setX == SET_AB1B2C[1] and dico_setB1 is not None:             # setB1
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setB1,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init, 
                                     setX=setX)
            elif setX == SET_AB1B2C[2] and dico_setB2 is not None:             # setB2
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setB2,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init, 
                                     setX=setX)
            elif setX == SET_AB1B2C[3] and dico_setC is not None:             # setC
                Pi = player_i["Pi"]; Ci = player_i["Ci"]; 
                Si = player_i["Si"][0]; Si_init = player_i["Si_init"]; 
                bool_Pi, bool_Ci, bool_Si, bool_Si_init \
                    = boolean_PiCiSi(dico_setX=dico_setC,
                                     Pi=Pi, Ci=Ci, Si=Si, Si_init=Si_init, 
                                     setX=setX)
                    
            cpt_t_Pi += 1 if bool_Pi == True else 0
            cpt_t_Ci += 1 if bool_Ci == True else 0
            cpt_t_Si += 1 if bool_Si == True else 0
            cpt_t_Si_init += 1 if bool_Si_init == True else 0
            
            # print("{}: Pi={}, Ci={}, Si={}, Si_init={}, bool_Pi={}, bool_Ci={}, bool_Si={}, bool_Si_init={}".format(
            #         player_name, Pi, Ci, Si, Si_init, bool_Pi, bool_Ci, bool_Si, bool_Si_init))
                    
            
        print("{} {} - correct: %Pi={}, %Ci={}, %Si={}, %Si_int={}".format( 
              scenario_name, t,
              round(cpt_t_Pi/cpt_players, 2), round(cpt_t_Ci/cpt_players, 2), 
              round(cpt_t_Si/cpt_players, 2), round(cpt_t_Si_init/cpt_players, 2), 
                ))
            
            
###############################################################################
#            generate Pi, Ci by scenarios 1 --> fin
###############################################################################

###############################################################################
#            generate Pi, Ci by scenarios 2,3 --> debut
###############################################################################
def generate_PiCiSi_scenario23instances(setA_m_players, dico_setA,
                                        setB1_m_players, dico_setB1,
                                        setB2_m_players, dico_setB2,
                                        setC_m_players, dico_setC,
                                        t_periods, 
                                        scenario, 
                                        scenario_name):
     """
        generate Pi, Si, Ci of M players for multi periods on scenario 2, 3
    
        Parameters
        ----------
        setA_m_players : int
            DESCRIPTION. number of players in the set A
        dico_setA : dict
            DESCRIPTION. contains the interval of values for each variable. 
            for example dico_setA = {"Pi":(5,10+1), "Ci":(15,15+1), "Si":(0,0+1),"Si_max":(20,20+1)}
        setC_m_players : int
            DESCRIPTION. number of players in the set C
        dico_setC : dict
            DESCRIPTION. contains the interval of values for each variable. 
            for example dico_setC = {"Pi":(21,30+1), "Ci":(20,20+1), "Si":(8,8+1),"Si_max":(20,20+1)}
        t_periods : int
            DESCRIPTION. number of periods. here t_periods = 1
        scenario : TYPE, optional
            DESCRIPTION. The default is None.
        scenario_name : TYPE, optional
            DESCRIPTION. The default is "scenario50instances".
    
        Returns
        -------
        dico_T_players: dict
        for example:
            {"t0":dico_players_t0, "t1":dico_players_t1, "t2":dico_players_t2, ...}  
            with dico_players_t0 = {"pl_0":dico_pl0, pl_1":dico_pl1, ... }
                dico_pl0 = {"Pi":[], "Ci":[], "Si":[], "Si_max":[], ....}
    
     """
     # ____ generation of sub set of players in setA, setB1, setB2 and setC : debut ____
     m_players = setA_m_players + setB1_m_players + setB2_m_players + setC_m_players
     list_players = range(0, m_players)
    
     setA_id_players = list(np.random.choice(list(list_players), 
                                            size=setA_m_players, 
                                            replace=False))
     remain_players = list(set(list_players) - set(setA_id_players))
     setB1_id_players = list(np.random.choice(list(remain_players), 
                                            size=setB1_m_players, 
                                            replace=False))
     remain_players = list(set(list_players) 
                          - set(setA_id_players) 
                          - set(setB1_id_players))
     setB2_id_players = list(np.random.choice(list(remain_players), 
                                            size=setB2_m_players, 
                                            replace=False))
     remain_players = list(set(list_players) 
                          - set(setA_id_players) 
                          - set(setB1_id_players)
                          - set(setB2_id_players))
     setC_id_players = list(np.random.choice(list(remain_players), 
                                            size=setC_m_players, 
                                            replace=False))
     remain_players = list(set(list_players) 
                          - set(setA_id_players) 
                          - set(setB1_id_players)
                          - set(setB2_id_players)
                          - set(setC_id_players))
     print("Remain_players: {} -> OK ".format(remain_players)) \
         if len(remain_players) == 0 \
         else print("Remain_players: {} -> NOK ".format(remain_players))
     print("generation players par setA, setB1, setB2, setC = OK") \
         if len(set(setA_id_players)
                   .intersection(
                       set(setB1_id_players)
                       .intersection(
                           set(setB2_id_players)
                           .intersection(
                               set(setC_id_players)
                           ))
                       )
                ) == 0 \
         else print("generation players par setA, setB1, setB2, setC = NOK")
     # ____ generation of sub set of players in setA, setB1, setB2 and setC : fin ____
     
     dico_T_players = dict()
     
     for t in range(0, t_periods):
         dico_players_t = dict()
         for id_pl_i in range(0, m_players):
             Pi, Ci, Si, Si_max, setX_pl_i = None, None, None, None, None
             if id_pl_i in setA_id_players:
                 setX_pl_i = SET_AB1B2C[0]                                     # setA = Deficit
                 Pi = np.random.randint(low=dico_setA["Pi"][0], 
                                       high=dico_setA["Pi"][1])
                 Ci = np.random.randint(low=dico_setA["Ci"][0], 
                                       high=dico_setA["Ci"][1])
                 Si = np.random.randint(low=dico_setA["Si"][0], 
                                       high=dico_setA["Si"][1])
                 Si_max = np.random.randint(low=dico_setA["Si_max"][0], 
                                           high=dico_setA["Si_max"][1])
             elif id_pl_i in setB1_id_players:
                setX_pl_i = SET_AB1B2C[1]                                      # setB1 = Self
                Pi = np.random.randint(low=dico_setB1["Pi"][0], 
                                       high=dico_setB1["Pi"][1])
                Ci = np.random.randint(low=dico_setB1["Ci"][0], 
                                       high=dico_setB1["Ci"][1])
                Si = np.random.randint(low=dico_setB1["Si"][0], 
                                       high=dico_setB1["Si"][1])
                Si_max = np.random.randint(low=dico_setB1["Si_max"][0], 
                                           high=dico_setB1["Si_max"][1])
             
             elif id_pl_i in setB2_id_players:
                setX_pl_i = SET_AB1B2C[2]                                      # setB2 = Self
                Pi = np.random.randint(low=dico_setB2["Pi"][0], 
                                       high=dico_setB2["Pi"][1])
                Ci = np.random.randint(low=dico_setB2["Ci"][0], 
                                       high=dico_setB2["Ci"][1])
                Si = np.random.randint(low=dico_setB2["Si"][0], 
                                       high=dico_setB2["Si"][1])
                Si_max = np.random.randint(low=dico_setB2["Si_max"][0], 
                                           high=dico_setB2["Si_max"][1])
                
             elif id_pl_i in setC_id_players:
                setX_pl_i = SET_AB1B2C[3]                                      # setC = Surplus
                Pi = np.random.randint(low=dico_setC["Pi"][0], 
                                       high=dico_setC["Pi"][1])
                Ci = np.random.randint(low=dico_setC["Ci"][0], 
                                       high=dico_setC["Ci"][1])
                Si = np.random.randint(low=dico_setC["Si"][0], 
                                       high=dico_setC["Si"][1])
                Si_max = np.random.randint(low=dico_setC["Si_max"][0], 
                                           high=dico_setC["Si_max"][1])
            
             # update arrays cells with variables
             col_vals = [("Pi",Pi), ("Ci",Ci), 
                        ("Si_init",Si), ("Si",Si), ("Si_max",Si_max), 
                        ("mode_i",""), ("state_i",""), ("setX", setX_pl_i)]
             dico_player_i = dict()
             for col in fct_aux.INDEX_ATTRS.keys():
                 if col in ["Pi", "Ci", "Si_init", "Si", "Si_max", 
                           "setX"]:
                    val = [col_val[1] for col_val in col_vals if col_val[0] == col]
                    if col in ["Si", "setX"]:
                        dico_player_i[col] = val
                    else:
                        dico_player_i[col] = val[0]
                 else:
                    dico_player_i[col] = []
                
             dico_players_t[fct_aux.RACINE_PLAYER+str(id_pl_i)] = dico_player_i    
       
         dico_T_players[fct_aux.RACINE_TPERIOD+str(t)] = dico_players_t
        
     return dico_T_players
    
def get_or_create_PiCiSi_players_scenario23instances(setA_m_players, dico_setA,
                                                     setB1_m_players, dico_setB1,
                                                     setB2_m_players, dico_setB2,
                                                     setC_m_players, dico_setC,
                                                     t_periods, 
                                                     scenario, scenario_name,
                                                     path_2_save, used_instances):
    dico_T_players = None;
    "dico_T{}_Mplayers_setA_{}_setB1_{}_setB2_{}_setC_{}_{}.json"
    filename_json = RACINE_SCEN23_FILENAME_JSON_PLAYERS.format(t_periods, 
                        setA_m_players, 
                        setB1_m_players, setB2_m_players, 
                        setC_m_players, scenario_name)
    
    if path_2_save == "" :
        path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    Path(path_2_save).mkdir(parents=True, exist_ok=True)
    path_2_json_T_players = os.path.join(*[path_2_save, filename_json])
    
    if os.path.exists(path_2_json_T_players):
        # read dico_T_players from file
        if used_instances:
            # Read dico_T_players from file:
            dico_T_players = json.load( open( path_2_json_T_players ) )
            print("READ dico INSTANCE GENERATED")
            
        else:
            # create dico_T_players when used_instances = False
            dico_T_players =\
                generate_PiCiSi_scenario23instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setB1_m_players=setB1_m_players, dico_setB1=dico_setB1,
                    setB2_m_players=setB2_m_players, dico_setB2=dico_setB2,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
            # convert dict to json then save : Serialize data into file:
            json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
            
            print("CREATE dict INSTANCE used_instance={}".format(used_instances))
    else:
        # create dico_T_players
        dico_T_players =\
                generate_PiCiSi_scenario23instances(
                    setA_m_players=setA_m_players, dico_setA=dico_setA,
                    setB1_m_players=setB1_m_players, dico_setB1=dico_setB1,
                    setB2_m_players=setB2_m_players, dico_setB2=dico_setB2,
                    setC_m_players=setC_m_players, dico_setC=dico_setC,
                    t_periods=t_periods, 
                    scenario=scenario, 
                    scenario_name=scenario_name)
                
        # convert dict to json then save : Serialize data into file:
        json.dump( dico_T_players, open( path_2_json_T_players, 'w' ) )
          
        print("NO PREVIOUS dict INSTANCE GENERATED: CREATE NOW !!!")
        
    return dico_T_players
###############################################################################
#            generate Pi, Ci by scenarios 2,3 --> fin
###############################################################################

#------------------------------------------------------------------------------
#           definitions of unittest
#------------------------------------------------------------------------------
def test_get_or_create_PiCiSi_players_scenario50instances():
    setA_m_players = 200 #2 #20;
    setB_m_players = 300 #3 #30;
    setC_m_players = 400 #4 #40;
    dico_setA = {"Pi":(5,10+1), "Ci":(15,15+1), "Si":(0,0+1),"Si_max":(20,20+1)}
    dico_setB = {"Pi_inf_prob":(5,8+1), "Ci_inf_prob":(10,10+1), 
                 "Pi_sup_prob":(21,30+1), "Ci_sup_prob":(31,31+1), 
                 "Si_inf_prob":(6,6+1),"Si_max_inf_prob":(20,20+1),
                 "Si_sup_prob":(8,8+1),"Si_max_sup_prob":(20,20+1)}
    dico_setC = {"Pi":(21,30+1), "Ci":(20,20+1), "Si":(8,8+1),"Si_max":(20,20+1)}
    t_periods = 1
    scenario = None 
    scenario_name = "scenario50instances"
    path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    used_instances = True #False
    
    dico_T_players = get_or_create_PiCiSi_players_scenario50instances(
                        setA_m_players=setA_m_players, dico_setA=dico_setA,
                        setB_m_players=setB_m_players, dico_setB=dico_setB,
                        setC_m_players=setC_m_players, dico_setC=dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
    
    checkout_dico_T_players(dico_T_players=dico_T_players, 
                            dico_setA=dico_setA, dico_setB=dico_setB, 
                            dico_setC=dico_setC)
    return dico_T_players

def test_get_or_create_PiCiSi_players_scenarios123():
    setA_m_players = 200 #200 #2 #20;
    setB1_m_players = 300 #300 #3 #30;
    setB2_m_players = 300 #300 #3 #30;
    setC_m_players = 400 #400 #4 #40;
    t_periods = 5
    path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    used_instances = False #True #False, True
    
    # values of variables for scenarios1,2,3
    scen1_pr = 0.6
    scen1_dico_setA = {"Pi":(0,0+1), "Ci":(10,10+1), "Si":(3,3+1),"Si_max":(20,20+1)}
    scen1_dico_setC = {"Pi":(20,20+1), "Ci":(10,10+1), "Si":(10,10+1),"Si_max":(20,20+1)}
    prob_A_A = scen1_pr; prob_A_C = 1-scen1_pr;
    prob_C_A = 1-scen1_pr; prob_C_C = scen1_pr;
    scenario1 = [(prob_A_A, prob_A_C), 
                (prob_C_A, prob_C_C)]
    
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
    
    
    #root_doc_VALUES = "Doc{}".format(doc_VALUES)
    dico_scenarios = {"scenario1": scenario1,
                     "scenario2": scenario2, 
                     "scenario3": scenario3}
    for scenario_name, scenario in dico_scenarios.items():
        if scenario_name == "scenario1":
            dico_T_players = get_or_create_PiCiSi_players_scenario1instances(
                        setA_m_players=setA_m_players, dico_setA=scen1_dico_setA,
                        setC_m_players=setC_m_players, dico_setC=scen1_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
    
            checkout_dico_T_players_scenario123(dico_T_players=dico_T_players, 
                                    scenario_name=scenario_name,
                                    dico_setA=scen1_dico_setA, 
                                    dico_setB1=None, dico_setB2=None, 
                                    dico_setC=scen1_dico_setC)
        elif scenario_name == "scenario2":
            dico_T_players = get_or_create_PiCiSi_players_scenario23instances(
                        setA_m_players=setA_m_players, dico_setA=scen2_dico_setA,
                        setB1_m_players=setB1_m_players, dico_setB1=scen2_dico_setB1,
                        setB2_m_players=setB2_m_players, dico_setB2=scen2_dico_setB2,
                        setC_m_players=setC_m_players, dico_setC=scen2_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
            checkout_dico_T_players_scenario123(dico_T_players=dico_T_players, 
                                    scenario_name=scenario_name,
                                    dico_setA=scen2_dico_setA, 
                                    dico_setB1=scen2_dico_setB1, 
                                    dico_setB2=scen2_dico_setB2, 
                                    dico_setC=scen2_dico_setC)
        elif scenario_name == "scenario3":
            dico_T_players = get_or_create_PiCiSi_players_scenario23instances(
                        setA_m_players=setA_m_players, dico_setA=scen3_dico_setA,
                        setB1_m_players=setB1_m_players, dico_setB1=scen3_dico_setB1,
                        setB2_m_players=setB2_m_players, dico_setB2=scen3_dico_setB2,
                        setC_m_players=setC_m_players, dico_setC=scen3_dico_setC,
                        t_periods=t_periods, 
                        scenario=scenario, 
                        scenario_name=scenario_name,
                        path_2_save=path_2_save, 
                        used_instances=used_instances)
            checkout_dico_T_players_scenario123(dico_T_players=dico_T_players, 
                                    scenario_name=scenario_name,
                                    dico_setA=scen3_dico_setA, 
                                    dico_setB1=scen3_dico_setB1, 
                                    dico_setB2=scen3_dico_setB2, 
                                    dico_setC=scen3_dico_setC)

if __name__ == "__main__":
    ti = time.time()
    dico = test_get_or_create_PiCiSi_players_scenario50instances()
    
    test_get_or_create_PiCiSi_players_scenarios123()
    print(" running time ={}".format(time.time()-ti))