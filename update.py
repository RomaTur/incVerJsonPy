import inquirer
import argparse
import json
import os

parser = argparse.ArgumentParser(description='Versions UPD')
parser.add_argument('--build', dest='build', nargs='?', const='c', action='store',
                    help='default key to update for package, appCsp/appSahalin (expo.version or expo.ios.buildNumber, expo.android.versionCode)')
parser.add_argument('--bundle', dest='bundle', nargs='?', const='c', action='store',
                    help='default key to update for package (version), appCsp/appSahalin (expo.version)')
parser.add_argument('--circuit', action='store', nargs='?', const='c', dest='circuit',
                    help='important to update for either appCsp or appSahalin')
args = parser.parse_args()

# path = os.path.dirname('/Users/ana/Desktop/incVerJsonPy')
path = os.path.abspath(os.path.dirname(__file__))


# Базовые обновления version & expo.version
# from 2.1.0 to 2.1.1
def patch_update(occurred_file):
    if occurred_file == 'appCsp.json':
        with open(occurred_file, 'r+') as file:
            data = json.load(file)
            exclude_second = data['expo']['version'][-1:]
            another_to_change = str(int(exclude_second) + 1)
            data['expo']['version'] = data['expo']['version'][:4] + another_to_change
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    elif occurred_file == 'appSahalin.json':
        with open(occurred_file, 'r+') as file:
            data = json.load(file)
            exclude_second = data['expo']['version'][-1:]
            another_to_change = str(int(exclude_second) + 1)
            data['expo']['version'] = data['expo']['version'][:4] + another_to_change
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    else:
        with open(occurred_file, 'r+') as package:
            data = json.load(package)
            exclude_first = data['version'][-1:]
            last_to_change = str(int(exclude_first) + 1)
            data['version'] = data['version'][:4] + last_to_change
            package.seek(0)
            json.dump(data, package, indent=4)
            package.truncate()


# from 2.1.0 to 2.2.0
def minor_update(occurred_file):
    if occurred_file == 'appCsp.json':
        with open(occurred_file, 'r+') as file:
            data = json.load(file)
            exclude_second = data['expo']['version'][2:-2]
            another_to_change = str(float(exclude_second) + 1)
            data['expo']['version'] = data['expo']['version'][:2] + another_to_change
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
    elif occurred_file == 'appSahalin.json':
        with open(occurred_file, 'r+') as f:
            d = json.load(f)
            exclude_second = d['expo']['version'][2:-2]
            another_to_change = str(float(exclude_second) + 1)
            d['expo']['version'] = d['expo']['version'][:2] + another_to_change
            f.seek(0)
            json.dump(d, f, indent=4)
            f.truncate()
    else:
        with open(occurred_file, 'r+') as pack:
            data = json.load(pack)
            exclude_first = data['version'][-3:]
            last_to_change = str(float(exclude_first) + 1)
            data['version'] = data['version'][:2] + last_to_change
            pack.seek(0)
            json.dump(data, pack, indent=4)
            pack.truncate()


# from 2.1.0 to 3.1.0
def major_update(occurred_file):
    if occurred_file == 'appCsp.json' or occurred_file == 'appSahalin.json':
        with open(occurred_file, 'r+') as file_js:
            data = json.load(file_js)
            exclude_second = data['expo']['version'][:1]
            another_to_change = str(int(exclude_second) + 1)
            data['expo']['version'] = another_to_change + data['expo']['version'][-4:]
            file_js.seek(0)
            json.dump(data, file_js, indent=4)
            file_js.truncate()

    else:
        with open(occurred_file, 'r+') as pack:
            data = json.load(pack)
            exclude_first = data['version'][:1]
            last_to_change = str(int(exclude_first) + 1)
            data['version'] = last_to_change + data['version'][-4:]
            pack.seek(0)
            json.dump(data, pack, indent=4)
            pack.truncate()


# pretty choose for options
choosing = [
    inquirer.List('upgrade',
                  message='Update release',
                  choices=['patch', 'minor', 'major'], ), ]
answers = inquirer.prompt(choosing)
if args.circuit:
    additional_choose = [
        inquirer.List('circuit',
                      message='Circuit',
                      choices=['csp', 'sahalin'], ), ]
    replies = inquirer.prompt(additional_choose)


