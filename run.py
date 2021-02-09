import skimage.io
import numpy
import argparse
from tqdm.auto import tqdm
import os
from FileListExpander import Expander


def get_padded(addr_to_read, addr_to_save, pix_size, color):
    img = skimage.io.imread(addr_to_read)

    pimg = numpy.pad(img, pix_size)[..., pix_size:-pix_size]
    pimg[:pix_size] = color
    pimg[-pix_size:] = color
    pimg[:, :pix_size] = color
    pimg[:, -pix_size:] = color

    skimage.io.imsave(addr_to_save, pimg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Rescale and/or convert to 8bit 3d TIFF volumes')

    parser.add_argument('--input-files', help='Files to process. As list, directory, glob or file containing addresses')
    parser.add_argument('--regexp', default=None, help='RegExp to filter files from --input-files.')
    parser.add_argument('--regexp-mode', default='includes', help='Mode of RegExp interpretation. Possible ones are [includes, matches, not_includes, not_matches]. Default is includes.')

    parser.add_argument('--output-folder', default=None, help='Files to output the result of processing. If folder is provided will be saved with the same name as input files. If nothing provided will replace input files.')

    parser.add_argument('--pixels', default=1, type=int, help='size of border in pixels. Default of 1.')
    parser.add_argument('--value', default='(238, 238, 238, 255)', type=str, help='tuple of colors in RGBA format. Default is (238, 238, 238, 255).')

    args = parser.parse_args()

    fle = Expander(verbosity=True)
    input_files = fle(args.input_files , args.regexp, args.regexp_mode)
    print(input_files, args.input_files)

    for i_f in tqdm(input_files):
        if args.output_folder is not None:
            o_f = os.path.join(args.output_folder, os.path.basename(i_f))
        else:
            o_f = i_f

        get_padded(i_f, o_f, args.pixels, eval(args.value))
