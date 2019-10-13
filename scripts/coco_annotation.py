import json
import os
def convert_voc_annotation(data_path, data_type, anno_path):
    data =  json.load(open(data_path,'r'))
    data_path = os.path.join('./coco', data_type + '2017')
    with open(anno_path, 'a') as f:
        for img in os.listdir(data_path):
            image = os.path.join(data_path,img)
            annotation = image
            image_id = img[-10:-4]
            for ann in data['annotations']:
                #annotation = os.path.join(data_path,ann['file_name'])
                if ann['image_id'] == int(image_id):
                    x,y,w,h = ann['bbox'][0:4]
                    xmin,ymin,xmax,ymax = str(int(x)),str(int(y)),str(int(x+w)),str(int(y+h))
                    class_ind = ann['category_id']
                    annotation += ' ' + ','.join([xmin, ymin, xmax, ymax, str(class_ind)])
            f.write(annotation + "\n")
    return len(open(anno_path,'r').readlines())  
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/Env/tensorflow-yolov3")
    parser.add_argument("--train_annotation", default="./data/dataset/coco_train.txt")
    parser.add_argument("--test_annotation",  default="./data/dataset/coco_test.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):os.remove(flags.test_annotation)

    num1 = convert_voc_annotation(os.path.join(flags.data_path, 'coco/annotations/instances_train2017.json'),'train',flags.train_annotation)
    num2 = convert_voc_annotation(os.path.join(flags.data_path, 'coco/annotations/instances_val2017.json'),'val',flags.test_annotation)
    print('=> The number of image for train is: %d\tThe number of image for test is:%d' %(num1 , num2))