# Functions below are to complete actions if there is --circuit
def patch():
    # update anyway
    patch_update('package.json')
    if replies.get('circuit') == 'csp':
        # обновление версии expo.version patch
        patch_update('appCsp.json')

    if replies.get('circuit') == 'sahalin':
        # обновление версии expo.version patch
        patch_update('appSahalin.json')


def minor():
    # update anyway
    minor_update('package.json')
    if replies.get('circuit') == 'csp':
        # обновление версии expo.version minor
        minor_update('appCsp.json')

    if replies.get('circuit') == 'sahalin':
        # обновление версии expo.version minor
        minor_update('appSahalin.json')


def major():
    major_update('package.json')
    if replies.get('circuit') == 'csp':
        # обновление версии expo.version minor
        major_update('appCsp.json')

    if replies.get('circuit') == 'sahalin':
        # обновление версии expo.version minor
        major_update('appSahalin.json')


############################################################
# --build --circuit
# меняются абсолютно все поля, но нужно выбрать дополнительный файл - csp / sahalin
if args.build and args.circuit:
    if answers.get('upgrade') == 'patch':
        patch()  # version, expo.version  - выбор circuit реализован

         # buildNumber, versionCode - выбор файла
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            with open('appCsp.json', 'r+') as csp:
                csp_file = json.load(csp)

                c1 = csp_file['expo']['ios']['buildNumber']
                c2 = csp_file['expo']['android']['versionCode']

                csp_file['expo']['ios']['buildNumber'] = int(c1) + 1
                csp_file['expo']['android']['versionCode'] = int(c2) + 1
                csp.seek(0)
                json.dump(csp_file, csp, indent=4)
                csp.truncate()

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            with open('appSahalin.json', 'r+') as sahalin:
                sah_file = json.load(sahalin)

                s1 = sah_file['expo']['ios']['buildNumber']
                s2 = sah_file['expo']['android']['versionCode']

                sah_file['expo']['ios']['buildNumber'] = int(s1) + 1
                sah_file['expo']['android']['versionCode'] = int(s2) + 1
                sahalin.seek(0)
                json.dump(sah_file, sahalin, indent=4)
                sahalin.truncate()

    if answers.get('upgrade') == 'minor':
        minor()
        # buildNumber, versionCode - выбор файла
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            with open('appCsp.json', 'r+') as csp:
                csp_file = json.load(csp)

                c1 = csp_file['expo']['ios']['buildNumber']
                c2 = csp_file['expo']['android']['versionCode']

                csp_file['expo']['ios']['buildNumber'] = int(c1) + 1
                csp_file['expo']['android']['versionCode'] = int(c2) + 1
                csp.seek(0)
                json.dump(csp_file, csp, indent=4)
                csp.truncate()

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            with open('appSahalin.json', 'r+') as sahalin:
                sah_file = json.load(sahalin)

                s1 = sah_file['expo']['ios']['buildNumber']
                s2 = sah_file['expo']['android']['versionCode']

                sah_file['expo']['ios']['buildNumber'] = int(s1) + 1
                sah_file['expo']['android']['versionCode'] = int(s2) + 1
                sahalin.seek(0)
                json.dump(sah_file, sahalin, indent=4)
                sahalin.truncate()

    if answers.get('upgrade') == 'major':
        major()
        # buildNumber, versionCode - выбор файла
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            with open('appCsp.json', 'r+') as csp:
                csp_file = json.load(csp)

                c1 = csp_file['expo']['ios']['buildNumber']
                c2 = csp_file['expo']['android']['versionCode']

                csp_file['expo']['ios']['buildNumber'] = int(c1) + 1
                csp_file['expo']['android']['versionCode'] = int(c2) + 1
                csp.seek(0)
                json.dump(csp_file, csp, indent=4)
                csp.truncate()

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            with open('appSahalin.json', 'r+') as sahalin:
                sah_file = json.load(sahalin)

                s1 = sah_file['expo']['ios']['buildNumber']
                s2 = sah_file['expo']['android']['versionCode']

                sah_file['expo']['ios']['buildNumber'] = int(s1) + 1
                sah_file['expo']['android']['versionCode'] = int(s2) + 1
                sahalin.seek(0)
                json.dump(sah_file, sahalin, indent=4)
                sahalin.truncate()


# --bundle --circuit
# меняется version, expo.version
elif args.bundle and args.circuit:
    if answers.get('upgrade') == 'patch':
        patch()  # version, expo.version  - выбор circuit реализован, как и в других ниже

    if answers.get('upgrade') == 'minor':
        minor()

    if answers.get('upgrade') == 'major':
        major()

