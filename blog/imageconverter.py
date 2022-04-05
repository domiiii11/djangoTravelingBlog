import psycopg2



def get_binary_array(path):
    with open(path, "rb") as image:
        f = image.read()
        b = bytes(f).hex()
        return b

def send_files_to_postgresql(connection, cursor, file_names):
    query = "INSERT INTO table(image) VALUES (decode(%s, 'hex'))"
    mylist = []
    for file_name in file_names:
        mylist.append(get_binary_array(file_name))
 
    try:
        cursor.executemany(query, mylist)
       
        connection.commit()  # commit the changes to the database is advised for big files, see documentation
        count = cursor.rowcount # check that the images were all successfully added
        print (count, "Records inserted successfully into table")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_connection_cursor_tuple():
    connection = None
    try:
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(dbname = "postgres", user="postgres", password="123456789", host="127.0.0.1", port="5432")
        cursor = connection.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return connection, cursor

connection, cursor = get_connection_cursor_tuple()
img_names = ['../static/images/0.jpg', '../static/images/1.jpg']
send_files_to_postgresql(connection, cursor, img_names)