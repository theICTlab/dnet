import cv2
import os
import numpy as np

# Walk through path and get file names as strings
def get_filenames(path):
    f_names = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        f_names.extend(sorted(file_names))
        break
    return  [ a for a in f_names if not a[-3:]=='txt']

def value_pass(val):
    try:
        float(val)
    except ValueError:
        return False
    return True

def parse_mean(mean):
    mean = mean[1:-1].split(" ")
    mean = [float(num) for num in mean if value_pass(num)]
    return mean
    
def get_mean(path):
    f = open(path+"/mean.txt","r")
    mean = parse_mean(f.read())
    f.close()
    return np.array(mean)

def get_args(path):
    f = open(path+'/settings.txt','r')
    train_arg = f.read()
    f.close()
    train_arg = train_arg.split("\n")[:-1]
    d = {}
    for arg in train_arg:
        n,m = arg.split(":")
        d[n] = m[1:]
        if n == 'mean':
            d[n] = parse_mean(d[n])
    return d
    
# Load images in given directory
def load_imgs(dir_name, start, end, step):
    fnames = get_filenames(dir_name)
    imgs = []
    count = 0
    for imgname in fnames:
        if count not in range(start,end,step):
            continue
        count += 1
        img = load_img(dir_name,imgname)
        imgs.append(img)
    return imgs

    
def load_img(dir_name, imgname):
    fullpath = os.path.join(dir_name, imgname)
    img = cv2.imread(fullpath)
    img = img/255.0
    if len(img.shape) ==2:
        img = np.reshape(img,(img.shape[0],img.shape[1],1))
    return img

def load_data(path, start=0, end=999, step=1):
    """Load images into a list
    #Arguments
        paths: List of strings representing paths to folders containing
            images that must be named as numbers
        start,end,step: Refers to the number of name of images. Only loads
            images with in this range.
    """
    imgs = load_imgs(path,start,end,step)

    return imgs
    