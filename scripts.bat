@echo off
if "%1" == "generate" (
    echo Generating data ....
    python project.py -dg -i generate.txt -o Data/Defaults/data.json -c Data/Defaults/configuration.json
) else if "%1" == "run" (
    echo Running .....
    python project.py run defaults -o Output/data.json -e on
) else (
    echo Invalid Command please try again.
)