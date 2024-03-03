"""Attempt 3

strategy.integrate() doesnt return anything, but Integral.integrate_with() returns the report

integral.integrate_with(strategy) is the user's entrypoint
For rigorous testing of n integrals with m strategies, entrypoint is Integrator():
- Make n Integrator() objects
- Switch strategies at runtime 

When do I decorate f(x)? Maybe different for python than c++

Strategies left:
- Newton cotes that are higher order than Simpson's 1/3rd
- Gaussian quadrature with arbitrary n
- Clenshaw–Curtis quadrature with DCT

Make adaptive
Make graph showing error vs parameters / time / iterations / fn evals
"""
from __future__ import annotations

from math import exp, sin, cos, sqrt, pi
import random
import time

class Integral:
    def __init__(self, f: callable, a: float, b: float):
        self.plain_f = f
        self.a = a
        self.b = b
        # integrate_with() will make an Integrator() which will fill self.f
        # with a function which calls f(x) and increments the number of func evals counter in its report class
        self.f = None
    def integrate_with(self, strategy: Strategy) -> Report:
        integrator = Integrator(self, strategy) # doesnt need to outlive this function
        # Integrator() can make string_of_f
        report = integrator.integrate() # does need to outlive this function lol
        return report

class Report: # Report of the integration
    def __init__(self):
        # self.string_of_integral = stringify(integral) # may not be possible
        # self.string_of_f = ""
        self.number_of_func_evals = 0
        self.start_time = 0
        self.end_time = 0
        self.output = 0
        self.method = ""
    def __str__(self):
        # Must only be called after integration is performed, otherwise the report will be meaningless
        return (
            f"Output: {self.output}, Number of func evals: {self.number_of_func_evals}\n"
            f"Calculated with {self.method} in {self.end_time - self.start_time}s."
        )

# Abstract base class
# Each concrete class may have their own parameters, like h1_guess or nsamples
class Strategy:
    # Shouldn't return report, should feed existing report
    def integrate(self, integral: Integral, report: Report):
        pass

class Integrator:
    def __init__(self, integral: Integral, strategy: Strategy = None):
        self.integral = integral
        self.report = Report()
        self.integral.f = self.make_call_and_record_func(self.integral.plain_f)
        self.strategy = strategy # Can be None bc set at runtime
        self.intermediate_values = [] # optional
    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy
    def make_call_and_record_func(self, plain_f: callable):
        def call_and_record(x: float): # in c++ check assembly to ensure this is inlined
            self.report.number_of_func_evals += 1
            return plain_f(x)
        return call_and_record
    def integrate(self) -> Report:
        # Strategy must be set by the time the integration is performed
        if not self.strategy:
            print("Tried to integrate before setting strategy")
            return
        self.report.method = self.strategy.__class__.__name__
        self.report.start_time = time.time()
        self.strategy.integrate(self.integral, self.report)
        self.report.end_time = time.time()
        return self.report

class Trapezoid(Strategy):
    def __init__(self, n_steps: int = 10000):
        self.n_steps = n_steps
    def integrate(self, integral: Integral, report: Report):
        h = (integral.b - integral.a) / self.n_steps
        x = integral.a + h # skipping over f(x = a) because it will be accounted for in the next line
        # Note that `area_under_curve` hasn't been multiplied by h, so it doesnt truly represent the area under the curve yet
        area_under_curve = 0.5 * (integral.f(integral.a) + integral.f(integral.b))
        for i in range(self.n_steps):
            area_under_curve += integral.f(x)
            x += h
        answer = area_under_curve * h
        report.output = answer

class SimpsonsOneThird(Strategy):
    def __init__(self, n_steps: int = 10000):
        if n_steps % 2 != 0:
            raise ValueError("For Simpson's One Third Rule, the number of steps must be even.")
        self.n_steps = n_steps
    def integrate_old(self, integral: Integral, report: Report):
        # Clearer implementation but slower
        h = (integral.b - integral.a) / self.n_steps
        area_under_curve = 0
        for i in range(self.nsteps / 2):
            area_under_curve += \
                      integral.f(integral.a + (2 * i)     * h) \
                + 4 * integral.f(integral.a + (2 * i + 1) * h) \
                +     integral.f(integral.a + (2 * i + 2) * h)
        area_under_curve *= (1 / 3) * h
        report.output = area_under_curve


