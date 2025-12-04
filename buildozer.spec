[app]

# (str) Title of your application
title = My Kivy Application

# (str) Package name (lowercase, no special characters)
package.name = mykivyapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
# Use simple names; python-for-android automatically selects compatible versions.
requirements = python3,kivy,pillow

# (list) Supported orientations: landscape, portrait, portrait-reverse or landscape-reverse
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions needed by your app
android.permissions = INTERNET, (name=android.permission.WRITE_EXTERNAL_STORAGE;maxSdkVersion=18)

# (int) Target Android API, should be as high as possible. Google Play currently requires API 33+.
android.api = 34

# (int) Minimum API your APK / AAB will support. (21 or 24 is a safe minimum for modern apps)
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use (e.g., 25b is a stable choice)
android.ndk = 25b

# (list) The Android architectures to build for (covers most devices)
android.archs = arm64-v8a, armeabi-v7a

# (bool) If True, then automatically accept SDK license agreements.
# THIS IS CRITICAL FOR GITHUB ACTIONS (CI/CD)
android.accept_sdk_license = True

# ------------------------------------------------------------------
# Less common or optional settings (uncomment to use):
# ------------------------------------------------------------------

# (str) Icon of the application file path
#icon.filename = %(source.dir)s/data/icon.png

# (str) Presplash image file path
#presplash.filename = %(source.dir)s/data/presplash.png
