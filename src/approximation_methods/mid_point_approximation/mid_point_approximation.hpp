#pragma once
#include <cassert>
#include <type_traits>


namespace integration::methods{
    struct MidPointRuleApproximation
    {
        template<typename Function, typename Real, typename Integer>
        Real approximate(Function f, Real a, Real b, Integer n){
           static_assert(std::is_invocable_v<Function, Real> and std::is_integral_v<Integer>);
           assert(n > 0); // n must be positive

           Real delta_x = (b - a) / n;
           Real sum = 0;
           for (Real i = 1; i <= n; i++){
               sum += f(a + (i - static_cast<Real>(0.5)) * delta_x);
           }
           return delta_x * sum;
        }
    };
}

