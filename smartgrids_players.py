#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 08:54:28 2021

@author: willy
"""

import time
import math
import numpy as np

import fonctions_auxiliaires as fct_aux

class Player:
    
    cpt_player =  0
    
    def __init__(self, Pi, Ci, Si_init, Si_max, 
                 gamma_i, prod_i, cons_i, r_i, state_i):
        self.name = ("").join(["a",str(self.cpt_player)])
        self.Pi = Pi
        self.Ci = Ci
        self.Si_init = Si_init
        self.Si_max = Si_max
        self.gamma_i = gamma_i
        Player.cpt_player += 1
        
        # variables depend on a decision of the instance
        self.prod_i = prod_i
        self.cons_i = cons_i
        self.R_i = 0
        self.Si = 0
        self.Si_minus = 0
        self.Si_plus = 0
        self.r_i = r_i
        self.state_i = state_i
        self.mode_i = ""
        
    #--------------------------------------------------------------------------
    #           definition of caracteristics of an agent
    #--------------------------------------------------------------------------
    def get_Pi(self):
        """
        return the value of quantity of production
        """
        return self.Pi
    
    def set_Pi(self, new_Pi, update=False):
        """
        return the new quantity of production or the energy quantity 
        to add from the last quantity of production.
        
        self.Pi = new_Pi if update==True else self.Pi + new_Pi
        """
        self.Pi = (update==False)*new_Pi + (update==True)*(self.Pi + new_Pi)
            
    def get_Ci(self):
        """
        return the quantity of consumption 
        """
        return self.Ci
    
    def set_Ci(self, new_Ci, update=False):
        """
        return the new quantity of consumption or the energy quantity 
        to add from the last quantity of production.
        
        self.Ci = new_Ci if update==True else self.Ci + new_Ci
        """
        self.Ci = (update==False)*new_Ci + (update==True)*(self.Ci + new_Ci)
       
    def get_Si_init(self):
        """
        return the value of quantity of battery storage
        """
        return self.Si_init
    
    def set_Si_init(self, new_Si_init, update=False):
        """
        return the new quantity of battery storage or the energy quantity 
        to add from the last quantity of storage.
        
        self.Si = new_Si if update==True else self.Si + new_Si
        """
        self.Si_init = (update==False)*new_Si_init \
                        + (update==True)*(self.Si_init + new_Si_init)
    
    def get_Si(self):
        """
        return the value of quantity of battery storage
        """
        return self.Si
    
    def set_Si(self, new_Si, update=False):
        """
        return the new quantity of battery storage or the energy quantity 
        to add from the last quantity of storage.
        
        self.Si = new_Si if update==True else self.Si + new_Si
        """
        self.Si = (update==False)*new_Si + (update==True)*(self.Si + new_Si)
        
    def get_Si_max(self):
        """
        return the value of quantity of production
        """
        return self.Si_max
    
    def set_Si_max(self, new_Si_max, update=False):
        """
        return the new quantity of the maximum battery storage or the energy 
        quantity to add from the last quantity of teh maximum storage.
        
        self.Si = new_Pi if update==True else self.Pi + new_Pi
        """
        self.Si_max = (update==False)*new_Si_max \
                        + (update==True)*(self.Si_max + new_Si_max)
                        
    def get_R_i(self):
        """
        return the reserv amount before updating Si

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.R_i
    
    def set_R_i(self, new_R_i, update=False):
        """
        turn the old reserv amount into new_R_i if update=False else add 
        new_R_i  to the last value

        Parameters
        ----------
        new_R_i : float
            DESCRIPTION.
        update : booelan, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.R_i = (update==False)*new_R_i \
                        + (update==True)*(self.R_i + new_R_i)
                        
    def get_Si_minus(self):
        """
        return the min battery storage amount between 2 modes of one state state_i

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.Si_minus
    
    def set_Si_minus(self, new_Si_minus, update=False):
        """
        turn the old min battery storage amount into new_Si_minus if update=False else add 
        new_Si_minus to the last value

        Parameters
        ----------
        new_Si_minus : float
            DESCRIPTION.
        update : boolean, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.Si_minus = (update==False)*new_Si_minus \
                        + (update==True)*(self.Si_minus + new_Si_minus)
                        
    def get_Si_plus(self):
        """
        return the max battery storage amount between 2 modes of one state state_i

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.Si_plus
    
    def set_Si_plus(self, new_Si_plus, update=False):
        """
        turn the old max battery storage amount into new_Si_plus if update=False else add 
        new_Si_plus to the last value

        Parameters
        ----------
        new_Si_plus : float
            DESCRIPTION.
        update : boolean, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.Si_plus = (update==False)*new_Si_plus \
                        + (update==True)*(self.Si_plus + new_Si_plus)
                        
    def get_gamma_i(self):
        """
        gamma denotes the behaviour of the agent to store energy or not. 
        the value implies the price of purchase/sell energy.
        return the value of the behaviour  
    
        NB: if gamma_i = np.inf, the agent has a random behaviour ie he has 
            50% of chance to store energy
        """
        return self.gamma_i
    
    def set_gamma_i(self, new_gamma_i):
        """
        return the new value of the behaviour or the energy 
        quantity to add from the last quantity of the maximum storage.
        
        NB: if gamma_i = np.inf, the agent has a random behaviour ie he has 
            50% of chance to store energy
        """
        self.gamma_i = new_gamma_i 
        
    def get_prod_i(self):
        """
        return the production amount to export to SG 

        Returns
        -------
        an integer or float.

        """
        return self.prod_i
    
    def set_prod_i(self, new_prod_i, update=False):
        """
        turn the production amount into new_prod_i if update=False else add 
        new_prod_i  to the last value

        Parameters
        ----------
        new_prod_i : float
            DESCRIPTION.
        update : booelan, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.prod_i = (update==False)*new_prod_i \
                        + (update==True)*(self.prod_i + new_prod_i)
                        
    def get_cons_i(self):
        """
        return the consumption amount to import from HP to SG 

        Returns
        -------
        an integer or float.

        """
        return self.cons_i
    
    def set_cons_i(self, new_cons_i, update=False):
        """
        turn the consumption amount into new_cons_i if update=False else add 
        new_cons_i  to the last value

        Parameters
        ----------
        new_cons_i : float
            DESCRIPTION.
        update : booelan, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.cons_i = (update==False)*new_cons_i \
                        + (update==True)*(self.cons_i + new_cons_i)
                        
    def get_r_i(self):
        """
        return the consumption amount to import from HP to SG 

        Returns
        -------
        an integer or float.

        """
        return self.r_i
    
    def set_r_i(self, new_r_i, update=False):
        """
        turn the amount of energy stored (or preserved by a player) into 
        new_r_i if update=False else add new_ri_i  to the last value

        Parameters
        ----------
        new_r_i : float
            DESCRIPTION.
        update : booelan, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        float.

        """
        self.r_i = (update==False)*new_r_i \
                        + (update==True)*(self.r_i + new_r_i)
                        
    def get_state_i(self):
        """
        return the state of the player

        Returns
        -------
        None.

        """
        return self.state_i
    
    def find_out_state_i(self):
        """
        return the state of the player depending on the operation conditions 

        Returns
        -------
        a string.

        """
        if self.Pi + self.Si_init <= self.Ci:
            self.state_i = fct_aux.STATES[0]
        elif self.Pi + self.Si_init > self.Ci and self.Pi <= self.Ci:
            self.state_i = fct_aux.STATES[1]
        elif self.Pi >= self.Ci:
            self.state_i = fct_aux.STATES[2]
        else:
            self.state_i = None
        return self.state_i
    
    def set_state_i(self, new_state_i):
        """
        turn the player state into 
        new_state_i

        Parameters
        ----------
        new_state_i : string
            DESCRIPTION.

        Returns
        -------
        a string.

        """
        self.state_i = new_state_i 
        
    def get_mode_i(self):
        """
        return the mode of player i

        Returns
        -------
        a string.

        """
        return self.mode_i
    
    def set_mode_i(self, new_mode_i):
        """
        update the mode of player i

        Returns
        -------
        None.

        """
        self.mode_i = new_mode_i
        
        
    #--------------------------------------------------------------------------
    #           definition of functions of an agent
    #--------------------------------------------------------------------------
    def select_mode_i(self, p_i=0.5):
        """
        select randomly a mode of an agent i
        
        Parameters
        ----------
        p_i: float [0,1], 
            DESCRIPTION. The default is 0.5
            probability to choose the first item in state mode

        Returns
        -------
        update variable mode_i containing
        string value if state_i != None or None if state_i == None

        """
        mode_i = None
        rd_num =  np.random.choice([0,1], p=[p_i, 1-p_i])
        if self.state_i == None:
            mode_i = None
        elif self.state_i == fct_aux.STATES[0]:                                 # Deficit or state1
            mode_i = fct_aux.STATE1_STRATS[rd_num]
        elif self.state_i == fct_aux.STATES[1]:                                 # Self or state2
            mode_i = fct_aux.STATE2_STRATS[rd_num]
        elif self.state_i == fct_aux.STATES[2]:                                 # Surplus or state3
            mode_i = fct_aux.STATE3_STRATS[rd_num]
        self.mode_i = mode_i
        
    def update_prod_cons_r_i(self):
        """
        compute prod_i, cons_i and r_i following the characteristics of agent i 

        Returns
        -------
        update variable prod_i, cons_i, r_i containing
        float value if state != None or np.nan if state == None.

        """
        
        # compute preserved stock r_i
        if self.mode_i == fct_aux.STATE1_STRATS[0]:                            # CONS+
            self.r_i = 0
        elif self.mode_i == fct_aux.STATE1_STRATS[1]:                          # CONS-
            self.r_i = self.Si_init
        elif self.mode_i == fct_aux.STATE3_STRATS[1]:                          # PROD 
            self.r_i = self.Si_init
        elif self.mode_i == fct_aux.STATE2_STRATS[0] \
            and self.state_i ==  fct_aux.STATES[1]:                            # DIS, Self or state2
            self.r_i = self.Si_init - (self.Ci - self.Pi)
        elif self.mode_i == fct_aux.STATE3_STRATS[0] \
            and self.state_i ==  fct_aux.STATES[2]:                            # DIS, Surplus or state3
            self.r_i = min(self.Si_max - self.Si_init, self.Pi - self.Ci)
        
        if self.state_i ==  fct_aux.STATES[0]:                                 # Deficit
            self.prod_i = 0
            self.cons_i = (self.mode_i == "CONS+")*(self.Ci - (self.Pi + self.Si_init)) \
                            + (self.mode_i == "CONS-")*(self.Ci - self.Pi)
            self.Si = (self.mode_i == "CONS+")*0 \
                        + (self.mode_i == "CONS-")*self.Si_init
            self.R_i = self.Si_max - self.Si
            
            
        elif self.state_i ==  fct_aux.STATES[1]:                               # Self
            self.prod_i = 0
            self.cons_i = (self.mode_i == "DIS")*0 \
                            + (self.mode_i == "CONS-")*(self.Ci - self.Pi)
            self.Si = (self.mode_i == "DIS")*(
                        max(0, self.Si_init - (self.Ci - self.Pi))) \
                        + (self.mode_i == "CONS-")*self.Si_init
    
        elif self.state_i ==  fct_aux.STATES[2]:                               # Surplus
            self.cons_i = 0
            if self.Pi == self.Ci:
                self.Si = self.Si_init
                self.prod_i = 0
            else:
                self.Si = (self.mode_i == "DIS") \
                                *(min(self.Si_max, self.Si_init + (self.Pi - self.Ci))) \
                            + (self.mode_i == "PROD")*self.Si_init
                self.R_i = self.Si_max - self.Si_init
                self.prod_i = (self.mode_i == "PROD")*(self.Pi - self.Ci)\
                               + (self.mode_i == "DIS") \
                                   *fct_aux.fct_positive(sum([self.Pi]), 
                                                         sum([self.Ci, self.R_i]))
            
        else:
            # state_i = mode_i = None
            self.prod_i = np.nan
            self.cons_i = np.nan
            self.r_i = np.nan
        
    def balanced_player(self, thres=0.1, dbg=False):
        if dbg:
            print("_____ balanced_player Pi={}, Ci={}, Si_init={}, Si_max={}, Si={}, state_i={}, mode_i={}"\
                  .format(self.Pi, self.Ci, self.Si_init, self.Si_max(), self.Si, 
                          self.state_i, self.mode_i ))
                
        boolean = None
        if self.state_i == "Deficit" and self.mode_i == "CONS+":
            boolean = True if np.abs(self.Ci - (self.Pi+self.Si_init+self.cons_i))<thres \
                            else False
            formule = "Ci - (Pi+Si_init+cons_i)"
        elif self.state_i == "Deficit" and self.mode_i == "CONS-":
            boolean = True if np.abs(self.Ci - (self.Pi+self.cons_i))<thres \
                            else False
            formule = "Ci - (Pi+cons_i)"
        elif self.state_i == "Self" and self.mode_i == "DIS":
            # boolean = True if np.abs(self.Si_init - (self.Si+self.Ci-self.Pi))<thres \
            #                 else False
            # formule = "Si_init - (Si+Ci-Pi)"
            boolean = True if np.abs(self.Si_init-self.Si-self.Ci+self.Pi)<thres \
                            else False
            formule = "Si_init-Si - Ci+Pi"
        elif self.state_i == "Self" and self.mode_i == "CONS-":
            boolean = True if np.abs(self.Pi+self.cons_i - self.Ci)<thres \
                            else False
            formule = "Pi+cons_i - Ci"
        elif self.state_i == "Surplus" and self.mode_i == "PROD":
            boolean = True if np.abs(self.Pi - self.Ci-self.prod_i)<thres else False
            formule = "Pi - Ci-prod_i"
        elif self.state_i == "Surplus" and self.mode_i == "DIS":
            boolean = True if np.abs((self.Pi+self.Si_init) \
                                     - (self.Ci+self.Si+self.prod_i)) < thres \
                            else False
            formule = "Pi+Si_init - (Ci+Si+prod_i)"
            
        return boolean, formule
    
    
#------------------------------------------------------------------------------
#           unit test of functions
#------------------------------------------------------------------------------
def test_class_player_geneMTobjets(dbg):
    import os
    import generation_data_scenarios as geneData
    
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
    
    setA_m_players = 2 #20;
    setB1_m_players = 3 #30;
    setB2_m_players = 3 #30;
    setC_m_players = 4 #40;
    setA_m_players = 2000; setB1_m_players = 3000; setB2_m_players = 3000; setC_m_players = 4000;
    t_periods = 5
    path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    used_instances = False #True #False, True
    
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
    
    gamma_i, prod_i, cons_i, r_i, state_i = 0, 0, 0, 0, ""
    for t, dico_players in dico_T_players.items():
        cpt_boolTrue_t = 0
        dure_init = time.time()
        state_is = []; mode_is = []; prod_is = []; cons_is = []; balanced_s = []
        Pis = []; Cis = []; Sis_init=[]; Sis = []; Sis_max = [];
        for player_name, player_i in dico_players.items():
            Pi = player_i["Pi"]; Ci = player_i["Ci"]; Si_max = player_i["Si_max"];
            Si = player_i["Si"][0]; Si_init = player_i["Si_init"];
            ag = [Pi, Ci, Si_init, Si_max, gamma_i, prod_i, cons_i, r_i, state_i]
            pl = Player(*ag)
            state_pli = pl.find_out_state_i()
            pl.select_mode_i(0.5)
            pl.update_prod_cons_r_i()
            boolean, formule = pl.balanced_player(thres=0.1, dbg=False)
            cpt_boolTrue_t += 1 if boolean else 0
            
            state_is.append(pl.get_state_i()); mode_is.append(pl.get_mode_i());
            prod_is.append(pl.get_prod_i()); cons_is.append(pl.get_cons_i());
            Pis.append(pl.get_Pi()); Cis.append(pl.get_Ci()); 
            Sis_init.append(pl.get_Si_init()); Sis.append(pl.get_Si());
            Sis_max.append(Si_max);
            balanced_s.append(boolean)
            
        if dbg:
            print("st_mod_prod_cons={}".format( list(zip(state_is,mode_is,prod_is,cons_is)) ))
        print("t={} balanced_player={}, duree={}".format(
                t, round(cpt_boolTrue_t/len(dico_players), 2), 
                round(time.time()-dure_init,5)))
            
def test_class_player_geneMobjets(dbg):
    import os
    import generation_data_scenarios as geneData
    
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
    
    setA_m_players = 2 #20;
    setB1_m_players = 3 #30;
    setB2_m_players = 3 #30;
    setC_m_players = 4 #40;
    setA_m_players = 2000; setB1_m_players = 3000; setB2_m_players = 3000; setC_m_players = 4000;
    t_periods = 5
    path_2_save = os.path.join(*["tests", "AUTOMATE_INSTANCES_GAMES"])
    used_instances = False #True #False, True
    
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
    
    gamma_i, prod_i, cons_i, r_i, state_i = 0, 0, 0, 0, ""
    for t, dico_players in dico_T_players.items():
        cpt_boolTrue_t = 0
        dure_init = time.time()
        l_players = list()
        for id_pl in range(0, len(dico_players)):
            Pi=0; Ci=0; Si_init=0; Si_max=0; gamma_i=0; prod_i=0; cons_i=0; r_i=0; state_i=""
            ag = [Pi, Ci, Si_init, Si_max, gamma_i, prod_i, cons_i, r_i, state_i]
            pl = Player(*ag)
            l_players.append(pl)
        state_is = []; mode_is = []; prod_is = []; cons_is = []
        Pis = []; Cis = []; Sis_init=[]; Sis = []; Sis_max = [];
        balanced_s = []
        id_pl = 0
        for player_name, player_i in dico_players.items():
            Pi = player_i["Pi"]; Ci = player_i["Ci"]; Si_max = player_i["Si_max"];
            Si = player_i["Si"][0]; Si_init = player_i["Si_init"];
            pl = l_players[id_pl]
            pl.set_Pi(new_Pi=Pi, update=False); pl.set_Ci(new_Ci=Ci, update=False);
            pl.set_Si(new_Si=Si, update=False); 
            pl.set_Si_init(new_Si_init=Si_init, update=False);
            state_pli = pl.find_out_state_i()
            pl.select_mode_i(0.5)
            pl.update_prod_cons_r_i()
            boolean, formule = pl.balanced_player(thres=0.1, dbg=False)
            cpt_boolTrue_t += 1 if boolean else 0
            state_is.append(pl.get_state_i()); mode_is.append(pl.get_mode_i());
            prod_is.append(pl.get_prod_i()); cons_is.append(pl.get_cons_i());
            Pis.append(pl.get_Pi()); Cis.append(pl.get_Ci()); 
            Sis_init.append(pl.get_Si_init()); Sis.append(pl.get_Si());
            Sis_max.append(Si_max);
            balanced_s.append(boolean)
            
            # print("player {}: id={}".format(id_pl, id(pl)))
            id_pl += 1
            
        if dbg:
            print("st_mod_prod_cons_Pi_Ci_Si_Siinit_Simax_balanced={}".format( 
                list(zip(state_is,mode_is,prod_is,cons_is, Pis, Cis, Sis, Sis_init, Sis_max, balanced_s)) ))
        print("t={} balanced_player={}, duree={}".format(
                t, round(cpt_boolTrue_t/len(dico_players), 2), 
                round(time.time()-dure_init,5)))
            
        
if __name__ == "__main__":
    ti = time.time()
    dbg = False#True
    print("geneMTobjets")
    test_class_player_geneMTobjets(dbg=dbg)
    print("geneMobjets")
    test_class_player_geneMobjets(dbg=dbg)
    print(" running time ={}".format(time.time()-ti))           
            