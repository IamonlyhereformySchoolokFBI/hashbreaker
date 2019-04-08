import os
from time import sleep
from mpi4py import MPI
from datetime import datetime


class Process_farm:

    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()
        self.status = MPI.Status()

    def run(self, 
            hash_to_crack, 
            hash_method, 
            compute_function, 
            scope, 
            granulation):

        if self.rank == 0:   
            partition_array = Process_farm.create_partition_array(scope + 1, granulation)
            print(partition_array)
            result = self.master(partition_array , granulation)
            return result
        else:
            self.slave(compute_function, hash_to_crack, hash_method)

    def master(self, partition_array, granulation):
        work = granulation
        result = [0]

        # send first jobs 
        for proc in range(1, self.size):
            data = partition_array[ proc - 1 ], partition_array[ proc ]
            self.comm.send(data, dest=proc)

            work -= 1

        while work:
            work -= 1
            data_from_slave = self.comm.recv(source=MPI.ANY_SOURCE, status=self.status)
            if len(data_from_slave) == 2:
                result = data_from_slave

            if not len(data_from_slave) == 1:
                data = partition_array[ proc ], partition_array[ proc + 1]
            else:
                data = -101
            
            source = self.status.Get_source()       
            self.comm.send(data, dest=source)
            proc += 1

        # recv rest data from slaves
        for proc in range(1,self.size):
            data_from_slave = self.comm.recv(source=MPI.ANY_SOURCE)
            # print(data_from_slave)
            if len(data_from_slave) == 2:
                result = data_from_slave

        # end all slaves
        for proc in range(1,self.size):
            end_status = -1
            self.comm.send(end_status, dest=proc)

        return result


    def slave(self, function, hash_to_crack, hash_method):
        while True:
            data = self.comm.recv(source=0)
            if data == -1:
                exit()
            if data == -101: # empty run 
                data = [0]
            else:
                data = function(hash_to_crack, data[0], data[1] - 1, hash_method)
            
            self.comm.send(data, dest = 0)


    @staticmethod
    def create_partition_array(scope, granulation):
        partition_array = []
        begin_at = 1

        if granulation == 0:
            granulation = 1

        num_of_ele_in_one_part = (scope - begin_at) // granulation
        for i in range(granulation):
            partition_array.append(begin_at)
            begin_at += num_of_ele_in_one_part

        partition_array.append(scope)

        return partition_array

    def save_to_file(self, *args):
        if self.rank == 0:
            if not os.path.exists('results'):
                os.makedirs('results')

            result_filename = 'hash_' + datetime.now().strftime('%Y%m%d_%H%M%S')
            result_filename = 'results/' + result_filename + '.txt'

            result_file = open(result_filename, 'w')
            result_file.write('Computation on {} processors with granulation: {}.\n'.format(self.size, args[0]))
            result_file.write('Time = '+ args[1]+' [sec].\n')

            if len(args[-1]) == 1:
                result_file.write('Do NOT found match password\n.')
            else:
                result_file.write('Found password with hash: ' + args[-1][1] + '\n' + 'Your password is: ' + args[-1][0])

            result_file.close()

        return result_filename
