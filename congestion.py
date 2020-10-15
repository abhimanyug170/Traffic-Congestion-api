# normal_times = [40, 20, 30, 70]
# traffic_times = [60, 25, 40, 120]
def get_signal_times(normal_times, traffic_times):
	mean = sum(traffic_times)//len(traffic_times)
 
	lower_limit = 20
	upper_limit = 70
	start_val = 50
	signal_times = []
	delay_percents = []
	for i in range(len(traffic_times)):
	    curr_diff = traffic_times[i] - mean
	    res = start_val + curr_diff
	    if res < lower_limit:
	        res = lower_limit
	    if res > upper_limit:
	        res = upper_limit
	    signal_times.append(res)
	    delay_percents.append(int(((traffic_times[i] - normal_times[i])*100)/normal_times[i]))
 
	return (signal_times, delay_percents)