import os
import time

keys = "Angol, Biológia, Fizika, Irodalom, Matek, Német, Németh - Barbar, Nyelvtan, Történelem"
keys = keys.split(", ")


if __name__ == "__main__":
    folder = f'files - {time.time()}'

    os.system(f'mkdir "{folder}"')

    for key in keys:
        file_path = f'.\\{folder}\\.{key}.ps1'
        content = f'& "$env:USERPROFILE\\Code\\path_variables\\folders\\iskola\\{key}.ps1"'
        content += "\n"
        content += f'& "$env:USERPROFILE\\Code\\path_variables\\commands\\one.bat"'
        #os.system(f'echo "&" "$env:USERPROFILE\\Code\\path_variables\\folders\\iskola\\{key}.ps1" > {file_path}')
        #os.system(f'echo "&" "$env:USERPROFILE\\Code\\path_variables\\commands\\one.bat" >> {file_path}')

        with open(file_path, 'w') as f:
            f.write(content)
