$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-PSReadLineOption -PredictionSource None

function global:prompt {
	$path = (Get-Location).Path -replace [regex]::Escape($env:USERPROFILE), "~"
	return "$path> "
}

Remove-Item Alias:ls -ErrorAction SilentlyContinue
function global:ls {
    param(
        [string]$Path = "."
    )

    $items = Get-ChildItem -Path $Path

    if (-not $items) {
        return
    }

    # Get terminal width to decide columns count roughly
    $width = (Get-Host).UI.RawUI.WindowSize.Width
    $maxLength = ($items | ForEach-Object { $_.Name.Length } | Measure-Object -Maximum).Maximum
    $maxLength = [Math]::Min($maxLength + 2, 30) # Max column width with padding
    $cols = [Math]::Floor($width / $maxLength)
    if ($cols -lt 1) { $cols = 1 }

    # Prepare colored output for each item
    $coloredItems = foreach ($item in $items) {
        $name = $item.Name

        if ($item.PSIsContainer) {
            # Folder: Blue
            [PSCustomObject]@{
                Text = $name.PadRight($maxLength)
                Color = 'Blue'
            }
        }
        elseif ($name -match '\.exe$|\.bat$|\.cmd$|\.ps1$') {
            # Executable scripts: Green
            [PSCustomObject]@{
                Text = $name.PadRight($maxLength)
                Color = 'Green'
            }
        }
        elseif ($item.Attributes -band [System.IO.FileAttributes]::Hidden) {
            # Hidden files: DarkGray
            [PSCustomObject]@{
                Text = $name.PadRight($maxLength)
                Color = 'DarkGray'
            }
        }
        else {
            # Regular files: Default color
            [PSCustomObject]@{
                Text = $name.PadRight($maxLength)
                Color = $Host.UI.RawUI.ForegroundColor
            }
        }
    }

    # Print items in columns
    for ($i = 0; $i -lt $coloredItems.Count; $i += $cols) {
        $lineItems = $coloredItems[$i..([Math]::Min($i + $cols - 1, $coloredItems.Count - 1))]
        foreach ($item in $lineItems) {
            Write-Host -NoNewline -ForegroundColor $item.Color $item.Text
        }
        Write-Host ""
		Write-Host ""
    }
}



here.bat
