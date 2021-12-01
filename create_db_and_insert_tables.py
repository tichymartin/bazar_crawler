from general import create_database_file, delete_database_file

if __name__ == '__main__':
    try:
        delete_database_file()
    except:
        pass
    create_database_file()
