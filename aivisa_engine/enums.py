
# Standard photographic print size. Called "13 x 18 cm" worldwide.
class Paper4R():
    height = 4
    width = 6
    padding = 50

    def __init__(self) -> None:
        pass

    def __str__(self):
        return str(self.height) + " x " + str(self.width)

    @classmethod
    def getSizePixel(self):
        return self.height * 300, self.width * 300, self.padding
