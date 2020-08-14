import time
import random
import filter_ex
import create_dataset

def generate_files_in_range(folder_path, number_files, range_start_size, range_end_size, size_unit, extension=None):
    """Function to generate files in range
    :argument
        folder_path: Path of folder, where files would be generated
        number_files: Number of files to generate
        range_start_size: Start range of size e.g. 1
        range_end_size: End range of size e.g. 10
        size_unit: Unit size of file to generate e.g. KB/MB/GB, if not given files of all sizes would be generated
        extension: Extension of files, if not given default extensions would be used
    :returns: List of file path
    """
    list_files = []
    if not extension:
        extension = filter_ex.EXTENSION_ALL
    else:
        if not isinstance(extension, list):
            extension = [extension]
    if not size_unit:
        size_unit = ["B", "KB", "MB", "GB"]
    else:
        if not isinstance(size_unit, list):
            size_unit = [size_unit]
    for count in range(1, number_files + 1):
        if range_start_size != range_end_size:
            random_size = random.randrange(range_start_size, range_end_size)
        else:
            random_size = range_start_size
        file_type = random.choice(extension)
        print(f"File type {file_type}, type is {type(extension)}")
        print(f"Random file size {random_size}")
        random_size_unit = random.choice(size_unit)
        print(f"Random size unit {random_size_unit}")
        file_name_create = f"{count}_{random_size}_{random_size_unit}_file_{create_dataset.random_generator()}{file_type}"
        file_name_create_path = f"{folder_path}/{file_name_create}"
        print("File path to create {}...".format(file_name_create_path))
        list_files.append((f"{file_name_create_path}", f"{random_size} {random_size_unit.upper()}"))
    return list_files

if __name__=="__main__":
    list_created_file = generate_files_in_range(folder_path="D:\\auto_UNXYQY_folder\\depth_1_Ffapccq9bKF",
                                                number_files=100, range_start_size=1,
                                                range_end_size=100, size_unit=["B", "KB", "MB"])
    tic = time.perf_counter()
    create_dataset.launch_threads(create_dataset.create_new_file_with_size, list_created_file)
    toc = time.perf_counter()
    print (f"Elapsed time {toc-tic:0.4f} seconds")