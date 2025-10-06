#!/bin/bash
set -e

# CONFIG
PY_VERSION=3.11
GAME_FILE=game.py

# 1. Load emsdk (make sure you installed via official emsdk)
source ~/emsdk/emsdk_env.sh

# 2. Build CPython
if [ ! -d "cpython" ]; then
    git clone https://github.com/python/cpython
    cd cpython
    git checkout $PY_VERSION
    emconfigure ./configure --host=wasm32 --build=$(./config.guess)
    emmake make -j$(nproc)
    cd ..
fi

# 3. Build pygame-ce
if [ ! -d "pygame-ce" ]; then
    git clone https://github.com/pygame-community/pygame-ce
    cd pygame-ce
    export CC=emcc
    export LDSHARED="emcc -shared"
    export AR=emar
    export RANLIB=emranlib
    python3 setup.py build_ext -i
    cd ..
fi

# 4. Compile to WebAssembly
emcc \
  -O2 \
  -Icpython/Include \
  -Icpython \
  -Lcpython \
  -lpython3.11 \
  -s USE_SDL=2 \
  -s USE_SDL_IMAGE=2 \
  -s USE_SDL_TTF=2 \
  -s USE_SDL_MIXER=2 \
  -s WASM=1 \
  -s ALLOW_MEMORY_GROWTH=1 \
  -s ENVIRONMENT=web \
  -s FORCE_FILESYSTEM=1 \
  -s "EXPORTED_RUNTIME_METHODS=['FS','callMain']" \
  --embed-file $GAME_FILE \
  -o game.html

echo "✅ Build finished! Run: python3 -m http.server 8000"
echo "Then open: http://localhost:8000/game.html"
