from element import Job
from parameter import Parameter
import numpy as np

class JobGenerator1(object):
    def __init__(self, pa, rseed):
        # type: (Parameter) -> object
        self.job_sequence = []
        self.job_dag_id = []
        self.dag_matrix = []
        self.total_len = 0.0

        self.short_rate = 0.5
        #
        # self.long_upper = pa.job_max_len
        # self.long_lower = pa.job_max_len  / 2 + 1
        # self.short_upper = pa.job_max_len / 2
        # self.short_lower = 1
        self.long_upper = pa.job_max_len
        self.long_lower = 1
        self.short_upper = pa.job_max_len
        self.short_lower = 1


        # self.dominant_upper = pa.job_max_slot
        # self.dominant_lower = pa.job_max_slot / 2 + 1
        # self.other_upper = pa.job_max_slot / 2
        # self.other_lower = 1

        self.dominant_upper = pa.job_max_slot
        self.dominant_lower = 1
        self.other_upper = pa.job_max_slot
        self.other_lower = 1
        self.batch_num = pa.batch_num

        np.random.seed(rseed)

        pa.job_num = np.random.randint(100, 200)
        pa.dag_max_depth = np.random.randint(4,9)
        layer = list()
        for i in xrange(pa.job_num):
            layer.append(np.random.randint(pa.dag_max_depth))

        for k in xrange(self.batch_num):
            self.dag_matrix.append([])
            for i in xrange(pa.job_num):
                self.dag_matrix[0].append([])
                for j in xrange(pa.job_num):
                    if layer[i] < layer[j] and np.random.random() <= 0.1:
                        self.dag_matrix[0][i].append(1)
                    else:
                        self.dag_matrix[0][i].append(0)



        for k in xrange(self.batch_num):
            self.job_dag_id.append(0)
            self.job_sequence.append([])
            for i in xrange(pa.job_num):
                if np.random.rand() <= self.short_rate:          # generate a short job
                    duration = np.random.randint(self.short_lower, self.short_upper + 1)
                else:
                    duration = np.random.randint(self.long_lower, self.long_upper + 1)

                donimant_res = np.random.randint(0, pa.res_num)
                res_vec = []
                for j in xrange(pa.res_num):
                    if j == donimant_res:
                        res_vec.append(np.random.randint(self.dominant_lower, self.dominant_upper + 1))
                    else:
                        res_vec.append(np.random.randint(self.other_lower, self.other_upper + 1))

                self.total_len += duration
                self.job_sequence[k].append(Job(0, duration, pa.res_num, pa.job_max_slot, pa.res_slot, res_vec, i))


        for k in xrange(self.batch_num):
            for i in xrange(pa.job_num):
                if self.job_sequence[k][i].c_len == 0:
                    self.dfs(k, i)
                # print "$$"

        # for k in xrange(self.batch_num):
        #     for i in xrange(pa.job_num):
        #         self.job_sequence[k][i].c_state = np.zeros([pa.dag_max_depth, pa.job_max_len])
        #         self.job_sequence[k][i].c_res_state = np.zeros([pa.res_num, pa.dag_max_depth, pa.job_max_slot])
        #         job = self.job_sequence[k][i]
        #         self.job_sequence[k][i].c_state[job.depth][:job.duration] = 1
        #         for ii in xrange(pa.res_num):
        #             self.job_sequence[k][i].c_res_state[ii][job.depth][:job.res_vec[ii]] = 1
        #         j = job.c_next
        #         while j != -1:
        #             job = self.job_sequence[k][j]
        #             self.job_sequence[k][i].c_state[job.depth][ :job.duration] = 1
        #             for ii in xrange(pa.res_num):
        #                 self.job_sequence[k][i].c_res_state[ii][job.depth][:job.res_vec[ii]] = 1
        #             j = job.c_next


                # self.job_sequence[k].sort(key=lambda x: (- x.depth, - x.c_len, x.id))






    def dfs(self, b_id, j_id):
        ret_depth = -1
        ret_next = -1
        ret_len = 0
        dag_id = self.job_dag_id[b_id]
        for i in xrange(len(self.dag_matrix[dag_id][j_id])):
            if self.dag_matrix[dag_id][j_id][i]:
                if self.job_sequence[b_id][i].c_len == 0:
                    self.dfs(b_id, i)
                if self.job_sequence[b_id][i].depth > ret_depth:
                    ret_depth = self.job_sequence[b_id][i].depth
                if self.job_sequence[b_id][i].c_len > ret_len:
                    ret_len = self.job_sequence[b_id][i].c_len
                    ret_next = i
        self.job_sequence[b_id][j_id].depth, self.job_sequence[b_id][j_id].c_next, self.job_sequence[b_id][j_id].c_len = ret_depth + 1, ret_next, ret_len + self.job_sequence[b_id][j_id].duration
        # return self.job_sequence[b_id][j_id].depth, self.job_sequence[b_id][j_id].c_next, self.job_sequence[b_id][j_id].c_len
