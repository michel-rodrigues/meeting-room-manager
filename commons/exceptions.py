
class ScheduleConflict(Exception):

    def __init__(self):
        self.message = 'The room is already booked in this period.'
        self.code = 'conflict'

    def __repr__(self):
        return '<ScheduleConflict({}, {})'.format(self.message, self.code)
