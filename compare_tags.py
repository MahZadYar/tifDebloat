import tifffile
orig=r'd:/OneDrive - Kaunas University of Technology/~Personal Projects/TIFF_comp/sample/A1_005.tif'
new=r'd:/OneDrive - Kaunas University of Technology/~Personal Projects/TIFF_comp/sample/A1_005_gray_compressed.tif'
print('Original tags:')
with tifffile.TiffFile(orig) as t:
    for tag in t.pages[0].tags.values():
        print(tag.code, tag.name, type(tag.value))
print('\nNew tags:')
with tifffile.TiffFile(new) as t:
    for tag in t.pages[0].tags.values():
        print(tag.code, tag.name, type(tag.value))
