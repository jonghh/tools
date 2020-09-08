class Person:    # 클래스
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.doc = ""

    def greeting(self):
        print('안녕하세요. 저는 {0}입니다.'.format(self.name))
        self.doc = '안녕하세요. 저는 {0}입니다.'.format(self.name)

    def introduce(self):
        print('{0}는 {1}살입니다.'.format(self.name, self.age))
        print(self.doc)
