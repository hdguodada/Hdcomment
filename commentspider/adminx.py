import xadmin
from commentspider.models import HotelIndex


class HotelIndexAdmin(object):
    pass


xadmin.site.register(HotelIndex, HotelIndexAdmin)
