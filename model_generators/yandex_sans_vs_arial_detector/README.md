Данный скрипт содержит модель нейросети, использованной для детектирования YS и содержит методы, необходимые для предобработки данных.

Запуск:
1. Запустить из директории model_generators скрипт
 ```PYTHON_PATH=. python yandex_sans_vs_arial_model_generator.py absolute_path_to_collection file_extension_preceeded_with_dot```

Результат: файл с минимальным значением входов в коллекции, файл с максимальным значением квходов в коллекции, файл с моделью и весами.
