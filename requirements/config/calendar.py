from datetime import datetime, timedelta, date
from workalendar.america import Brazil
import sys

data_atual = date.today()

class VortxCalendar(Brazil):
        include_fat_tuesday = True
        fat_tuesday_label = "Tuesday carnaval"
        include_good_friday = True
        include_ash_wednesday = False
        include_corpus_christi = True
        include_easter_sunday = False

        def get_variable_days(self, year):
            """
            Define the brazilian variable holidays
            """
            days = super().get_variable_days(year)
            tuesday_carnaval = self.get_fat_tuesday(year)
            monday_carnaval = tuesday_carnaval - timedelta(days=1)
            days.append((monday_carnaval, "Monday carnaval"))
            return days
        def find_following_working_day(self, day):
            """
            Find for the next working day by ignoring weekends,
            fixed and non fixed holidays
            """
            while not self.is_working_day(day):
                day = day + timedelta(days=1)
            return day

class ConfigCalendar():
    def __init__(self):
        pass
    
    def verifica_dia_util(self, calendario, lgr):
        if not calendario.is_working_day(data_atual):
            lgr.add_log("HOJE NÃO É DIA ÚTIL, PARANDO EXECUÇÃO...", level='info')
            sys.exit(0)
    