@echo off
setlocal EnableDelayedExpansion
cd %~dp0CopyOfFiles

::generating a 'random number' that I wont use because this program is annoying 
set m=%random%

set loop=0
:loop
set /a loop=%loop%+1 
if "%loop%"=="1000" goto end

::calculating 2 random boi
set n=0
for %%f in (*.*) do (
   set /A n+=1
   set "file[!n!]=%%f"
)
::Generating an actual random number
set /A "rand1=(n*%random%)/32768+1"
set /A "rand2=(n*%random%)/32768+1"

if "%rand1%" == "%rand2%" goto next

::chose file from the first folder
move "%~dp0CopyOfFiles\!file[%rand1%]!" "%~dp0CopyOfFiles\ThInGy" > nul
move "%~dp0CopyOfFiles\!file[%rand2%]!" "%~dp0CopyOfFiles\!file[%rand1%]!" > nul
move "%~dp0CopyOfFiles\ThInGy" "%~dp0CopyOfFiles\!file[%rand2%]!" > nul
rem pause
:next

goto loop

:next

:end
exit