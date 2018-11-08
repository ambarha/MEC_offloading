'''
Game theory functions
'''

import numpy as np

from parameters import *

def play_offloading_game(server_selected, b_old, prices):
    '''
    Users play the offloading game to find their best response based on what
    the other users played.

    Parameters
    ----------

    server_selected: 1-D array
        list containing the server to which each user is associated
    b_old: 1-D array
        offloading data each user had decided to send on the previous
        iteration

    Returns
    -------

    b: 1-D array
        offloading data each user has decided to send on the current
        iteration

    '''

    # Sum of all best responses
    B = np.sum(b_old)

    # Best response of all users except the user
    B_minus_u = B - b_old

    # price paid by user based on server's price
    paid = prices[tuple([server_selected])]

    # calculation of best response for every user based on Theorem 1
    b = (B_minus_u/l) * ((k*l/(a*paid)) - 1)

    # limit result inside [0, Iu] -> [b_min, b_max]
    b[b>b_max] = b_max
    b[b<b_min] = b_min

    return b

def play_pricing_game(server_selected, b):
    '''
    Servers play the pricing game to find their best response based on what
    the users played. Basically just maximize their gain

    Parameters
    ----------

    server_selected: 1-D array
        list containing the server to which each user is associated
    b: 1-D array
        offloading data each user had decided to send

    Returns
    -------

    prices: 1-D array
        Set the new prices of the servers

    '''

    # Sum of all best responses
    B = np.sum(b)
    # Best response of all users except the user
    B_minus_u = B - b

    # np.bincount sums all values on the specific index, so all values corresponding
    # to each server. We specify minlength so that even if the last server
    # is not chosen, we have 0 as a value
    inside_sum = B_minus_u/a

    # The sum is different for each server since we take into account only the
    # users that are associated with the server
    numerator_sum = np.bincount(server_selected, inside_sum, minlength=S)

    numerator = c*k*l*numerator_sum

    # The sum is different for each server since we take into account only the
    # users that are associated with the server
    denominator_sum = np.bincount(server_selected, B_minus_u, minlength=S)

    denominator = (1 - fs)*denominator_sum

    # If the server has not been chosen, then give a value to the denominator
    # so that the price is set to 0/0.1 = 0
    denominator[denominator==0] = 0.1

    prices = np.sqrt(numerator/denominator)

    if prices.any() < 0:
        raise ValueError('Prices should be > 0')

    prices[prices == 0] = price_min

    return prices

def game_converged(b, b_old, p, p_old):
    '''
    Check if the game has converged

    Parameters
    ----------

    b: 1-D array
        The offloading values the users chose on the last game
    b_old: 1-D array
        The offloading values the users chose on the previous game
    p: 1-D array
        The prices the servers chose on the last game
    p_old: 1-D array
        The prices the servers chose on the previous game

    Returns
    -------

    convergence: Boolean
        Boolean on whether all users are sure of the selected server or not
    '''

    # e1 and e2 are the error tolerance defined in parameters
    if np.abs(b - b_old).all() < e1 and np.abs(p - p_old).all() < e2:
        return True
    return False
