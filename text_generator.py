keys = "Angol, Biológia, Fizika, Irodalom, Matek, Német, Németh - Barbar, Nyelvtan, Történelem".split(", ")

def get_text(key):
    text = f'echo Set-Location \"C:\\Users\\adama\\Iskola\\2024-25\\Fizika\" && Write-Host \"\"> \".{key}.ps1\"'

    return text

for key in keys:
    print(get_text(key), end=" && ")
