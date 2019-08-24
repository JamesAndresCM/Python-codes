import boto3
import psycopg2
import os

def connect_psql():
    try:
        db = psycopg2.connect("dbname='db_name' user='postgres_user' host='host_name' password='password'")
    except:
        print("Error to connect to the database")
    else:
        return db

def scan_users(table):
    response = table.scan()
    for user in response['Items']:
        user_sql = 'INSERT INTO users(user_id,first_name,last_name) VALUES(%s,%s,%s)'
        user_id = user['user_id']
        first_name = user['first_name']
        last_name = user['last_name']
        user_values=(user_id,first_name,last_name)
        conn_cursor.execute(user_sql,user_values)
        conn.commit()
        print("User inserted: {}".format(user_values))
    
    conn_cursor.close()

conn = connect_psql()
conn_cursor = conn.cursor()

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('name_table')
scan_users(table)
