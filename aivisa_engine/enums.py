
# Standard photographic print size. Called "13 x 18 cm" worldwide.
class Paper4R():
    height = 4
    width = 6
    padding = 0
    padding_top = 0
    padding_bottom = 0
    padding_left = 1
    padding_right = 1

    def __init__(self) -> None:
        pass

    def __str__(self):
        return str(self.height) + " x " + str(self.width)

    @classmethod
    def getSizePixel(self):
        return self.height * 300, self.width * 300, self.padding
