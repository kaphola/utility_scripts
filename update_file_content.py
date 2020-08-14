import os
import time
import filter_ex
import random
import math

##  This function is used to handle size with any unit (In automation we usually give size as user friendly 1 B, 1 MB)
def _map_size_to_bytes(size):
    """
    :param size: size e.g. "1 MB"
    :return: size evaluated to bytes
    """
    size_units = {
        "B": "* 1",
        "KB": "* 1024",
        "K": "* 1024",
        "MB": "* 1024 * 1024",
        "GB": "* 1024 *1024 * 1024"
    }
    size_split = str(size).split(" ")
    if len(size_split) > 1:
        size = size_split[0]
        unit = size_split[1:][0]
        size_eval = str(int(size)) + str(size_units[unit])
    else:
        size_eval = str(int(size) * 1024 * 1024)
    size = eval(size_eval)
    return size

def write_to_file(file_path, size_in_byte, file_object):
    """
    Function to write random data to file in chunks
    :param file_path: Path of file to write
    :param size_in_byte: File size in byte
    :return: None
    """
    chunk_size = 1024
    chunks = math.ceil(size_in_byte / chunk_size)
    for data in range(chunks):
        data_random = os.urandom(chunk_size) 
        file_object.write(data_random)
    data_random = os.urandom(int(size_in_byte % chunks))
    file_object.write(data_random)
    print(f"Successfully write done to file {file_path} of size {size_in_byte}")


def update_file_content(file_path, data_change_location, data_change_size="offset_boundary"):
    """
    data_change_size: 1 B, more than one block size, less than one block size, overlaps block boundry, Whole file
    """
    ## This list is to handle data_change_size, if Other than this size is given would be expected as with unit e.g. 1 B, 1 MB, 1 GB
    list_data_change_size = ["offset_boundary", "overlaps_block_boundary", "whole_file"]
    file_size = os.path.getsize(file_path)
    print (f"File size of {file_path} is {file_size}")
    extension = os.path.splitext(file_path)[1]
    print (f"Extension is {extension}")
    print ("get block size based on extension")
    block_size = "64 K" if extension in filter_ex.EXTENSION_SIXTY_FOUR_K_BLOCK + filter_ex.EXTENSION_ZERO_COMPRESSION_SIXTY_FOUR_K_BLOCK else "4 MB"
    print (f"Block size {block_size}")
    ################################################
    ## Calculation to get file/block size to write
    ## Block size would be decided to write
    ################################################
    if data_change_size not in list_data_change_size:
        block_size_bytes = _map_size_to_bytes(data_change_size)
    else:
        block_size_bytes = _map_size_to_bytes(block_size)
    print (f"Bolck size in bytes {block_size_bytes}")
    ################################################
    ## Code to get number of blocks in file
    ################################################
    total_number_of_blocks = int(file_size/block_size_bytes)
    print (f"Number of blocks {total_number_of_blocks}")
   
    ################################################
    ## Calculation to get block_number_to_overwrite based on
    ## data_change_location
    ################################################
    if data_change_location=="start":
        block_number_to_overwrite = 0
    elif data_change_location=="middle":
        block_number_to_overwrite = int(total_number_of_blocks/2)
    elif data_change_location=="random":
        block_number_to_overwrite = random.choice(range(1, total_number_of_blocks))
    elif data_change_location=="end":
        block_number_to_overwrite = total_number_of_blocks - 1 
    
    if data_change_location=="append":
        with open(file_path, "ab") as obj_file:
            write_to_file(file_path, block_size_bytes, obj_file)
    else:
        ################################################
        ## Calculation to get offset based on
        ## data_change_size
        ################################################
        if data_change_size=="offset_boundary":
            offset = block_number_to_overwrite * block_size_bytes
        elif data_change_size=="overlaps_block_boundary":
            offset = (block_number_to_overwrite * block_size_bytes) + random.choice(range(1, block_size_bytes))        
        elif data_change_size=="whole_file":
            offset=0
            block_size_bytes = file_size
        print (f"offset to move {offset}")
        with open(file_path, "rb+") as obj_file:        
            obj_file.seek(offset)
            where_am_i = obj_file.tell()
            print (f"Where is pointer {where_am_i}")
            write_to_file(file_path, block_size_bytes, obj_file)
    file_size = os.path.getsize(file_path)
    print (f"File size of {file_path} is {file_size} after update")

if __name__=="__main__":
    tic = time.perf_counter()    
    update_file_content(file_path="D:\\auto_UNXYQY_folder\\depth_1_Ffapccq9bKF\\6_dqUNRO.exe",
                        data_change_location="start", data_change_size="offset_boundary")
    toc = time.perf_counter()
    print (f"Elapsed time {toc-tic:0.4f} seconds")
    
