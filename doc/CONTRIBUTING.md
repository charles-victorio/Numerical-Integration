
## Code Organization

- **Source Files Location**: All source files, including `.cpp` `.hpp` `.tpp` and `.h` files, must be placed inside the `src` directory. This helps maintain a clean and organized codebase.

## Coding Standards

- **Function Naming**: All functions must use snake_case naming. For example, a function that calculates the average should be named `calculate_average()`, not `CalculateAverage` or `calculateAverage`.
  
- **Class Naming**: Class names should follow CamelCase naming conventions. For instance, use `MyBigClass` instead of `my_big_class` or `Mybigclass`.

- **Variable Naming**: Choose descriptive and meaningful names for variables, use snake_case. Avoid using abbreviated or simplified names such as `num`, `msr`, etc. The goal is for the code to be self-explanatory, improving readability and maintainability.

## Commenting and Documentation

- While we strive for self-explanatory code through clear naming conventions and structure, please document complex logic or algorithms that may not be immediately obvious to others. Use comments to explain the "why" behind non-trivial solutions or decisions.


## Creating New Branches

- **Naming**: choose any descriptive name for a feature you are designing and append `dev-` as its prefix. If the feature is part of another feature then the nameing should look like `dev-global_feature-local_feature`


## File management

**DO NOT** write files with more then 100 lines of code in them. 
**DO NOT** leave big chunks of commented code in a file that is currently being used, if you need something specific, save it on your local branch
**DO NOT** name files with spaces. e.g. `my cool file.cpp`

## Issues

- remember that you can always post and issue on github, please make notes of the code progress and report bugs in a modest way.

## Example

You want to create write a new branch for regulating reports in new directory /reports. go to terminal, type:
```bash
git checkout -b dev-reports
# do all the work necessary, then git add and git commit 
git push -u origin HEAD
# assuming you connected to the remote with `git remote add origin ...`
```
