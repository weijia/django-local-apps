
class Counter(object):
    def __init__(self, total_number, interval=100, name="Counter"):
        super(Counter, self).__init__()
        self.total_number = total_number
        self.processed_child = 1
        self.interval = interval
        self.name = name
        print "%s total: %d" % (self.name, self.total_number)

    def increase(self):
        self.processed_child += 1
        if self.processed_child % self.interval == 0:
            print "%s processed: %d/%d" % (self.name, self.processed_child, self.total_number)