class OdeStrategy(Strategy):
    def __init__(self, n_steps: int = 10000):
        self.n_steps = n_steps
    def integrate(self, integral: Integral, report: Report): # template pattern
        # have to make these member vars here so template fn can access them
        # in c++ may rearrange stuff and use completely different architecture
        # so it doesnt matter that its sloppy here
        self.integral = integral
        self.report = report
        self.x = integral.a
        self.y = 0
        h = (integral.b - integral.a) / self.n_steps
        for i in range(self.n_steps):
            # self.things_to_do_each_step(x, y, h, integral.f, report)
            self.things_to_do_each_step()
        report.output = self.y
        # print(self.__class__.__name__, self.y)
    # def things_to_do_each_step(self, x, y, h, f, report):
    def things_to_do_each_step(self):
        pass

class Euler(OdeStrategy):
    # def things_to_do_each_step(self, x, y, h, f, report): # what if I just inlined this lol
    #     y += f(x) * h
    #     report.intermediate_values.append((x, y))
    #     x += h
    def things_to_do_each_step(self):
        self.y += self.integral.f(self.x) * self.h
        self.report.intermediate_values.append((self.x, self.y))
        self.x += self.h

class Midpoint(OdeStrategy):
    # The Midpoint method for ODEs, when using ODE solvers to solve integrals,
    # turns into the Midpoint method for integration
    # since f(x) just depends on x, not y
    def things_to_do_each_step(self):
        self.y += self.h * self.integral.f(self.x + 0.5 * self.h)
        self.report.intermediate_values.append((self.x, self.y))
        self.x += self.h

class RungeKutta4(OdeStrategy):
    def things_to_do_each_step(self):
        # possible to reuse x and f(x) values in the future
        # k1, k2, k3, maybe even x, y, h, f should probably be in registers
        # if k1,2,3 must be on stack, hopefully declared outside the loop idk if that matters tho
        # Note that k1, k2, and k3 haven't been multiplied by h yet, so they aren't truly the k1, k2, and k3 values yet
        k1 = self.integral.f(self.x)
        k2 = self.integral.f(self.x + 0.5 * self.h)
        # k2 = k3 since the ODE of f(x) only depends on x, not y
        k4 = self.integral.f(self.x + self.h)
        self.y += self.h * (k1 / 6 + (2/3) * k2 + k4 / 6)
        self.report.intermediate_values.append((self.x, self.y))


class MonteCarlo(Strategy):
    def __init__(self, n_samples: int = 1000000 ):
        self.n_samples = n_samples
    def integrate(self, integral: Integral, report: Report):
        # get avg val
        sum_ = 0
        for i in range(self.n_samples):
            sum_ += integral.f(random.uniform(integral.a, integral.b))
        avg_val = sum_ / self.n_samples
        answer = (integral.b - integral.a) * avg_val
        report.output = answer
        # print(self.__class__.__name__, answer)

