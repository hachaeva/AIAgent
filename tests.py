from functions.get_files_info import get_files_info

if __name__ == "__main__":
    print (f"{get_files_info("calculator",".")}")
    print (f"{get_files_info("calculator","pkg")}")
    print (f"{get_files_info("calculator","/bin")}")
    print (f"{get_files_info("calculator","../")}")