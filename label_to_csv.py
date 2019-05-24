"""
Usage:
# Create train data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/train -o [PATH_TO_ANNOTATIONS_FOLDER]/train_labels.csv

# Create test data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/test -o [PATH_TO_ANNOTATIONS_FOLDER]/test_labels.csv
"""

import os
import glob
import pandas as pd
import argparse
from PIL import Image


def label_to_csv(path, name):
    """Iterates through all .xml files (generated by labelImg) in a given directory and combines them in a single Pandas datagrame.

    Parameters:
    ----------
    path : {str}
        The path containing the .xml files
    Returns
    -------
    Pandas DataFrame
        The produced dataframe
    """

    csv_list = []
    for image_file in glob.glob(path + '/*.jpg'):
        # print(image_file)
        im = Image.open(image_file)
        width, height = im.size
        label_fd = open(os.path.join(path, 'Label', image_file.split('/')[-1].replace('.jpg', '.txt')))
        data = label_fd.readline().rstrip().lstrip(image_file.split('/')[-2]).lstrip(' ').split(' ')
        value = image_file.split('/')[-1], width, height,'plate', round(float(data[0])), round(float(data[1])), round(float(data[2])), round(float(data[3]))
        # break

    #     tree = ET.parse(image_file)
    #     root = tree.getroot()
    #     for member in root.findall('object'):
    #         value = (root.find('filename').text,
    #                 int(root.find('size')[0].text),
    #                 int(root.find('size')[1].text),
    #                 member[0].text,
    #                 int(member[4][0].text),
    #                 int(member[4][1].text),
    #                 int(member[4][2].text),
    #                 int(member[4][3].text)
    #                 )
        csv_list.append(value)
    column_name = ['filename', 'width', 'height',
                name, 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(csv_list, columns=column_name)
    return xml_df


def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter")
    parser.add_argument("-i",
                        "--inputDir",
                        help="Path to the folder where the input .jpg files are stored. It should contains Labels folder",
                        type=str)
    parser.add_argument("-o",
                        "--outputFile",
                        help="Name of output .csv file (including path)", type=str)
    parser.add_argument("-c",
                        "--className",
                        help="Name of the class", type=str)
    args = parser.parse_args()

    if(args.inputDir is None):
        args.inputDir = os.getcwd()
    if(args.outputFile is None):
        args.outputFile = args.inputDir + "/labels.csv"
    if(args.className is None):
        # raise("Class name is mandatory, use --help for usage")
        args.className = "className"

    assert(os.path.isdir(args.inputDir))

    xml_df = label_to_csv(args.inputDir,args.className)
    xml_df.to_csv(
        args.outputFile, index=None)
    print('Successfully converted txt to csv.')


if __name__ == '__main__':
    main()