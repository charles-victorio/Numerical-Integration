#pragma once
#include <cassert>
#include <type_traits>


namespace integration::methods{
    struct MidPointRuleApproximation
    {
        template<typename Function, typename Real, typename Integer>
        Real approximate(Function f, Real a, Real b, Integer n){
           static_assert(std::is_invocable_v<Function, Rational> and std::is_integral_v<Integer>);
           assert(n > 0); // n must be positive

           Rational delta_x = (b - a) / n;
           Rational sum = 0;
           for (Rational i = 1; i <= n; i++){
               sum += f(a + (i - static_cast<Rational>(0.5)) * delta_x);
           }
           return delta_x * sum;
        }
    };
}

