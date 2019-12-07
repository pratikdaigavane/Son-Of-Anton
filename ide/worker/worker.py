import base64
import logging
import time

# 3rd party imports
import pika
import psycopg2

# language specific imports
from langs import *

# import settings
with open('config.json') as f:
    settings = json.load(f)
#this is a check
# connection to database
conn = psycopg2.connect(database=settings['database']['name'],
                        user=settings['database']['username'],
                        password=settings['database']['password'],
                        host=os.environ.get('DB_HOST', 'localhost'),
                        port=settings['database']['port'])
cur = conn.cursor()

# connection to logger database
connLog = psycopg2.connect(database=settings['loggerDatabase']['name'],
                           user=settings['loggerDatabase']['username'],
                           password=settings['loggerDatabase']['password'],
                           host=os.environ.get('DB_HOST', 'localhost'),
                           port=settings['loggerDatabase']['port'])
curLog = connLog.cursor()

# Logger configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')


class GeneralHandler(logging.Handler):
    """
    Logging Handler for all logs
    """
    global conn
    global cur

    def emit(self, record):
        timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S%z"))
        log_entry = self.format(record)
        level = record.levelname
        query = """INSERT INTO submission_workergenerallog (time, level, message) VALUES (%s, %s, %s)"""
        curLog.execute(query, (timestamp, level, log_entry))
        connLog.commit()


class ErrorHandler(logging.Handler):
    """
    Logging Handler for Error logs only
    """
    global conn
    global cur

    def emit(self, record):
        timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S%z"))
        log_entry = self.format(record)
        level = record.levelname
        query = """INSERT INTO submission_workererrorlog (time, level, message) VALUES (%s, %s, %s)"""
        curLog.execute(query, (timestamp, level, log_entry))
        connLog.commit()


# General Log Handler Configuration
generalHandler = GeneralHandler()
generalHandler.setFormatter(formatter)
generalHandler.setLevel(logging.DEBUG)
logger.addHandler(generalHandler)

# General Log Handler Configuration
errorHandler = ErrorHandler()
errorHandler.setFormatter(formatter)
errorHandler.setLevel(logging.ERROR)
logger.addHandler(errorHandler)

