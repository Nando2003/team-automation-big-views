from PyInstaller.utils.hooks import collect_data_files

datas = []
datas += collect_data_files('big_views', includes=['styles/*.qss'])
datas += collect_data_files('big_views', includes=['assets/*'])
datas += collect_data_files('big_views', includes=['locales/*.json'])
