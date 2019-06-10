import aerospike
import time


# put max_retries also

class LoxAM:
    def __init__(self, lock_string, owner, db_backend=None, timeout=60, retry=5, max_retries=10):
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
        except Exception as e:
            print("failed to connect to the cluster with", self.config['hosts'], e)
        return self

    def acquire(self):
        locked = True
        while locked and self.max_retries:
            (key, meta) = self.client.exists(self.key)
            if meta:
                print("Already acquired by someone else. Retrying after {} seconds".format(self.retry))
                time.sleep(self.retry)
                self.max_retries -= 1
                continue
            else:
                locked = False
            try:
                self.client.put(self.key, {
                    'owner': self.owner
                })
                print("Acquired lock for lock_string", self.lock_string)
                locked = False
            except Exception as e:
                print("error while acquiring lock: {0}".format(e))

    def __exit__(self, exc_type, exc_val, exc_tb):
        # put the release logic here either deleting the record or updating the record, require discussion
        # delete as per discussion
        try:
            self.client.remove(self.key)
        except Exception as e:
            print(self.key)
            print(e)
        self.client.close()
        print("Exiting context")
