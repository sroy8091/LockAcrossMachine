import aerospike
import time
import logging
logging.basicConfig(level=logging.DEBUG, format='[%(thread)d] - %(asctime)s - %(levelname)s - %(message)s')

# if some owner is acquiring the lock should we reset the ttl?


class LoxAM:
    """
    A custom context manager to manage locks accross distributed machines using aerospike
    """
    def __init__(self, lock_string, owner, db_backend=None, timeout=60, retry=5, max_retries=1):
        self.lock_string = lock_string
        self.db_backend = db_backend
        self.owner = owner
        self.timeout = timeout
        self.retry = retry
        self.max_retries = max_retries
        self.key = ('bbcache', 'lox', self.lock_string)
        self.config = {
            'hosts': [('127.0.0.1', 3000)]
        }

    def __enter__(self):
        try:
            self.client = aerospike.client(self.config).connect()
            # self.client.udf_put("atomicity.lua")
            logging.info("Trying to get lock")
        except Exception as e:
            logging.debug("Failed to connect to the cluster with {}\n {}".format(self.config['hosts'], e))
        return self

    def acquire(self):
        locked = False
        while not locked and self.max_retries:
            try:
                locked = self.client.apply(self.key, "atomicity", "get_or_create", [{'owner': self.owner}])
                if locked:
                    logging.info("Acquired lock for lock_string {}".format(self.key))
                else:
                    logging.info("Already acquired by someone else. Retrying in {}".format(self.retry))
            except Exception as e:
                logging.exception("Error while acquiring lock: {}".format(e))
                locked = True
            time.sleep(self.retry)
            self.max_retries -= 1
        if locked:
            return
        raise Exception("Unable to acquire lock")

    def release(self):
        try:
            (key, metadata, record) = self.client.get(self.key)
            if key and record.get("owner") == self.owner:
                self.client.remove(self.key)
                logging.info("Lock released and key{}".format(self.key))
        except aerospike.exception.RecordNotFound:
            pass
        except Exception as e:
            print(self.key)
            print(type(e))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        self.client.close()
        logging.info("Exiting context")
