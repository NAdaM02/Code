$gitRoot = git rev-parse --show-toplevel 2>$null

Set-Location $gitRoot
