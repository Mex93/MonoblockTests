@echo off
echo Sync Time started...
net start w32time
w32tm /resync
echo Sync Time stop.
pause