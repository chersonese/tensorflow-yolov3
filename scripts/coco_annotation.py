from pycocotools.coco import COCO
import os
import argparse

def read_class_ids(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[name.strip('\n')] = ID
    return names


def convert_coco_annotation(data_path,data_type,anno_path):
    names = read_class_ids('./data/classes/coco.names')
    print(names)
    coco = COCO(data_path)
    imgIds = coco.getImgIds()
    with open(anno_path,'a') as f:
        for imgId in imgIds:
            img_name = '000000' + str(imgId) + '.jpg'
            image = os.path.join('./coco/' + data_type +'2017', img_name)
            if os.path.exists(image):
                annIds = coco.getAnnIds(imgIds = imgId)
                anns = coco.loadAnns(annIds)
                if(len(anns)>0):
                    for ann in anns:
                        x,y,w,h = ann['bbox'][:]
                        xmin,ymin,xmax,ymax = str(int(x)),str(int(y)),str(int(x+w)),str(int(y+h))
                        cat_id = names[coco.loadCats(ids=ann['category_id'])[0]['name']]
                        image += ' ' + ','.join([xmin, ymin, xmax, ymax, str(cat_id)])
            print(image)            
            f.write(image + '\n')
    return len(open(anno_path,'r').readlines())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/Env/tensorflow-yolov3")
    parser.add_argument("--train_annotation", default="./data/dataset/coco_train.txt")
    parser.add_argument("--test_annotation",  default="./data/dataset/coco_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1 = convert_coco_annotation(os.path.join(flags.data_path, 'coco/annotations/instances_train2017.json'),'train',flags.train_annotation)
    num2 = convert_coco_annotation(os.path.join(flags.data_path, 'coco/annotations/instances_val2017.json'),'val',flags.test_annotation)
    print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1 , num2))
