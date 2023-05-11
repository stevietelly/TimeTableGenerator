@echo off
if "%1" == "generate" (
    echo Generating data ....
    python project.py -dg -i generate.txt -o Data/Defaults/data.json -c Data/Defaults/configuration.json
) else if "%1" == "run" (
    echo Running .....
    python project.py run defaults -o Output/data.json -e on
) else if "%1" == "genetic" (
    echo Running Genetic ALgorithm ........
    python project.py run -i Data/Defaults/data.json -o Output/data.json -e on -a genetic
) else (
    echo Invalid Command please try again.
)