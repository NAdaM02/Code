; Activate Firefox and switch to the first pinned tab
IfWinExist, ahk_exe firefox.exe
{
    WinActivate
    ; Send Ctrl+2 to switch to the first pinned tab
    Send, ^2
}
else
{
    Run, firefox.exe  ; Open Firefox if it's not running
}
