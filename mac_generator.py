from element import Machine
from parameter import Parameter

class MacGenerator(object):
    def __init__(self, pa):
        # type: (Parameter) -> object
        self.mac_sequence = []
        # res_vec = []
        # for i in xrange(pa.res_num):
        #     res_vec.append(pa.res_slot)
        # for i in xrange(pa.mac_num):
        #     self.mac_sequence.append(Machine(pa.res_num, pa.res_slot, res_vec, i))

        # mac_info = [[4, [5, 5]],
        #             [3, [10, 10]],
        #             [3, [20, 20]]
        #             ]
        mac_info = [[10, [8, 8]]]

        k = 0
        for i in mac_info:
            for j in xrange(i[0]):
                k += 1
                self.mac_sequence.append(Machine(pa.res_num, pa.res_slot, i[1], k))
