__author__ = 'Sacumen'

err_code_dict = {
            'InvalidClientTokenId'  : 'AWS ACCESS_KEY is invalid',
            'SignatureDoesNotMatch' : 'AWS SECRET_KEY seems to be invalid',
            'AWS.SimpleQueueService.NonExistentQueue' : 'The specified queue does not exist',
            'InvalidAddress'        : 'The address is Invalid',
            'InvalidQueryParameter' : 'The query parameters are Invalid',
            'InvalidRequest'        : 'The request is Invalid',
            'InvalidSecurity'       : 'Th security keys are Invalid',
            'MissingCredentials'    : 'Credentials are missing',
            }

err_type_dict = {
            'EndpointConnectionError' : 'Perhaps, the region name is incorrect',
            }


#===============================================================================
class Error_SQS_Log_Downloader:
    #---------------------------------------------------------------------------
    def __init__(self, operation_name='', error_type='', error_code='',
                    error_msg_pre='', error_msg_actual=''):
        self.operation_name   = operation_name
        self.error_type       = error_type
        self.error_code       = error_code
        self.error_msg_pre    = error_msg_pre
        self.error_msg_actual = error_msg_actual
        self.error_msg        = ''
        
        self.compute_err_msg()
    
    #---------------------------------------------------------------------------
    def compute_err_msg(self):
        msg = ''
        if self.error_code in err_code_dict:
            msg = err_code_dict[self.error_code]
        elif self.error_type in err_type_dict:
            msg = err_type_dict[self.error_type]
        
        self.error_msg = (' '.join([self.error_msg_pre, msg])) if msg else (self.error_msg_actual or "Unrecognized error")
