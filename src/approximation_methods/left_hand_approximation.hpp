#pragma once
#include <cassert>
#include <type_traits>

// example code: 
// note that the signatures will be changed at later stages, this is just an implementation example

namespace integration::methods{
    struct LeftHandRuleApproximation
    {
        template<typename Function, typename Real, typename Integer>
        Real approximate(Function f, Real a, Real b, Integer n){
           static_assert(std::is_invocable_v<Function, Real> and std::is_integral_v<Integer>);
           assert(n > 0); // n must be positive 
           Real delta_x = (b - a) / n;
           Real sum = 0;
           for (Real i = 0; i < n; i++){
               sum += f(a + i * delta_x);
           }
           return delta_x * sum;
        }
    };
}
