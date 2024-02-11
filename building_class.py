
class GetBuildingClass:

    def __init__(self):
        questionnaire = Questionnaire()
        self.questions = Questions(questionnaire)
        self.classes = {
            'econom': 'Эконом',
            'comfort': 'Комфорт',
            'business': 'Бизнес',
            'elite': 'Премиум'
        }

    def first_algorithm(self):
        # Алгоритм 1. Дифференцирование на группы «массовое жилье» и «жилье повышенной комфортности»

        if self.questions.construction():
            return 'mass'
        if self.questions.flat_sq_ratio(ratio=0.7):
            return 'mass'
        if not self.questions.sq_threshold(alg_level='mass'):
            return 'mass'
        if not self.questions.ceiling(base_height=2.75):
            return 'mass'
        if not self.questions.bathroom(base_n_bathrooms=1):
            return 'mass'
        if not self.questions.arch_project():
            return 'mass'
        # if not self.q7():
        #     return 'mass'
        if not self.questions.territory():
            return 'mass'
        if not self.questions.parking(carplace_per_flat=1):
            return 'mass'
        return 'higher comfort'

    def second_algorithm(self):
        # Алгоритм 2. Дифференцирование массового жилья на эконом- и комфорт- классы

        if self.questions.flat_sq_ratio(ratio=0.75):
            return 'econom'
        if not self.questions.sq_threshold(alg_level='econom'):
            return 'econom'
        if not self.questions.ceiling(base_height=2.7):
            return 'econom'
        return 'comfort'

    def third_algorithm(self):
        # Алгоритм 3.  Дифференцирование жилья повышенной комфортности на бизнес- и элитный классы

        if self.questions.flat_sq_ratio(ratio=0.65):
            return 'business'
        if not self.questions.sq_threshold(alg_level='business'):
            return 'business'
        if not self.questions.ceiling(base_height=3):
            return 'business'
        if not self.questions.parking(carplace_per_flat=1.5):
            return 'business'
        if self.questions.commercials_inside():
            return 'business'
        return 'elite'

    def main(self):
        if self.first_algorithm() == 'mass':
            result = self.second_algorithm()
        else:
            result = self.third_algorithm()
        return 'Объект относится к классу "{}"'.format(self.classes[result])


class Questionnaire:

    def __init__(self):
        print('Ответьте, пожалуйста, на несколько вопросов')
        self.construction_type = None
        self.n_flats = None
        self.n_carplaces = None
        self.creative_arch_project = None
        self.closed_territory = None
        self.commercials = None
        self.flats_square = None
        self.full_square = None
        self.living_square = None
        self.kitchen_square = None
        self.n_rooms = None
        self.ceiling_height = None
        self.n_bathrooms = None

    def get_construction_type(self):
        self.construction_type = True if input('Является ли здание по конструкции сборно-железобетонным (панельным, блочным)? [Да/Нет] ').lower() == 'да' else False

    def get_n_flats_and_carplaces(self):
        self.n_flats = int(input('Укажите количество квартир в здании: '))
        self.n_carplaces = int(input('Укажите суммарное количество парковочных мест на подземном паркинге и на закрытой придомовой территории: '))

    def get_creative_arch_project(self):
        self.creative_arch_project = True if input('Является ли проект здания индивидуальным, с подчеркнутой дизайнерской проработкой внешнего облика? [Да/Нет]: ').lower() == 'да' else False

    def get_closed_territory(self):
        self.closed_territory = True if input('Является ли придомовая территория огороженной и охраняемой по периметру? [Да/Нет] ').lower() == 'да' else False

    def get_commercials(self):
        self.commercials = True if input('Имеются ли в доме коммерческие объекты со свободным входом с улицы через придомовую территорию? [Да/Нет] ').lower() == 'да' else False

    def get_floor_knowledge(self):
        self.flats_square = float(input('Укажите суммарную площадь квартир на этаже в кв.м: ').replace(',', '.'))
        self.full_square = float(input('Укажите общую площадь этажа в кв.м: ').replace(',', '.'))

    def get_apartment_knowledge(self):
        self.living_square = float(input('Укажите жилую площадь квартиры в кв.м: ').replace(',', '.'))
        self.kitchen_square = float(input('Укажите площадь кухни в кв.м: ').replace(',', '.'))

    def get_n_rooms(self):
        self.n_rooms = int(input('Укажите количество жилых комнат в квартире (студии считайте 1комнатной квартирой): '))

    def get_ceiling_height(self):
        self.ceiling_height = float(input('Укажите высоту потолка в метрах: ').replace(',', '.'))

    def get_n_bathrooms(self):
        self.n_bathrooms = int(input('Укажите количество ванных комнат в квартире: '))


