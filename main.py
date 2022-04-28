from localpackage.subpackage.Calculator import execute
import sys
import os
sys.path.insert(1, os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "localpackage"
))
execute()
