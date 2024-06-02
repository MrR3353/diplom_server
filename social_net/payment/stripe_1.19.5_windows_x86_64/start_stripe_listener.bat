@echo off
echo Starting Stripe listener...

REM Change directory to where stripe.exe is located, if necessary
REM cd path\to\stripe

REM Start stripe.exe and run the listen command
stripe.exe listen --forward-to localhost:8000/payment/webhook/

REM Pause to keep the command prompt open in case of errors
pause
