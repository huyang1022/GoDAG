from environment import Environment
from parameter import Parameter
from mac_generator import MacGenerator
from job_generator import JobGenerator
from genjob import  JobGenerator1
import act_generator
import tensorflow as tf
import numpy as np
from actor_critic import Actor, Critic
import os
# import plot
import multiprocessing as mp
import time

LOG_DIR = "./log"
LOG_FILE = LOG_DIR + "/rl_log"
MODEL_DIR = "./model"

def master(pa, net_queues, exp_queues):
    sess = tf.Session()
    actor = Actor(sess, pa)
    critic = Critic(sess, pa)
    sess.run(tf.global_variables_initializer())
    s_time = time.time()

    # writer = tf.summary.FileWriter(LOG_DIR, sess.graph)
    saver = tf.train.Saver()
    logger = open(LOG_FILE, "w")  # file to record the logs
    train_avg_data, train_min_data, train_max_data = [], [], []
    test_avg_data, test_min_data, test_max_data = [], [], []

    for i in xrange(pa.exp_epochs):
        print "================", "Start EP", i, "================"
        ep_train_w, ep_test_w = [], []
        ep_td, ep_c_loss, ep_a_loss, ep_a_entropy = [], [], [], []
        for j in xrange(pa.batch_num / pa.worker_num):
            ep_s, ep_a, ep_v= [], [], []
            a_parameters = actor.get_parameters()
            c_parameters = critic.get_parameters()

            for k in xrange(pa.worker_num):
                train_id = j * pa.worker_num + k
                test_id = train_id + pa.batch_num
                net_queues[k].put([train_id, a_parameters, c_parameters])
                if pa.test_flag:
                    net_queues[k + pa.worker_num].put([test_id, a_parameters, c_parameters])

            for k in xrange(pa.worker_num):
                buffer_s, buffer_a, buffer_v, butter_w = exp_queues[k].get()
                ep_s.append(buffer_s)
                ep_a.append(buffer_a)
                ep_v.append(buffer_v)
                ep_train_w.append(butter_w)

                if pa.test_flag:
                    butter_test_w = exp_queues[k + pa.worker_num].get()
                    ep_test_w.append(butter_test_w)

            # ep_a_gradients, ep_c_gradients =[], []
            for k in xrange(pa.worker_num):
                td_error, c_loss = critic.learn(ep_s[k], ep_v[k])
                # td_error, c_loss, c_gradients = critic.get_gradients(ep_s[j], ep_v[j])
                if i < pa.su_epochs:
                    a_entropy, a_loss = actor.s_learn(ep_s[k], ep_a[k])
                    # a_entropy, a_loss, a_gradients = actor.get_s_gradients(ep_s[j], ep_a[j])
                else:
                    a_entropy, a_loss = actor.learn(ep_s[k], ep_a[k], td_error)
                    # a_entropy, a_loss, a_gradients = actor.get_gradients(ep_s[j], ep_a[j], td_error)
                # ep_a_gradients.append(a_gradients)
                # ep_c_gradients.append(c_gradients)
                ep_td.append(td_error)
                ep_c_loss.append(c_loss)
                ep_a_loss.append(a_loss)
                ep_a_entropy.append(a_entropy)

        # for j in xrange(pa.batch_num):
        #     actor.update_parameters(ep_a_gradients[j])
        #     critic.update_parameters(ep_c_gradients[j])
        print "================", "Train EP", i, "================"
        ep_td = np.concatenate(ep_td)
        ep_c_loss = np.array(ep_c_loss)
        ep_a_loss = np.array(ep_a_loss)
        ep_a_entropy = np.array(ep_a_entropy)

        train_avg_data.append(float(np.mean(ep_train_w)))
        train_min_data.append(np.min(ep_train_w))
        train_max_data.append(np.max(ep_train_w))
        if pa.test_flag:
            test_avg_data.append(float(np.mean(ep_test_w)))
            test_min_data.append(np.min(ep_test_w))
            test_max_data.append(np.max(ep_test_w))
        else:
            test_avg_data.append(0.0)
            test_min_data.append(0.0)
            test_max_data.append(0.0)


        print \
            "EP:", i, "\n", \
            "Batch Number:", pa.batch_num, "\n", \
            "EP_avg_c_loss: ", np.mean(ep_c_loss), "\n", \
            "EP_avg_a_loss: ", np.mean(ep_a_loss), "\n", \
            "EP_avg_a_entropy: ", np.mean(ep_a_entropy), "\n", \
            "EP_avg_td_error: ", np.mean(ep_td), "\n", \
            "EP_train_time: ", time.time() - s_time, "\n", \
            "EP_train_makespan: ", train_avg_data[-1], train_min_data[-1], train_max_data[-1], "\n", \
            "EP_test_makespan: ", test_avg_data[-1], test_min_data[-1], test_max_data[-1], "\n"

        logger.write("EP: %d\n" % i)
        logger.write("Batch Number: %d\n" % pa.batch_num)
        logger.write("EP_avg_c_loss: %f\n" % np.mean(ep_c_loss))
        logger.write("EP_avg_a_loss: %f\n" % np.mean(ep_a_loss))
        logger.write("EP_avg_a_entropy: %f\n" % np.mean(ep_a_entropy))
        logger.write("EP_avg_td_error: %f\n" % (np.mean(ep_td)))
        logger.write("EP_train_time: %f\n" % (time.time() - s_time))
        logger.write("EP_train_makespan: %f %f %f\n" % (train_avg_data[-1], train_min_data[-1], train_max_data[-1]))
        logger.write("EP_test_makespan: %f %f %f\n\n" % (test_avg_data[-1], test_min_data[-1], test_max_data[-1]))
        logger.flush()

        if (i + 1) % pa.save_step == 0:
            saver.save(sess, "%s/%d.ckpt" % (MODEL_DIR, (i + 1)))
    # plot.run()


