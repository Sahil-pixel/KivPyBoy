# KivPyBoy

KivPyBoy is a cross-platform Game Boy and Game Boy Color emulator frontend built with Kivy and powered by PyBoy.

## Author

### 👨‍💻 Sahil Pixel

**GitHub:** https://github.com/Sahil-pixel

The project demonstrates how to run PyBoy on Android using a custom python-for-android recipe, native Java audio output, and a fully touch-enabled Kivy interface.

## Features

- Game Boy (DMG) emulation
- Game Boy Color (CGB) emulation
- Built with Kivy
- Powered by PyBoy
- Custom Android-compatible PyBoy recipe
- Headless emulation (no SDL dependency)
- Native Android AudioTrack audio backend
- Desktop audio using Pygame
- Touch controls
- Keyboard controls
- Pixel-perfect scaling
- ARM64 Android support
- Buildozer compatible

## Technical Highlights

### Custom PyBoy Android Port
https://github.com/baekalfen/pyboy

PyBoy normally depends on SDL-based components that are not ideal for Android packaging.

This project includes a custom python-for-android recipe that:

- Builds PyBoy directly from source
- Disables SDL dependencies
- Enables headless rendering
- Uses Android NDK toolchains automatically
- Installs PyBoy into the application environment

Environment configuration:

```text
PYBOY_HEADLESS=1
PYBOY_NO_SDL=1
```

### Video Pipeline

```text
PyBoy
   │
   ▼
screen.ndarray
   │
   ▼
NumPy RGB Frame
   │
   ▼
Kivy Texture
   │
   ▼
Display
```

### Audio Pipeline

Desktop:

```text
PyBoy
   │
   ▼
sound.ndarray
   │
   ▼
NumPy
   │
   ▼
Pygame Mixer
```

Android:

```text
PyBoy
   │
   ▼
sound.ndarray
   │
   ▼
NumPy PCM Samples
   │
   ▼
Pyjnius
   │
   ▼
AudioBridge.java
   │
   ▼
Android AudioTrack
```

## Controls

### Touch Controls

- D-Pad
- A Button
- B Button
- Start
- Select

### Keyboard Controls

| Key | Action |
|------|---------|
| Arrow Keys | Movement |
| Z | A |
| X | B |
| Enter | Start |
| Space | Select |

## Build Requirements

- Python 3.11
- Kivy 2.3.1
- NumPy 1.26.4
- PyBoy
- Pyjnius
- Buildozer
- Android SDK
- Android NDK

## Android Build

```bash
buildozer android debug
```

Current tested target:

- Android API 35
- Android Min API 24
- ARM64-v8a

## Project Layout

```text
KivPyBoy/
│
├── main.py
├── buildozer.spec
├── pyboy_recipe/
│   └── pyboy/
│       └── __init__.py
│
├── java_codes/
│   └── AudioBridge.java
│
├── assets/
│
└── README.md
```

## Why This Project?

Most Python Game Boy emulators target desktop platforms.

KivPyBoy demonstrates:

- Running PyBoy on Android
- Building PyBoy with python-for-android
- Integrating Java AudioTrack with Pyjnius
- Using Kivy as a mobile emulator frontend
- Eliminating SDL dependencies for Android deployment

This repository can be used as a reference for porting other Python emulators to Android.

## Future Plans

- ROM file picker
- Remember last opened ROM directory
- Save states
- Load states
- Fast-forward
- Turbo mode
- Bluetooth controller support
- Physical gamepad support
- Cheat engine
- Custom skins
- Shader effects
- Save RAM management

## 📺 Demo Video

<p align="center">
  <a href="https://youtu.be/PS0TWPqjKb8">
    <img src="https://img.youtube.com/vi/PS0TWPqjKb8/maxresdefault.jpg" alt="KivPyBoy Demo" width="800">
  </a>
</p>

<p align="center">
  <b>Watch KivPyBoy running on Android</b><br>
  Custom PyBoy Android port with native AudioTrack audio and Kivy frontend.
</p>

👉 Video: https://youtu.be/PS0TWPqjKb8

## Credits

### PyBoy

Game Boy and Game Boy Color emulator written in Python.

### Kivy

Cross-platform Python framework for desktop and mobile applications.

### python-for-android

Android packaging framework used to build and deploy the application.

### Buildozer

Tool used to package Python applications for Android.

## License

MIT License

## Disclaimer

This repository does not contain any copyrighted ROMs.

Users are responsible for obtaining and using Game Boy and Game Boy Color ROMs legally.
