#pragma once
#include <cassert>
#include <type_traits>

namespace integration::methods{
     struct SimpsonsApproximation{
          template<typename Function, typename Real, typename Integer>
          Real approximate(Function f, Real a, Real b, Integer n){
             static_assert(std::is_invocable_v<Function, Real> and std::is_integral_v<Integer>);
             assert(n > 0 and n % 2 not_eq 1); // n must be positive

             Real delta_x = (b - a) / n;
             Real first_sum = 0;
             Real second_sum = 0;

             static auto x = [a, delta_x](Integer i){
               return a + i * delta_x;
             };

             for (Integer i = 1; i < n; i += 2) first_sum += f(x(i));
             for (Integer i = 2; i < n; i += 2) second_sum += f(x(i));

             return delta_x / 3 * ((a) + (4 * first_sum) + (2 * second_sum) + f(b));
          }
     };
     
}

