import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from pandas.io.parsers import read_csv
import numpy as np

"""
avgTemp => X
minTemp => X
maxTemp => X 
rainFall => X
avgPrice => Y
"""

class Blood:
    @staticmethod
    def model(raw_data):

        x_data = np.array(raw_data[:, 2:4], dtype=np.float32)
        y_data = np.array(raw_data[:, 4], dtype=np.float32)
        y_data = y_data.reshape(25, 1)

        X = tf.placeholder(tf.float32, shape=[None, 2], name='x-input') # 입력
        Y = tf.placeholder(tf.float32, shape=[None, 1], name='y-input')     # 출력
        W = tf.Variable(tf.random_normal([2, 1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')

        hypothesis = tf.matmul(X, W) + b    #뉴런(가설의 예측값)
        cost = tf.reduce_mean(tf.square(hypothesis - Y))
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.000005)
        train = optimizer.minimize(cost)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        cost_history = []
        for step in range(1000):
            cost_, hypo_, _ = sess.run([cost, hypothesis, train], {X: x_data, Y: y_data})
            if step % 500:
                print(f'step: {step}, cost: {cost_}')
                cost_history.append(sess.run(cost, {X: x_data, Y: y_data}))
        saver = tf.train.Saver()
        saver.save(sess, 'blood.ckpt')

    def initialize(self, weight, age):
        self._weight = weight
        self._age = age

    @staticmethod
    def raw_data():
        tf.set_random_seed(777)     # 777번째의 랜덤 값임
        return np.genfromtxt('blood.txt', skip_header=36)

    def service(self):
        X = tf.placeholder(tf.float32, shape=[None, 2], name='x-input') # 입력
        W = tf.Variable(tf.random_normal([2, 1]), name='weight')
        b = tf.Variable(tf.random_normal([1]), name='bias')
        saver = tf.train.Saver()
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            saver.restore(sess, 'blood/blood.ckpt')
            val = sess.run(tf.matmul(X, W) + b, {X: [[self._weight, self._age]]})
        print(f'혈중지방농도 : {val}')

        print('혈중 지방농도: {}'.format(val))
        if val < 150:
            result = '정상'
        elif 150 <= val < 200:
            result = '경계역 중성지방혈증'
        elif 200<= val < 500:
            result = '고 중성지방혈증'
        elif 500 <= val < 1000:
            result = '초고 중성지방혈증'
        elif 1000 <= val:
            result = '췌장염 발병 가능성 고도화'
        print(result)
        return result

if __name__ == '__main__':
    blood = Blood()
    blood.initialize(100, 30)
    blood.service()
    #raw_data = blood.raw_data()
    #blood.model(raw_data)