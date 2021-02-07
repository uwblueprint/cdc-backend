@ECHO OFF
TITLE PSQL Server Management
ECHO STARTING UP SERVER
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