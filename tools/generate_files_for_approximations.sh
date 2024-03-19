path="./src/approximation_methods"

methods=$(find "$path" -type f)



for method in $methods; do
    filename=$(basename "$method")
    filename="${filename%.*}" # remove extension


    if [[ "$filename" == *"approximation"* ]]; then
        mkdir -p "tests"
        mkdir -p "benchmarks"
        mkdir -p "doc/approximation_methods"

        root_directory=$(pwd)

        cd "tests"
        touch ""$filename"_test.cpp"
        cd $root_directory

        cd "benchmarks"
        touch ""$filename"_benchmark.cpp"
        cd $root_directory
         
        cd "doc/approximation_methods"
        touch "$filename.tex"
        cd $root_directory
    fi
    
   
   
    
done

