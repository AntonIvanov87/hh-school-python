#!/usr/bin/python

# fixed all issues:
# decided to use func.__name__ to determine what function should be called
# added detection of cycles
# added lazy_compile


class CyclicDependency(Exception):
	pass


class MissingParameter(Exception):
	pass


def simple_compile(functions):
	"""
	Returns a function compute_all.
	The compute_all accepts a map of input parameters
	and returns a map of all parameters that can be computed with given functions.
	Each function parameter name must match the name of the function that computes this parameter.
	Can raise CyclicDependency and MissingParameter.
	"""

	name_to_func = map_names_to_functions(functions)
	graph = make_graph(functions)
	top_order = reversed_top_order(graph, graph.keys())
	# graph is a dict {function name: function arguments}
	# in reversed topoligical order each argument goes before its' function
	# thus we have to call functions precisely in this order 

	def compute_all(input_map):

		return compute_from_top_order(top_order, name_to_func, input_map)

	return compute_all


def lazy_compile(functions):
	"""
	Returns a function compute_given.
	The compute_given accepts a map of input parameters, iterable of parameters that have to be computed
	and returns a map of computed parameters.
	Each function parameter name must match the name of the function that computes this parameter.
	Can raise CyclicDependency and MissingParameter.
	"""

	name_to_func = map_names_to_functions(functions)
	graph = make_graph(functions)
	# we will compute top_order only when we know what params have to be computed

	def compute_given(input_map, params_to_compute):

		top_order = reversed_top_order(graph, params_to_compute)
		return compute_from_top_order(top_order, name_to_func, input_map)

	return compute_given


def map_names_to_functions(functions):
	"""
	Service function that returns dict{function_name -> function}
	"""

	return dict([(func.__name__, func) for func in functions])


def make_graph(functions):
	"""
	Service function that return dict {function_name -> function_arguments}
	"""

	return dict([(func.__name__, func.func_code.co_varnames) for func in functions])


def reversed_top_order(graph, nodes_to_explore):
	"""
	Returns a reversed list of topologically sorted nodes of the graph.
	Raises CyclicDependancy if graph has cycles.
	"""

	top_order = list()
	completed = set() # this is just for performance. To quickly find topologically sorted nodes.
	pending = list(nodes_to_explore) # stack that holds nodes to perform dfs
	visited = set()
	while pending:

		node = pending[-1]

		# if node is already topologically sorted - just remove it and continue with next node
		if node in completed:
			del pending[-1]
			continue
			
		visited.add(node)

		# if node points to other nodes - add next node to pending list
		if node in graph:
			next_nodes = graph[node]
			for next_node in next_nodes:
				if next_node in visited:
					raise CyclicDependency()
				if next_node not in completed:
					pending.append(next_node)
					break

		# if no new node was added - add this node to top_order
		if pending[-1] == node:
			top_order.append(node)
			completed.add(node)
			visited.remove(node)
			del pending[-1]


	return top_order


def compute_from_top_order(top_order, name_to_func, input_map):
	"""
	Service function that computes all parameters in top_order.
	name_to_func - is a dict {function_name: function}
	input_map - is a dict {parameter_name: parameter_value}
	"""

	output_map = input_map.copy()

	for param in top_order:

		# if value of the parameter was already given - continue
		if param in output_map:
			continue

		# if there is no function to compute parameter - raise MissingParameter
		if param not in name_to_func:
			raise MissingParameter(param)

		function = name_to_func[param]
		args_names = function.func_code.co_varnames
		args_to_values = dict([(arg_name, output_map[arg_name]) for arg_name in args_names])
		output_map[param] = function(**args_to_values)

	return output_map


if __name__ == '__main__':

	# Example from article
	def n(xs):
		return len(xs)

	def m(xs, n):
		return float(sum(xs)) / n

	def m2(xs, n):
		global m2_was_called
		m2_was_called = True
		return float(sum(map(lambda x: x*x, xs))) / n

	def v(m, m2):
		global v_was_called
		v_was_called = True
		return m2 - m*m

	functions = (n, m, m2, v)


	# Simple compile
	compute_all = simple_compile(functions)
	output_map = compute_all({'xs': [1, 2, 3, 6]})
	assert output_map['n'] == 4
	assert output_map['m'] == 3
	assert output_map['m2'] == 12.5
	assert output_map['v'] == 3.5


	# Missing parameter
	try:
		compute_all({'ys': [1, 2, 3, 6]})
		# must raise MissingParameter, i.e. must not reach this row
		assert False
	except MissingParameter:
		pass


	# Cyclic dependency
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
	except CyclicDependency:
		pass


	# Lazy compile
	m2_was_called = False
	v_was_called = False
	compute_given = lazy_compile(functions)
	output_map = compute_given({'xs': [1, 2, 3, 6]}, 'm')
	assert output_map['n'] == 4
	assert output_map['m'] == 3
	assert not m2_was_called
	assert not v_was_called