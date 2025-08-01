<p align="center">
  <img width="250" src="./icon.png">
</p>

⚠️ **Warning:** This method of making Cha into a quote unquote "MacOS App" is quite janky and not ideal though it kind of works. If you have a better approach or method please contribute I would greatly appreciate it!

# Cha Launcher for MacOS

This project provides a simple MacOS `.app` that launches [Cha](https://github.com/MehmetMHY/cha) inside a [Kitty terminal](https://sw.kovidgoyal.net/kitty/), preloaded with your environment. Please note that this method only works on **MacOS**, no other operating system.

## Features

- Runs `cha` in a fast Kitty terminal session
- Automatically sources your environment from `~/.custom/.env`
- Keeps the terminal open after execution
- Includes a custom `icon.png` to use for the app

## Requirements

- [MacOS](https://en.wikipedia.org/wiki/MacOS)
- [Kitty terminal](https://sw.kovidgoyal.net/kitty/) installed
- [pyenv](https://github.com/pyenv/pyenv) for Python version management.
- An [OpenAI API key](https://openai.com/api/) or run [Ollama](https://ollama.com/) locally.

## Setup Instructions

### 1. Install Kitty

Download and install Kitty from [its website](https://sw.kovidgoyal.net/kitty/). Make sure it's in your `/Applications` folder.

### 2. Install and Configure `pyenv`

If you don't have `pyenv`, install it by following the official instructions at [https://github.com/pyenv/pyenv](https://github.com/pyenv/pyenv). This is the recommended way to manage Python environments for Cha.

### 3. Install Cha

Once `pyenv` is set up, install Cha using it. Follow the instructions on the [Cha GitHub repo](https://github.com/MehmetMHY/cha) to install it correctly within a `pyenv` environment. This ensures `cha` is accessible at a path like `$HOME/.pyenv/shims/cha`.

### 4. Configure Environment and API Keys

Cha requires API keys to function. You need to provide either an OpenAI API key or have a local Ollama instance running.

1.  Create a file at `~/.custom/.env`.
2.  Add your API keys and any other environment variables to this file. For example:

    ```bash
    export OPENAI_API_KEY="your-key-here"
    # or configure for a local Ollama instance
    ```

For more detailed setup instructions regarding environment variables, please check out the main [Cha README](https://github.com/MehmetMHY/cha). This script will automatically source `~/.custom/.env` before running `cha`.

### 5. Create the MacOS App

- Open **Script Editor** on MacOS.
- Load the included `cha.applescript` file.
- Save it as a MacOS **Application** (File → Save → Format: Application).
- Optional: Assign the included `icon.png` as the app icon by right-clicking the saved app, selecting "Get Info," and dragging `icon.png` onto the small icon in the top-left corner.

### 6. Launch

Double-click your saved `.app` to open Kitty, load your environment, and run Cha.
