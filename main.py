#!/usr/bin/env python3
import os
import shutil
import hashlib
import sys

def main():
    # Determine directory of main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'picture.jpg')
    
    # Guard: check if source image exists
    if not os.path.exists(source_path):
        print(f"Error: Source image 'picture.jpg' is missing next to main.py at {source_path}.", file=sys.stderr)
        sys.exit(1)
    
    # Determine output directory
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'entry.png')
    
    # Copy file byte-for-byte
    shutil.copyfile(source_path, output_path)
    
    # Post-copy verification
    source_size = os.path.getsize(source_path)
    output_size = os.path.getsize(output_path)
    
    if source_size != output_size:
        print(f"Error: Output file size ({output_size}) does not match source file size ({source_size})!", file=sys.stderr)
        sys.exit(1)
        
    print(f"Output verified to match source: {output_size} bytes")
    
    # Compute sha256
    sha256_hash = hashlib.sha256()
    with open(output_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256_hash.update(chunk)
    digest = sha256_hash.hexdigest()
    
    print(f"Output path: {output_path}")
    print(f"Byte size: {output_size}")
    print(f"SHA256: {digest}")

if __name__ == '__main__':
    main()
