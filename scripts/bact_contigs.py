
import sys
from ete3 import NCBITaxa
import plotly.express as px
import scipy.stats as stats
import numpy as np


ncbi = NCBITaxa()
# ncbi.update_taxonomy_database()

contig_stats = {}	# {contig:{size:size, genes:[genes])}

ct1 = 0
with open(sys.argv[1], 'r') as file:
	for line in file:
		ct1 += 1

print(f"Number blast hits: {ct1}")

ct2 = 0
with open(sys.argv[1], 'r') as file:
	for line in file:
		ct2 += 1

		if ct2 % 100 == 0:
			print(f"{(100*float(ct2) / ct1):.2f}% Processed", end="\r")
		
		line = line.strip().split("\t")

		contig = line[0]
		tax = line[12]
		size = int(line[13])

		try:
			tax = int(tax)
		except Exception as e:
			tax = 0

		if tax == 0:
			domain = "unknown"
		else:
			try: 
				lineage = ncbi.get_lineage(tax)
				domain = ncbi.get_taxid_translator(lineage)
				if "Eukaryota" in domain.values():
					domain = "Eukaryota"
				elif "Bacteria" in domain.values():
					domain = "Bacteria"
				else:
					domain = "other"
			except ValueError as e:
				print("missing taxid")


		if contig not in contig_stats.keys():
			contig_stats[contig] = {"size": size, "genes":[]}
		contig_stats[contig]["genes"].append(domain)

# print(contig_stats)

size = []
pbact_l = []
num = []
for contig in contig_stats.keys():
	bact = contig_stats[contig]["genes"].count("Bacteria")
	euk = contig_stats[contig]["genes"].count("Eukaryota")

	try:
		pbac = (bact) / (bact + euk)
	except:
		pbac = -0.1
	
	size.append(contig_stats[contig]["size"])

	pbact_l.append(pbac)
	if pbac < 0:
		num.append(1)
	else:
		num.append(bact + euk)

bins = np.linspace(0, 1, 21)
statistic, bin_edges, binnumber = stats.binned_statistic(
    x=pbact_l, values=size, statistic='sum', bins=bins)
# print(statistic)
# print(bin_edges)
# print(binnumber)

# print(pbact_l)
# print(size)
labels = dict(x="% bacterial genes", y="Contig Length")
fig = px.scatter(x=pbact_l, y=size, size=num, labels=labels)
fig.write_html("plt.html")

labels = dict(x="% bacterial genes", y="Cumulative Contig Length")
fig2 = px.bar(y=statistic, x=bin_edges[0:20], labels=labels)
fig2.write_html("barplt.html")

