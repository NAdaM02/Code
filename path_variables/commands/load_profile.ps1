$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-PSReadLineOption -PredictionSource None

function global:prompt {
	$path = (Get-Location).Path -replace [regex]::Escape($env:USERPROFILE), "~"
	return "$path> "
}

here.bat
