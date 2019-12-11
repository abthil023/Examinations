#!/usr/bin/env python

import sys
import os
import pathlib
import platform
import subprocess

# set HOME=%HOMEDRIVE%\%HOMEPATH%
# set COURSE=NTNU Simultaneous Localization and Mapping
# set EXAMTITLE=%COURSE% Final Exam 2016
# set ROOTDIR=%HOME%\OneDrive\Documents\%COURSE%\%EXAMTITLE%
# set EXAMDIR=%HOME%\OneDrive\Documents\Examinations
# set TEMPLATE=%EXAMDIR%\Templates
# set CODEDIR=%ROOTDIR%\Code

COURSE = 'Simultaneous Localization and Mapping'
YEAR = 2019
EXAMTYPE = 'Midterm'
UNIVERSITY = 'NTNU'

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = pathlib.Path(newPath).expanduser().resolve()

    def __enter__(self):
        self.savedPath = pathlib.Path.cwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

GIT_CMD = "git"

def runCommand( cmd ):
    try:
        o = subprocess.check_output( cmd, shell=True )
    except subprocess.CalledProcessError as e:
        print("ERROR", e.output)
        out = None
    else:
        out = o.decode('utf-8')
    return out
        
def updateGit( url, dirname, branch,  root ):
        with cd( root ):
            p = pathlib.Path( dirname )
            if ( branch ):
                bs = " --branch " + branch
            else:
                bs = ""
            if not p.is_dir():
                print("cloning {0} from url {1} root {2}".format( dirname, url, root ), 'git command', GIT_CMD)
                    
                cmd = GIT_CMD + " clone " + bs + " " + url + " " + dirname 
                o = runCommand( cmd )
                print(o)
            else:
                print("git directory exists")

            with cd( dirname ):
                print("Executing git pull")
                o = runCommand(GIT_CMD + " pull")
                print(o)

EXAMTITLE = COURSE + ' - ' + EXAMTYPE  + ' - ' + UNIVERSITY + ' - ' + str(YEAR)
EXAMDIR = pathlib.Path("./Examinations")

updateGit( "https://github.com/abthil023/Examinations.git", EXAMDIR.name, None, EXAMDIR.parent )

for d in [ pathlib.Path(EXAMTITLE), pathlib.Path(COURSE) / EXAMTITLE, pathlib.Path("/courses") / COURSE / EXAMTITLE, pathlib.Path(".")  ]:
    if d.is_dir() and pathlib.Path(d / pathlib.Path( EXAMTITLE + ".py" ) ).exists():
        ROOTDIR = d.resolve()
        break

if ( ROOTDIR is None ) or ( EXAMDIR is None ):
    print("ERROR: Unable to find ROOTDIR", ROOTDIR, "or EXAMDIR", EXAMDIR)
    sys.exit(2)

TEMPLATEDIR = EXAMDIR  / 'Templates' 
CODEDIR = ROOTDIR / 'Code'
STYLES = TEMPLATEDIR / 'exam_template.css'

codePaths = [ pathlib.Path('.' + '/' + 'Code' ).resolve(),
              pathlib.Path(CODEDIR),
              pathlib.Path(CODEDIR).parent.parent /  'Code' ]

questionPaths = [ pathlib.Path('.' + '/' + 'Questions' ).resolve(),
                  pathlib.Path(ROOTDIR) / 'Questions',
                  pathlib.Path(ROOTDIR).parent / 'Questions' ]

#for k in os.environ:
#    print('k', k, '=', os.environ[k] )

PYTHON_EXECUTABLE = sys.executable
VERBOSE = '-v -v'

examPath = pathlib.Path('.' + '/' + EXAMTITLE + ".py").resolve()
print('+++ examPath', examPath )

commandLine = PYTHON_EXECUTABLE \
                + ' ' '"' + str( EXAMDIR / 'create_exam.py' ) + '"' \
                + ' ' + VERBOSE + ' ' \
                + ' ' + '"' + str( examPath ) + '"' \
                + ' -t ' + '"' + str(TEMPLATEDIR) + '"' \
                + ' -s ' + '"' + str(STYLES) + '"'

for q in questionPaths:
    print('q',q)
    commandLine = commandLine + ' -r ' + '"' + str( q.resolve() ) + '"' + ' '

for c in codePaths:
    commandLine = commandLine + ' -r ' + '"' + str( c.resolve() ) + '"' + ' '

print('Command line', commandLine )
o = runCommand( commandLine )
print(o)