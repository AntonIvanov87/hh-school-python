#!/usr/bin/python

# fixed all issues:
# decided to use func.__name__ to determine what function should be called
# made detection of cycles

def simple_compile(functions):
	"""
	Returns a function compute_all.
	The compute_all accepts a map of input parameters
	and returns a map of all parameters that can be computed with given functions.
	Each function parameter name must match the name of the function that computes this param.
	In case of cyclic dependancies - ValueError is raised.
	"""

	graph = make_graph(functions)
	top_sorted = reversed_top_sort(graph)
	# graph is a dict {function name: function arguments}
	# in reversed topoligical order each argument goes before its' function
	# thus we have to call functions precisely in this order 

	name_to_func = dict([(func.__name__, func) for func in functions])

	def compute_all(input_map):

		output_map = input_map.copy()

		for param in top_sorted:

			# if value of the parameter was already in input_map - continue
			if param in output_map:
				continue

			function = name_to_func[param]
			args_names = graph[param]
			args_to_values = dict([(arg_name, output_map[arg_name]) for arg_name in args_names])
			output_map[param] = function(**args_to_values)

		return output_map

	return compute_all


def make_graph(functions):
	"""
	Makes dictionary of function name -> function arguments
	"""

	graph = {}
	for function in functions:
		graph[function.__name__] = function.func_code.co_varnames

	return graph


class CyclicDependancy(Exception):
	pass


def reversed_top_sort(graph):
	"""
	Returns a reversed list of topologically sorted nodes of the graph.
	Raises CyclicDependancy if graph has cycles.
	"""

	top_sorted_list = list()
	top_sorted_set = set() # this is just for performance. To quickly find topologically sorted nodes
	pending = list(graph) # stack that holds nodes to perform dfs
	visited = set()
	while pending:

		node = pending[-1]

		# if node is already topologically sorted - just remove it and continue with next node
		if node in top_sorted_set:
			del pending[-1]
			continue
			
		visited.add(node)

		# if node points to other nodes - add next node to pending list
		if node in graph:
			next_nodes = graph[node]
			for next_node in next_nodes:
				if next_node in visited:
					raise CyclicDependancy()
				if next_node not in top_sorted_set:
					pending.append(next_node)
					break

		# if no new node was added to pending list - this node is sorted
		if pending[-1] == node:
			top_sorted_list.append(node)
			top_sorted_set.add(node)
			visited.remove(node)
			del pending[-1]


	return top_sorted_list


if __name__ == '__main__':

	# Example from article
	def n(xs):
		return len(xs)

	def m(xs, n):
		return float(sum(xs)) / n

	def m2(xs, n):
		return float(sum(map(lambda x: x*x, xs))) / n

	def v(m, m2):
		return m2 - m*m

	functions = (n, m, m2, v)
	compute_all = simple_compile(functions)
	output_map = compute_all({'xs': [1, 2, 3, 6]})

	assert output_map['n'] == 4
	assert output_map['m'] == 3
	assert output_map['m2'] == 12.5
	assert output_map['v'] == 3.5

	# Cyclic dependancy
	def x(y):
		pass

	def y(z):
		pass

	def z(x):
		pass

	try:
		simple_compile((x, y, z))
		# must raise CyclicDependancy, i.e. must not reach this row
		assert False
	except CyclicDependancy:
		pass