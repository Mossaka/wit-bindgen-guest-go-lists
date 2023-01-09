# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.234.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Debian OS version (use bullseye on local arm64/Apple Silicon): buster, bullseye
FROM docker.io/mossaka/wit-bindgen:d24b97f

# TinyGo installation, see https://tinygo.org/getting-started/install/linux/ for instructions
ARG TINYGO_URL="https://github.com/tinygo-org/tinygo/releases/download/v0.26.0/tinygo_0.26.0_amd64.deb"
RUN curl -sL "$TINYGO_URL" -o tinygo_amd64.deb && dpkg -i tinygo_amd64.deb && rm tinygo_amd64.deb

# install wasi_snapshot_preveiw2 
RUN curl -LO https://github.com/bytecodealliance/preview2-prototyping/releases/download/latest/wasi_snapshot_preview1.wasm