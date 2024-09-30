; Activate Firefox and switch to the first pinned tab
IfWinExist, ahk_exe firefox.exe
{
    WinActivate
    ; Send Ctrl+1 to switch to the first pinned tab
    Send, ^1
}
else
{
    Run, firefox.exe  ; Open Firefox if it's not running
}
