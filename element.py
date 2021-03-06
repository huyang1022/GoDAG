import numpy as np


class Machine(object):
    count = 0

    def __init__(self, res_num, res_slot, res_vec, mac_id):
        Machine.count += 1
        self.id = mac_id
        self.res_num = res_num
        self.res_slot = res_slot
        self.res_vec = res_vec
        self.state = np.zeros([res_num, res_slot])

        assert len(res_vec) == res_num
        for i in xrange(res_num):
            self.state[i, res_vec[i]:] = -1

    @staticmethod
    def reset():
        Machine.count = 0
        # for i in xrange(self.res_num):
        #     self.state[i, :self.res_vec[i]] = 0
        #     self.state[i, self.res_vec[i]:] = -1

    def step(self):
        for i in xrange(self.res_num):
            self.state[i][self.state[i] > 0] -= 1
            # no_zero = (self.state[i] > 0)
            # self.state[i, :no_zero.sum()] = self.state[i, no_zero]
            # self.state[i, no_zero.sum():] = 0

    def show(self):
        for i in xrange(self.res_num):
            if i == 0:
                print "Mac ID: ", self.id, "\t", self.state[i]
            else:
                print "\t\t\t", self.state[i]



class Job(object):
    count = 0

    def __init__(self, submission_time, duration, res_num, res_slot, max_slot, res_vec, job_id):
        Job.count += 1
        self.id = job_id
        self.res_num = res_num
        self.res_slot = res_slot
        self.res_vec = res_vec
        self.submission_time = submission_time
        self.duration = duration
        self.starting_time = -1
        self.execution_time = -1
        self.status = "Pending"
        self.state = np.zeros([res_num, max_slot])

        assert len(res_vec) == res_num
        for i in xrange(res_num):
            self.state[i, :res_vec[i]] = duration


        self.depth = 0
        self.c_next = -1
        self.c_len = 0
        self.c_state = None
        self.c_res_state = None

        assert len(res_vec) == res_num


    @staticmethod
    def reset():
        Job.count = 0
        # self.starting_time = -1
        # self.execution_time = -1

    def start(self, current_time):
        self.starting_time = current_time
        self.execution_time = 0
        self.status = "Running"

    def step(self):
        assert self.execution_time < self.duration
        assert self.status == "Running"
        self.execution_time += 1
        if self.execution_time == self.duration:
            self.status = "Finished"

    def show(self):
        for i in xrange(self.res_num):
            if i == 0:
                print "Job ID: ", self.id, "\t", self.res_vec[i]
            else:
                print "\t\t\t", self.res_vec[i]

class Action(object):
    def __init__(self, job_id, mac_id):
        self.job_id = job_id
        self.mac_id = mac_id

    def show(self):
        print "Action:      Job_id = ", self.job_id, "       Mac_id = ", self.mac_id
