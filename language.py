class CalibrationLng():
    def __init__(self, lng):
        if lng == 'rus':
            self.title = 'Градуировочная таблица'
            self.tankLbl = 'емкость/резервуар'
            self.levelLbl = 'уровень (мм)'
            self.productLbl = 'продукт'
            self.tempLbl = 'температура'
            self.textBtn = 'вычислить'
            self.volume = 'объем (м3)'
            self.density = 'плотность (кг/м3)'
            self.mass = 'масса (тонн)'
            self.redactBtn = 'Редактировать'
            # self.tankBox = ['Е-5/2', 'Е-5/3', 'Е-5/4',
            #                 'Е-6/1 ', 'Е-6/2', 'Е-6/3',
            #                 'Е-6/4', 'Е-7', 'РВС-5',
            #                 'РВС-6', 'РВС-7', 'РВС-8']
            # self.tanks = {'Е-5/2': None, 'Е-5/3': None,
            #               'Е-5/4': None, 'Е-6/1': None,
            #               'Е-6/2': None, 'Е-6/3': None,
            #               'Е-6/4': None, 'Е-7': None,
            #               'РВС-5': None, 'РВС-6': None,
            #               'РВС-7': 'rvs7', 'РВС-8': None}
            # self.productEdit = ['ФДТ', 'ЭКТО', 'Риформат',
            #                     'МТБЭ', 'Лёгкий бензин']
            self.choiceBox = ['>>>', '<<<']
            # self.products = {'ФДТ': 0.825, 'ЭКТО': 0.756,
            #                  'Риформат': 0.777, 'МТБЭ': 0.741,
            #                  'Лёгкий бензин': 0.673}
            self.levelError = ('Ошибка уровня', 'Неверно введён уровень')
            self.tempError = ('Ошибка температуры', 'Неверно введена температура')
            self.massError = ('Ошибка массы', 'Неверно введена масса')
            self.densityError = ('Ошибка плотности', 'Неверно введена плотность')
            self.backError = ('Ошибка диапазона', 'Значение вне диапазона')
            self.volumeError = ('Ошибка плотности', 'Неверно введена плотность')

class AddWindow():
    def __init__(self, lng):
        if lng == 'rus':
            self.title = 'Добавление/удаление данных'
            self.back = 'Назад'
            self.addLabel = 'Добавление таблицы'
            self.codNameLabel = 'Кодовое имя'
            self.nameTableLabel = 'Имя таблицы'
            self.typeLabel = 'Тип емкости'
            self.fileLabel = 'Файл с данными'
            self.addProduct = 'Добавление продукта'
            self.productNameLabel = 'Продукт'
            self.valueLabel = 'Плотность (кг/м3)'
            self.delTableLabel = 'Удаление таблиц'
            self.delProductLabel = 'Удаление продукта'
            self.add = 'Добавить'
            self.delete = 'Удалить'
            self.typeBox = ['РВС', 'РГС']
            self.density = 'кг/м3'
            self.save_db = ['Сохранение таблицы', 'Таблица сохранена']
            self.del_table_msg = ['Удаление таблицы', 'Таблица удалена']
            self.add_prod_msg = ['Добавление продукта', 'Продукт добавлен']
            self.del_prod_msg = ['Удаление продукта', 'Продукт удалён']
            self.data_error = ['Ошибка данных', 'Неверно введена плотность']
            self.data_for_sql = ['Ошибка данных', 'Ошибка данных файла Excel']
            self.data_add_msg = ['Добавление данных', 'После закрытия данного сообщения\n'
                                                      'начнется процесс добавления данных'
                                                      '\nэто может занять несколько минут']
