keys = "Angol, Biológia, Fizika, Irodalom, Matek, Német, Németh - Barbar, Nyelvtan, Történelem".split(", ")

def get_text(key):
    text = f'echo "Angol.ps1 && one.bat" > ".{key}.bat"'

    return text

for key in keys:
    print(get_text(key), end=" && ")
