
import socket                   # Import socket module
import tensorflow as tf  ## pip install tensorflow
import numpy as np
import cv2         ## pip install opencv-python
import math
import os
from _thread import *
import threading
from scipy import ndimage
from tensorflow.examples.tutorials.mnist import input_data
#from socket import *

def getBestShift(img):
    cy,cx = ndimage.measurements.center_of_mass(img)

    rows,cols = img.shape
    shiftx = np.round(cols/2.0-cx).astype(int)
    shifty = np.round(rows/2.0-cy).astype(int)

    return shiftx,shifty

def shift(img,sx,sy):
    rows,cols = img.shape
    M = np.float32([[1,0,sx],[0,1,sy]])
    shifted = cv2.warpAffine(img,M,(cols,rows))
    return shifted



def threadit(conn, clientname, addr, sess, x, y, y_):
    with open(clientname+'/received_file', 'wb') as f:
        print ('file opened')
        while True:
            print('receiving data...')
            data = conn.recv(1024)
            #print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')

    # conn.send('Thank you for connecting')
    conn.close()
    

    # create an array where we can store our 4 pictures
    images = np.zeros((1,784))   # (numofpicture,784)
    # and the correct values
    correct_vals = np.zeros((1,10))  # (numofpicture,10)

    # we want to test our images which you saw at the top of this page
    i = 0
    for no in [clientname+'/received_file']:
        print("no is: " + str(no))
        # read the image
        #gray = cv2.imread(str(no)+".png", cv2.CV_LOAD_IMAGE_GRAYSCALE)
        #gray = cv2.imread(str(no)+".PNG", cv2.IMREAD_GRAYSCALE)
        gray = cv2.imread(str(no), cv2.IMREAD_GRAYSCALE)

        # resize the images and invert it (black background)
        gray = cv2.resize(255-gray, (28, 28))
        (thresh, gray) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # remove columns that does not include and input
        while np.sum(gray[0]) == 0:
            gray = gray[1:]

        while np.sum(gray[:,0]) == 0:
            gray = np.delete(gray,0,1)

        while np.sum(gray[-1]) == 0:
            gray = gray[:-1]

        while np.sum(gray[:,-1]) == 0:
            gray = np.delete(gray,-1,1)

        rows,cols = gray.shape


        if rows > cols:
            factor = 20.0/rows
            rows = 20
            cols = int(round(cols*factor))
            gray = cv2.resize(gray, (cols,rows))
        else:
            factor = 20.0/cols
            cols = 20
            rows = int(round(rows*factor))
            gray = cv2.resize(gray, (cols, rows))

        colsPadding = (int(math.ceil((28-cols)/2.0)),int(math.floor((28-cols)/2.0)))
        rowsPadding = (int(math.ceil((28-rows)/2.0)),int(math.floor((28-rows)/2.0)))
        gray = np.lib.pad(gray,(rowsPadding,colsPadding),'constant')
        shiftx,shifty = getBestShift(gray)
        shifted = shift(gray,shiftx,shifty)
        gray = shifted

    	# save the processed images
        cv2.imwrite(str(no)+".png", gray)
        """
        all images in the training set have an range from 0-1
        and not from 0-255 so we divide our flatten images
        (a one dimensional vector with our 784 pixels)
        to use the same 0-1 based range
        """
        flatten = gray.flatten() / 255.0
        """
        we need to store the flatten image and generate
        the correct_vals array
        correct_val for the first digit (9) would be
        [0,0,0,0,0,0,0,0,0,1]
        """
        images[i] = flatten
        correct_val = np.zeros((10))
        correct_val[7] = 1
        correct_vals[i] = correct_val
        i += 1

    """
    the prediction will be an array with four values,
    which show the predicted number
    """
    prediction = tf.argmax(y,1)
    """
    we want to run the prediction and the accuracy function
    using our generated arrays (images and correct_vals)
    """

    a = sess.run(prediction, feed_dict={x: images, y_: correct_vals})
    print(a)

    result = str(a[0]).encode('utf-8')

    s2=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s2.sendto(result,(addr[0],3009))
    s2.close()

def Main():

    # create a MNIST_data folder with the MNIST dataset if necessary
    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    """
    a placeholder for our image data:
    None stands for an unspecified number of images
    784 = 28*28 pixel
    """
    x = tf.placeholder("float", [None, 784])

    # we need our weights for our neural net
    W = tf.Variable(tf.zeros([784,10]))
    # and the biases
    b = tf.Variable(tf.zeros([10]))

    """
    softmax provides a probability based output
    we need to multiply the image values x and the weights
    and add the biases
    (the normal procedure, explained in previous articles)
    """
    y = tf.nn.softmax(tf.matmul(x,W) + b)

    """
    y_ will be filled with the real values
    which we want to train (digits 0-9)
    for an undefined number of images
    """
    y_ = tf.placeholder("float", [None,10])

    """
    we use the cross_entropy function
    which we want to minimize to improve our model
    """
    cross_entropy = -tf.reduce_sum(y_*tf.log(y))

    """
    use a learning rate of 0.01
    to minimize the cross_entropy error
    """
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

    # initialize all variables
    init = tf.initialize_all_variables()

    # create a session
    sess = tf.Session()
    sess.run(init)

    # use 1000 batches with a size of 100 each to train our net
    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        # run the train_step function with the given image values (x) and the real output (y_)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    """
    Let's get the accuracy of our model:
    our model is correct if the index with the highest y value
    is the same as in the real digit vector
    The mean of the correct_prediction gives us the accuracy.
    We need to run the accuracy function
    with our test set (mnist.test)
    We use the keys "images" and "labels" for x and y_
    """
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


    port = 40000                    # Reserve a port for your service.
    s = socket.socket()             # Create a socket object
    #host = socket.gethostbyaddr(socket.gethostname())[2][0]     # Get local machine name
    host = '131.128.49.109'
    print (host)
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.

    print ('Server listening....') 



    while True:
        conn, addr = s.accept()     # Establish connection with client.
        print ('Got connection from %s'  % str(addr))
        clientname = str(addr[0])
        try:
            os.mkdir(clientname)
        except:
            print("path exists")
        
        start_new_thread(threadit, (conn, clientname, addr, sess, x, y, y_))

if __name__ == '__main__':
    Main()
