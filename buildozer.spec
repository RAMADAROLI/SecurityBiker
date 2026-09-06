[app]

title = Security Biker
package.name = securitybiker
package.domain = org.securitybiker

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,json

version = 1.0

requirements = python3,kivy==2.3.0,plyer==2.1.0

orientation = portrait

fullscreen = 0

android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CALL_PHONE,POST_NOTIFICATIONS

android.api = 33
android.minapi = 23

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
