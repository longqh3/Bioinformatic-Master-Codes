from gtfparse import read_gtf
import pandas as pd
import numpy as np
# returns GTF with essential columns such as "feature", "seqname", "start", "end"
# 将GTF文件读取为dataframe，并将有用的信息挑选出来
rawdata = read_gtf("F:/Data/RawDatabase/Gencode/gencode.v31.annotation.gtf/gencode.v31.annotation.gtf")
used_feature = ["seqname", "source", "feature", "start", "end", "gene_id", "gene_name", "gene_type", "transcript_id", "transcript_name", "transcript_type", "exon_number", "exon_id"]
df = rawdata[used_feature]
# df.to_csv("F:/Data/RawDatabase/Gencode/gencode.csv", sep="\t", index=False)
count = df["feature"].value_counts()  # 计数
cn = df.columns.values.tolist()  # 列名称
df_genes = df.loc[df["feature"] == "gene"]
df_genes.iloc[:, 0].size
df_transcript = df.loc[df["feature"] == "transcript"]
Allgenes = df_genes["gene_name"]
Uniquegenes= set(df_genes["gene_name"])
dupgenes = df_genes[Allgenes.duplicated()]
sorted_dupgenes = dupgenes.sort_values(by='gene_name')

# 将没有重复的和重复的基因所有信息分开并提取出来
Nodup = df_genes.drop_duplicates(subset=["gene_name"], keep=False)   # 将所有重复过的基因全部剔除，不保留其中任何一个
Nodup.iloc[:, 0].size
# keep_one_dup = df_genes.drop_duplicates(subset=["gene_name"])
flag = df_genes["gene_name"].isin(Nodup["gene_name"])    # 如果Nodup的基因存在于df_genes中，则返回T，否则F
diff_flag = [not f for f in flag]   # 这步即R中的！，将T转为F，F转为T，如果Npdup的基因不存在与df_genes中，则说明是被删除了的重复基因，我们要挑选的就是这部分
res = df_genes[diff_flag].sort_values(by='gene_name')    # Nodup和df_genes的差集即所有重复的基因信息，按照gene_name进行排序
dupgenes_count = res["gene_name"].value_counts()

# 挑选能被保留下来的重复的基因信息，与Nodup合并，后再将文件导出
tmp = res[-res["gene_name"].str.contains("RF")]
tmp2 = tmp[-tmp["gene_id"].str.contains("PAR")]
tmp3 = tmp2.drop_duplicates(subset="gene_name")
finalfile = Nodup.append(tmp3)
final = finalfile.sort_values(by=["seqname","start"])
if len(set(finalfile["gene_name"])) == finalfile.iloc[:, 0].size:
    print("There is no dupplicated gene in the dataframe !")
else:
    print("There still exists dupplicated genes !")
# 将final文件按照染色体编号进行排序
chr = ["chr"+str(a) for a in range(1, 23)] + ["chr"+b for b in ["X", "Y", "M"]]
sorted_final = pd.DataFrame(columns=used_feature)
for chrom in chr:
    schr = final[final["seqname"].isin([chrom])]
    sorted_final = sorted_final.append(schr)
sorted_final.to_csv("F:/DigenicProg/Data/Gencode/Gencode_geneinfo.csv", sep="\t", index=False)

# 根据finalfile的gene_id将transcript和exon等挑选出来，剔除不需要的信息
allinfo = df[df["gene_id"].isin(sorted_final["gene_id"])]
final2 = allinfo.sort_values(by=["seqname","start"])
sorted_final2 = pd.DataFrame(columns=used_feature)
for chrom in chr:
    schr = final2[final2["seqname"].isin([chrom])]
    sorted_final2 = sorted_final2.append(schr)
sorted_final2.to_csv("F:/DigenicProg/Data/Gencode/Gencode_allinfo.csv", sep="\t", index=False)







