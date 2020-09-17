# command: mpirun -np 4 python parallel.py
import sys
import os
import mpi4py.MPI as MPI
import numpy as np
import bigfile
import time

#
#  Global variables for MPI
#
 
# instance for invoking MPI relatedfunctions
comm = MPI.COMM_WORLD
# the node rank in the whole community
comm_rank = comm.Get_rank()
# the size of the whole community, i.e.,the total number of working nodes in the MPI cluster
comm_size = comm.Get_size()
 
if __name__ == '__main__':
    if comm_rank == 0:
        pig = bigfile.File("/pylon5/as5pi3p/bluetides3/PIG_251/")
    pig = comm.bcast(pig if comm_rank == 0 else None, root = 0)
    num_files = pig.open('FOFGroups/MassByType/').size
    local_files_offset = np.linspace(0, num_files, comm_size +1).astype('int')
    len_local = local_files_offset[comm_rank + 1] - local_files_offset[comm_rank]
    sys.stderr.write("%d/%d processor gets %d/%d data \n" %(comm_rank, comm_size, len_local, num_files))
    cnt = 0
    t1 = time.time()
    file1 = open("MyFile3.txt", "w") 
    max_range = 1e-2
    min_range = 5e-3
    data = pig.open('FOFGroups/MassByType/')[local_files_offset[comm_rank]:len_local+local_files_offset[comm_rank]]
    #print("data: ", data)
    data = data[:, 5]
    res = np.where((data <= max_range) & (data >= min_range))
    if res != []:
        file1.write(np.array_str(np.array(res)))
    pig.close()
    file1.close()
    t2 = time.time()
    print('Time to fetch data is : %.2f s'%(t2-t1))
