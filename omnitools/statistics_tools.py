def linear(x, gradient, intercept):
    return gradient * x + intercept


from numpy import array, square, mean
from copy import copy


def loss_function(data, fit, error=None):
    if error is None:
        error = copy(data)
    res = (data - fit) / error
    return -0.5 * square(res).sum()


def loss_grad_function(data, fit, error=None):
    if error is None:
        error = copy(data)
    res = (data - fit) / error
    return -res.sum() * array([1, 0])


def linear_fit(data, x, gradient, intercept, error=None):
    fx = linear(x, gradient, intercept)
    return loss_function(data, fx, error=error)


def get_range(data) -> list:
    return [min(data), max(data)]


class LinearFit:

    def __init__(self, x, y, error=None, hmc:bool=False):
        self.x = x
        self.y = y
        self.error = error

        self.hmc = hmc

    def cost(self, theta):
        gradient, intercept = theta
        return linear_fit(self.y, self.x, gradient, intercept, error=self.error)

    def gradient(self, theta):
        gradient, intercept = theta
        fit = linear(self.x, gradient, intercept)
        return loss_grad_function(self.y, fit, error=self.error)

    def starting_point(self):
        estimate_gradient = (self.y[self.x.argmax()] - self.y[self.x.argmin()]) / (self.x.max() - self.x.min())
        return [estimate_gradient, mean(self.y)]

    def fit(self, runtime_mins=1 / 60):
        if self.hmc:
            from inference.mcmc import HamiltonianChain
            self._chain = HamiltonianChain(self.cost, grad=self.gradient, start=self.starting_point())
        else:
            from inference.mcmc import GibbsChain
            self._chain = GibbsChain(self.cost, start=self.starting_point())

        # run fit and sample
        self._chain.run_for(minutes=runtime_mins)
        self._chain.autoselect_burn_and_thin()
        self.mode = self._chain.mode()

        self.fx = linear(self.x, *self.mode)

    def plot_fit(self, sample: bool = False, **kwargs):
        from matplotlib.pyplot import subplots
        fig, ax = subplots()

        ax.plot(self.x, self.y, 'x', label='Data')
        ax.plot(self.x, self.fx, 'o', label='Fit')

        ax.set_ylabel('y')
        ax.set_xlabel('x')

        ax.legend()

        fig.show()

    def plot_data_series(self):
        from matplotlib.pyplot import subplots
        fig, ax0 = subplots()

        ax0.plot(self.x, color='C0')
        ax0.set_ylabel('x', color='C0')

        ax1 = ax0.twinx()
        ax1.plot(self.y, color='C1')
        ax0.set_ylabel('y', color='C1')

        fig.tight_layout()

        fig.show()