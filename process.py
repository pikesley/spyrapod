from tinydb import TinyDB

from lib.ride_enhancer import RideEnhancer

processor = RideEnhancer(TinyDB("/data/tiny-data/rides.json"))
processor.process()
