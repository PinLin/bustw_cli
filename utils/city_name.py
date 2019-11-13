class CityName:
    def __init__(self, cities: list):
        self.__english = list(map(lambda x: x['english_name'], cities))
        self.__chinese = list(map(lambda x: x['chinese_name'], cities))

    @property
    def english(self):
        return self.__english

    @property
    def chinese(self):
        return self.__chinese

    def to_english(self, name: str):
        return self.__english[self.__chinese.index(name)]

    def to_chinese(self, name: str):
        return self.__chinese[self.__english.index(name)]
