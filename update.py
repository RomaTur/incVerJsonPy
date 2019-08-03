import argparse
import inquirer
import json

def package_patch_update():
    with open('package.json') as json_file:
        data = json.load(json_file)
        version_to_change = int(data['version'][-1:]) + 1
        json.dump(version_to_change, json_file)













if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Versions UPD')
    parser.add_argument('--build', dest='build', nargs='?', const='c', action='store',
                        help='update for expo.version, expo.ios.buildNumber, expo.android.versionCode')
    parser.add_argument('--bundle', action='store', nargs='?', const='c', dest='bundle', help='update for expo.version')
    parser.add_argument('--circuit', action='store', nargs='?', const='c', dest='circuit',
                        help='works for either appCsp or appSahalin')
    args = parser.parse_args()

    if args.build or args.bundle:
        choosing = [
            inquirer.List('upgrade',
                          message='Update release',
                          choices=['patch', 'minor', 'major'], ), ]
        answers = inquirer.prompt(choosing)
    if args.build and args.circuit or args.bundle and args.circuit:
        additional_choose = [
            inquirer.List('if_circuit',
                          message='Circuit',
                          choices=['csp', 'sahalin'], ), ]
        replies = inquirer.prompt(additional_choose)

