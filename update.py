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


# Базовые обновления patch / minor / major (version & expo.version)
# from 2.1.0 to 2.1.1
# from 2.1.0 to  2.2.0
# from 2.1.0 to 3.1.0

def versioning(file_occurred, part):
    if file_occurred == 'appCsp.json' or file_occurred == 'appSahalin.json':
        with open(file_occurred, 'r+') as f:
            file = json.load(f)
            spl = file['expo']['version'].split('.')
            spl[part] = str(int(spl[part]) + 1)
            file['expo']['version'] = '.'.join(spl)
            f.seek(0)
            json.dump(file, f, indent=4)
            f.truncate()
    else:
        with open(file_occurred, 'r+') as pack:
            p = json.load(pack)
            spl = p['version'].split('.')
            spl[part] = str(int(spl[part]) + 1)
            p['version'] = '.'.join(spl)
            pack.seek(0)
            json.dump(p, pack, indent=4)
            pack.truncate()


# Обновление expo.version/version, если --circuit
def upd_version_with_circuit():
    if answers.get('upgrade') == 'patch':
        versioning('package.json', 2)

        if args.circuit:
            if replies.get('circuit') == 'csp':
                os.system('echo bundle csp')
                versioning('appCsp.json', 2)
            elif replies.get('circuit') == 'sahalin':
                os.system('echo bundle sahalin')
                versioning('appSahalin.json', 2)

    if answers.get('upgrade') == 'minor':
        versioning('package.json', 1)

        if args.circuit:
            if replies.get('circuit') == 'csp':
                os.system('echo bundle csp ')
                versioning('appCsp.json', 1)
            elif replies.get('circuit') == 'sahalin':
                os.system('echo bundle sahalin')
                versioning('appSahalin.json', 1)

    if answers.get('upgrade') == 'major':
        versioning('package.json', 0)

        if args.circuit:
            if replies.get('circuit') == 'csp':
                os.system('echo bundle csp ')
                versioning('appCsp.json', 0)
            elif replies.get('circuit') == 'sahalin':
                os.system('echo bundle sahalin')
                versioning('appSahalin.json', 0)

# Обновление buildNumber
def increase_special_fields(file):
    with open(file, 'r+') as f:
        js_file = json.load(f)

        j1 = js_file['expo']['ios']['buildNumber']
        j2 = int(js_file['expo']['android']['versionCode'])

        js_file['expo']['ios']['buildNumber'] = j1 + 1
        js_file['expo']['android']['versionCode'] = str(j2 + 1)
        f.seek(0)
        json.dump(js_file, f, indent=4)
        f.truncate()


c_special_fields = []
s_special_fields = []