# --build
# меняется version(package.json), buildNumber, versionCode и в sahalin и csp
elif args.build and not args.circuit:
    os.system('echo build csp and sahalin')
    patch_update('appCsp.json')  # expo.version  - csp
    patch_update('appSahalin.json')  # expo.version - sahalin
    # buildNumber, versionCode  - csp & sahalin
    result_app = [file for file in os.listdir(path) if file.startswith('app')]
    for js in result_app:
        with open(os.path.join(path, js), 'r+') as json_file:
            json_text = json.load(json_file)
            versions = []
            versions.append(json_text["expo"]["ios"]['buildNumber'])
            versions.append(json_text["expo"]["android"]['versionCode'])
            for i in versions:
                json_text["expo"]["ios"]['buildNumber'] = int(i) + 1
                json_text["expo"]["android"]['versionCode'] = int(i) + 1
                json_file.seek(0)
                json.dump(json_text, json_file, indent=4)
                json_file.truncate()

#  --bundle
# меняется только version, expo.version во всех файлах
elif args.bundle and not args.circuit:
    if answers.get('upgrade') == 'patch':
        os.system('echo bundle csp and sahalin')
        patch_update('package.json')
        patch_update('appCsp.json')  # expo.version  - csp
        patch_update('appSahalin.json')  # expo.version - sahalin

    if answers.get('upgrade') == 'minor':
        os.system('echo bundle csp and sahalin')
        minor_update('package.json')
        minor_update('appCsp.json')  # expo.version  - csp
        minor_update('appSahalin.json')  # expo.version - sahalin

    if answers.get('upgrade') == 'major':
        os.system('echo bundle csp and sahalin')
        major_update('package.json')
        major_update('appCsp.json')  # expo.version  - csp
        major_update('appSahalin.json')  # expo.version - sahalin

    # =========================================================
    # сравнение версий между собой выбор в сторону наибольшего

    result_app = [file for file in os.listdir(path) if file.startswith('app')]
    expo = []
    number = []
    android = []
    for js in result_app:
        with open(os.path.join(path, js), 'r+') as json_file:
            json_text = json.load(json_file)
            expo.append(json_text['expo']['version'])
            number.append(json_text['expo']['ios']['buildNumber'])
            android.append(str(json_text['expo']['android']['versionCode']))
            same_path = number + android
            json_text['expo']['ios']['buildNumber'] = max(same_path)
            json_text['expo']['android']['versionCode'] = max(same_path)
            json_file.seek(0)
            json.dump(json_text, json_file, indent=4)
            json_file.truncate()

    with open('/Users/ana/Desktop/incVerJsonPy/package.json', 'r+') as p:
        fil = json.load(p)
        expo.append(fil['version'])
        p.seek(0)
        json.dump(fil, p, indent=4)
        p.truncate()

    result_app = [file for file in os.listdir(path) if file.startswith('app')]
    for js in result_app:
        with open(os.path.join(path, js), 'r+') as pack:
            package = json.load(pack)
            ver = package['expo']['version']
            m2 = max(expo)
            if m2 > ver:
                ver = m2
                package['expo']['version'] = m2
            else:
                m2 = ver
                package['expo']['version'] = m2
            pack.seek(0)
            json.dump(package, pack, indent=4)
            pack.truncate()
    with open('/Users/ana/Desktop/incVerJsonPy/package.json', 'r+') as p:
        fil = json.load(p)
        fil['version'] = max(expo)
        p.seek(0)
        json.dump(fil, p, indent=4)
        p.truncate()

else:
    raise ValueError('failure with command or some key is missing')

    # =========================================================

# Далее выводится итог:
with open('appSahalin.json', 'r+') as apsahalin:
    sah_file = json.load(apsahalin)

    s1 = sah_file['expo']['ios']['buildNumber']
    s2 = sah_file['expo']['version']

with open('appCsp.json', 'r+') as apcsp:
    sah_file = json.load(apcsp)

    a1 = sah_file['expo']['ios']['buildNumber']
    a2 = sah_file['expo']['version']

print('Update info:\n sahalin: v{} | build {} \n csp: v{} | build {}'.format(s2, s1, a2, a1))
print('Get builds https://expo.io/builds')