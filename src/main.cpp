#include <iostream>
#include "methods/right_hand_approximation/right_hand_approximation.hpp"

#include <cmath>

double f (double x){
     return pow(x, x);
}
int main(){
     
    
     double a = 1.5, b = 3.7;
     uint16_t n = 10000;

     std::cout << "The integral of x^x from " << a << " to " << b << " is " << integration::methods::right_hand_rule(f, a, b, n) << std::endl;

     return 0;
     
}