def check():
    with open('package.json', 'r+') as pack:
        package = json.load(pack)
        p_version = []
        c_expo = []
        s_expo = []
        p_version.append(package['version'])
        with open('appCsp.json', 'r') as cs:
            new = json.load(cs)
            c_expo.append(new['expo']['version'])
            c_special_fields.append(int(new['expo']['ios']['buildNumber']))
            c_special_fields.append(int(new['expo']['android']['versionCode']))
            with open('appSahalin.json', 'r') as sa:
                sah = json.load(sa)
                s_expo.append(sah['expo']['version'])
                s_special_fields.append(int(sah['expo']['ios']['buildNumber']))
                s_special_fields.append(int(sah['expo']['android']['versionCode']))

        # присваивание version наибольшего значения
        find_common_version = max(p_version + c_expo + s_expo)
        package['version'] = find_common_version
        pack.seek(0)
        json.dump(package, pack, indent=4)
        pack.truncate()

        special = max(s_special_fields + c_special_fields)

    # если есть circuit, изменение версии  buildNumber или versionCode
    # в специально выбранном файле в большую сторону
    if args.circuit:
        if replies.get('circuit') == 'csp':

            with open('appCsp.json', 'r+') as main:
                csp_main = json.load(main)

                if csp_main['expo']['ios']['buildNumber'] < special:
                    csp_main['expo']['ios']['buildNumber'] = special

                elif int(csp_main['expo']['android']['versionCode']) < special:
                    csp_main['expo']['android']['versionCode'] = str(special)
                csp_main['expo']['version'] = find_common_version
                main.seek(0)
                json.dump(csp_main, main, indent=4)
                main.truncate()

        if replies.get('circuit') == 'sahalin':
            with open('appSahalin.json', 'r+') as m:
                sah_m = json.load(m)
                if sah_m['expo']['ios']['buildNumber'] < special:
                    sah_m['expo']['ios']['buildNumber'] = special

                elif int(sah_m['expo']['android']['versionCode']) < special:
                    sah_m['expo']['android']['versionCode'] = str(special)
                sah_m['expo']['version'] = find_common_version
                m.seek(0)
                json.dump(sah_m, m, indent=4)
                m.truncate()

    else:
        with open('appCsp.json', 'r+') as cs_w:
            new_w = json.load(cs_w)
            new_w['expo']['version'] = find_common_version
            new_w['expo']['ios']['buildNumber'] = special
            new_w['expo']['android']['versionCode'] = str(special)
            cs_w.seek(0)
            json.dump(new_w, cs_w, indent=4)
            cs_w.truncate()
        with open('appSahalin.json', 'r+') as sa_w:
            to_write = json.load(sa_w)
            to_write['expo']['version'] = find_common_version
            to_write['expo']['ios']['buildNumber'] = special
            to_write['expo']['android']['versionCode'] = str(special)
            sa_w.seek(0)
            json.dump(to_write, sa_w, indent=4)
            sa_w.truncate()


# --build --circuit
# меняются абсолютно все поля, но нужно выбрать дополнительный файл - csp / sahalin
if args.build and args.circuit:
    upd_version_with_circuit()  # version, expo.version  - выбор circuit реализован

    if answers.get('upgrade') == 'patch':
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            increase_special_fields('appCsp.json')

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            increase_special_fields('appSahalin.json')

    if answers.get('upgrade') == 'minor':
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            increase_special_fields('appCsp.json')

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            increase_special_fields('appSahalin.json')

    if answers.get('upgrade') == 'major':
        # buildNumber, versionCode - выбор файла
        if replies.get('circuit') == 'csp':
            os.system('echo build csp')
            increase_special_fields('appCsp.json')

        elif replies.get('circuit') == 'sahalin':
            os.system('echo build sahalin')
            increase_special_fields('appSahalin.json')
    check()

# --bundle --circuit
# меняется version, expo.version - нужно выбрать дополнительный файл - csp / sahalin
elif args.bundle and args.circuit:
    upd_version_with_circuit()
    check()


# --build
# меняется version(package.json), buildNumber, versionCode и в sahalin и csp
elif args.build and not args.circuit:
    os.system('echo build csp and sahalin')
    if answers.get('upgrade') == 'patch':
        versioning('package.json', 2)
        versioning('appCsp.json', 2)  # expo.version  - csp
        versioning('appSahalin.json', 2)  # expo.version - sahalin
    elif answers.get('upgrade') == 'minor':
        versioning('package.json', 1)
        versioning('appCsp.json', 1)  # expo.version  - csp
        versioning('appSahalin.json', 1)  # expo.version - sahalin
    elif answers.get('upgrade') == 'major':
        versioning('package.json', 0)
        versioning('appCsp.json', 0)  # expo.version  - csp
        versioning('appSahalin.json', 0)  # expo.version - sahalin
    increase_special_fields('appCsp.json')
    increase_special_fields('appSahalin.json')
    check()

#  --bundle
# меняется только version, expo.version во всех файлах
elif args.bundle and not args.circuit:
    os.system('echo bundle')
    upd_version_with_circuit()
    check()
else:
    raise ValueError('no key was found or you boy just strange')

# Итог:
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