# connection to rabbitMQ
credentials = pika.PlainCredentials(settings['taskQueue']['username'], settings['taskQueue']['password'])
connection = pika.BlockingConnection(
    pika.ConnectionParameters(os.environ.get('RABBITMQ_HOST', 'localhost'), credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue=settings['taskQueue']['name'], durable=True)


def readMeta(fileName):
    """
    function to read meta data of the program such as execution time, memory, etc

    Parameters:
        fileName(str): Name of file which contains meta data of program

    Returns:
        dict: Dictionary which contains all metadata
    """
    fin = open(fileName, "rt")
    data = fin.read()
    data = data.replace(':', '=')
    fin.close()
    fin = open(fileName, "wt")
    fin.write(data)
    fin.close()
    meta = {}
    with open(fileName) as myfile:
        for line in myfile:
            name, var = line.partition("=")[::2]
            meta[name.strip()] = str(var).rstrip()
    os.remove(fileName)
    return meta


def updateDatabase(uid, status, box_id, meta):
    """
    updates the verdict to database

    Parameters:
        uid(int): unique ID of the submission
        status(str): verdict of the submission
        box_id(int): isolate box ID for the submission
        meta(dict): meta data of the submission
    """
    global conn
    global cur
    if status == 'OK':
        print('status is okay', flush=True)
        f_output = open("./" + str(box_id) + "/box/output.txt", "r")
        data = f_output.read()
        print(len(data), flush=True)
        if len(data) >= 1e7:
            # if output is too long it is truncated
            data = data[:1e6]
            data = data + '(output truncated)'

        data = base64.b64encode(data.encode()).decode()
        f_output.close()
        print(meta['time-wall'])
        print(meta['cg-mem'])
        # to be added in database
        query = """UPDATE submission_submission SET output = %s, mem = %s, exctime = %s, status = 'OK' WHERE id = %s"""
        cur.execute(query, (str(data), meta['cg-mem'], meta['time-wall'], uid))

    if status == 'CTE':
        print('compile time error', flush=True)
        f_error = open("./" + str(box_id) + "/box/error.txt", "r")
        data = f_error.read()
        f_error.close()
        data = base64.b64encode(data.encode()).decode()
        query = """UPDATE submission_submission SET error = %s , status = 'CTE' WHERE id = %s"""
        cur.execute(query, (str(data), uid))

    if status == 'TLE' or status == 'RTE' or status == 'SG' or status == 'XX':
        message = meta['message']
        data = base64.b64encode(message.encode()).decode()
        query = """UPDATE submission_submission SET error = %s , status = %s WHERE id = %s"""
        cur.execute(query, (data, status, uid))
    conn.commit()


def isolateInit(box_id, inputData, code, lang):
    """
    initialize the isolate sandbox

    Parameters:
        box_id(int): isolate box ID for the submission
        inputData(str): isolate box ID for the submission
        code(str): isolate box ID for the submission
        lang(str): isolate box ID for the submission
    """
    ext = {
        'cpp': 'cpp',
        'c': 'c'
    }
    # initialize box for isolate module
    subprocess.call("isolate --cleanup -b " + str(box_id), shell=True)
    subprocess.call("isolate --cg --init -d rw -b " + str(box_id), shell=True)
    f_input = open("./" + str(box_id) + "/box/input.txt", "w+")
    f_input.write(inputData)
    f_input.close()
    f_code = open("./" + str(box_id) + "/box/code." + ext[lang], "w+")
    f_code.write(code)
    f_code.close()


def callback(ch, method, properties, body):
    """Main function which is called by RabbitMQ"""
    global conn
    global cur
    inputData = ''
    code = ''
    language = ''
    uid = int(body)
    box_id = uid % 1000
    try:
        # fetch submission from database
        cur.execute("SELECT code,input,language from submission_submission WHERE id=" + str(uid))
        row = cur.fetchone()
        code = base64.b64decode(row[0]).decode()
        inputData = base64.b64decode(row[1]).decode()
        language = row[2]
        logger.info('SUB ID: {} Code fetched from the database.'.format(uid))
    except:
        # if submission is not present in the database
        logger.error('SUB ID: {} Submission ID not present in database'.format(uid))
        print("Submission ID not present in database", flush=True)
        return
    isolateInit(box_id, inputData, code, language)
    if language == 'cpp':
        compileCode = getattr(cpp, 'compile')
        runCode = getattr(cpp, 'run')
    if language == 'c':
        compileCode = getattr(c, 'compile')
        runCode = getattr(c, 'run')
    logger.info("SUB ID: {} Compilation started.".format(uid))
    isCompile = compileCode(box_id)
    print('Compiling Code...', flush=True)
    if not isCompile:
        logger.error("SUB ID: {} Compilation Error".format(uid))
        print("Compilation Error", flush=True)
        status = 'CTE'
        updateDatabase(uid, status, box_id, 'NULL')
    else:
        logger.info("SUB ID: {} Compilation Complete".format(uid))
        print('Compiling Complete', flush=True)
        print('Running Code....', flush=True)
        print(box_id, flush=True)
        runCode(box_id)
        meta = readMeta('meta.ini')
        if 'status' in meta.keys():
            # some error
            if meta['status'] == 'TO':
                # Time Limit Exceeded
                logger.error("SUB ID: {} Time Limit Exceeded".format(uid))
                status = 'TLE'
                print('TLE', flush=True)
                updateDatabase(uid, status, box_id, meta)
            elif meta['status'] == 'RE':
                # Runtime Error
                logger.error("SUB ID: {} Run Time Error".format(uid))
                status = 'RTE'
                print('RTE', flush=True)
                updateDatabase(uid, status, box_id, meta)
            elif meta['status'] == 'SG':
                # Program Exited with non-zero signal
                logger.error("SUB ID: {} Program Exited with non-zero signal".format(uid))
                status = 'SG'
                print('SG', flush=True)
                updateDatabase(uid, status, box_id, meta)
            elif meta['status'] == 'XX':
                logger.error('SUB ID: {} Sandbox Error'.format(uid))
                # Sandbox error
                status = 'XX'
                print('XX', flush=True)
                updateDatabase(uid, status, box_id, meta)
        else:
            # ALl OKAY!
            logger.info('SUB ID: {} Program ran successfully'.format(uid))
            status = 'OK'
            print('OK', flush=True)
            updateDatabase(uid, status, box_id, meta)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("\n", flush=True)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue',
                      on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C', flush=True)
channel.start_consuming()
