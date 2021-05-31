class City:
    def __init__(self):
        self.cities = {
            "Keelung": "基隆市",
            "NewTaipei": "新北市",
            "Taipei": "台北市",
            "YilanCounty": "宜蘭縣",
            "Taoyuan": "桃園市",
            "Hsinchu": "新竹市",
            "HsinchuCounty": "新竹縣",
            "MiaoliCounty": "苗栗縣",
            "Taichung": "台中市",
            "ChanghuaCounty": "彰化縣",
            "NantouCounty": "南投縣",
            "YunlinCounty": "雲林縣",
            "Chiayi": "嘉義市",
            "ChiayiCounty": "嘉義縣",
            "Tainan": "台南市",
            "Kaohsiung": "高雄市",
            "PingtungCounty": "屏東縣",
            "TaitungCounty": "台東縣",
            "HualienCounty": "花蓮縣",
            "PenghuCounty": "澎湖縣",
            "KinmenCounty": "金門縣",
            "LienchiangCounty": "連江縣",
            "InterCity": "公路客運",
        }

    @property
    def english_names(self):
        return self.cities.keys()

    @property
    def chinese_names(self):
        return self.cities.values()

    def translate(self, name: str):
        return self.cities[name]
