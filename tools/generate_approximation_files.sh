path="./src/approximation_methods"

find "$path" -type d | while read directory; do
    
    if [[ "$directory" =~ approximation$ ]]; then
        dir_name=$(basename "$directory")
        

        hpp_file="$directory/$dir_name.hpp"
        
         
        rm -r "$directory"
       
     #    if [ ! -f "$hpp_file" ]; then
     #        touch "$hpp_file"
     #        echo "Created $hpp_file"
     #    fi
    fi
done
