"""
Oligopoly model
"""

import numpy as np
from itertools import product
from scipy.optimize import fsolve


class model(object):
    """
    model

    Attributes
    ----------
    n : int
        number of players
    alpha : float
        product differentiation parameter
    beta : float
        exploration parameter
    delta : float
        discount factor
    mu : float
        product differentiation parameter
    a : int
        value of the products
    a0 : float
        value of the outside option
    c : float
        marginal cost
    k : int
        dimension of the grid
    stable: int
        periods of game stability
    """

    def __init__(self, **kwargs):
        """Initialize game with default values"""
        # Default properties
        self.n = kwargs.get('n', 3) #in this oligopoly model, n=3 which makes it a triopoly model
        self.alpha = kwargs.get('alpha', 0.15)
        self.beta = kwargs.get('beta', 4e-6)
        self.delta = kwargs.get('delta', 0.95)
        self.c = kwargs.get('c', 1)
        self.a = kwargs.get('a', 2)
        self.a0 = kwargs.get('a0', 0)
        self.mu = kwargs.get('mu', 0.25)
        self.k = kwargs.get('k', 15)
        self.tstable = kwargs.get('tstable', 1e5)
        self.tmax = kwargs.get('tstable', 1e7)

        # Derived properties
        self.sdim, self.s0 = self.init_state()
        self.p_minmax = self.compute_p_competitive_monopoly()
        self.A = self.init_actions()
        self.PI = self.init_PI()
        self.Q = self.init_Q()

    def demand(self, p):
        """Computes demand"""
        e = np.exp((self.a - p) / self.mu)
        d = e / (np.sum(e) + np.exp(self.a0 / self.mu))
        return d

    def foc(self, p):
        """Compute first order condition"""
        d = self.demand(p)
        zero = 1 - (p - self.c) * (1 - d) / self.mu
        return np.squeeze(zero)

    def foc_monopoly(self, p):
        """Compute first order condition of a monopolist"""
        d = self.demand(p)
        d1 = np.flip(d)
        p1 = np.flip(p)
        zero = 1 - (p - self.c) * (1 - d) / self.mu + (p1 - self.c) * d1 / self.mu
        return np.squeeze(zero)

    def compute_p_competitive_monopoly(self):
        """Computes competitive and monopoly prices"""
        p0 = np.ones((1, self.n)) * 3 * self.c
        p_competitive = fsolve(self.foc, p0)
        p_monopoly = fsolve(self.foc_monopoly, p0)
        return p_competitive, p_monopoly

    def init_actions(self):
        """Get action space of the firms"""
        a = np.linspace(min(self.p_minmax[0]), max(self.p_minmax[1]), self.k - 2)
        delta = a[1] - a[0]
        A = np.linspace(min(a) - delta, max(a) + delta, self.k)
        return A

    def init_state(self):
        """Get state dimension and initial state""" #in comparison to the original code, we have now 3 firms and the state dimension is grown
        sdim = tuple([self.k for _ in range(self.n)])
        s0 = np.zeros(len(sdim)).astype(int)
        return sdim, s0

    def compute_profits(self, p):
        """Compute payoffs"""
        d = self.demand(p)
        pi = (p - self.c) * d
        return pi

    def init_PI(game):
        """Initialize Profits""" #this is adjusted for oligopoly model now with 3 firms
        PI = np.zeros(game.sdim + (game.n,))
        for s in product(*[range(i) for i in game.sdim]):
            p = np.asarray(game.A[np.asarray(s)])
            PI[s] = game.compute_profits(p)
        return PI

    def init_Q(game):
        """Initialize Q function (n x #s x k)"""
        Q = np.zeros((game.n,) + game.sdim + (game.k,))
        for n in range(game.n):
            # Average over other firms' strategies
            pi = game.PI
            for i in range(game.n):
                if i != n:
                    pi = np.mean(pi, axis=-1)
            print("Shape of pi after averaging:", pi.shape)  # Let's print the shape for debugging purposes

            
        pi = pi.reshape((game.k, game.k))  # Make sure pi is of shape (15, 15)

        # Replicate the pi values for each of the dimensions
        pi_replicated = np.repeat(pi[:, :, np.newaxis], game.k, axis=2)
        pi_replicated = np.repeat(pi_replicated[:, :, :, np.newaxis], game.k, axis=3)

        # Assign to Q[n]
        Q[n] = pi_replicated / (1 - game.delta)
            
        return Q
