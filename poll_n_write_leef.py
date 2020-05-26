import logging
import threading
import time
from logging import handlers

import boto3
import botocore

import lib

#Config setup for AWS and syslog
config = lib.ConfigHelper()
logging_server = config.rl_syslog_host
REGION_NAME = config.rl_aws_region
qname = config.rl_aws_queue
poll_interval       = 5
poll_duration       = 10
MaxNumberOfMessages = 10
VisibilityTimeout   = 3600


syslog_logger     = logging.getLogger('SYSLOG')
syslog_formatter  = logging.Formatter("%(asctime)s PRISMA_CLOUD %(message)s\n", "%b %d %H:%M:%S")
syslog_logger.setLevel(logging.INFO)

syslog_handler = logging.handlers.SysLogHandler(address = (logging_server, 514),
                                                facility = logging.handlers.SysLogHandler.LOG_LOCAL3)
syslog_handler.setFormatter(syslog_formatter)
syslog_handler.append_nul = False
syslog_logger.addHandler(syslog_handler)


#-------------------------------------------------------------------------------
# Get the specified resource object
def get_resource (service_name,
                    REGION_NAME):
    # Build the Config dict
#    config = Config(proxies=proxies_dict, connect_timeout=300) if proxies_dict else None

    # Construct the resource object
    sqs = boto3.resource(service_name,
                         region_name = REGION_NAME)



    return sqs


#-------------------------------------------------------------------------------
# Connect to the queue
def get_queue(rsrc_sqs, qname):
    # Get the queue by name
    q = rsrc_sqs.get_queue_by_name(QueueName = qname)
    return q


class SyslogThread(threading.Thread):
    def __init__(self, name, refreshTime, queue, poll_interval,poll_duration, MaxNumberOfMessages,VisibilityTimeout):
        threading.Thread.__init__(self, name=name)
        self.event = threading.Event()
        self.refreshTime = refreshTime
        self.queue = queue
        self.poll_interval = poll_interval
        self.poll_duration = poll_duration
        self.MaxNumberOfMessages = MaxNumberOfMessages
        self.VisibilityTimeout = VisibilityTimeout


    def run(self):

        firstTime = True
        counter = 0
        while not self.event.is_set():
            counter = counter + 1

            if firstTime:

                self.threadTask()

            self.event.wait(self.refreshTime)

        syslog_handler.close()


    def threadTask(self):
        _poll_n_write(self.queue,
                        self.poll_interval,
                        self.poll_duration,
                        self.MaxNumberOfMessages,
                        self.VisibilityTimeout
                      )

#-------------------------------------------------------------------------------
# Poll indefinitely
# Write the received messages to socket logger
def _poll_n_write (q,
                    poll_interval,
                    poll_duration,
                    MaxNumberOfMessages,
                    VisibilityTimeout):
        #qpylib.log('Start polling message from SQS', level='info')
    msgs = q.receive_messages (MaxNumberOfMessages = MaxNumberOfMessages,
                                   WaitTimeSeconds     = poll_duration,
                                   VisibilityTimeout   = VisibilityTimeout)

    print ("Got message from SQS")
        # Write the received messages to socket logger
        # Delete the message from queue after writing it.
    if len(msgs):
       for m in msgs:

           try:

            syslog_str = "{event_attributes}".format(event_attributes=lib.LEEFJson.parseJson(m.body))

            syslog_logger.info(syslog_str)
            time.sleep(5)

           except:
            print ("Error in processing message:%s"  % (m.body).strip())


                # Delete the message that is written to logger
           try:
            m.delete()
           except:
            print ('Error in deleting message in SQS:%s' %(m.body).strip())





#put logic after this to kill thread with the same name
# get reference to thread and kill using thread.event.set()
def stopThread():

    for threadObj in threading.enumerate():
        threadName = threadObj.name
        #qpylib.log('Thread Name Enum %s' %threadName, level='info')
        if threadName == "redlockthread":
            #print "Stopping RedLock Thread for %s" % threadName
            threadObj.event.set()
            threadObj.join()

    is_alive = True
    while is_alive:
        syslog_found = False
        for threadObj in threading.enumerate():
            threadName = threadObj.name

            #qpylib.log('Thread Name Check for %s' %threadName, level='info')
            #qpylib.log('qradar_found %s' % qradar_found, level='info')
            if threadName == "redlockthread":
                #qpylib.log('Got redlock thread %s' % qradar_found, level='info')
                syslog_found = True
                #qpylib.log('qradar_found set to %s' % qradar_found, level='info')

        if not syslog_found:
            #qpylib.log('making is_alive to False and qradar_found %s' % qradar_found, level='info')
            is_alive = False





#-------------------------------------------------------------------------------
# Get the queue
# Start polling the queue
# Write the received messages to Socket logger
def poll_queue_n_write(REGION_NAME,
                        qname,
                        poll_interval,
                        poll_duration,
                        MaxNumberOfMessages,
                        VisibilityTimeout):
    # Get the SQS resource; Get queue by queue name
    # Handle possible exceptions

#    cipher = AESCipher()

    # Read from data file
#    stored_data = read_data_store()

    #qpylib.log('read data done in poll_queue_n_write method', level='info')

    # Encrypt keys if available else read from data file
