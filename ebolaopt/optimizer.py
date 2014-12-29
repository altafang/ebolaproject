# Python2.7
import scipy.optimize
import numpy
from ebolaopt.parse_input import parse_data
from ebolaopt.cost_function import CostFunction
import StochCalc.StochLib as StochLib
from ebolaopt.constraints import Constraints

##############
#XXX Placeholder function for now for Yile's code, which should be imported
def fit_params(data):
    OrigParams = StochLib.pyModelParams()
    OrigParams.setBeta_I(0.084)
    OrigParams.setBeta_H(0.11342857)
    OrigParams.setBeta_F(1.0932857)
    OrigParams.setAlpha(0.142857)
    OrigParams.setGamma_h(0.2)
    OrigParams.setGamma_f(0.5)
    OrigParams.setGamma_i(0.1)
    OrigParams.setGamma_d(0.104167)
    OrigParams.setTheta_1(0.67)
    OrigParams.setDelta_1(0.8)
    OrigParams.setDelta_2(0.8)
    return OrigParams
##############

# Default values
default_data = numpy.loadtxt("ebolaopt/data/default_data.txt")

class Optimizer:
    """This is the main overall wrapper class."""

    def __init__(self, data_file=None, constraints_file=None, country="Liberia"):
        """Initialize optimizer object and parse input files."""
        # Use default values if none are provided
        if data_file is None:
            self.data = default_data
        else:
            self.data = parse_data(data_file, country)
        
        # Create constraints object
        self.Constraints = Constraints(constraints_file)

    def initialize_model(self):
        """Fit the deterministic model parameters."""
        self.OrigParams = fit_params(self.data) #XXX first time self.OrigParams is defined
        self.Constraints.check_total(self.OrigParams)
    
    def initialize_stoch_solver(self, N_samples=200, trajectories=10, \
                               t_final=250., I_init=3, S_init=199997):
        """Initialize stochastic calculation parameters"""
        self.StochParams = StochLib.pyStochParams()
        self.StochParams.setN_samples(N_samples)
        self.StochParams.setTrajectories(trajectories)
        self.StochParams.setI_init(I_init)
        self.StochParams.setS_init(S_init)
        self.StochParams.setH_init(0)
        self.StochParams.setF_init(0)
        self.StochParams.setR_init(0)
        self.StochParams.setE_init(0)
        self.StochParams.setT_final(t_final)

    def run_optimization(self):
        """Call the Scipy optimization function."""
        #XXX Need to check that setup was done properly
        costfunc_object = CostFunction(self.StochParams, self.OrigParams, \
                                       self.Constraints)
        n = len(self.Constraints.interventions.keys())
        x0 = numpy.ones(n)*1./float(n) # Start by distributing resources uniformly
        def ineq_maker(index):
            return lambda x: x[index]
        cons = [ineq_maker(i) for i in range(n)]
        # Sum of resource allocation fractions must be less than 1
        def sum1func(x):
            return 1. - numpy.sum(x)
        cons.append(sum1func)
        self.xmin = scipy.optimize.fmin_cobyla(costfunc_object, x0, cons, disp=0)
        return self.xmin
    
    def represent_allocation(self, resource_alloc):
        """Pretty print the final result."""
        print "Resource allocation:"
        for i, param in enumerate(self.Constraints.interventions):
            print param, "should get", resource_alloc[i]*100., "percent of the allocation"

    def plot_optimum(self):
        """Do plotting."""
        # Sandra's part goes here
        return



