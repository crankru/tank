Это репозиторий робота-танка на Raspberry Pi 3

- [Запуск](#Запуск)
- [Много букв о том как его делал](./docs/index.md)
- [Список и стоимость деталей](https://docs.google.com/spreadsheets/d/1Ukt3rJ1fKwBE6TXDDFmFCdl11GmUvG5iqSfO8u2NnJY/edit?usp=sharing)


# Запуск
Запуск сервера управления (видео через него же пока немного притормаживает)
```
python run.py
```

## Отдельный процесс трансляции видео
Для запуска видео стрима отдельным процессом нужно прописать `SEPARATE_STREAM_PROCESS = True` в файле настроек [config.py](./project/config.py), а затем выполнить:
```
python video-stream.py
```


## TODO
- Оптимизировать вывод видео и разобраться с многопоточностью
- Отдельные классы для picamera и usb камеры
- Глюки с кнопкой включения выключения видео
- Tooltip на слайдере