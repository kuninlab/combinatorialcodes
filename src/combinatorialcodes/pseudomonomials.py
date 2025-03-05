import numpy as np

class PseudoMonomial:
    """Represents a polynomial of the form x^sigma (1-x)^tau, where sigma and tau are subsets of {0,...,n-1}.
    Because this is python, we use 0-based indexing.
    
    If sigma and tau are both empty, then this represents 0."""
    # sigma: set
    # tau: set
    # n: int
    # sigma: np.ndarray
    # tau: np.ndarray
    
    def __init__(self, s, t) -> None:
        # for name, var in zip(["sigma","tau"], [s, t]):
        #     if any((x < 0) or not isinstance(x, int) for x in var):
        #         raise ValueError(f"{name} must be a subset of [0,...,n-1] (got {s} of type {type(s) = })")
        # self.sigma = set(s)
        # self.tau = set(t)
        # if n is None:
        #     n = 0
        #     if len(self.sigma) > 0:
        #         n = max(n, max(self.sigma))
        #     if len(self.tau) > 0:
        #         n = max(n, max(self.tau))
        #     # n = max(max(self.sigma), max(self.tau))
        # self.n = n
        self.sigma = np.sort(s)
        self.tau = np.sort(t)


    def __str__(self) -> str:
        # ans = ""
        sigma_part = " ".join(f"x_{s+1}" for s in self.sigma)
        tau_part = " ".join(f"(1 - x_{t+1})" for t in self.tau)
        ans = " ".join([sigma_part, tau_part])
        # if len(self.sigma) > 0:
        #     ans += f"x^{self.sigma} "
        # for s in self.sigma:
        #     ans += f"x_{s} "
        # # if len(self.tau) > 0:
        # #     ans += f"(1-x)^{self.tau}"
        # for t in self.tau:
        #     ans += f"(1 - x_{t}) "
        if len(ans) == 0:
            ans = "0"
        return ans
    
    def __repr__(self) -> str:
        return f"PseudoMonomial({self.sigma.__repr__()}, {self.tau.__repr__()})"
        # , {self.n}
    
    def __mul__(self, other):
        if isinstance(other, int):
            if other % 2 == 0:
                return PseudoMonomial([], [], self.n)
            else:
                return PseudoMonomial(self.sigma, self.tau)  # self.n
        if isinstance(other, PseudoMonomial):
            # return PseudoMonomial(self.sigma.union(other.sigma), self.tau.union(other.tau))  # max(self.n, other.n)
            return PseudoMonomial(np.union1d(self.sigma, other.sigma), np.union1d(self.tau, other.tau))
        raise TypeError(f"Cannot multiply pseudomonomial by {other=} of type {type(other)=}")
    

    def __rmul__(self, other):
        return self * other
    
    
    def divides(self, other):
        if not isinstance(other, PseudoMonomial):
            raise TypeError(f"Can only check if pseudomonomials divide other pseudomonomials (got {type(other)=})")
        return set(self.sigma).issubset(set(other.sigma)) and set(self.tau).issubset(set(other.tau))
        # return self.sigma.issubset(other.sigma) and self.tau.issubset(other.tau)
    

    def __call__(self, words):
        words = np.array(words)
        if len(words.shape) == 1:
            # single codeword 
            return int(np.all(words[self.sigma]) and not np.any(words[self.tau]))
        elif len(words.shape) == 2:
            # multiple codewords
            return (np.all(words[:, self.sigma], axis=1) & ~np.any(words[:, self.tau], axis=1)).T.astype(int)
        else:
            raise ValueError(f"Can't call pseudomonomial on array of shape {words.shape}")
        
    
    def to_array(self, n=None):
        """Return the signed array representation of this pseudomonomial.
        Returns an array of shape (n,). If n is None, use the maximum element in sigma, tau"""
        if n is None:
            n = 0
            if len(self.sigma) > 0:
                n = np.max(self.sigma, )
            if len(self.tau) > 0:
                n = max(n, max(self.tau))
        ans = np.zeros(n, dtype=int)
        ans[self.sigma] = 1
        ans[self.tau] = -1
        return ans
    
    
    def from_array(arr):
        """Converts a vector of +/-1s into a pseudomonomial;
        sigma is the set of indices with a +1, tau is the set of indices with a -1."""
        return PseudoMonomial(np.nonzero(arr > 0)[0], np.nonzero(arr < 0)[0])

    def __hash__(self):
        return hash(tuple(tuple(self.sigma), tuple(self.tau)))
