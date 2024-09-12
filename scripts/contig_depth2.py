
import sys
import plotly.express as px
import numpy as np
import scipy.stats as stats
import time
import math
import pandas as pd
import statistics
import subprocess


# python3 contig_depth2.py <sorted bam file> [<min_contig_depth=1000>]


if len(sys.argv) > 2:
	min_contig_size = int(sys.argv[2])
else:
	min_contig_size = 1000

print(f"min_contig_size: {min_contig_size}")

ave_cov = {}



def calc_depth(bam):
	"""https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running"""
	print("Running samtools depth")
	cmd = f"samtools depth -a {bam}"
	popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	for stdout_line in iter(popen.stdout.readline, ""):
		#print(stdout_line)
		# hack...
		if len(stdout_line) < 1:
			break
		yield stdout_line 
	popen.stdout.close()
	#return_code = popen.wait()
	#if return_code:
		#raise subprocess.CalledProcessError(return_code, cmd)



current_contig = None
covs = []
completed = 0
for line in calc_depth(sys.argv[1]):

	try:
		contig, pos, cov = line.strip().split()
	except:
		print(line)
	pos = int(pos)
	cov = int(cov)

	if current_contig == None:
		current_contig = contig

	if contig != current_contig:

		ave_cov[f"{contig}"] = {"cov": (statistics.median(covs)), "len": old_pos}

		v = ave_cov[f"{contig}"]
		completed += 1
		print(f"completed: {completed} -- {contig}: {v}")
		covs = []
		current_contig = contig

	else:
		covs.append(cov)
		old_pos = pos

print()
print(ave_cov)
df = pd.DataFrame.from_dict(ave_cov, orient="index")


df["loglen"] = np.log10(df['len'])
print(df)
df.columns = ['median depth', 'contig length', 'log10(contig length)']
df.index.name = 'contig'
print(df)
df.to_csv(f"contig_median_depth_{min_contig_size}.txt", sep="\t")

df = df[df['median depth'] < 500]
fig = px.histogram(df, x='median depth', nbins=500)
fig.write_html(f"{sys.argv[1]}_cov_{min_contig_size}.html")


fig = px.scatter(df, y="log10(contig length)", x="median depth")
fig.write_html(f"{sys.argv[1]}_covxlen_{min_contig_size}.html")

