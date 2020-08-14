"""
Script to generate dataset based on given input.
"""
import os
import sys
import string
import time
import random
import math
import concurrent.futures
import filter_ex

def get_random_unicode(no_of_char):
    """
    This function will return unicode name with length no_of_chars
    :no_of_chars : length of unicode string
    :return : unicode string
    """
    get_char = chr
    include_ranges = [(0x0900, 0x097F)]
    alphabet = [get_char(code_point) for current_range in include_ranges for code_point in
                range(current_range[0], current_range[1] + 1)]
    return ''.join(random.choice(alphabet) for i in range(1, no_of_char))

def get_folder_name(no_of_char=20):
    letters = string.ascii_letters + string.digits
    folder_len = random.choice(range(2, no_of_char))    
    if "win" in sys.platform:
        unicode_letters = get_random_unicode(10)        
        mixed_letters = letters + unicode_letters
    normal_folder_name = ''.join(random.choice(letters) for j in range(1, folder_len))
    if "win" in sys.platform:
        unicode_folder_name = ''.join(random.choice(unicode_letters) for j in range(1, folder_len))
        mixed_folder_name = ''.join(random.choice(mixed_letters) for j in range(1, folder_len))
        folder_name_list = [normal_folder_name, unicode_folder_name, mixed_folder_name]
    else:
        folder_name_list = [normal_folder_name]
    folder_file_name = random.choice(folder_name_list)
    return folder_file_name

def launch_threads(target_function, list_arguments, ignore_failure=False, max_workers=10):
    """
    Function to launch multiple threads for target function with different arguments
    :param target_function: Function which would be launched in thread pool with different arguments
    :param list_arguments: List of arguments to pass in target function.
                            e.g. [('arg1', 'arg2', 'arg3'), ('arg4', 'arg5', 'arg6')]
    :param ignore_failure: If set to false exception won't be raised if any of the thread fails
    :param max_workers: Max number of threads to start
    :return: List of results for each thread
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        result_futures = {executor.submit(target_function, *args): args for args in list_arguments}
        for future in concurrent.futures.as_completed(result_futures):
            arguments = result_futures[future]
            # Below code block is to handle exception in any thread, if exception execution wont stop for other threads
            try:
                results.append(future.result())
            except Exception as exc:
                error_message = f"Target function {target_function} got exception with arguments {arguments}.." \
                                f"Failed due to {exc}"
                print(error_message)
                print (error_message)
                if not ignore_failure:
                    raise Exception(error_message)
            else:                
                print(f"All thread execution completed for function {target_function}")
    return results

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Function to generate random variable
    :param size: Length of random characters
    :param chars: Combinations in random string
    :return: Random variable
    """
    return ''.join(random.choice(chars) for x in range(size))

def create_file_folder_list(path, depth, number_of_folders, number_of_files, max_file_size="1 GB", list_path=[]):
    """
    Function to create file folder list base on given input
    Arguments:
    =========
       path: Path Where data set would be generated
       depth: Depth count till which file folder would be created
       number_of_folders: Number of folders in each depth
       number_of_files: Number of files in each depth
       max_file_size: Max file size in dataset (e.g. if 1 GB is given, 1 gb file would be created in first depth only)
       list_path: This is for internal purpose to save the state during recursion
    Returns:
    ========
        Returns list_path, having tuples (file_path, size)
    """
    size_unit = ["B", "KB", "MB", "GB"]    
    split_max_file_size_unit = max_file_size.split(" ")
    max_file_size_num = split_max_file_size_unit[0]
    max_file_size_unit = split_max_file_size_unit[1]
    size_unit = size_unit[:size_unit.index(max_file_size_unit)]    
    if depth<=0:        
        return list_path        
    else:
        if not isinstance(path, list):            
            depth_count = len(path.split(os.path.sep) )            
            folder_path = os.path.join(path, f"auto_{random_generator()}_folder")                       
            path = [folder_path]        
        folder_path = []        
        for i in path:            
            for p in range(number_of_folders):
                depth_count = len(i.split(os.path.sep))                
                folder_path_temp = os.path.join(i, f"depth_{depth_count}_{get_folder_name()}")
                folder_path.append(folder_path_temp)                
                for index, nof in enumerate(range(number_of_files)):
                    file_type = random.choice(filter_ex.EXTENSION_ALL)
                    file_path_temp = os.path.join(folder_path_temp, f"{nof+1}_{get_folder_name()}{file_type}")                                        
                    if not list_path and index<=0:
                        list_path.append((file_path_temp, f"{random.randrange(1, int(max_file_size_num)+1)} {max_file_size_unit}"))
                    else:
                        list_path.append((file_path_temp, f"{random.randrange(1, 200)} {random.choice(size_unit)}"))                                    
        return create_file_folder_list(folder_path, depth-1, number_of_folders, number_of_files, max_file_size, list_path)

def create_folders_file(file_path, size):
    """Function to create folders and file"""
    print(f"Creating path {file_path}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    create_new_file_with_size(file_path, size)


def write_to_file(file_path, size_in_byte):
    """
    Function to write random data to file in chunks
    :param file_path: Path of file to write
    :param size_in_byte: File size in byte
    :return: None
    """
    chunk_size = 1024
    chunks = math.ceil(size_in_byte / chunk_size)
    with open(file_path, "wb") as fh:
        for data in range(chunks):
            data_random = os.urandom(int(size_in_byte / chunks))
            fh.write(data_random)
        data_random = os.urandom(int(size_in_byte % chunks))
        fh.write(data_random)
    print(f"Successfully created file {file_path} of size {size_in_byte}")

def _map_size_to_bytes(size):
    """
    :param size: size e.g. "1 MB"
    :return: size evaluated to bytes
    """
    size_units = {
        "B": "* 1",
        "KB": "* 1024",
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

def create_new_file_with_size(file_path, size):
    """
    Creates file at path given with given size
    :param path: Path of file
    :param size: e.g. 1MB
    :return:
    """
    size = _map_size_to_bytes(size)    
    if not os.path.isfile(file_path):
        try:
            write_to_file(file_path=file_path, size_in_byte=size)
        except Exception as e:
            raise Exception("Could not write to file path {}, error is {}".format(file_path, e))
    else:
        print("File already exists")
    return file_path

if __name__=="__main__":    
    list_path = create_file_folder_list(path="D:/", depth=5, number_of_folders=1, number_of_files=10, max_file_size="1 GB") 
    tic = time.perf_counter()
    launch_threads(create_folders_file, list_path)
    toc = time.perf_counter()
    print (f"Elapsed time {toc-tic:0.4f} seconds")