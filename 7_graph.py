#!/usr/bin/python

def simple_compile(graph):
	"""
	Returns a function compute_all.
	The compute_all accepts a map of input parameters
	and returns a map of all parameters that can be computed according go graph.
	Graph - a map from function_name to function.
	Each function parameter name must match the name of function that computes this param.
	"""

	def compute_all(input_map):

		output_map = input_map.copy()

		# create map of functions that were not already computed
		funcs_to_call = dict([(func_name, func)
							for (func_name, func) in graph.items()
							if func_name not in output_map])

		# keep iterating while new functions can be called
		while(True):

			new_funcs_to_call = {}
			for (func_to_call, func) in funcs_to_call.items():

				required_params = func.func_code.co_varnames
				known_params = required_params & output_map.viewkeys()

				# if we has all paramters to call func - call it
				if len(known_params) == len(required_params):

					dict_of_known_params = dict([(param_name, output_map[param_name])
													for param_name in known_params])
					
					output_map[func_to_call] = func(**dict_of_known_params)

				# if we do not have all params - leave func to call later
				else:
					new_funcs_to_call[funcs_to_call] = required_params

			# if no new function was called - break
			if len(new_funcs_to_call) == len(funcs_to_call):
				return output_map

			funcs_to_call = new_funcs_to_call

	return compute_all


if __name__ == '__main__':

	def n(xs):
		return len(xs)

	def m(xs, n):
		return float(sum(xs)) / n

	def m2(xs, n):
		return float(sum(map(lambda x: x*x, xs))) / n

	def v(m, m2):
		return m2 - m*m

	graph = {
		'n': n,
		'm': m,
		'm2': m2,
		'v': v}
	compute_all = simple_compile(graph)
	output_map = compute_all({'xs': [1, 2, 3, 6]})

	assert output_map['n'] == 4
	assert output_map['m'] == 3
	assert output_map['m2'] == 12.5
	assert output_map['v'] == 3.5