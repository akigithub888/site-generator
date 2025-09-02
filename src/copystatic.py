import os
import shutil

def copy_static(src, dst):
    for name in os.listdir(src):
        if ":" in name or name.endswith(":Zone.Identifier"):
            continue 
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            # ensure parent dir exists (in case you call copy_static flexibly)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} -> {dst_path}")
        else:
            # directory: create then recurse
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
                print(f"Created dir: {dst_path}")
            copy_static(src_path, dst_path)