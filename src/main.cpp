#include <iostream>
#include <cmath>
#include "approximation_methods/approximations.hpp"
 

int main(){    

     auto f = [](double x){
          return pow(x, x);
     };

     using namespace integration::methods;
     Approximation approximation(f, 1.2, 5.3, 100000); // notice that both a and b should be of the same type
 
     std::cout << approximation.approximate_with(RightHandRuleApproximation{}) << std::endl;
     std::cout << approximation.approximate_with<MidPointRuleApproximation>() << std::endl;
     std::cout << approximation.approximate_with(SimpsonsApproximation{}) << std::endl;
 
     return 0;
     
}