#    encrypted_access_key = cipher.encrypt(ACCESS_KEY) if ACCESS_KEY else stored_data.get('access_key', '')
#    encrypted_secret_key = cipher.encrypt(SECRET_KEY) if SECRET_KEY else stored_data.get('secret_key', '')

    # Decrypt values
#    ACCESS_KEY = cipher.decrypt(encrypted_access_key) if encrypted_access_key else encrypted_access_key
#    SECRET_KEY = cipher.decrypt(encrypted_secret_key) if encrypted_secret_key else encrypted_secret_key

    # Load other values from data store if not provided

#    REGION_NAME = REGION_NAME or stored_data.get('region_name', '')
#    qname = qname or stored_data.get('qname', '')
#    poll_interval = poll_interval or stored_data.get('poll_interval', '')
#    poll_duration = poll_duration or stored_data.get('poll_duration', '')
#    MaxNumberOfMessages = MaxNumberOfMessages or stored_data.get('max_number_of_messages', '')
#    VisibilityTimeout = VisibilityTimeout or stored_data.get('visibility_timeout', '')

#    proxies_dict = proxies_dict or stored_data.get('proxies_dict', {})

    #qpylib.log('Calling SQS to get data in poll_queue_n_write method', level='info')
    try:
#        rsrc_sqs = get_resource('sqs', ACCESS_KEY, SECRET_KEY, REGION_NAME, proxies_dict)
        rsrc_sqs = get_resource('sqs', REGION_NAME)
        q = get_queue(rsrc_sqs, qname)

    except botocore.exceptions.ClientError as e:
        err = lib.Error_SQS_Log_Downloader(operation_name = e.operation_name,
                    error_type = 'ClientError',
                    error_code = e.response['Error']['Code'])
        return err

    except botocore.exceptions.EndpointConnectionError as e:
        err = lib.Error_SQS_Log_Downloader(error_type = 'EndpointConnectionError',
                    error_msg_pre = e.message)
        return err

    except ValueError as e:
        if 'Invalid endpoint' in e.message:
            err = lib.Error_SQS_Log_Downloader(error_type = 'EndpointConnectionError',
                        error_msg_pre = e.message)
        else:
            err = lib.Error_SQS_Log_Downloader()
        return err

    except Exception as e:
        err = lib.Error_SQS_Log_Downloader()

        try     : err.error_code = e.response['Error']['Code']
        except  : pass

        try     : err.error_type = type(e).split('.')[-1]
        except  : pass

        try     : err.operation_name = e.operation_name
        except  : pass

        try     : err.error_msg_actual = e.message
        except  : pass

        err.compute_err_msg()
        return err


    stopThread()

    print("Finished stopping thread")

    refreshTime=1


    thread = SyslogThread(
		"redlockthread",
		refreshTime=refreshTime,
		queue=q,
		poll_interval=poll_interval,
		poll_duration=poll_duration,
		MaxNumberOfMessages=MaxNumberOfMessages,
		VisibilityTimeout=VisibilityTimeout
	     )
    thread.start()
    return True

#-------------------------------------------------------------------------------
# Test the SQS connection
def testSQSConnection(REGION_NAME,
                        qname,
                        poll_interval,
                        poll_duration,
                        MaxNumberOfMessages,
                        VisibilityTimeout,
                        proxies_dict):
    # Get the SQS resource; Get queue by queue name
    # Handle possible exceptions

    #qpylib.log('testSQSConnection method called', level='info')
    try:
        rsrc_sqs = get_resource('sqs', REGION_NAME, proxies_dict)
        q = get_queue(rsrc_sqs, qname)

    except botocore.exceptions.ClientError as e:
        err = lib.Error_SQS_Log_Downloader(operation_name = e.operation_name,
                    error_type = 'ClientError',
                    error_code = e.response['Error']['Code'])
        return err

    except botocore.exceptions.EndpointConnectionError as e:
        err = lib.Error_SQS_Log_Downloader(error_type = 'EndpointConnectionError',
                    error_msg_pre = e.message)
        return err

    except ValueError as e:
        if 'Invalid endpoint' in e.message:
            err = lib.Error_SQS_Log_Downloader(error_type = 'EndpointConnectionError',
                        error_msg_pre = e.message)
        else:
            err = lib.Error_SQS_Log_Downloader()
        return err

    except Exception as e:
        err = lib.Error_SQS_Log_Downloader()

        try     : err.error_code = e.response['Error']['Code']
        except  : pass

        try     : err.error_type = type(e).split('.')[-1]
        except  : pass

        try     : err.operation_name = e.operation_name
        except  : pass

        try     : err.error_msg_actual = e.message
        except  : pass

        err.compute_err_msg()
        return err




    return True

if __name__ == "__main__":
             res = poll_queue_n_write(REGION_NAME,
                                           qname,
                                   poll_interval,
                                   poll_duration,
                             MaxNumberOfMessages,
                               VisibilityTimeout)

if res == True:
   print("Successfully connnected to SQS queue.")
   while True:
    try:
        time.sleep(100)
    except KeyboardInterrupt as e:
        stopThread()
        break;
else:
    print("Error: %s" % res.error_msg)

#    print res.error_msg
