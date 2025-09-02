import os
import shutil
from copystatic import copy_static
import sys
from generate_pages import generate_pages_recursive

if len(sys.argv) < 2:
    basepath = "/"
else:
    basepath = sys.argv[1]

def main():
    src = "static"
    dst = "docs"
    
    # clean destination
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    copy_static(src, dst)
    print("Static assets copied.")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    

if __name__ == "__main__":
    main()
