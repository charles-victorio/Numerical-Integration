#pragma once
#include <cassert>
#include <type_traits>

// example code: 
// note that the signatures will be changed at later stages, this is just an implementation example

namespace integration::methods{
     template<typename Function, typename Rational, typename Integer>
     Rational left_hand_approximation(Function f, Rational a, Rational b, Integer n){
        static_assert(std::is_invocable_v<Function, Rational> and std::is_integral_v<Integer>);
        assert(n > 0); // n must be positive

        Rational delta_x = (b - a) / n;
        Rational sum = 0;
        for (Rational i = 0; i < n; i++){
            sum += f(a + i * delta_x);
        }
        return delta_x * sum;
     }
}

