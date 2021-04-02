# Scripts for just one-off things when testing android  
#### abe.jar can be obtained from it's original location:
https://github.com/nelenkov/android-backup-extractor/releases/download/20210309062218-e30cc24/abe.jar

## decrypt-android-react.py
Run the script in the shared_prefs directory of an android app written in React Native, you should see
the RN_KEYCHAIN.xml and crypto.KEY_256.xml in the shared_prefs directory  
```
$ python3 ./decrypt-android-react.py --help
usage: decrypt-android-react.py [-h] [--dir DIR]

optional arguments:
  -h, --help  show this help message and exit
  --dir DIR   path to shared_prefs directory  


python3 ./decrypt-android-react.py --dir com.app.whatever/shared_prefs/
```