def worker(pa, net_queue, exp_queue):
    sess = tf.Session()
    actor = Actor(sess, pa)
    critic = Critic(sess, pa)

    env = Environment(pa)
    mac_gen = MacGenerator(pa)
    job_gen = JobGenerator(pa)
    env.job_gen = job_gen
    env.mac_gen = mac_gen


    for i in xrange(pa.exp_epochs):
        for j in xrange(pa.batch_num / pa.worker_num):
            batch_id, a_parameters, c_parameters = net_queue.get()
            actor.set_parameters(a_parameters)
            critic.set_parameters(c_parameters)
            env.reset()
            env.add_cluster()
            env.batch_id = batch_id
            buffer_s, buffer_a, buffer_r, buffer_v = [], [], [], []
            while True:
                if env.check_done() or env.current_time >= pa.exp_len:
                    value = (pa.job_num * 10.0 / env.current_time) ** 2
                    for r in buffer_r[::-1]:
                        value = pa.discount_rate * value
                        buffer_v.append(value)
                        # value += 1

                    buffer_v.reverse()
                    buffer_s, buffer_a, buffer_v = np.vstack(buffer_s), np.vstack(buffer_a), np.vstack(buffer_v)
                    exp_queue.put([buffer_s, buffer_a, buffer_v, env.current_time])
                    break
                elif env.check_learning():
                    state = env.obs()
                    if i < pa.su_epochs:
                        act_id = act_generator.get_id(env, i)
                    else:
                        act_id = actor.predict(state[np.newaxis, :])
                    state_, reward, done = env.step_act(act_id)
                    buffer_s.append(state)
                    buffer_a.append(act_id)
                    buffer_r.append(reward)
                else:
                    env.step()


def tester(pa, net_queue, exp_queue):
    sess = tf.Session()
    actor = Actor(sess, pa)
    critic = Critic(sess, pa)

    env = Environment(pa)
    mac_gen = MacGenerator(pa)
    job_gen = JobGenerator(pa)
    env.job_gen = job_gen
    env.mac_gen = mac_gen
    for i in xrange(pa.exp_epochs):
        for j in xrange(pa.batch_num / pa.worker_num):
            batch_id, a_parameters, c_parameters = net_queue.get()
            actor.set_parameters(a_parameters)
            critic.set_parameters(c_parameters)
            env.reset()
            env.add_cluster()
            env.batch_id = batch_id
            while True:
                if env.check_done() or env.current_time >= pa.exp_len:
                    exp_queue.put(env.current_time)
                    break
                elif env.check_learning():
                    state = env.obs()
                    if i < pa.su_epochs:
                        act_id = act_generator.get_id(env, i)
                    else:
                        act_id = actor.predict(state[np.newaxis, :])
                    env.step_act(act_id)
                else:
                    env.step()

def gogo(Tnum, Tlist,j):
    pa = Parameter()
    env = Environment(pa)
    mac_gen = MacGenerator(pa)
    env.mac_gen = mac_gen
    f = open("./log/%d" % j, "w")
    for i in xrange(Tnum):
        job_gen = JobGenerator1(pa, i * 6)
        env.job_gen = job_gen
        env.reset()
        env.add_cluster()
        env.batch_id = 0
        st = time.time()
        while True:
            if env.check_done() or env.current_time >= pa.exp_len:
                break
            elif env.check_learning():
                act_id = act_generator.get_id(env, j)
                env.step_act(act_id)
            else:
                env.step()
        Tlist.append(env.current_time)
        f.write("%d\n" % env.current_time)
        print j, i, time.time() - st, env.current_time
    print np.average(Tlist)
    f.close()

def main():
    if not os.path.exists(MODEL_DIR):
        os.mkdir(MODEL_DIR)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    pa = Parameter()
    env = Environment(pa)
    mac_gen = MacGenerator(pa)

    env.mac_gen = mac_gen
    Tnum = 20
    Tduration = 0
    Tlist = list()
    workers = []

    gogo(Tnum, Tlist, 4)


    # for j in xrange(5):
    #     Tlist.append([])
    #     workers.append(mp.Process(target=gogo,
    #                               args=(Tnum,Tlist[j],j)))
    #
    # for j in xrange(5):
    #     workers[j].start()
    # for j in xrange(5):
    #     workers[j].join()
    #
    # for j in xrange(5):
    #     print np.average(Tlist[j])
if __name__ == '__main__':
    main()
