from re import S
import SimpleITK as sitk
import matplotlib.pyplot as plt
import time
from tqdm.notebook import tqdm
import random
data_path_txt = './../../medical_dataset/ABIDE/all_paths.txt'
data_path = './../../medical_dataset/ABIDE/image_2D/'

f = open(data_path_txt,'r')
lines = f.readlines()
all_data = []
for line in lines:
    name, path_ = line[:-1].split('\t')
    all_data.append([int(name),path_])
f.close()

labels = []
for data in all_data:
    labels.append(data[0])
    
i = 0
atlas = sitk.ReadImage('C:/Users/user/Desktop/abide/ABIDE/50002/MP-RAGE/2000-01-01_00_00_00.0/S164623/ABIDE_50002_MRI_MP-RAGE_br_raw_20120830172854796_S164623_I328631.nii')
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(atlas)
thres=-1
dict_data_count = {}

for data in all_data:
    if i >thres:
        time_1 = time.time()
        read_sitk = sitk.ReadImage(data[1])
        elastixImageFilter.SetMovingImage(read_sitk)
        elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap('translation'))
        elastixImageFilter.Execute()
        read_sitk = elastixImageFilter.GetResultImage()

        img_vol = sitk.GetArrayFromImage(read_sitk)
        if img_vol.shape[0] >=100:
            side = [i+90 for i in range(40)]
            front = [i+100 for i in range(50)]
            cross = [i+90 for i in range(40)]
            random.shuffle(side)
            random.shuffle(front)
            random.shuffle(cross)
            image_2D_path = data_path +str(int(data[0])) +'_' +str(i) +'_'
            if not (data[0] in list(dict_data_count.keys())):
                dict_data_count[data[0]] = 1
                for s in side[:20]:
                    save_path = image_2D_path+ 'side' + str(s) +'.png'
                    plt.imshow(img_vol[:,:,s], cmap='gray')
                    plt.axis('off')
                    # plt.show
                    plt.savefig(save_path, bbox_inches='tight',pad_inches = 0)
                    del save_path
                plt.close('all')
                plt.clf()
                ##################
                for f in front[:20]:
                    save_path = image_2D_path+ 'front' + str(f) +'.png'
                    plt.imshow(img_vol[:,f], cmap='gray')
                    plt.axis('off')
                    # plt.show
                    plt.savefig(save_path, bbox_inches='tight',pad_inches = 0)
                    del save_path
                plt.close('all')
                plt.clf()
                ############################
                for c in cross[:20]:
                    save_path = image_2D_path+ 'cross' + str(c) +'.png'
                    plt.imshow(img_vol[50], cmap='gray')
                    plt.axis('off')
                    # plt.show
                    plt.savefig(save_path, bbox_inches='tight',pad_inches = 0)
                    del save_path
                plt.close('all')
                plt.clf()
                
                del read_sitk
                del img_vol
                del image_2D_path
    i+=1