class Romberg(Strategy): # non-iterative refinement version
    def __init__(self, M: int, atol: float = None, rtol: float = None):
        self.M = M # Number of applications of richardson's extrapolation
        self.atol = atol if atol else float("-inf")
        self.rtol = rtol if rtol else float("-inf")
    @staticmethod
    def pprint2darr(arr):
        for row in arr:
            for x in row:
                print(f"{x:+5.2f}", end=" ")
            print("\n")
    @staticmethod
    def calc_rel_error(x, y): # d_inf: https://en.wikipedia.org/wiki/Relative_change_and_difference
        return abs(x - y) / max(abs(x), abs(y), 1) # added one to avoid 1 / 0 ???
        # in case of divide by zero, just becomes absolute error
    def integrate(self, integral: Integral, report: Report):
        h = integral.b - integral.a
        # Make empty (M + 1) x (M + 1) array.
        # Will fill the lower triangle with the successive estimates for the integral.
        # Row 0 column 0 is the non-composite single-partition trapezoid rule, before any iterations of richardsons extrapolation
        # Column 0 stores the trapezoid rule estimates, row j has 2^j partitions
        # Each row j > 0 stores the estimates from the jth application of richardson's extrapolation,
        # combining the trapezoid rule with 2^j partitions and the previous row's results.
        # It uses this formula:
        # arr[row][col] = (4^(col - 1) * I_(row, col - 1) - I_(row - 1, col - 1)) / (4^(col - 1) - 1)
        # Note when reading Numerical Methods for Engineers: row j, column k, they use |7 triangle instead of lower triangle 
        # The main diagonal stores the final estimates for the row it's in
        arr = [[float("inf") for _ in range(self.M + 1)] for _ in range(self.M + 1)]
        arr[0][0] = 0.5 * h * (integral.f(integral.a) + integral.f(integral.b))

        prev_answer = arr[0][0]
        # Each iteration of the outer loop is
        # - a row in the table
        # - an iteration of trapezoid rule (using previous values)
        # The step size for a row j is h = (b - a) / 2^j
        for row in range(1, self.M + 1):
            h /= 2 
            print(f"{row=} h = ({integral.b} - {integral.b}) / 2^{row} = {h}")
            Romberg.pprint2darr(arr)
            # Make more accurate trapezoid rule with 2^row partitions (2^row + 1 function evaluations)
            # But can reuse the 2^row / 2 + 1 = 2^(row - 1) + 1 function evaluations of the previous row's trapezoid rule
            # The 2^(row - 1) new function evaluations are here:
            sum_of_new_function_evaluations = sum([integral.f(integral.a + (2 * i + 1) * h) for i in range(2 ** (row - 1))])
            # Combine with the function evaluations of the previous row's trapezoid rule
            # Remember that the previous row's h's were twice as big as the current row,
            # get all of the h's to the right size by halving the previous trapezoid rule.
            arr[row][0] = 0.5 * arr[row - 1][0] + h * sum_of_new_function_evaluations

            # Fill in rest of row with richardson's extrapolation
            for col in range(1, row + 1):
                # arr[row][col - 1] is more accurate, arr[row - 1][col - 1] is less accurate, so weighted less
                arr[row][col] = arr[row][col - 1] + (arr[row][col - 1] - arr[row - 1][col - 1]) / (4 ** col - 1)
            
            # Current answer is arr[row][row]
            current_answer = arr[row][row]
            if (self.atol and abs(current_answer - prev_answer) < self.atol) \
                or (self.rtol and Romberg.calc_rel_error(current_answer, prev_answer) < self.rtol):
                print("Converged before M iterations")
                break
            prev_answer = current_answer
        
        # Final answer is in the main diagonal
        # If did all M trials before terminating, it will be in the bottom right of the M + 1 x M + 1 grid
        answer = arr[row][row]
        Romberg.pprint2darr(arr)
        report.output = answer

def rescale(f, a, b): # For Gaussian and Clenshaw-Curtis
    def rescaled_func(x): # rescale func to [-1, 1]
        B_t = (b - a) * 0.5 * x + (a + b) * 0.5
        return (b - a) * 0.5 * f(B_t)
    return rescaled_func

