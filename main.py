import aerospike
import time
import sys


# put max_retries also
# if some owner is acquiring the lock show we reset the ttl?


class LoxAM:
    def __init__(self, lock_string, owner, db_backend=None, timeout=60, retry=5, max_retries=3, thread=1):
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
        self.thread = thread

    def __enter__(self):
        try:
            self.client = aerospike.client(self.config).connect()
            self.client.udf_put("atomicity.lua")
            print("Thread ", self.thread)
        except Exception as e:
            print("failed to connect to the cluster with", self.config['hosts'], e)
        return self

    def acquire(self):
        locked = False
        while not locked and self.max_retries:
            try:
                locked = self.client.apply(self.key, "atomicity", "get_or_create", [{'owner': self.owner}])
                if locked:
                    print("Acquired lock for lock_string for thread", self.key, self.thread, locked)
                else:
                    print("Already acquired by someone else. Retrying in {}".format(self.retry))
            except Exception as e:
                print("error while acquiring lock: {0}".format(e))
                locked = True
            time.sleep(self.retry)
            self.max_retries -= 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        # put the release logic here either deleting the record or updating the record, require discussion
        # delete as per discussion
        try:
            self.client.remove(self.key)
            print("Lock released for thread {} and key{}".format(self.thread, self.key))
        except Exception as e:
            print(self.key)
            print(e)
        self.client.close()
        print("Exiting context", self.thread)
