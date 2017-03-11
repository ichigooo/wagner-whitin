"""
wagner whitin algorithm

example use:
$ ww.py 100 1 10 60 15 150 110
with fixed cost = 100, holding cost = 1, and demands are 10 60 15 150 110


Linna Wang

"""

import sys
import numpy as np
from argparse import ArgumentParser

def wagner_whitin(K, h, demand):
	"""
	K:@float, the fixed ordering cost.
	h:@float, the holding cost.
	demand:@list[float], an array of demand for each period.
	return
	F:@float, optimal total fixed ordering and holding costs.
	order:@list[float], optimal number of purchase at each period.
	"""

	order = [] # optimal order of purchase at each period
	demand = np.array(demand)
	n = len(demand)
	print ("n: ", n)
	cost = [[0 for i in range(0,n)] for j in range(0, n)]
	# print (cost)
	for i in range(0, n):
		for j in range(i , n):
			cost[i][j] += K
			for k in range(i + 1, (j + 1)):
				# print ("demand: ", k, "holding days: ", k - i)
				cost[i][j] += h * (k - i) * demand[k]
	print ("==========================constructing cost matrix==========================")
	print ("cost matrix: ", cost)

	#  initializing the optimal order cost within the period i, j
	F = [[0 for i in range(0,n)] for j in range(0, n)]
	order_m = [[[j] for i in range(0,n)] for j in range(0, n)]

	print ("==========================constructing total cost matrix==========================")
	for j in range(0, n):
		for i in range(0, j+1):
			print ("Fij: ", j - i, j)
			F[j - i][j] = cost[j - i][j]
			for k in range(j - i, j):
				if (cost[j - i][k] + F[k+1][j] < F[j - i][j]):
					F[j - i][j] = cost[j - i][k] + F[k+1][j]
					order_m[j - i][j] = [j - i, k+1]
					# order[j - i] = sum(demand[j - i: k + 1])
					# for m in range(j - i + 1, k + 1):
					# 	order[m] = 0
					print ("costik + Fk+1j: cost", j - i, k, "  + F", k + 1, j, " is smaller, order at period ", k+1)
	print ("F: ", F)
	# print ("order_m: ", order_m)

	optimal = F[0][len(F) - 1]

	order_periods = find_order_periods(order_m, len(demand))
	order = get_order_amount(order_periods, demand)

	print ("==========================optimal answer==========================")
	print ("optimal: ", optimal)
	# print ("order in the following periods: ", order_periods)
	print ("order amount for each period: ", order)

	return optimal, order


#  get the periods which needs to order
def find_order_periods(order_matrix, n):
	order_periods = []
	order_periods.append(0)
	next = order_matrix[0][n - 1][1]
	order_periods.append(next)
	while(len(order_matrix[next][n - 1]) == 2):
		order_periods.append(order_matrix[next][n - 1][1])
		next = order_matrix[next][n - 1][1]
	return order_periods


def get_order_amount(order_periods, demand):
	order = [0 for i in range(0, len(demand))]
	for i, num in enumerate(order_periods):
		order[num] = sum(demand[num:order_periods[i+1]]) if (i + 1 < len(order_periods)) else sum(demand[num:len(demand)])
	return order
		
def create_cli_parser():
    """
    Creates a command line interface parser.
    """

    cli_parser = ArgumentParser(description=__doc__)

    cli_parser.add_argument('fcost', default="10", type=float,
        help="The fixed ording cost")
    cli_parser.add_argument('hcost', default="3", type=float,
        help="The holding cost")
    cli_parser.add_argument('demands', nargs='+', type=int,
        help="Demands during each period")

    return cli_parser

def main(argv):
    # Create the command line parser.
    cli_parser = create_cli_parser()
    # Get the options and arguments.
    args = cli_parser.parse_args(argv)
    f_cost = args.fcost
    h_cost = args.hcost
    demands = args.demands
    print ("==========================getting input data==========================")
    print ("f_cost: ", f_cost, " h_cost: ", h_cost, " demands: ", demands)
    print ("f_cost: ", f_cost, " h_cost: ", h_cost)

    wagner_whitin(f_cost, h_cost, demands)



if __name__ == "__main__":
    main(sys.argv[1:])