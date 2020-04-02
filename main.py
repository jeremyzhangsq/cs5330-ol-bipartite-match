import numpy as np
import sys
import baseline
import alg1
import alg2
import alg3

if __name__ == '__main__':
	fid = int(sys.argv[1])
	alg = sys.argv[2]
	files = ["actor-movie.txt","github.txt","youtube.txt"]
	fname = "./dataset/"+files[fid]
	

