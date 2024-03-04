#pragma once
#include <cassert>
#include <type_traits>

namespace integration::methods{
     template<typename Function, typename Rational, typename Integer>
     Rational trapezoidal_approximation(Function f, Rational a, Rational b, Integer n){
        static_assert(std::is_invocable_v<Function, Rational> and std::is_integral_v<Integer>);
        assert(n > 0); // n must be positive
     
        Rational delta_x = (b - a) / n;
        Rational sum = 0;

        static auto x = [](Integer i){
          return a + i * delta_x;
        }
        
        for (Integer i = 1; i < n; i +=1) sum += f(x(i));
       
        return delta_x * (0.5 * (f(a) + f(b)) + sum); 
     }
}