class Gaussian(Strategy):
    def __init__(self, n: int):
        if n != 64: # N should be flexible later maybe
            raise NotImplementedError("Must use n = 64 for now, can't compute x_i's and w_i's for arbitrary n yet.")
        self.n = n
        # x_i's and w_i's from: https://pomax.github.io/bezierinfo/legendre-gauss.html
        # order doesnt matter as long as w_i corresponds to correct x_i
        self.x = [
            -0.0243502926634244,
            0.0243502926634244,
            -0.0729931217877990,
            0.0729931217877990,
            -0.1214628192961206,
            0.1214628192961206,
            -0.1696444204239928,
            0.1696444204239928,
            -0.2174236437400071,
            0.2174236437400071,
            -0.2646871622087674,
            0.2646871622087674,
            -0.3113228719902110,
            0.3113228719902110,
            -0.3572201583376681,
            0.3572201583376681,
            -0.4022701579639916,
            0.4022701579639916,
            -0.4463660172534641,
            0.4463660172534641,
            -0.4894031457070530,
            0.4894031457070530,
            -0.5312794640198946,
            0.5312794640198946,
            -0.5718956462026340,
            0.5718956462026340,
            -0.6111553551723933,
            0.6111553551723933,
            -0.6489654712546573,
            0.6489654712546573,
            -0.6852363130542333,
            0.6852363130542333,
            -0.7198818501716109,
            0.7198818501716109,
            -0.7528199072605319,
            0.7528199072605319,
            -0.7839723589433414,
            0.7839723589433414,
            -0.8132653151227975,
            0.8132653151227975,
            -0.8406292962525803,
            0.8406292962525803,
            -0.8659993981540928,
            0.8659993981540928,
            -0.8893154459951141,
            0.8893154459951141,
            -0.9105221370785028,
            0.9105221370785028,
            -0.9295691721319396,
            0.9295691721319396,
            -0.9464113748584028,
            0.9464113748584028,
            -0.9610087996520538,
            0.9610087996520538,
            -0.9733268277899110,
            0.9733268277899110,
            -0.9833362538846260,
            0.9833362538846260,
            -0.9910133714767443,
            0.9910133714767443,
            -0.9963401167719553,
            0.9963401167719553,
            -0.9993050417357722,
            0.9993050417357722
        ]
        self.w = [
            0.0486909570091397,
            0.0486909570091397,
            0.0485754674415034,
            0.0485754674415034,
            0.0483447622348030,
            0.0483447622348030,
            0.0479993885964583,
            0.0479993885964583,
            0.0475401657148303,
            0.0475401657148303,
            0.0469681828162100,
            0.0469681828162100,
            0.0462847965813144,
            0.0462847965813144,
            0.0454916279274181,
            0.0454916279274181,
            0.0445905581637566,
            0.0445905581637566,
            0.0435837245293235,
            0.0435837245293235,
            0.0424735151236536,
            0.0424735151236536,
            0.0412625632426235,
            0.0412625632426235,
            0.0399537411327203,
            0.0399537411327203,
            0.0385501531786156,
            0.0385501531786156,
            0.0370551285402400,
            0.0370551285402400,
            0.0354722132568824,
            0.0354722132568824,
            0.0338051618371416,
            0.0338051618371416,
            0.0320579283548516,
            0.0320579283548516,
            0.0302346570724025,
            0.0302346570724025,
            0.0283396726142595,
            0.0283396726142595,
            0.0263774697150547,
            0.0263774697150547,
            0.0243527025687109,
            0.0243527025687109,
            0.0222701738083833,
            0.0222701738083833,
            0.0201348231535302,
            0.0201348231535302,
            0.0179517157756973,
            0.0179517157756973,
            0.0157260304760247,
            0.0157260304760247,
            0.0134630478967186,
            0.0134630478967186,
            0.0111681394601311,
            0.0111681394601311,
            0.0088467598263639,
            0.0088467598263639,
            0.0065044579689784,
            0.0065044579689784,
            0.0041470332605625,
            0.0041470332605625,
            0.0017832807216964,
            0.0017832807216964
        ]
    def integrate(self, integral: Integral, report: Report):
        rescaled_f = rescale(integral.f, integral.a, integral.b)
        report.output = sum([w_i * rescaled_f(x_i) for x_i, w_i in zip(self.x, self.w)])

class ClenshawCurtis(Strategy): # O(n^2) version
    # https://math.mit.edu/~stevenj/trap-iap-2011.pdf
    def __init__(self, max_k: int = 200, max_n: int = 100):
        self.max_k = max_k # doesnt need to be even and >2 for this implementation
        self.max_n = max_n

    def ak(self, f, k):
        # f domain [-1, 1]
        N = self.max_n
        sum_ = sum([
            f(cos(n * pi / N))
            * cos(k * n * pi / N)
            for n in range(1, N) # intentionally exclude N
        ])
        avg_endpts = (f(1) + f(-1)) * 0.5
        return (2 / N) * (avg_endpts + sum_)

    def integrate(self, integral: Integral, report: Report):
        f = rescale(integral.f, integral.a, integral.b);
        a_0 = self.ak(f, 0)
        sum_ = sum([
            # (2 * ClenshawCurtis.ak(f, k)) / (1 - k * k)
            # for k in range(2, MAX_K, 2)
            (2 * self.ak(f, 2 * k)) / (1 - 4 * k * k)
            for k in range(1, self.max_k)
        ])
        I = a_0 + sum_
        report.output = I

if __name__ == "__main__":
    I1 = Integral(lambda x: exp(-x) * sin(4 * x) ** 2, -2, 2)
    print(I1.integrate_with(MonteCarlo(30000)))
    print(I1.integrate_with(ClenshawCurtis(200, 100)))
    print(I1.integrate_with(Gaussian(64)))