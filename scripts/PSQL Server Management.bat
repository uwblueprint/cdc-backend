@ECHO OFF
TITLE PSQL Server Management
ECHO STARTING UP SERVER
::========================================================================================
:: This code is for starting and stopping the postgres service on windows
::
:: If pgadmin has issues connecting, windows may have stopped the service for some reason,
:: so you can run the script to restart the postgres service.
::
:: Might have to run as administrator.
::
:: When you run the script, it starts the server by default.
:: You can enter additional commands like "start", "stop" or "restart" if any issues
:: Entering "exit" will close the script AND stop the server.
::========================================================================================
pg_ctl -D "C:\Program Files\PostgreSQL\12\data" start
:label
set /p Input=Enter command [start][stop][restart][exit]:
IF /I "%Input%" NEQ "exit" (
	pg_ctl -D "C:\Program Files\PostgreSQL\12\data" %Input%
	goto :label
)
ECHO SHUTTING DOWN SERVER
pg_ctl -D "C:\Program Files\PostgreSQL\12\data" stop
ECHO EXITING
exit
