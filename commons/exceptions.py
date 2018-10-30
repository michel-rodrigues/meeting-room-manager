
class ScheduleConflict(Exception):

    def __init__(self, message, code):
        self.message = message
        self.code = code

    def __repr__(self):
        return '<ScheduleConflict({}, {})'.format(self.message, self.code)
