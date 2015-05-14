#!/usr/bin/env python
import sct_utils as sct
import sys
from msct_parser import Parser
from msct_gmseg_utils import leave_one_out_by_slice
import os

if __name__ == '__main__':
    parser = Parser(__file__)
    parser.usage.set_description('Gray matter segmentation with several types of registration')
    parser.add_option(name="-i",
                      type_value="file",
                      description="T2star image you want to segment "
                                  "if no input image is specified, leave one out cross validation",
                      mandatory=False,
                      example='t2star.nii.gz')
    parser.add_option(name="-dic",
                      type_value="folder",
                      description="Path to the dictionary of images",
                      mandatory=True,
                      example='/home/jdoe/data/dictionary')
    parser.add_option(name="-target-reg",
                      type_value='multiple_choice',
                      description="type of registration of the target to the model space "
                                  "(if pairwise, the registration applied to the target are the same as"
                                  " those of the -reg flag)",
                      mandatory=False,
                      default_value='pairwise',
                      example=['pairwise', 'groupwise'])

    arguments = parser.parse(sys.argv[1:])
    target_fname = None
    target_reg = 'pairwise'
    cmd_gmseg = ''
    if "-i" in arguments:
        target_fname = arguments["-i"]
    if "-target-reg" in arguments:
        target_reg = arguments["-target-reg"]
    path_dictionary = arguments["-dic"]

    # transformations_to_try = ['Rigid', 'Affine', 'SyN', 'Rigid,Affine']
    transformations_to_try = ['Affine', 'Rigid,Affine']

    if target_fname is not None:
        cmd_gmseg = 'sct_asman -i ' + target_fname + ' -dic ' + path_dictionary + ' -model compute -target-reg ' + target_reg

    for transformation in transformations_to_try:
        if target_fname is not None:
            cmd_gmseg += ' -reg ' + transformation
            sct.run(cmd_gmseg)
        else:
            sct.run('mkdir ./' + transformation + '_gm_with_levels')
            sct.run('cp -r ' + path_dictionary + ' ./' + transformation + '_gm_with_levels' + '/dictionary')
            os.chdir('./' + transformation + '_gm_with_levels')
            leave_one_out_by_slice('dictionary/', reg=transformation, target_reg=target_reg, use_levels=True, seg_type='gm')
            os.chdir('..')

            sct.run('mkdir ./' + transformation + '_gm_without_levels')
            sct.run('cp -r ' + path_dictionary + ' ./' + transformation + '_gm_without_levels' + '/dictionary')
            os.chdir('./' + transformation + '_gm_without_levels')
            leave_one_out_by_slice('dictionary/', reg=transformation, target_reg=target_reg, use_levels=False, seg_type='gm')
            os.chdir('..')

            sct.run('mkdir ./' + transformation + '_wm_with_levels')
            sct.run('cp -r ' + path_dictionary + ' ./' + transformation + '_wm_with_levels' + '/dictionary')
            os.chdir('./' + transformation + '_wm_with_levels')
            leave_one_out_by_slice('dictionary/', reg=transformation, target_reg=target_reg, use_levels=True, seg_type='wm')
            os.chdir('..')

            sct.run('mkdir ./' + transformation + '_wm_without_levels')
            sct.run('cp -r ' + path_dictionary + ' ./' + transformation + '_wm_without_levels' + '/dictionary')
            os.chdir('./' + transformation + '_wm_without_levels')
            leave_one_out_by_slice('dictionary/', reg=transformation, target_reg=target_reg, use_levels=False, seg_type='wm')
            os.chdir('..')