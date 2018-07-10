import numpy as np
import random, time
import tensorflow as tf
import matplotlib.pyplot as plt
from bird import YuanYangEnv

env = YuanYangEnv()
tf.reset_default_graph()
input1 = tf.placeholder(shape=[1,100], dtype=tf.float32)
W = tf.Variable(tf.random_uniform([100, 4], 0, 0.01))
Qout = tf.matmul(input1, W)
ma = tf.argmax(Qout, 1)
Qlearning = tf.placeholder(shape=[1, 4], dtype=tf.float32)
loss = tf.reduce_sum(tf.square(Qlearning - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updatevalue = trainer.minimize(loss)
init = tf.global_variables_initializer()
gamma = 0.99
e = 0.1
num_step = 2000
rlist = []
with tf.Session() as sess:
    sess.run(init)
    for i in range(num_step):
        s = env.reset()
        rall = 0
        t = False
        j = 0
        while j < 99:
            j += 1
            dex, allq = sess.run([ma, Qout], feed_dict={input1: np.identity(100)[s:s+1]})
            if np.random.rand(1) < e:
                dex[0] = int(random.random() * len(env.actions))
            s_next, r, d = env.transform(s,env.actions[dex[0]])
            allq1 = sess.run(Qout, feed_dict={input1: np.identity(100)[s_next:s_next+1]})
            maxq1 = np.max(allq1)
            targetQ = allq
            targetQ[0, dex[0]] = r + gamma * maxq1
            _, W1 = sess.run([updatevalue, W], feed_dict={input1: np.identity(100)[s:s+1], Qlearning: targetQ})
            rall += r
            s = s_next
            if d == True:
                e = 1. / ((i / 50) + 10)
                break

        rlist.append(rall)

    plt.plot(rlist)
    plt.show()

    for i in range(10):
        s = env.reset()
        env.render()
        d = False
        print(i)
        while d == False:
            a = sess.run(ma, feed_dict={input1: np.identity(100)[s:s+1]})
            env.bird_male_position = env.state_to_position(s)
            env.render()
            time.sleep(1)
            s_next, r, d = env.transform(s, env.actions[a[0]])
            print(s, a, s_next)
            s = s_next

