from datetime import datetime


class Emotion:
    "Emotion class object includes: "

    _id: int
    image: str
    LoaiCamXuc: int
    ThietBi: int
    Ngay: datetime
    Kip: int

    def __init__(self, _id, image, LoaiCamXuc, ThietBi, Ngay, Kip) -> None:
        self._id = _id
        self.image = image
        self.LoaiCamXuc = LoaiCamXuc
        self.ThietBi = ThietBi
        self.Ngay = Ngay
        self.Kip = Kip
