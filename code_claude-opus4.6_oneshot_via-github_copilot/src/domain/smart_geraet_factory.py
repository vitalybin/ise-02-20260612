from domain.enums import GeraeteTyp
from domain.smart_geraet import SmartGeraet
from domain.smart_lampe import SmartLampe
from domain.smart_heizung import SmartHeizung
from domain.smart_sensor import SmartSensor
from domain.smart_steckdose import SmartSteckdose
from domain.smart_kamera import SmartKamera


class SmartGeraetFactory:
    @staticmethod
    def create(typ: GeraeteTyp, name: str) -> SmartGeraet:
        if typ == GeraeteTyp.LAMPE:
            return SmartLampe(name=name)
        elif typ == GeraeteTyp.HEIZUNG:
            return SmartHeizung(name=name)
        elif typ == GeraeteTyp.SENSOR:
            return SmartSensor(name=name)
        elif typ == GeraeteTyp.STECKDOSE:
            return SmartSteckdose(name=name)
        elif typ == GeraeteTyp.KAMERA:
            return SmartKamera(name=name)
        else:
            raise ValueError(f"Unbekannter GeraeteTyp: {typ}")
