import io
import os
import time
import configparser

def fatal(errMsg):
    print('[FATAL] ' + errMsg)
    print('[FATAL] Program is now exiting.')
    time.sleep(2)
    exit()

def main():
    if not os.path.isfile('config.ini'): fatal('Cannot find \'config.ini\'')
    # open config.ini for reading
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get values from config file
    TVSHOWS_PATH = config['Paths']['TVShowsPath']
    MOVIES_PATH = config['Paths']['MoviesPath']
    RECENT_SUBFILES_TXT = config['Paths']['RecentSubsPath']
    MAX_AGE = float(config['DEFAULT']['MaxAgeForSubs'])

    if not os.path.isdir(TVSHOWS_PATH): fatal(TVSHOWS_PATH + ' not found. Make sure to set the config.ini')
    if not os.path.isdir(MOVIES_PATH): fatal(MOVIES_PATH + ' not found. Make sure to set the config.ini')

    # open file for writing
    print('Getting recent sub FILENAMES\n')
    wfile = io.open(RECENT_SUBFILES_TXT, 'w', encoding='utf_8_sig')

    # recursively walk through tv shows path and find srt FILENAMES
    currTime = time.time()
    for ROOT, DIRS, FILENAMES in os.walk(TVSHOWS_PATH):
        for filename in FILENAMES:
            if filename.endswith('.srt'):
                file = os.path.join(ROOT, filename)
                crTime = os.path.getctime(file)
                if ((currTime-crTime)/(60*60*24)) <= MAX_AGE:
                    print('Added ' + os.path.basename(file))
                    wfile.write(file + '\n')

    # recursively walk through movies path and find srt FILENAMES
    for ROOT, DIRS, FILENAMES in os.walk(MOVIES_PATH):
        for filename in FILENAMES:
            if filename.endswith('.srt'):
                file = os.path.join(ROOT, filename)
                crTime = os.path.getctime(file)
                if ((currTime-crTime)/(60*60*24)) <= MAX_AGE:
                    print('Added ' + os.path.basename(file))
                    wfile.write(file + '\n')

if __name__ == '__main__':
    main()
    print('\nDone')
    time.sleep(2)