class Questions:

    def __init__(self, questionnaire):
        self.spaces_square = {
            'mass': {1: 45, 2: 65, 3: 85, 4: 120, 5: 150, 'kitchen': 12},
            'econom': {1: 34, 2: 50, 3: 65, 4: 85, 5: 100, 'kitchen': 8},
            'business': {1: 60, 2: 80, 3: 120, 4: 250, 5: 350, 'kitchen': 20}
        }
        self.questionnaire = questionnaire

    def flat_sq_ratio(self, ratio):
        '''
        Превышает ли отношение суммарной площади квартир к общей площади жилых этажей значение "ratio"
        (допустимая альтернатива расчета: отношение суммарной площади квартир и нежилых помещений к общей площади здания)?
        '''
        if self.questionnaire.flats_square is None or  self.questionnaire.full_square is None:
            self.questionnaire.get_floor_knowledge()
        return self.questionnaire.flats_square / self.questionnaire.full_square > ratio

    def sq_threshold(self, alg_level):
        '''
        Соответствует ли площадь квартир (без учета летних помещений) и кухни следующим значениям (кв. м)?
        '''
        if self.questionnaire.living_square is None or self.questionnaire.kitchen_square is None:
            self.questionnaire.get_apartment_knowledge()
        if self.questionnaire.n_rooms is None:
            self.questionnaire.get_n_rooms()
        return (
            self.questionnaire.living_square >= self.spaces_square[alg_level][self.questionnaire.n_rooms]
            and self.questionnaire.kitchen_square >= self.spaces_square[alg_level]['kitchen']
        )

    def ceiling(self, base_height):
        '''
        Соответствует ли высота потолков квартир значению от "base_height" м?
        '''
        if self.questionnaire.ceiling_height is None:
            self.questionnaire.get_ceiling_height()
        return self.questionnaire.ceiling_height > base_height

    def parking(self, carplace_per_flat):
        '''
        Обеспечивает ли закрытый паркинг для жителей 1,5 машино-места на квартиру?
        '''
        if self.questionnaire.n_carplaces is None or self.questionnaire.n_flats is None:
            self.questionnaire.get_n_flats_and_carplaces()
        return self.questionnaire.n_carplaces / self.questionnaire.n_flats >= carplace_per_flat

    def commercials_inside(self):
        '''
        Имеются ли в доме коммерческие объекты со свободным входом с улицы через придомовую территорию?
        '''
        if self.questionnaire.commercials is None:
            self.questionnaire.get_commercials()
        return self.questionnaire.commercials

    def construction(self):
        '''
        Является ли здание по конструкции сборно-железобетонным (панельным, блочным)?
        '''
        if self.questionnaire.construction_type is None:
            self.questionnaire.get_construction_type()
        return self.questionnaire.construction_type

    def bathroom(self, base_n_bathrooms=1):
        '''
        Обеспечено ли наличие от 2 санузлов в квартирах свыше двух комнат?
        '''
        if self.questionnaire.n_bathrooms is None:
            self.questionnaire.get_n_bathrooms()
        if self.questionnaire.n_rooms is None:
            self.questionnaire.get_n_rooms()
        return self.questionnaire.n_bathrooms > base_n_bathrooms if self.questionnaire.n_rooms > 2 else self.questionnaire.n_bathrooms > 0

    def arch_project(self):
        '''
        Является ли проект здания индивидуальным, с подчеркнутой дизайнерской проработкой внешнего облика?
        '''
        if self.questionnaire.creative_arch_project is None:
            self.questionnaire.get_creative_arch_project()
        return self.questionnaire.creative_arch_project

    # def q7(self):
    #     '''
    #     Обеспечено ли энергоснабжение квартир трехфазными вводами с расчетной максимальной нагрузкой свыше 10 кВт?
    #     '''
    #     return

    def territory(self):
        '''
        Является ли придомовая территория огороженной и охраняемой по периметру в соответствии
        с разделом «Генеральный план и благоустройство» проектно-сметной документации жилого комплекса?
        '''
        if self.questionnaire.closed_territory is None:
            self.questionnaire.get_closed_territory()
        return self.questionnaire.closed_territory


if __name__ == '__main__':
    processing = GetBuildingClass()
    print(processing.main())