from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('botflow', includes=['styles/*.qss'])
datas += collect_data_files('botflow', includes=['assets/*'])
datas += collect_data_files('botflow', includes=['locales/*.json'])
