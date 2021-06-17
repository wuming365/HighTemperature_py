from osgeo import gdal
import shapefile
import CONSTANT


def openSingleImage(imagefilename):
    """
    打开遥感影像
    """
    dataset = gdal.Open(imagefilename)
    im_width = dataset.RasterXSize  # 列数
    im_height = dataset.RasterYSize  # 行数
    # im_bands = dataset.RasterCount  # 波段数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_band = dataset.GetRasterBand(1)
    Image = im_band.ReadAsArray(0, 0, im_width, im_height)
    del dataset
    # 关闭图像进程
    return np.double(Image), im_geotrans, im_proj


def clipTiff(path_inputraster, path_outputraster, path_clipshp, NDV):
    """
    裁剪影像
    path_inputraster:str
    path_outputraster:str
    path_clipshp:str
    """
    input_raster = gdal.Open(path_inputraster)
    mkdir(os.path.dirname(path_outputraster))
    # 两个投影一样
    r = shapefile.Reader(path_clipshp)
    ds = gdal.Warp(path_outputraster,
                   input_raster,
                   format='GTiff',
                   outputBounds=r.bbox,
                   cutlineDSName=path_clipshp,
                   dstNodata=NDV)
    ds = None