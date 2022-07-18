gencode.v22.annotation <- read.table("D:/TCGA/Received_data/gencode.v22.annotation.gtf", sep="\t", quote="", stringsAsFactors=FALSE)
# 提取出第九列信息
gene_info<-as.matrix(gencode.v22.annotation[,9])
# ???;作为分隔符进行字符串拆分
gene_info<-strsplit(gene_info, ";", fixed = TRUE)
# 新建list，并指定列名
my_list<-list(gene_id="gene_id",gene_name="gene_name")
# 通过???"gene_id" "gene_name"进行查找确定位置，并将该位置上对应信息写入my_list??? 
for(i in 1:length(gene_info)){
  gene_id_pos<-grep("gene_id",gene_info[[i]],fixed = TRUE)
  gene_name_pos<-grep("gene_name", gene_info[[i]],fixed=TRUE)
  my_list[[1]][i]<-gene_info[[i]][gene_id_pos]
  my_list[[2]][i]<-gene_info[[i]][gene_name_pos]
}
# Emmm注意到分隔符有tab和空格两种，并没有找到啥好办法分开，于是就用tab分隔导出，再用空格分隔导???
# 以后应该有更好的办法
write.table(my_list,file="result_gtf.txt",quote=FALSE,sep = "\t",row.names = FALSE,col.names = FALSE)
result_gtf<-read.table("result_gtf.txt", sep= " ", check.names = TRUE)
# 去除所有完全重复的???
result_gtf_final<-result_gtf[!duplicated(result_gtf),]
#for(i in 1:length(result_gtf_final[,2])){
#  result_gtf_final[i,2]<-sub("\t", "", result_gtf_final[i,2],fixed = TRUE)
#}
# Export the processed data
write.table(result_gtf_final, "result_gtf_final.txt",quote = FALSE,sep="\t",row.names = FALSE,col.names = FALSE)

#for(i in 1:length(my_list[[1]])){
#  sub(";", "", my_list[[1]][i], fixed=TRUE)
#  sub(";", "", my_list[[2]][i], fixed=TRUE)
#}

for(i in 1:lengths(gene_name)){
  pos<-grep(gene_name[i,1],gencode.v22.annotation[,9])
  for(j in pos){
    if(gencode.v22.annotation[j,3] == 'gene'){
      my_list[[1]][i]<-gene_name[i,1]
      my_list[[2]][i]<-gencode.v22.annotation[pos,1]
      my_list[[3]][i]<-gencode.v22.annotation[pos,4]
      my_list[[4]][i]<-gencode.v22.annotation[pos,5]
    }
  }
  
}
