namespace integration::methods{
     template <typename Function, typename Real, typename Integer>
     class Approximation{
          public:
          Approximation(Function f, Real a, Real b, Integer n)
               : _f(f), _a(a), _b(b), _n(n)
          {
          }

          template<typename ApproximationImplementation>
          constexpr inline Real approximate_with(ApproximationImplementation approximation){
               return approximation.approximate(_f, _a, _b, _n);
          }

          template<typename ApproximationImplementation>
          constexpr inline Real approximate_with(){
               return ApproximationImplementation{}.approximate(_f, _a, _b, _n);
          }
          void set_n(Integer n){
               _n = n;
          }
          void set_range(Real a, Real b){
               _a = a;
               _b = b;
          }
          void set_function(Function f){
               _f = f;
          }
          protected:
               Function _f;
               Real _a, _b;
               Integer _n;
     };
}