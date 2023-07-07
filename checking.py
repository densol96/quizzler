class Test:
    def __init__(self):
        self.name = "Test"
    
    def checki(self):
        self.check = 123

test = Test()
print(test.name)
test.checki()
print(test.check)